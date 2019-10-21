#-*- coding: utf-8 -*-
from manager import Manager
import datetime

test_manager = Manager() 					# avec proxy
test_manager = Manager(how_to_auth='cert') 	# avec cert

other_params = {    
	'requestedFlightFields': [
        'flightState', 
        'cfmuFlightType'
    ]
}

# startTime et endTime peuvent être des objets datetime.datetime ou des str au format AAAA-MM-JJ HH:MM
# attention : startTime et endTime doivent être exprimées en heures UTC
startTime=datetime.datetime(year=2019, month=10, day=21, hour=14, minute=30, tzinfo=datetime.timezone.utc)
endTime=  datetime.datetime(year=2019, month=10, day=21, hour=15, minute=30, tzinfo=datetime.timezone.utc)

# démo queryFlightsByAirspace
flight_list = test_manager.queryFlightsByAirspace(
    airspace="LFFFTH", 
    startTime=startTime, endTime=endTime,
    other_params=other_params)
print(flight_list.data)

# démo queryFlightsByAerodrome
flight_list = test_manager.queryFlightsByAerodrome(
    aerodrome="LFPG",
	aerodromeRole="DEPARTURE",
   	startTime=startTime, endTime=endTime,
	other_params=other_params)
print(flight_list.data)

# démo queryFlightsByTrafficVolume
flight_list = test_manager.queryFlightsByTrafficVolume(
    trafficVolume='LFFTN',
   	startTime=startTime, endTime=endTime,
	other_params=other_params)
print(flight_list.data)