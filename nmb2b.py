#-*- coding: utf-8 -*-

import datetime
import logging
import os
import sys
import xml.etree.ElementTree as ET

#from elasticsearch import Elasticsearch
import requests
from requests.auth import HTTPBasicAuth

from conf.shared_vars import (B2B_PROXY, CERTS_PATH, DATA_PATH,
                              DEFAULT_B2B_VERSION, DEFAULT_DATASET,
                              DEFAULT_ORG, GENERIC_WRAPPER, get_dataset,
                              get_entry_point, get_local_proxy)
#from decolog import *
#from nmb2butils import *
#from utils import *
from utils import autosendtime, save_metrics_to_es, write_content_to_file


'''
B2BPROXY = proxy réalisé par Benjamin sur AWS.
TODO : trouver une bonne façon de loguer ce qui est nécessaire (paramétrage)
'''

class NmB2bGetterBase():
	"""
	Classe générique d'accès au webservice b2b de NM.
	Des paramètres nommés et/ou non nommés peuvent être passés au constructeur.
	"""
	
	def __init__(
		self, org=DEFAULT_ORG, version=DEFAULT_B2B_VERSION, save_metrics_to_es=True, save_data_to_xml=True, wanted_dataset=DEFAULT_DATASET, 
		getter_name="undefined", nm_service_function="undefined", request_core="undefined", **kwargs):
		'''
		Attributs initialisés :
			- local_proxy : proxy local DSNA
			- entry_point : point d'accès NM B2B selon version
			- save_metrics_to_es : utilisation ou non d'Elastic Search pour enregistrer les metriques
			- wanted_dataset : dataset NM souhaité
			-
			-
			- 
		'''
		self.local_proxy 			= get_local_proxy(org)
		self.entry_point 			= get_entry_point(version)
		self.save_metrics_to_es		= save_metrics_to_es
		self.save_data_to_xml		= save_data_to_xml
		self.dataset 				= get_dataset(wanted_dataset)
		self.getter_name			= getter_name
		self.nm_service_function	= nm_service_function
		self.request_core			= request_core
		self.nm_request 			= None
		self.nm_response			= None
		

	def show_conf(self):
		'''
		Affiche les éléments de configuration pertinents :
			-utilisation d'un proxy local ou non
			-accès direct au B2B NM ou via proxy AWS
			-utilisation d'elastic search pour les métriques
		# TODO : surcharger la méthode __str__ tout simplement.
		'''
		if self.local_proxy:
			print("Proxy local (DSNA) : ", self.local_proxy)		
		print("Entry point : ", self.entry_point)		
		print("Utilisation d'Elastic Search pour les métriques : ", self.save_metrics_to_es)

	def is_conf_valid(self):
		if "undefined" in [self.getter_name, self.nm_service_function, self.request_core]:
			print("L'un des attributs getter_name, nm_service_function ou request_core n'a pas été défini.")
			return False
		return True

	def wrap_request(self, request_to_wrap):
		'''
		Permet d'encapsuler une requête :
			- request_to_wrap = requête en paramètre que l'on va encapsuler
		'''
		return GENERIC_WRAPPER.format(request_to_wrap=request_to_wrap)
	
	def is_connexion_ok(self):
		'''
		Return True si la connection au B2B NM est ouverte, False sinon.
		TODO : A consolider/valider.
		'''
		response = None
		
		if not B2B_PROXY:
			response = requests.get(
				self.entry_point, proxies=self.local_proxy, 
				cert=CERTS_PATH)
		else:
			response = requests.get(
				self.entry_point, proxies=self.local_proxy, 
				auth=HTTPBasicAuth(B2B_PROXY['key'], B2B_PROXY['secret']))

		if response.status_code != 200:
			print(response.text)
			return False
		return True
	
	def _save_data_to_xml(self):
		'''
		Permet d'enregistrer la requête envoyée à NM et la réponse brute de NM au format XML.
		'''
		if self.nm_request:
			print("Enregistrement de la requête au format XML...")
			request_filename = os.path.join(
				DATA_PATH, self.getter_name, "requests",
				f"request-{self.getter_name}-{datetime.datetime.utcnow().strftime('%s')}.xml")
			write_content_to_file(filename=request_filename, content=self.nm_request.text)
			print("Enregistrement de la requête au format XML terminé.")
		if self.nm_response:
			print("Enregistrement de la réponse NM au format XML...")
			response_filename = os.path.join(
				DATA_PATH, self.getter_name, "responses",
				f"response-{self.getter_name}-{datetime.datetime.utcnow().strftime('%s')}.xml")
			write_content_to_file(filename=response_filename, content=self.nm_response.text)
			print("Enregistrement de la réponse NM au format XML terminé.")

	def set_metrics_wanted(self, response):
		# TODO : vérifier que response est bien une response
		self.metrics_wanted = {
			"ts-start": 			datetime.datetime.utcnow().strftime("%s"),
			"date0": 				datetime.datetime.strftime(datetime.datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ"),
			"ts-end": 				datetime.datetime.utcnow().strftime("%s"),
			"data": 				response.text,
			"datasize":				len(response.text),
			"getter_name": 			self.getter_name,
			"nm_service_function": 	self.nm_service_function 
		}

	def generate_and_save_response_from_nm(self):
		'''
		Permet de récupérer la réponse NM à partir d'une requête customisée.
		Enregistre le résultat dans un répertoire requests au format XML.
		'''
		
		if not self.is_conf_valid():
			print("Configuration du getter non valide, impossible d'exécuter toute requête.")
			raise Exception

		# if not self.is_connexion_ok():
		# 	print("Impossible d'établir une connexion avec NM.")
		# 	raise Exception
		
		ast = autosendtime()
		initial_request = f"<{self.nm_service_function}>{ast}{self.request_core}</{self.nm_service_function}>"
		nm_full_request = self.wrap_request(request_to_wrap=initial_request)

		print("initial_request : ", initial_request)
		print("nm_full_request : ", nm_full_request)

		if not B2B_PROXY:
			self.nm_response = requests.post(
				self.entry_point, data=nm_full_request, proxies=self.local_proxy, 
				cert=CERTS_PATH)
		else:
			self.nm_response = requests.post(
				self.entry_point, data=nm_full_request, proxies=self.local_proxy, 
				auth=HTTPBasicAuth(B2B_PROXY['key'], B2B_PROXY['secret']))

		if self.save_metrics_to_es and self.nm_response: 
			self.set_metrics_wanted(response=self.nm_response)
			save_metrics_to_es(self.metrics_wanted)
		
		if self.save_data_to_xml:
			self._save_data_to_xml()

	def get_nm_response_as_xml(self):
		'''
		Retourne la response du NM au format XML.
		'''
		if not self.nm_response:
			print("Aucune réponse NM n'a été générée et/ou enregistrée en mémoire.")
			return None
		return ET.fromstring(self.nm_response.text)
