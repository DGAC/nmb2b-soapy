#-*- coding: utf-8 -*-
# NOTE : à exécuter dans un shell Python plutôt que comme un script !
from manager import Manager

test_manager = Manager() 					# avec proxy
test_manager = Manager(how_to_auth='cert') 	# avec cert
requestedFlightFields = ['flightState', 'cfmuFlightType']

# démo queryFlightsByAirspace
flight_list = test_manager.queryFlightsByAirspace(
    airspace="LFFFTH",
   	startTime="2019-10-16 17:00",
	endTime="2019-10-16 18:30",
	requestedFlightFields=requestedFlightFields)
print(flight_list.data)

# démo queryFlightsByAerodrome
flight_list = test_manager.queryFlightsByAerodrome(
    aerodrome="LFPG",
	aerodromeRole="DEPARTURE",
   	startTime="2019-10-16 17:00",
	endTime="2019-10-16 18:30",
	requestedFlightFields=requestedFlightFields)
print(flight_list.data)

# démo queryFlightsByTrafficVolume
flight_list = test_manager.queryFlightsByTrafficVolume(
    trafficVolume='LFFTN',
   	startTime="2019-10-16 17:00",
	endTime="2019-10-16 18:30",
	requestedFlightFields=requestedFlightFields)
print(flight_list.data)

