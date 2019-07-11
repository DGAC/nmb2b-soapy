import operator

from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client, Settings
from zeep.cache import SqliteCache
from zeep.transports import Transport

from shared_vars import (B2B_PROXY, DEFAULT_B2B_VERSION, DEFAULT_DATASET,
                         WSDL_PROXY, get_dataset)
import utils


class Manager():

    def __init__(
        self, version=DEFAULT_B2B_VERSION, wanted_services="FlightServices", 
        dataset=DEFAULT_DATASET, *args, **kwargs):
        
        self.wanted_services = wanted_services
        self.available_services = []
        self.available_operations = {}
        self.dataset = get_dataset(dataset)
        self.session = Session()
        self.session.auth = HTTPBasicAuth(B2B_PROXY['key'], B2B_PROXY['secret'])        
        self.wsdl = WSDL_PROXY + wanted_services + "_PREOPS_" + version + ".wsdl"
        self.cache = SqliteCache(path='./data/sqlite.db', timeout=60)
        self.transport = Transport(session=self.session, cache=self.cache)        
        self.conf = {
            'wsdl': self.wsdl,
            'transport': self.transport
        }
    
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
    
    def set_operations_of_service(self, service_name):
        if not self.available_services:
            self.set_available_services()
        if not service_name in self.available_services:
            print(f"Le service {service_name} n'est pas disponible.")
        client = Client(**self.conf, service_name=service_name)
        operations = [op for op in client.service.__dir__() if not op.startswith('__')]
        self
        print(f"Les opérations disponibles pour {service_name} sont : ")
        for op in operations:
            print(' * ', op)
    
    def queryFlightsByAirspace(
        self, airspace, sendTime=utils.sendTime(), dataset, trafficType,
        includeProposalFlights, includeForecastFlights, 
        trafficWindow):
        client = Client(**self.conf, service_name='FlightManagementService')
        return client.service.queryFlightsByAirspace(
            airspace=airspace, sendTime=sendTime, dataset=self.dataset, trafficType=trafficType,
            includeProposalFlights=includeProposalFlights, includeForecastFlights=includeForecastFlights, 
            trafficWindow=trafficWindow)
