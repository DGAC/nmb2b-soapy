import glob
import json
import operator
import os

from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client, Settings
from zeep.cache import SqliteCache
from zeep.helpers import serialize_object
from zeep.transports import Transport

import utils
from shared_vars import (DEFAULT_B2B_VERSION, DEFAULT_DATASET, WSDL_PROXY,
						 WSDL_PREOPS_MAIN, get_dataset)

# NOTE : plutôt envoyer un **kwargs en param des méthodes. Puis, itérer sur les kwargs.
# si présence de clé dans _default_params_for_queries et pas de val...

class Manager():

	def __init__(
		self, 
		version=DEFAULT_B2B_VERSION, 
		service_group="FlightServices", 
		dataset=DEFAULT_DATASET,
		how_to_auth='proxy',
		*args, **kwargs
		):
		
		self.wsdl = ''
		self.service_group = service_group
		self.version = version
		self.session = Session()
		self.available_services = []
		self.available_operations = {}		
		self._default_params_for_queries = {
			'requestedFlightFields':	[],
			'dataset':                  get_dataset(dataset),
			'trafficType':              'LOAD',
			'includeProposalFlights':   True, 
			'includeForecastFlights':   True,
			'sendTime':                 utils.sendTime(),
		}
		self.params_for_queries = self._default_params_for_queries

		# ------------- certificat ou proxy ? ------------- #
		if how_to_auth == 'cert': 
			# Si authentification par certificat
			self.wsdl = f"data/wsdl/{self.version}/{self.service_group}_PREOPS_{self.version}.wsdl"
			self.session.cert = (glob.glob("cert/crt.pem")[0], glob.glob("cert/key.pem")[0])
		
		elif how_to_auth == 'proxy': 
			# Si authentification via proxy (défaut)
			NM_B2B_API_KEY_ID = os.environ.get('NM_B2B_API_KEY_ID')  # default is None
			NM_B2B_API_SECRET = os.environ.get('NM_B2B_API_SECRET')  # default is None
			if not NM_B2B_API_KEY_ID or not NM_B2B_API_SECRET:
				print(f"Impossible de définir un couple clé/pass pour le proxy b2b.\
					Vérifiez que NM_B2B_API_KEY_ID et NM_B2B_API_SECRET sont bien définis dans votre environnement.")
				exit(1)
			self.wsdl = WSDL_PROXY + self.service_group + "_PREOPS_" + version + ".wsdl"
			self.session.auth = HTTPBasicAuth(NM_B2B_API_KEY_ID, NM_B2B_API_SECRET)
		
		else:
			print("Le mode d'authentification que vous avez spécifié n'existe pas (pour l'instant : 'cert' ou 'proxy').")
			exit(1)

		# -------------	
		self.cache = SqliteCache(path='./data/sqlite.db')
		self.transport = Transport(session=self.session, cache=self.cache)        
		self.conf = {
			'wsdl':         self.wsdl,
			'transport':    self.transport
		}		
		self.tmp_data = None
	
	# -----------------------------------------------------------------------------------------
	def set_available_services(self):
		self.available_services = []
		client = Client(**self.conf)
		for service in client.wsdl.services.values():
			self.available_services.append(service.__str__().split()[1])

	def show_available_services(self):
		if not self.available_services:
			self.set_available_services()
		print("Les services disponibles via {} sont : ".format(self.service_group)),
		for service in self.available_services:
			print('  * ', service)
	
	# -----------------------------------------------------------------------------------------
	def set_operations_of_service(self, service_name):
		if not self.available_services:
			self.set_available_services()
		if not service_name in self.available_services:
			raise Exception(f"Le service {service_name} n'est pas disponible.")
		client = Client(**self.conf, service_name=service_name)
		operations = [op for op in client.service.__dir__() if not op.startswith('__')]
		self.available_operations[service_name] = operations
	
	def show_operations_of_service(self, service_name):
		if not service_name in self.available_operations:
			self.set_operations_of_service(service_name=service_name)
		print(f"Les opérations disponibles pour {service_name} sont : ")
		for operation in self.available_operations[service_name]:
			print('  * ', operation)
	
	# -----------------------------------------------------------------------------------------
	def convert_data_to_json(self, obj):
		return serialize_object(self.tmp_data)

	def update_params_for_queries(self, new_params):
		for param in new_params:
			if param in self.params_for_queries:
				self.params_for_queries[param] = new_params[param]
	
	def set_traffic_window(self, startTime, endTime):
		return {
			'wef': utils.format_datetime_for_nm(startTime), 
			'unt': utils.format_datetime_for_nm(endTime)
		}
	
	# -----------------------------------------------------------------------------------------
	def queryFlightsByAirspace(self, airspace, startTime, endTime, other_params={}):
		""" Liste des vols par airspace
		
		Récupère la liste des vols transitant par un volume d'espace donné.
		
		Parameters
		----------
		airspace
			volume d'espace souhaité
		startTime
			heure de début (UTC)
		endTime
			heure de fin (UTC)
		other_params
			dictionnaire pour overrider les valeurs par défaut de _default_params_for_queries
    	"""
		
		trafficWindow = self.set_traffic_window(startTime, endTime)
		self.update_params_for_queries(other_params)		
		client = Client(**self.conf, service_name='FlightManagementService')
		self.tmp_data = client.service.queryFlightsByAirspace(
			airspace=airspace, 
			trafficWindow=trafficWindow, 
			**self.params_for_queries)
		return self.tmp_data
	
	def queryFlightsByAerodrome(self, aerodrome, aerodromeRole, startTime, endTime, other_params={}):
		""" Liste des vols par aérodrome
		
		Récupère la liste des vols au départ ou à l'arrivée d'un aérodrome.
		
		Parameters
		----------
		aerodrome
			code OACI du terrain souhaité
		aerodromeRole
			rôle du terrain (DEPARTURE...)
		startTime
			heure de début (UTC)
		endTime
			heure de fin (UTC)
		other_params
			dictionnaire pour overrider les valeurs par défaut de _default_params_for_queries
    	"""
		trafficWindow = self.set_traffic_window(startTime, endTime)
		self.update_params_for_queries(other_params)
		client = Client(**self.conf, service_name='FlightManagementService')
		self.tmp_data = client.service.queryFlightsByAerodrome(
			aerodrome=aerodrome, aerodromeRole=aerodromeRole,
			trafficWindow=trafficWindow,
			**self.params_for_queries)
		return self.tmp_data
	
	def queryFlightsByTrafficVolume(self, trafficVolume, startTime, endTime, other_params={}):
		""" Liste des vols par Traffic Volume (TV)
		
		Récupère la liste des vols transitant par un TV.
		
		Parameters
		----------
		trafficVolume
			nom du TV
		startTime
			heure de début (UTC)
		endTime
			heure de fin (UTC)
		other_params
			dictionnaire pour overrider les valeurs par défaut de _default_params_for_queries
    	"""
		trafficWindow = self.set_traffic_window(startTime, endTime)
		self.update_params_for_queries(other_params)
		client = Client(**self.conf, service_name='FlightManagementService')
		self.tmp_data = client.service.queryFlightsByTrafficVolume(
			trafficVolume=trafficVolume, 
			trafficWindow=trafficWindow,
			**self.params_for_queries)
		return self.tmp_data
