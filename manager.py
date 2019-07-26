import operator

from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client, Settings
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.helpers import serialize_object
import json

from shared_vars import (B2B_PROXY, DEFAULT_B2B_VERSION, DEFAULT_DATASET,
                         WSDL_PROXY, get_dataset)
import utils


class Manager():

    def __init__(
        self, 
        version=DEFAULT_B2B_VERSION, 
        wanted_services="FlightServices", 
        dataset=DEFAULT_DATASET, 
        *args, **kwargs
        ):
        
        self.wanted_services = wanted_services
        self.available_services = []
        self.available_operations = {}
        
        self._default_params_for_queries = {
            'dataset':                  get_dataset(dataset),
            'trafficType':              'LOAD',
            'includeProposalFlights':   True, 
            'includeForecastFlights':   True,
            'sendTime':                 utils.sendTime(),
        }
        
        self.session = Session()
        self.session.auth = HTTPBasicAuth(B2B_PROXY['key'], B2B_PROXY['secret'])        
        self.wsdl = WSDL_PROXY + wanted_services + "_PREOPS_" + version + ".wsdl"
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
        print("Les services disponibles via {} sont : ".format(self.wanted_services)),
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

    # -----------------------------------------------------------------------------------------
    def queryFlightsByAirspace(
        self, 
        airspace, 
        startTime, 
        endTime, 
        requestedFlightFields=  [],
        dataset=                None,
        trafficType=            None,
        includeProposalFlights= None,
        includeForecastFlights= None,
        sendTime=               None,
        ):

        dataset = self._default_params_for_queries['dataset'] if not dataset else dataset
        trafficType = self._default_params_for_queries['trafficType'] if not trafficType else trafficType
        includeProposalFlights = self._default_params_for_queries['includeProposalFlights'] if not includeProposalFlights else includeProposalFlights
        includeForecastFlights = self._default_params_for_queries['includeForecastFlights'] if not includeForecastFlights else includeForecastFlights
        sendTime = self._default_params_for_queries['sendTime'] if not sendTime else sendTime
        trafficWindow = {'wef': startTime, 'unt': endTime}

        client = Client(**self.conf, service_name='FlightManagementService')
        self.tmp_data = client.service.queryFlightsByAirspace(
            airspace=airspace, 
            dataset=dataset, trafficType=trafficType,
            includeProposalFlights=includeProposalFlights, includeForecastFlights=includeForecastFlights, 
            trafficWindow=trafficWindow, requestedFlightFields=requestedFlightFields, sendTime=sendTime)
        return self.tmp_data
    
    def queryFlightsByAerodrome(
        self, 
        aerodrome,
        aerodromeRole,
        startTime, 
        endTime, 
        requestedFlightFields=  [],
        dataset=                None,
        trafficType=            None,
        includeProposalFlights= None,
        includeForecastFlights= None,
        sendTime=               None,
        ):

        dataset = self._default_params_for_queries['dataset'] if not dataset else dataset
        trafficType = self._default_params_for_queries['trafficType'] if not trafficType else trafficType
        includeProposalFlights = self._default_params_for_queries['includeProposalFlights'] if not includeProposalFlights else includeProposalFlights
        includeForecastFlights = self._default_params_for_queries['includeForecastFlights'] if not includeForecastFlights else includeForecastFlights
        sendTime = self._default_params_for_queries['sendTime'] if not sendTime else sendTime
        trafficWindow = {'wef': startTime, 'unt': endTime}

        client = Client(**self.conf, service_name='FlightManagementService')
        self.tmp_data = client.service.queryFlightsByAerodrome(
            aerodrome=aerodrome, aerodromeRole=aerodromeRole, 
            dataset=dataset, trafficType=trafficType,
            includeProposalFlights=includeProposalFlights, includeForecastFlights=includeForecastFlights, 
            trafficWindow=trafficWindow, requestedFlightFields=requestedFlightFields, sendTime=sendTime)
        return self.tmp_data
    
    def queryFlightsByTrafficVolume(
        self, 
        trafficVolume, 
        startTime, 
        endTime, 
        requestedFlightFields=  [],
        dataset=                None,
        trafficType=            None,
        includeProposalFlights= None,
        includeForecastFlights= None,
        sendTime=               None,
        ):

        dataset = self._default_params_for_queries['dataset'] if not dataset else dataset
        trafficType = self._default_params_for_queries['trafficType'] if not trafficType else trafficType
        includeProposalFlights = self._default_params_for_queries['includeProposalFlights'] if not includeProposalFlights else includeProposalFlights
        includeForecastFlights = self._default_params_for_queries['includeForecastFlights'] if not includeForecastFlights else includeForecastFlights
        sendTime = self._default_params_for_queries['sendTime'] if not sendTime else sendTime
        trafficWindow = {'wef': startTime, 'unt': endTime}

        client = Client(**self.conf, service_name='FlightManagementService')
        self.tmp_data = client.service.queryFlightsByTrafficVolume(
            trafficVolume=trafficVolume, 
            dataset=dataset, trafficType=trafficType,
            includeProposalFlights=includeProposalFlights, includeForecastFlights=includeForecastFlights, 
            trafficWindow=trafficWindow, requestedFlightFields=requestedFlightFields, sendTime=sendTime)
        return self.tmp_data