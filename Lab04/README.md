## Opis projektu

Celem laboratorium było przygotowanie środowiska kontenerowego dla wcześniej stworzonej aplikacji ML udostępniającej API w frameworku Flask. 
W ramach zajęć wykorzystano Docker oraz Docker Compose do budowania obrazu aplikacji, uruchamiania kontenerów oraz konfiguracji wielu serwisów.

W projekcie utworzono plik `Dockerfile`, który:
- wykorzystuje oficjalny obraz `python:3.9-slim`,
- kopiuje plik `requirements.txt` oraz aplikację `app.py`,
- instaluje wymagane zależności,
- uruchamia aplikację w kontenerze.

Następnie zbudowano obraz Dockera lokalnie oraz uruchomiono kontener z aplikacją ML. 
Działanie endpointów API zostało przetestowane za pomocą narzędzia cURL.

W kolejnej części laboratorium skonfigurowano plik `docker-compose.yml`, który automatyzuje uruchamianie wielu serwisów jednocześnie. 
Docker Compose uruchamia:
- kontener aplikacji ML,
- dodatkowy serwis Redis,
- wspólną sieć dockerową umożliwiającą komunikację pomiędzy kontenerami.

Do uruchomienia aplikacji wykorzystano serwer Waitress, który umożliwia działanie aplikacji Flask w trybie produkcyjnym oraz działa poprawnie w środowisku Windows.