## Zadanie 1. Przygotowanie środowiska i podstawowe wczytanie pliku Parquet

W ramach zadania przygotowano środowisko do pracy z Apache Spark oraz Spark SQL. Do utworzenia sesji Spark wykorzystano klasę `SparkSession`. Aplikacji nadano nazwę `SparkSQL_Parquet`, a sesję uruchomiono lokalnie w trybie `local[*]`, co oznacza wykorzystanie lokalnych zasobów komputera.

Poprawność konfiguracji środowiska sprawdzono przez uruchomienie skryptu `main.py`. Program wyświetlił nazwę aplikacji, wersję Apache Spark, tryb pracy oraz ścieżkę do interpretera Python używanego przez środowisko `.venv`. Wynik potwierdził, że Apache Spark jest poprawnie zainstalowany i skonfigurowany.

Następnie przygotowano przykładowy plik Parquet z danymi sprzedażowymi. Dane zawierały informacje o transakcjach, takie jak identyfikator transakcji, data, miasto, kategoria produktu, liczba sztuk, cena jednostkowa oraz całkowita wartość transakcji. Plik został zapisany w folderze `data` pod nazwą `sales_data.parquet`.

W kolejnym kroku utworzono osobny skrypt `zad1_read_parquet.py`, którego zadaniem było wczytanie pliku Parquet do obiektu DataFrame w PySpark. Do odczytu danych użyto metody `spark.read.parquet()`, wskazując ścieżkę `data/sales_data.parquet`.

Po wczytaniu danych wyświetlono kilka pierwszych wierszy DataFrame za pomocą metody `show()`. Wynik pokazał poprawnie odczytane rekordy sprzedażowe zawierające między innymi kolumny `transaction_id`, `date`, `city`, `product_category`, `quantity`, `unit_price` oraz `total_amount`.

Na końcu sprawdzono strukturę danych za pomocą metody `printSchema()`. Schemat pokazał nazwy kolumn oraz typy danych rozpoznane przez Spark, między innymi typy `long` oraz `string`. Dzięki temu potwierdzono, że plik Parquet został poprawnie wczytany i może być dalej wykorzystywany w zapytaniach Spark SQL.

## Zadanie 2. Ładowanie danych CSV i rejestracja jako widok tabelaryczny

W ramach zadania przygotowano plik CSV z danymi sprzedażowymi i zapisano go w folderze `data` pod nazwą `retail_sales_dataset.csv`. Zbiór danych zawiera informacje o transakcjach, takie jak identyfikator transakcji, data, identyfikator klienta, płeć, wiek, kategoria produktu, liczba sztuk, cena jednostkowa oraz całkowita wartość transakcji.

Następnie dane zostały wczytane do obiektu DataFrame w PySpark. Do odczytu wykorzystano metodę `spark.read.csv()`, ustawiając parametry `header=True` oraz `inferSchema=True`. Dzięki temu pierwszy wiersz pliku został potraktowany jako nagłówek, a Spark automatycznie rozpoznał typy danych w kolumnach.

Po wczytaniu danych wyświetlono podstawowe informacje o zbiorze, w tym ścieżkę pliku, liczbę wierszy oraz listę kolumn. Następnie pokazano podgląd danych za pomocą metody `show()` oraz sprawdzono ich strukturę przy użyciu `printSchema()`. Pozwoliło to potwierdzić, że dane zostały poprawnie załadowane i mają oczekiwaną strukturę.

W kolejnym kroku zarejestrowano wczytany DataFrame jako widok tymczasowy o nazwie `retail_sales` z użyciem metody `createOrReplaceTempView()`. Dzięki temu możliwe było wykonywanie zapytań SQL bezpośrednio na danych zapisanych w DataFrame.

Na końcu wykonano proste zapytanie SQL:

```sql
SELECT * FROM retail_sales LIMIT 10
```

## Zadanie 3. Spark SQL – tworzenie zapytań

W ramach zadania wykonano bardziej rozbudowane zapytania SQL na danych przetwarzanych w Apache Spark. Do analizy wykorzystano główny zbiór danych sprzedażowych `retail_sales_dataset.csv`, zawierający informacje o transakcjach, klientach, kategoriach produktów, liczbie sztuk, cenie jednostkowej oraz całkowitej wartości sprzedaży.

Dane sprzedażowe zostały wczytane do obiektu DataFrame, a następnie zarejestrowane jako widok tymczasowy `retail_sales`. Dodatkowo przygotowano drugi zestaw danych `product_categories.csv`, zawierający informacje opisowe o kategoriach produktów. W pliku tym każdej kategorii przypisano dział oraz poziom marży. Drugi DataFrame został zarejestrowany jako widok tymczasowy `product_categories`.

Po zarejestrowaniu widoków wykonano zapytanie agregujące dla całego zbioru danych. Obliczono liczbę transakcji, całkowitą wartość sprzedaży, średnią wartość transakcji oraz łączną liczbę sprzedanych sztuk. Wyniki pokazały, że zbiór zawiera `1000` transakcji, całkowita wartość sprzedaży wynosi `456000`, średnia wartość transakcji wynosi `456.0`, a liczba sprzedanych sztuk to `2514`.

Następnie wykonano grupowanie według kategorii produktu. Dla kategorii `Electronics`, `Clothing` oraz `Beauty` obliczono liczbę transakcji, sumę sprzedanych sztuk, całkowitą sprzedaż oraz średnią wartość transakcji. Najwyższą całkowitą sprzedaż uzyskała kategoria `Electronics`, dla której suma sprzedaży wyniosła `156905`. Kategoria `Clothing` osiągnęła wynik `155580`, a `Beauty` `143515`.

W kolejnym kroku wykonano grupowanie po dwóch kolumnach: kategorii produktu oraz płci klienta. Pozwoliło to porównać sprzedaż w poszczególnych kategoriach z podziałem na klientów oznaczonych jako `Female` i `Male`. Wyniki pokazały różnice w liczbie transakcji oraz wartości sprzedaży między grupami.

Następnie zastosowano warunkowe filtrowanie danych. Wykonano zapytanie wybierające transakcje, których całkowita wartość była większa niż `1000`. Wynik został posortowany malejąco według wartości transakcji, dzięki czemu na początku widoczne były największe sprzedaże. W pokazanych wynikach najwyższe transakcje miały wartość `2000`.

Na końcu wykonano `JOIN` dwóch widoków: `retail_sales` oraz `product_categories`. Połączenie wykonano na podstawie kategorii produktu. Dzięki temu dane sprzedażowe zostały uzupełnione o dodatkowe informacje opisowe, takie jak dział oraz poziom marży. Wynik połączonego zapytania zawierał podsumowanie sprzedaży według kategorii, działu i poziomu marży.

Wynik zapytania z użyciem `JOIN` został zapisany do pliku `output/spark_sql_join_summary.csv`. Plik ten zawiera końcowe podsumowanie sprzedaży według kategorii produktów wraz z dodatkowymi informacjami z drugiego zestawu danych.
