## Zadanie 1. Przygotowanie środowiska i instalacja MLflow

W ramach zadania przygotowano nowe środowisko wirtualne `.venv` w projekcie PyCharm. Środowisko zostało utworzone za pomocą polecenia `python -m venv .venv`, a następnie aktywowane w terminalu PowerShell.

Po aktywacji środowiska zainstalowano bibliotekę `mlflow` za pomocą polecenia `pip install mlflow`. Poprawność instalacji sprawdzono komendą `mlflow --version`. Polecenie zwróciło wynik `mlflow, version 3.14.0`, co potwierdza, że biblioteka została poprawnie zainstalowana.

Następnie uruchomiono lokalny serwer MLflow za pomocą polecenia `mlflow ui`. Po uruchomieniu serwera otwarto interfejs MLflow w przeglądarce pod adresem `http://127.0.0.1:5000`.

Interfejs MLflow uruchomił się poprawnie. W panelu widoczna była strona główna MLflow oraz domyślny eksperyment `Default`. Oznacza to, że środowisko zostało poprawnie skonfigurowane i jest gotowe do dalszego logowania eksperymentów, parametrów, metryk oraz modeli.

## Zadanie 2. Stworzenie prostego eksperymentu MLflow z logowaniem hiperparametrów i metryk

W ramach zadania utworzono prosty eksperyment MLflow z wykorzystaniem biblioteki `scikit-learn`. Zamiast przykładowego modelu `DecisionTreeClassifier` oraz zbioru Iris wybrano model `LogisticRegression` oraz zbiór danych Breast Cancer Wisconsin dostępny w `sklearn.datasets`.

Dane zostały załadowane za pomocą funkcji `load_breast_cancer()`, a następnie podzielone na zbiór treningowy i testowy w proporcji 80% / 20% z użyciem `train_test_split`. Przed treningiem zastosowano `StandardScaler`, ponieważ regresja logistyczna lepiej działa na danych o podobnej skali wartości.

Model został zbudowany jako `Pipeline`, składający się ze standaryzacji danych oraz klasyfikatora `LogisticRegression`. W eksperymencie ustawiono hiperparametry: `C = 1.0`, `max_iter = 1000` oraz `solver = "lbfgs"`.

Po uruchomieniu skryptu `train.py` model został wytrenowany, a następnie oceniony na zbiorze testowym. Do MLflow zalogowano parametry modelu, nazwę zbioru danych, rozmiar zbioru testowego oraz wartości hiperparametrów. Zalogowano również metryki: `accuracy`, `precision`, `recall` oraz `f1_score`.

Uzyskane wyniki były bardzo dobre: `accuracy = 0.9825`, `precision = 0.9861`, `recall = 0.9861` oraz `f1_score = 0.9861`. Wyniki te oznaczają, że model poprawnie klasyfikuje większość przykładów ze zbioru testowego.

Po wykonaniu skryptu w interfejsie MLflow pojawił się run o nazwie `logistic_regression_breast_cancer`. W szczegółach runu widoczne były zalogowane metryki, parametry oraz zapisany model, co potwierdza poprawne wykonanie eksperymentu MLflow.

## Zadanie 3. Porównanie eksperymentów poprzez zmianę hiperparametrów

W ramach zadania zmodyfikowano plik `train.py`, dodając pętlę uruchamiającą kilka eksperymentów MLflow dla różnych wartości hiperparametru `C`. Ponieważ w projekcie wykorzystano model `LogisticRegression`, zamiast parametru `max_depth` zastosowano parametr `C`, który kontroluje siłę regularyzacji modelu.

Przetestowano cztery wartości parametru: `C = 0.01`, `C = 0.1`, `C = 1.0` oraz `C = 10.0`. Dla każdej konfiguracji utworzono osobny run w MLflow, a następnie zalogowano parametry, metryki oraz model.

Po uruchomieniu skryptu w interfejsie MLflow pojawiły się cztery runy: `logistic_regression_C_0.01`, `logistic_regression_C_0.1`, `logistic_regression_C_1.0` oraz `logistic_regression_C_10.0`. Dzięki temu możliwe było porównanie wpływu hiperparametru `C` na jakość modelu.

