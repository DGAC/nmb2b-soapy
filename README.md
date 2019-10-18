Pour le wiki complet, [c'est par ici](https://gitlab.asap.dsna.fr/maxence.renaud/soapy/wikis/home).

Pour utiliser les fonctionnalités offertes par `soapy`,  tout passe par le `manager`.
```python
from soapy.manager import Manager

# on instancie son propre manager
test_manager = Manager()                   # si utilisation du proxy b2b NM
test_manager = Manager(how_to_auth='cert') # si utilisation de votre propre certificat

# pour afficher les différents services disponibles
test_manager.show_available_services()

# pour afficher les différentes opérations disponibles pour un service particulier
test_manager.show_operations_of_service(service_name='FlightManagementService')

# on précise les champs qui nous intéressent pour des requêtes de listes de vols (requestedFlightFields, voir doc NM), et si nécessaire on override les valeurs par défaut pour la requête (voir _default_params_for_queries dans le code source de Manager).
other_params = {    
	'requestedFlightFields': ['flightState', 'cfmuFlightType']
}

# pour afficher une liste de vols pour un terrain donné
flight_list = test_manager.queryFlightsByAerodrome(
    aerodrome="LFPG",
	aerodromeRole="DEPARTURE",
   	startTime="2019-10-18 17:00", endTime="2019-10-18 18:30",
	other_params=other_params)
print(flight_list.data)

# pour afficher une liste de vols pour un Traffic Volume donné
flight_list = test_manager.queryFlightsByTrafficVolume(
    trafficVolume='LFFTN',
   	startTime="2019-10-18 17:00", endTime="2019-10-18 18:30",
	other_params=other_params)
print(flight_list.data)
```