#-*- coding: utf-8 -*-
from manager import Manager

test_manager = Manager() 					# avec proxy
test_manager = Manager(how_to_auth='cert') 	# avec cert

other_params = {    
	'requestedFlightFields': [
        'flightState', 
        'cfmuFlightType'
    ]
}

# démo queryFlightsByAirspace
flight_list = test_manager.queryFlightsByAirspace(
    airspace="LFFFTH", 
    startTime="2019-10-18 17:00", endTime="2019-10-18 18:30",
    other_params=other_params)
print(flight_list.data)

# démo queryFlightsByAerodrome
flight_list = test_manager.queryFlightsByAerodrome(
    aerodrome="LFPG",
	aerodromeRole="DEPARTURE",
   	startTime="2019-10-18 17:00", endTime="2019-10-18 18:30",
	other_params=other_params)
print(flight_list.data)

# démo queryFlightsByTrafficVolume
flight_list = test_manager.queryFlightsByTrafficVolume(
    trafficVolume='LFFTN',
   	startTime="2019-10-18 17:00", endTime="2019-10-18 18:30",
	other_params=other_params)
print(flight_list.data)