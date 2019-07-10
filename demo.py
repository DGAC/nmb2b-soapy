from manager import Manager
from utils import sendTime

test_manager = Manager()
test_manager.show_services()
#test_manager.show_operations_of_service(service_name='FlightManagementService')
test = test_manager.queryFlightsByAirspace(
    airspace="LFFFUZ",
   	sendTime=sendTime(),
   	dataset='OPERATIONAL',
   	includeProposalFlights=False,
   	includeForecastFlights=True,
   	trafficType='LOAD',
   	trafficWindow={'wef': "2019-07-11 06:30", 'unt': "2019-07-11 07:00"}
)
print(test)
