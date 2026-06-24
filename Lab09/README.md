## Zadanie 1. Uruchomienie lokalnej instancji Apache Spark

W ramach zadania przygotowano lokalne środowisko do pracy z Apache Spark oraz PySpark. W projekcie wykorzystano środowisko wirtualne `.venv`, w którym zainstalowano pakiet `pyspark`. Dzięki temu możliwe było uruchamianie skryptów PySpark bezpośrednio z poziomu Pythona.

Do sprawdzenia konfiguracji utworzono plik `main.py`. W pliku tym utworzono lokalną sesję Spark za pomocą `SparkSession`. Sesja została uruchomiona w trybie `local[*]`, co oznacza, że Spark działa lokalnie i może wykorzystywać dostępne rdzenie procesora komputera.

W trakcie uruchamiania skryptu wyświetlono wersję Apache Spark, tryb pracy oraz ścieżkę do interpretera Python używanego przez projekt. Dodatkowo utworzono prosty testowy DataFrame zawierający dwie kolumny: `id` oraz `name`. Poprawne wyświetlenie tabeli potwierdziło, że lokalna sesja Spark działa prawidłowo.

Podczas konfiguracji ustawiono również zmienne środowiskowe `PYSPARK_PYTHON` oraz `PYSPARK_DRIVER_PYTHON`, aby driver i worker PySpark korzystały z tego samego interpretera Python ze środowiska `.venv`. Było to potrzebne, ponieważ wcześniejsze uruchomienie wskazało na różnicę wersji Pythona pomiędzy driverem i workerem. Po ustawieniu tych zmiennych skrypt wykonał się poprawnie.

Następnie sprawdzono działanie PySpark shell z poziomu terminala. Uruchomiono polecenie `pyspark`, które otworzyło interaktywną konsolę PySpark. W konsoli wykonano polecenie `spark.version`, które zwróciło wersję `4.1.2`. Potwierdziło to, że PySpark shell działa poprawnie.

W kolejnym kroku sprawdzono działanie Spark shell. Uruchomiono polecenie `spark-shell`, które otworzyło interaktywną konsolę Apache Spark działającą w języku Scala. W konsoli również wykonano polecenie `spark.version`. Wynik `4.1.2` potwierdził poprawne działanie Spark shell.

Na końcu sprawdzono instalację pakietu `pyspark` w środowisku Python za pomocą polecenia `pip show pyspark`. Polecenie wyświetliło informacje o pakiecie, w tym nazwę, wersję oraz lokalizację instalacji w folderze `.venv`. Zainstalowana wersja pakietu to `4.1.2`.

Podczas uruchamiania Sparka pojawiło się ostrzeżenie dotyczące braku `winutils.exe` oraz nieustawionej zmiennej `HADOOP_HOME`. Ostrzeżenie to nie zablokowało działania programu, ponieważ Spark uruchomił się poprawnie lokalnie, a testowy DataFrame został wyświetlony.

Zadanie potwierdza, że środowisko Apache Spark i PySpark zostało poprawnie przygotowane do dalszej pracy z DataFrame oraz RDD.

## Zadanie 2. Podstawowe operacje na DataFrame w PySpark

W ramach zadania wykonano podstawowe operacje na danych sprzedażowych z wykorzystaniem DataFrame w PySpark. Do projektu wykorzystano plik `retail_sales_dataset.csv`, który został zapisany w folderze `data`. Zbiór danych zawiera informacje o transakcjach sprzedażowych, między innymi identyfikator transakcji, datę, identyfikator klienta, płeć, wiek, kategorię produktu, liczbę sztuk, cenę jednostkową oraz całkowitą wartość transakcji.

Dane zostały wczytane do obiektu DataFrame przy użyciu `SparkSession`. Aplikacji nadano nazwę `DataFrameExample`, a sesję uruchomiono lokalnie. Podczas wczytywania pliku CSV zastosowano opcję `header=True`, dzięki czemu pierwszy wiersz pliku został potraktowany jako nazwy kolumn. Dodatkowo użyto `inferSchema=True`, aby Spark automatycznie rozpoznał typy danych w poszczególnych kolumnach.

Po wczytaniu danych wyświetlono pierwsze rekordy zbioru za pomocą metody `show()`. Pozwoliło to sprawdzić, czy plik CSV został poprawnie załadowany oraz czy dane mają oczekiwaną strukturę. Następnie użyto metody `printSchema()`, aby sprawdzić schemat DataFrame. W wyniku widoczne były nazwy kolumn oraz typy danych, takie jak `integer`, `string` oraz `date`.

