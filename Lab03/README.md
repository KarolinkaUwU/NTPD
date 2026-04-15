## Opis projektu

Projekt przedstawia prostą aplikację API stworzoną w frameworku Flask. 
Aplikacja udostępnia kilka endpointów umożliwiających komunikację z modelem uczenia maszynowego.

Zaimplementowane funkcjonalności:
- endpoint `/` – sprawdzenie działania API,
- endpoint `/predict` – wykonanie predykcji na podstawie danych wejściowych (model LogisticRegression),
- endpoint `/info` – informacje o modelu (typ, liczba cech, dane treningowe),
- endpoint `/health` – sprawdzenie stanu serwera.

Model został wytrenowany na prostych, przykładowych danych i służy do klasyfikacji na podstawie dwóch cech wejściowych.

## Dlaczego Flask + Waitress zamiast Flask + Gunicorn

Do uruchomienia aplikacji w trybie produkcyjnym wykorzystano serwer Waitress.

Gunicorn jest popularnym serwerem WSGI, jednak nie obsługuje systemu Windows, na którym realizowany był projekt. 
Z tego powodu użycie Gunicorn wymagałoby dodatkowej konfiguracji środowiska (np. WSL lub Linux).

Waitress jest lekkim serwerem WSGI rekomendowanym dla aplikacji Flask i działa natywnie na Windows, co umożliwia szybkie i poprawne uruchomienie aplikacji w trybie produkcyjnym bez dodatkowych narzędzi.

Dzięki temu rozwiązanie jest prostsze w konfiguracji i w pełni zgodne z wymaganiami zadania.