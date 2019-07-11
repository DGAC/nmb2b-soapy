from manager import Manager
import json
import utils

test_manager = Manager()
#test_manager.show_available_services()
#test_manager.show_operations_of_service(service_name='FlightManagementService')

requestedFlightFields = ['aircraftOperator']
# TODO : renseigner plusieurs airspace ?
fpl_data = test_manager.queryFlightsByAirspace(
    airspace="LFFFTH",
   	dataset='OPERATIONAL',
   	includeProposalFlights=True,
   	includeForecastFlights=True,
   	trafficType='LOAD',
   	trafficWindow={'wef': "2019-07-11 12:00", 'unt': "2019-07-11 14:00"},
	requestedFlightFields=requestedFlightFields,
	py_output=False
)

print(fpl_data)
#utils.write_content_to_file(filename="fpl_data.json", content=json.dumps(fpl_data))