W kolejnym kroku wykonano selekcję wybranych kolumn. Z pełnego zbioru danych wybrano kolumny `Transaction ID`, `Date`, `Product Category`, `Quantity`, `Price per Unit` oraz `Total Amount`. Dzięki temu ograniczono DataFrame do informacji najważniejszych z punktu widzenia analizy sprzedaży.

Następnie wykonano filtrowanie wierszy. Wybrano transakcje należące do kategorii `Electronics`, których całkowita wartość sprzedaży była większa niż 100. Operacja ta pokazała, w jaki sposób w PySpark można ograniczać dane do rekordów spełniających określone warunki logiczne.

Na końcu wykonano grupowanie i agregacje. Dane pogrupowano według kolumny `Product Category`, a następnie obliczono liczbę transakcji, sumę sprzedanych sztuk, całkowitą wartość sprzedaży oraz średnią cenę jednostkową dla każdej kategorii. Wynik pozwolił porównać sprzedaż dla kategorii `Electronics`, `Clothing` oraz `Beauty`.

Przetworzony DataFrame został zapisany do pliku `output/sales_summary.csv`. Do zapisu wykorzystano wynik agregacji, czyli DataFrame `grouped_df`. Ze względu na problem środowiska Windows związany z brakiem `HADOOP_HOME` oraz `winutils.exe`, wynik zapisano do pojedynczego pliku CSV za pomocą standardowego modułu `csv` w Pythonie. Operacje przetwarzania, filtrowania, grupowania i agregacji zostały jednak wykonane w PySpark.

## Zadanie 3. Praca z RDD w PySpark

W ramach zadania wykorzystano RDD, czyli niższy poziom abstrakcji dostępny w Apache Spark. Do pracy użyto tego samego pliku CSV z danymi sprzedażowymi, który wcześniej został wykorzystany w zadaniu z DataFrame.

Plik CSV został wczytany jako RDD za pomocą metody `textFile()`. Na początku odczytano nagłówek pliku, a następnie usunięto go ze zbioru danych, aby dalsze operacje były wykonywane tylko na rekordach sprzedażowych. Po usunięciu nagłówka zliczono liczbę wierszy danych. Wynik wyniósł `1000`, co potwierdziło poprawne wczytanie zbioru.

Następnie wykonano transformację `map`, której celem było ręczne sparsowanie kolejnych wierszy pliku CSV. Każdy wiersz został zamieniony na strukturę słownikową zawierającą takie pola jak `Transaction ID`, `Date`, `Customer ID`, `Gender`, `Age`, `Product Category`, `Quantity`, `Price per Unit` oraz `Total Amount`. Dzięki temu dane mogły być dalej przetwarzane w bardziej czytelnej formie.

W kolejnym kroku zastosowano transformację `filter`. Wybrano transakcje z kategorii `Electronics`, których całkowita wartość sprzedaży była większa niż 100. Operacja ta pokazała, że RDD pozwala filtrować dane na podstawie samodzielnie zdefiniowanych warunków logicznych.

Następnie wykorzystano akcję `reduce` do obliczenia sumy wybranych kolumn. Obliczono całkowitą wartość sprzedaży, która wyniosła `456000`, oraz łączną liczbę sprzedanych sztuk, która wyniosła `2514`. W tym celu najpierw za pomocą `map` wybrano odpowiednie wartości liczbowe, a następnie połączono je przy użyciu `reduce`.

Dodatkowo wykonano agregację według kategorii produktu z użyciem `reduceByKey`. Dane zostały przekształcone do postaci par klucz-wartość, gdzie kluczem była kategoria produktu, a wartością suma sprzedaży lub liczba sprzedanych sztuk. Wyniki pokazały, że sprzedaż według kategorii wyniosła: `Beauty` – `143515`, `Electronics` – `156905`, `Clothing` – `155580`. Liczba sprzedanych sztuk wyniosła odpowiednio: `Beauty` – `771`, `Electronics` – `849`, `Clothing` – `894`.

Na końcu użyto akcji `collect`, aby zebrać wynik agregacji z RDD i wyświetlić go w terminalu. Zadanie pokazało różnicę między pracą na DataFrame a RDD. W przypadku RDD więcej operacji, takich jak parsowanie wierszy i wybór wartości, trzeba wykonać ręcznie, ale jednocześnie daje to większą kontrolę nad sposobem przetwarzania danych.
