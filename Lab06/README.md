## Zadanie 1. Przygotowanie repozytorium z przykładowym modelem ML

Laboratorium wykonano w istniejącym repozytorium `NTPD`, w którym przechowywane są wszystkie laboratoria z przedmiotu. Zamiast tworzyć osobne repozytorium `ML-CI-CD`, przygotowano katalog `Lab06`, zgodny z dotychczasową strukturą projektu.

Do katalogu `Lab06` wykorzystano aplikację API z poprzednich zajęć. W projekcie znajdowały się pliki `app.py`, `Dockerfile`, `.dockerignore`, `requirements.txt`, `model.py` oraz `test_model.py`.

W pliku `model.py` przygotowano funkcje `train_and_predict()` oraz `get_accuracy()`. Funkcja `train_and_predict()` trenuje prosty model `LogisticRegression` na zbiorze Iris i zwraca predykcje oraz prawdziwe etykiety ze zbioru testowego. Funkcja `get_accuracy()` oblicza dokładność modelu.

W pliku `test_model.py` przygotowano testy jednostkowe z użyciem biblioteki `pytest`. Testy sprawdzają, czy predykcje nie są puste, czy ich liczba odpowiada liczbie próbek testowych, czy wartości predykcji mieszczą się w zakresie klas zbioru Iris `0–2` oraz czy model osiąga dokładność co najmniej `70%`.

Kod aplikacji został wysłany do repozytorium GitHub. W katalogu `Lab06` widoczne są wszystkie wymagane pliki, w tym `requirements.txt`, który zawiera zależności potrzebne do uruchomienia aplikacji i testów.

## Zadanie 2. Konfiguracja GitHub Actions do automatycznego testowania

W ramach zadania skonfigurowano GitHub Actions do automatycznego uruchamiania testów jednostkowych dla projektu z katalogu `Lab06`. W głównym katalogu repozytorium utworzono folder `.github/workflows`, a następnie dodano plik `lab06-tests.yml`.

Workflow został przygotowany tak, aby uruchamiał się automatycznie po wykonaniu `push` oraz `pull request` do głównej gałęzi repozytorium. Ponieważ projekt korzystał z gałęzi `master`, konfigurację rozszerzono również o tę gałąź. Dodano także możliwość ręcznego uruchomienia workflow za pomocą `workflow_dispatch`.

W pliku YAML zdefiniowano zadanie wykonywane na środowisku `ubuntu-latest`. Workflow pobiera kod repozytorium, konfiguruje środowisko Python w wersji `3.9`, instaluje zależności z pliku `Lab06/requirements.txt`, a następnie uruchamia testy jednostkowe z pliku `test_model.py` za pomocą biblioteki `pytest`.

Po wypchnięciu zmian do repozytorium workflow został uruchomiony w zakładce `Actions` na GitHubie. Uruchomienie zakończyło się statusem `Success`, a job `test` został wykonany poprawnie.

W szczegółach wykonania workflow widoczny był etap `Run unit tests`, w którym uruchomiono polecenie `pytest test_model.py`. Testy zakończyły się wynikiem `4 passed`, co potwierdza, że wszystkie testy jednostkowe przygotowane w Zadaniu 1 przeszły poprawnie w środowisku GitHub Actions.
