Pour le wiki complet, [c'est par ici](https://gitlab.asap.dsna.fr/maxence.renaud/soapy/wikis/home).

Aperçu de l'utilisation du module :
```python
from soapy.manager import Manager

# on instancie son propre manager
test_manager = Manager()

# pour afficher les différents services disponibles
test_manager.show_available_services()

# pour afficher les différentes opérations disponibles pour un service particulier
test_manager.show_operations_of_service(service_name='FlightManagementService')

# on précise les champs qui nous intéressent pour des requêtes de listes de vols (voir doc NM)
requestedFlightFields = ['flightState', 'cfmuFlightType']

# pour afficher une liste de vols pour un Traffic Volume donné
flight_list = test_manager.queryFlightsByTrafficVolume(
   trafficVolume='LFFTN',
   startTime="2019-07-26 11:00",
   endTime="2019-07-26 13:30",
   requestedFlightFields=requestedFlightFields)
print(flight_list.data)

# pour afficher une liste de vols pour un terrain donné
flight_list = test_manager.queryFlightsByAerodrome(
    aerodrome="LFPG",
    aerodromeRole="DEPARTURE",
    startTime="2019-07-26 11:00",
    endTime="2019-07-26 13:30",
    requestedFlightFields=requestedFlightFields)
print(flight_list.data)

```