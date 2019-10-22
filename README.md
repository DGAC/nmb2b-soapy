Pour le wiki complet :
* depuis GitLab : [c'est par ici](https://gitlab.asap.dsna.fr/maxence.renaud/soapy/wikis/home),
* depuis GitHub : [c'est par là](https://github.com/DGAC/nmb2b-soapy/wiki).

Pour utiliser les fonctionnalités offertes par `soapy`,  tout passe par le `manager`.
```python
from soapy.manager import Manager
import datetime

# on instancie son propre manager
test_manager = Manager()                   # si utilisation du proxy b2b NM
test_manager = Manager(how_to_auth='cert') # si utilisation de votre propre certificat

# pour afficher les différents services disponibles
test_manager.show_available_services()

# pour afficher les différentes opérations disponibles pour un service particulier
test_manager.show_operations_of_service(service_name='FlightManagementService')

# startTime et endTime peuvent être des objets datetime.datetime ou des str au format AAAA-MM-JJ HH:MM
# attention : startTime et endTime doivent être exprimées en heures UTC
startTime=datetime.datetime(year=2019, month=10, day=21, hour=14, minute=30, tzinfo=datetime.timezone.utc)
endTime=  datetime.datetime(year=2019, month=10, day=21, hour=15, minute=30, tzinfo=datetime.timezone.utc)

# on précise les champs qui nous intéressent pour des requêtes de listes de vols 
# (requestedFlightFields, voir doc NM), et si nécessaire on override les valeurs 
# par défaut pour la requête (voir _default_params_for_queries dans le code source de Manager).
other_params = {
    'requestedFlightFields': ['flightState', 'cfmuFlightType']
}

# pour afficher une liste de vols pour un terrain donné
flight_list = test_manager.queryFlightsByAerodrome(
    aerodrome="LFPG",
	aerodromeRole="DEPARTURE",
   	startTime=startTime, endTime=endTime,
	other_params=other_params)
print(flight_list.data)

# pour afficher une liste de vols pour un Traffic Volume donné
flight_list = test_manager.queryFlightsByTrafficVolume(
    trafficVolume='LFFTN',
   	startTime=startTime, endTime=endTime,
	other_params=other_params)
print(flight_list.data)
```