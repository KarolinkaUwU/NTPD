## Zadanie 1. Przygotowanie środowiska i danych

W ramach zadania przygotowano środowisko wirtualne `.venv` w projekcie PyCharm oraz zainstalowano wymagane biblioteki: `numpy`, `pandas`, `scikit-learn`, `tensorflow` i `joblib`.

Do laboratorium wybrano wbudowany zbiór danych Iris z biblioteki `scikit-learn`. Zbiór zawiera 150 próbek opisujących kwiaty irysa na podstawie 4 cech: długości i szerokości działki kielicha oraz długości i szerokości płatka. Dane należą do trzech klas: `setosa`, `versicolor` i `virginica`.

Po załadowaniu danych wykonano krótką analizę w konsoli. Dane przekonwertowano do obiektu `DataFrame`, wyświetlono pierwsze 5 wierszy, rozmiar danych, typy kolumn oraz liczność klas. Zbiór jest zbalansowany, ponieważ każda klasa zawiera po 50 przykładów.

## Wariant A: scikit-learn

## Zadanie 2. Stworzenie prostego modelu ML

W wariancie A wykorzystano bibliotekę `scikit-learn` oraz model `LogisticRegression`. Dane Iris zostały podzielone na zbiór treningowy i testowy w proporcji 80% / 20% za pomocą funkcji `train_test_split`. Zbiór treningowy zawierał 120 próbek, a testowy 30 próbek.

Następnie utworzono model `LogisticRegression(max_iter=1000)` i wytrenowano go metodą `fit()`. Po treningu wykonano predykcję na zbiorze testowym oraz obliczono podstawowe metryki klasyfikacji: `accuracy`, `precision`, `recall` i `F1-score`.

Model osiągnął bardzo dobre wyniki: `accuracy = 0.9667`, `precision = 0.9697`, `recall = 0.9667` oraz `F1-score = 0.9666`. Macierz pomyłek pokazała tylko jedną błędną klasyfikację.

## Zadanie 3. Zapisanie i ładowanie modelu — Wariant A

Wytrenowany model `LogisticRegression` zapisano do pliku `model_A_v1.joblib` w folderze `models` za pomocą biblioteki `joblib`.

Następnie utworzono osobny skrypt `load_model_A.py`, który wczytuje zapisany model i wykonuje predykcję dla przykładowego rekordu `[[5.1, 3.5, 1.4, 0.2]]`. Model przewidział klasę `0`, czyli `setosa`, co potwierdza, że zapis i odczyt modelu działają poprawnie.

## Wariant B: TensorFlow / Keras

## Zadanie 2. Stworzenie prostego modelu ML

W wariancie B wykorzystano bibliotekę `TensorFlow/Keras`. Dane, tak jak w wariancie A, zostały podzielone na zbiór treningowy i testowy. Przed treningiem wykonano standaryzację cech za pomocą `StandardScaler`, ponieważ sieci neuronowe lepiej uczą się na danych o podobnej skali.

Utworzono prosty model typu `Sequential` z warstwami `Dense`. Sieć składała się z dwóch warstw ukrytych: `Dense(32, activation="relu")` oraz `Dense(16, activation="relu")`, a także warstwy wyjściowej `Dense(3, activation="softmax")`, odpowiadającej trzem klasom zbioru Iris.

Proces uczenia skonfigurowano za pomocą `model.compile()`, ustawiając optymalizator `adam`, funkcję straty `sparse_categorical_crossentropy` oraz metrykę `accuracy`.

Po treningu model oceniono na zbiorze testowym. Uzyskano `Test loss = 0.1356` oraz `Test accuracy = 0.9667`. Dodatkowo model poprawnie przewidział klasę `setosa` dla przykładowego rekordu.

## Zadanie 3. Zapisanie i ładowanie modelu — Wariant B

Model sieci neuronowej zapisano do pliku `model_B_v1.keras` w folderze `models`. Dodatkowo zapisano obiekt `StandardScaler` jako `scaler_B_v1.joblib`, ponieważ nowe dane muszą być skalowane w taki sam sposób jak dane treningowe.

W osobnym skrypcie `load_model_B.py` wczytano model oraz scaler, a następnie wykonano predykcję dla przykładowego rekordu `[[5.1, 3.5, 1.4, 0.2]]`. Model przewidział klasę `0`, czyli `setosa`, co potwierdza poprawne zapisanie i załadowanie modelu oraz scalera.

## Zadanie 4. Wersjonowanie modelu w praktyce

Zapisane modele oraz pliki kodu zostały dodane do repozytorium Git. Do commita dodano pliki `mainA.py`, `mainB.py`, `load_model_A.py`, `load_model_B.py` oraz pliki z folderu `models`.

Dla wariantu A zapisano model jako `model_A_v1.joblib`, a dla wariantu B jako `model_B_v1.keras` oraz `scaler_B_v1.joblib`. Nazwy plików zawierają numer wersji `v1`, co ułatwia śledzenie kolejnych wersji modeli.

Po dodaniu plików wykonano commit `Add Lab01 ML models version 1`, a następnie utworzono tag `lab01-v1.0`. Tag oznacza pierwszą wersję modeli wykonanych w ramach laboratorium i pozwala wrócić do konkretnego stanu projektu.

Przyjęto prostą politykę wersjonowania: kolejne wersje, np. `v2`, powinny być tworzone po istotnych zmianach, takich jak zmiana hiperparametrów, algorytmu, jakości modelu albo danych treningowych.

W projekcie zastosowano również plik `.gitignore`, aby nie dodawać do repozytorium środowiska `.venv`, plików tymczasowych i katalogów `__pycache__`. W przypadku dużych modeli można byłoby użyć Git LFS, ale w tym laboratorium modele są małe i mogły zostać zapisane bezpośrednio w repozytorium.

## Zadanie 5. Różnice między środowiskiem deweloperskim a produkcyjnym

Środowisko deweloperskie służy do tworzenia i testowania modelu, najczęściej lokalnie, np. w PyCharmie. Model można uruchamiać ręcznie, sprawdzać różne algorytmy i analizować wyniki na zbiorze testowym.

Środowisko produkcyjne wymaga większej stabilności i automatyzacji. Model powinien działać przewidywalnie, obsługiwać nowe dane, być monitorowany oraz możliwy do odtworzenia w konkretnej wersji.

Główne różnice dotyczą zarządzania zależnościami, monitorowania jakości modelu, retrainingu i wdrażania. W produkcji należy dokładnie określać wersje bibliotek, np. w `requirements.txt`, monitorować metryki modelu oraz reagować, gdy jakość predykcji spada. W takim przypadku przygotowuje się nową wersję modelu, np. `model_A_v2.joblib`.

Ważne jest także wersjonowanie modeli i automatyzacja wdrożeń. Dzięki nazwom plików z numerami wersji oraz tagom Git można łatwo wrócić do wcześniejszej wersji. W większych projektach proces wdrażania można zautomatyzować za pomocą CI/CD.

Podsumowując, środowisko deweloperskie skupia się na eksperymentowaniu i tworzeniu modelu, natomiast produkcyjne na stabilnym, kontrolowanym i powtarzalnym działaniu modelu.