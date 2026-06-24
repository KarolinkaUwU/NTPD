## Zadanie 1. Konfiguracja środowiska Apache Airflow

W ramach zadania skonfigurowano środowisko Apache Airflow z wykorzystaniem Docker Compose. Uruchomiono kontenery wymagane do działania Airflow, w tym komponenty odpowiedzialne za interfejs użytkownika, harmonogramowanie zadań, przetwarzanie DAG-ów oraz obsługę bazy danych.

Poprawność działania środowiska sprawdzono za pomocą polecenia `docker ps`. Wynik polecenia pokazał uruchomione kontenery Airflow, między innymi `airflow-scheduler`, `airflow-apiserver`, `airflow-worker`, `airflow-dag-processor`, a także kontenery `postgres` i `redis`. Kontenery miały status `Up` oraz `healthy`, co oznacza, że środowisko zostało poprawnie uruchomione.

Następnie otwarto interfejs użytkownika Airflow w przeglądarce pod adresem `http://localhost:8080`. Logowanie do panelu zakończyło się poprawnie, a w widoku głównym widoczne były informacje o stanie systemu, między innymi działająca baza danych metadanych, scheduler oraz procesor DAG-ów.

Na końcu sprawdzono konfigurację folderu DAG-ów. Za pomocą polecenia `airflow config get-value core dags_folder` uruchomionego wewnątrz kontenera schedulera potwierdzono, że folder DAG-ów jest ustawiony na `/opt/airflow/dags`. Oznacza to, że pliki DAG umieszczane w lokalnym folderze `dags` są widoczne dla Airflow i mogą być uruchamiane z poziomu interfejsu.

## Zadanie 2. Prosty DAG do re-trenowania modelu

W ramach zadania utworzono nowy plik DAG o nazwie `retrain_model_dag.py` w folderze `dags`. Plik ten definiuje przepływ pracy odpowiedzialny za automatyczne re-trenowanie modelu ML w środowisku Apache Airflow.

DAG został przygotowany tak, aby wykonywał pełny proces re-trenowania modelu. W pierwszym kroku pobierany lub generowany jest nowy zbiór danych, który jest zapisywany w pliku `data/new_data.csv`. Dane zawierają cechy wejściowe oraz kolumnę `target`, czyli etykietę wykorzystywaną do uczenia modelu.

Następnie DAG trenuje nową wersję modelu klasyfikacyjnego `RandomForestClassifier`. Dane są dzielone na część treningową i walidacyjną, dzięki czemu po treningu możliwe jest sprawdzenie jakości modelu na osobnym zbiorze walidacyjnym.

Po zakończeniu treningu model zostaje zapisany w folderze `models/`. Nazwa pliku modelu zawiera timestamp, np. `rf_model_20260623_221500.pkl`, dzięki czemu kolejne wersje modelu nie nadpisują się wzajemnie. Takie rozwiązanie pozwala zachować historię wytrenowanych modeli i łatwiej wrócić do wcześniejszej wersji.

Dodatkowo wykonywana jest prosta walidacja modelu. Dla zbioru walidacyjnego obliczana jest metryka `accuracy`, a wynik zostaje zapisany w raporcie tekstowym w folderze `reports/`. Dzięki temu po każdym uruchomieniu DAG-a można sprawdzić, jaką jakość osiągnęła nowa wersja modelu.

Dla DAG-a ustawiono harmonogram `@daily`, co oznacza, że proces re-trenowania modelu może być wykonywany automatycznie raz dziennie. Ustawiono również `catchup=False`, aby Airflow nie uruchamiał zaległych wykonań dla wcześniejszych dat. Dzięki temu DAG wykonuje tylko aktualne zaplanowane uruchomienia.

Zadanie pokazuje podstawowy mechanizm dynamicznego re-trenowania modelu ML. Airflow odpowiada za harmonogramowanie i uruchamianie procesu, a kod DAG-a wykonuje kolejne etapy: przygotowanie danych, trening modelu, zapis nowej wersji oraz walidację.

## Zadanie 3. Rozszerzenie o walidację i warunkową wymianę modelu

W ramach zadania rozbudowano istniejący DAG `retrain_model` o dodatkową logikę walidacji oraz warunkowej aktualizacji modelu produkcyjnego. Po wytrenowaniu nowej wersji modelu wykonywana jest walidacja na zbiorze walidacyjnym, a jako metrykę jakości wykorzystano `accuracy`.

Nowa wersja modelu jest zapisywana w folderze `models/` jako osobny plik z timestampem w nazwie, np. `rf_model_20260624_073328.pkl`. Dzięki temu każda wytrenowana wersja modelu pozostaje zachowana jako model archiwalny i nie nadpisuje poprzednich wyników.

Następnie DAG sprawdza, czy istnieje aktualny model produkcyjny zapisany jako `models/production/current_model.pkl`. Jeśli taki model istnieje, jego wynik jest porównywany z wynikiem nowo wytrenowanego modelu. Jeżeli nowy model osiągnie wyższą wartość `accuracy`, zostaje skopiowany do folderu `models/production/` i podmieniony jako aktualny model produkcyjny. Jeśli wynik nie jest lepszy, nowy model pozostaje tylko jako wersja archiwalna.

Podczas pierwszego uruchomienia nie było jeszcze wcześniejszego modelu produkcyjnego, dlatego nowo wytrenowany model został ustawiony jako model produkcyjny. Potwierdzeniem wykonania zadania jest obecność pliku `current_model.pkl` w folderze `models/production/`.

Dodatkowo DAG zapisuje raport walidacji oraz raport decyzji o aktualizacji modelu w folderze `reports/`. Raporty te zawierają informacje o ścieżce nowego modelu, wyniku accuracy oraz decyzji, czy model produkcyjny został podmieniony.

W Airflow UI uruchomienia DAG-a zakończyły się statusem `Sukces`, co potwierdza, że cały przepływ działa poprawnie: przygotowanie danych, trenowanie modelu, walidacja oraz warunkowa aktualizacja modelu produkcyjnego.