W MLflow UI porównano wyniki poszczególnych eksperymentów. Najlepszy wynik uzyskała konfiguracja `C = 1.0`, dla której otrzymano `accuracy = 0.9825`, `precision = 0.9861`, `recall = 0.9861` oraz `f1_score = 0.9861`.

Porównanie pokazało, że zmiana hiperparametru wpływa na jakość klasyfikacji. Zbyt mała wartość `C` powoduje silniejszą regularyzację, przez co model może być prostszy i uzyskiwać słabsze wyniki. Wartość `C = 1.0` okazała się najlepszym wyborem dla tego zbioru danych i zastosowanego modelu.

## Zadanie 4. Rejestrowanie i wersjonowanie modelu w MLflow

W ramach zadania sprawdzono, w jaki sposób MLflow zapisuje modele po wykonaniu kolejnych eksperymentów. Każdy run utworzony w poprzednich zadaniach posiadał własny zapisany model dostępny w zakładce `Artifacts`.

Dla przykładowego runu `logistic_regression_C_10.0` otwarto sekcję `Artifacts`. Widoczne były pliki automatycznie zapisane przez MLflow, między innymi `MLmodel`, `conda.yaml`, `python_env.yaml`, `requirements.txt` oraz plik modelu `model.skops`.

Plik `MLmodel` opisuje zapisany model i sposób jego uruchomienia, natomiast pliki środowiskowe, takie jak `conda.yaml`, `python_env.yaml` i `requirements.txt`, zawierają informacje o zależnościach potrzebnych do odtworzenia środowiska. Dzięki temu MLflow pozwala nie tylko zapisać sam model, ale także przechować informacje potrzebne do jego późniejszego użycia.

Dodatkowo uruchomiono bardziej zaawansowaną konfigurację MLflow z obsługą rejestru modeli. Model został zarejestrowany w sekcji `Registered models` pod nazwą `BreastCancer_LogisticRegression`. W interfejsie MLflow widoczna była wersja `v4`, co oznacza, że kolejne uruchomienia eksperymentu tworzyły następne wersje tego samego modelu.

W praktyce każda konfiguracja hiperparametru `C` tworzyła osobny run, a więc osobną wersję modelu zapisaną w MLflow. Dzięki temu można porównywać wyniki różnych eksperymentów, wrócić do wcześniejszego modelu oraz wczytać konkretną wersję po identyfikatorze runu albo przez rejestr modeli.

Zastosowane podejście pokazuje, że MLflow może służyć nie tylko do logowania metryk i parametrów, ale także do kontrolowania kolejnych wersji modeli oraz przechowywania informacji potrzebnych do ich odtworzenia.

## Zadanie 5. Wykorzystanie modelu zarejestrowanego w MLflow

W ramach zadania utworzono osobny skrypt `predict.py`, którego celem było wczytanie wcześniej zapisanego modelu z MLflow. Do załadowania modelu wykorzystano unikatowy `Run ID` jednego z wcześniejszych runów oraz ścieżkę w formacie `runs:/<RUN_ID>/model`.

Model został poprawnie załadowany z MLflow, co potwierdził komunikat wyświetlony w terminalu. Następnie wykorzystano przykładową próbkę ze zbioru Breast Cancer Wisconsin, aby sprawdzić działanie modelu na nowych danych.

Dla wybranej próbki prawdziwa klasa wynosiła `0`, czyli `malignant`. Model również przewidział klasę `0`, czyli `malignant`, co potwierdza poprawne działanie załadowanego modelu.

Dodatkowo wyświetlono prawdopodobieństwa klas za pomocą metody `predict_proba()`. Model przypisał prawdopodobieństwo `1.0000` dla klasy `0 (malignant)` oraz `0.0000` dla klasy `1 (benign)`. Oznacza to, że model był pewny swojej predykcji i działał zgodnie z oczekiwaniami.
