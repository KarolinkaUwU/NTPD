## Zadanie 1. Przygotowanie środowiska

W ramach zadania przygotowano środowisko do pracy z Apache Spark Structured Streaming. Wykorzystano środowisko skonfigurowane podczas wcześniejszych laboratoriów, w którym zainstalowany był pakiet `pyspark`.

Utworzono aplikację PySpark w pliku `main.py`. Aplikacja uruchamia lokalną sesję Spark za pomocą klasy `SparkSession`. Sesji nadano nazwę `LAB11_StructuredStreaming`, co pozwala jednoznacznie rozpoznać aplikację podczas działania Sparka.

Aplikacja została uruchomiona lokalnie w trybie `local[*]`, co oznacza wykorzystanie lokalnych zasobów komputera. W kodzie ustawiono również zmienne środowiskowe `PYSPARK_PYTHON` oraz `PYSPARK_DRIVER_PYTHON`, aby driver i workery PySpark korzystały z tego samego interpretera Python ze środowiska `.venv`.

Poprawność działania środowiska sprawdzono przez uruchomienie skryptu poleceniem:

```powershell
python main.py
```

Program wyświetlił informacje o konfiguracji środowiska. Wersja Apache Spark wyniosła `4.1.2`, a wersja PySpark również `4.1.2`. Wyświetlono także nazwę aplikacji, tryb pracy oraz ścieżkę do interpretera Python.

Wynik potwierdził, że Apache Spark i PySpark działają poprawnie, a środowisko jest gotowe do dalszej pracy ze Structured Streaming.

## Zadanie 2. Strumieniowe wczytywanie danych

W ramach zadania przygotowano źródło danych strumieniowych oparte na plikach CSV dodawanych do folderu wejściowego. W projekcie utworzono folder `data/input_stream`, do którego dodano przykładowy plik `events_001.csv`.

Plik wejściowy zawierał dane zgodne z wymaganym formatem. Każdy rekord składał się z czasu zdarzenia, identyfikatora użytkownika, kategorii, wartości liczbowej oraz statusu zdarzenia. Wykorzystane kolumny to `event_time`, `user_id`, `category`, `amount` oraz `status`.

Dane zostały wczytane za pomocą mechanizmu `readStream`, czyli strumieniowego odczytu danych w Apache Spark Structured Streaming. Dla danych zdefiniowano jawny schemat przy użyciu `StructType`, dzięki czemu Spark wiedział, jakie kolumny i typy danych powinny występować w plikach CSV.

Po utworzeniu strumieniowego DataFrame sprawdzono właściwość `isStreaming`. Wynik `True` potwierdził, że DataFrame został utworzony jako obiekt strumieniowy, a nie jako zwykły DataFrame typu batch.

Następnie wyświetlono schemat początkowy danych. W schemacie kolumna `event_time` miała typ `string`, kolumna `amount` typ `double`, a pozostałe kolumny typ `string`. Był to schemat bezpośrednio wynikający z definicji danych wejściowych.

W kolejnym kroku wykonano podstawowe czyszczenie danych. Kolumna `event_time` została przekonwertowana z typu tekstowego na typ `timestamp`. Dodatkowo wartości w kolumnach `category` oraz `status` zostały oczyszczone ze spacji i zamienione na małe litery. Odfiltrowano również rekordy bez wartości w kolumnach `event_time`, `user_id` lub `amount`, a także rekordy z ujemną wartością `amount`.

Po czyszczeniu ponownie wyświetlono schemat DataFrame. Wynik pokazał, że kolumna `event_time` ma już typ `timestamp`, co oznacza, że dane są przygotowane do dalszego przetwarzania strumieniowego, w tym do agregacji oraz użycia okien czasowych w kolejnych zadaniach.

## Zadanie 3. Transformacje i agregacje strumieniowe

W ramach zadania wykonano transformacje oraz agregacje na danych strumieniowych w Apache Spark Structured Streaming. Dane wejściowe były odczytywane z folderu `data/input_stream_task3`, do którego podczas działania aplikacji dodawane były kolejne pliki CSV.

W aplikacji wykorzystano strumieniowy DataFrame utworzony za pomocą `readStream`. Następnie wykonano kilka transformacji danych. Kolumna `event_time` została przekonwertowana do typu `timestamp`, a kolumny `category` oraz `status` zostały oczyszczone i zamienione na małe litery. Dodatkowo zastosowano filtrowanie, aby w dalszym przetwarzaniu uwzględniać tylko rekordy ze statusem `paid`.

W kolejnym kroku wybrano najważniejsze kolumny: `event_time`, `user_id`, `category`, `amount` oraz `status`. Następnie obliczono dodatkową kolumnę `amount_with_tax`, która reprezentowała wartość zdarzenia powiększoną o podatek. Dzięki temu w zadaniu wykonano więcej niż dwie transformacje wymagane w poleceniu.

Na podstawie przetworzonych danych przygotowano agregację według kategorii. Dla każdej kategorii obliczono liczbę zdarzeń, sumę wartości `amount` oraz sumę wartości `amount_with_tax`. Wynik agregacji był zapisywany do konsoli z użyciem trybu `complete`, który pokazuje pełny aktualny wynik agregacji po każdym mikro-batchu.

Do zadania przygotowano prosty generator danych. Generator automatycznie dodawał kolejne pliki CSV do folderu wejściowego podczas działania aplikacji. Dzięki temu można było pokazać, że Spark Structured Streaming przetwarza nowe dane bez restartowania programu.

Wyniki w konsoli pokazały kolejne mikro-batche. W `Batch: 0` Spark przetworzył pierwszy plik wejściowy i wyświetlił agregację dla kategorii `books` oraz `electronics`. W `Batch: 1` po dodaniu kolejnego pliku wynik został zaktualizowany i pojawiła się również kategoria `clothes`. W `Batch: 2` po dodaniu trzeciego pliku Spark ponownie zaktualizował wynik agregacji, pokazując końcowe wartości dla kategorii `books`, `electronics` oraz `clothes`.

Zadanie potwierdziło, że aplikacja Structured Streaming poprawnie reaguje na pojawianie się nowych plików w folderze wejściowym i przetwarza je w kolejnych mikro-batchach bez konieczności restartu.

## Zadanie 4. Okna czasowe i watermarking

W ramach zadania rozbudowano aplikację strumieniową o agregacje wykonywane w oknach czasowych oraz zastosowano watermarking dla kolumny `event_time`. Dane były odczytywane strumieniowo z folderu `data/input_stream_task4`, do którego generator dodawał kolejne pliki CSV podczas działania aplikacji.

Na początku zdefiniowano strumieniowy DataFrame z jawnie określonym schematem danych. Następnie wykonano podstawowe czyszczenie danych: kolumna `event_time` została przekonwertowana na typ `timestamp`, kolumny `category` oraz `status` zostały oczyszczone i zamienione na małe litery, a do dalszego przetwarzania wybrano tylko rekordy ze statusem `paid`.

W aplikacji zastosowano watermarking dla kolumny `event_time` z opóźnieniem ustawionym na `10 minutes`. Watermarking pozwala Sparkowi kontrolować, jak długo powinien przechowywać stan dla danych opartych na czasie zdarzenia. Mechanizm ten jest szczególnie ważny przy danych opóźnionych, ponieważ zdarzenia nie zawsze trafiają do systemu dokładnie w takiej kolejności, w jakiej faktycznie wystąpiły.

W pierwszej części wykonano agregację w oknach stałych, czyli tumbling windows. Zastosowano okna 10-minutowe, w których każde zdarzenie może należeć tylko do jednego przedziału czasowego. Dla każdej kategorii obliczono liczbę zdarzeń oraz sumę wartości `amount`.

W drugiej części wykonano agregację w oknach przesuwających, czyli sliding windows. Okno miało długość 10 minut, ale przesuwało się co 5 minut. Oznacza to, że jedno zdarzenie mogło zostać przypisane do więcej niż jednego okna czasowego. Dzięki temu wyniki dla okien przesuwających zawierały więcej przedziałów niż wyniki dla okien stałych.

W trakcie działania aplikacji generator dodawał kolejne pliki CSV. Pierwsze pliki zawierały dane przychodzące w poprawnej kolejności czasowej. Następnie dodano dane z późniejszym czasem zdarzenia, aby przesunąć zakres przetwarzanych okien. Kolejny plik zawierał dane opóźnione, czyli zdarzenia z wcześniejszym `event_time`, które pojawiły się dopiero po danych nowszych.

Wyniki w konsoli pokazały kolejne mikro-batche. Dla okien stałych zdarzenia były grupowane w pojedynczych 10-minutowych przedziałach, na przykład od `10:00:00` do `10:10:00`. Dla okien przesuwających widoczne były dodatkowe zakresy, na przykład od `09:55:00` do `10:05:00` oraz od `10:00:00` do `10:10:00`, ponieważ to samo zdarzenie mogło pasować do kilku nakładających się okien.

Dane opóźnione zostały dodane w pliku `events_004_late.csv`. Po ich przetworzeniu wyniki dla wcześniejszych okien zostały zaktualizowane. Pokazuje to, że Spark Structured Streaming potrafi obsługiwać dane, które pojawiają się później niż wynikałoby to z czasu zdarzenia.

Czas zdarzenia oznacza moment, w którym dane zdarzenie faktycznie wystąpiło, czyli wartość zapisaną w kolumnie `event_time`. Czas przetwarzania oznacza moment, w którym Spark fizycznie odczytuje i przetwarza dane. Te dwa czasy mogą się różnić, ponieważ plik z danymi może zostać dodany do folderu wejściowego później niż wskazuje czas zdarzenia.

Watermarking wpływa na obsługę danych opóźnionych. Pozwala określić, jak długo Spark ma akceptować i uwzględniać spóźnione rekordy w agregacjach czasowych. Dane, które mieszczą się w dopuszczalnym opóźnieniu, mogą jeszcze zaktualizować wcześniejsze okna. Dane zbyt stare względem watermarka mogą zostać pominięte, ponieważ Spark uznaje, że dane okno czasowe zostało już zamknięte.

Zadanie pokazało różnicę między oknami stałymi i przesuwającymi. Okna stałe dzielą oś czasu na osobne, nienakładające się przedziały, dlatego każde zdarzenie trafia tylko do jednego okna. Okna przesuwające nakładają się na siebie, dlatego jedno zdarzenie może zostać uwzględnione w kilku agregacjach. W wynikach było to widoczne przez większą liczbę przedziałów czasowych w przypadku okien przesuwających.

## Zadanie 5. Zapis wyników i checkpointing

W ramach zadania rozbudowano aplikację strumieniową o zapis wyników do plików oraz mechanizm checkpointingu. Dane wejściowe były odczytywane jako strumień z folderu `data/input_stream_task5`, a wyniki zapisywano do folderu `data/output_stream_task5`.

Aplikacja została przygotowana w taki sposób, aby mogła zostać uruchomiona w dwóch trybach: `first` oraz `second`. W pierwszym trybie czyszczone były foldery wejściowe, wynikowe oraz foldery checkpointów. W drugim trybie checkpointy pozostawały zachowane, co pozwoliło sprawdzić, czy Spark pamięta wcześniej przetworzone pliki.

W aplikacji wykorzystano strumieniowy DataFrame tworzony za pomocą `readStream`. Dane wejściowe były plikami CSV zawierającymi kolumny `event_time`, `user_id`, `category`, `amount` oraz `status`. Następnie wykonano podstawowe przetwarzanie danych: konwersję kolumny `event_time` do typu `timestamp`, oczyszczenie kolumn `category` i `status`, filtrowanie tylko rekordów ze statusem `paid` oraz obliczenie dodatkowej kolumny `amount_with_tax`.

Wynik przetwarzania strumieniowego został zapisany do plików CSV za pomocą `writeStream` w trybie `append`. Dla zapisu do plików skonfigurowano osobny checkpoint w folderze `checkpoints/task5_file_sink`. Dodatkowo wynik był równolegle wyświetlany w konsoli, również z osobnym checkpointem zapisanym w folderze `checkpoints/task5_console_sink`.

Podczas pierwszego uruchomienia aplikacji dodano dwa pliki wejściowe: `events_001.csv` oraz `events_002.csv`. Spark przetworzył tylko rekordy ze statusem `paid`, dlatego w wynikach zapisano 4 rekordy. Następnie zapisane dane zostały wczytane jako zwykły DataFrame batch i wyświetlone w konsoli. Wynik batch był zgodny z danymi widocznymi wcześniej w konsoli podczas działania strumienia.

Następnie aplikację uruchomiono ponownie w trybie `second`. W tym trybie nie usunięto folderów checkpointów. Generator dodał nowy plik wejściowy `events_003_new_...csv`. Spark przetworzył tylko nowe dane, ponieważ wcześniejsze pliki były już zapisane w stanie checkpointingu. Po drugim uruchomieniu liczba rekordów w zapisanych wynikach wzrosła z 4 do 6, co potwierdziło, że stare pliki nie zostały przetworzone ponownie.

Checkpointing różni się od zwykłego zapisu plików wynikowych tym, że przechowuje stan działania zapytania strumieniowego. Dzięki checkpointom Spark wie, które pliki wejściowe zostały już przetworzone, jakie było ostatnie wykonane przetwarzanie oraz jak wznowić działanie po restarcie aplikacji. Zwykły zapis plików przechowuje jedynie wynik, ale nie zapisuje stanu przetwarzania.

Przetwarzanie batch polega na jednorazowym przetworzeniu istniejącego zbioru danych. Program odczytuje dane, wykonuje operacje i kończy działanie. Przetwarzanie streaming działa inaczej: aplikacja pozostaje uruchomiona i reaguje na nowe dane pojawiające się w źródle, na przykład na nowe pliki CSV dodawane do folderu wejściowego.

W Structured Streaming dostępne są różne tryby zapisu wyników. Tryb `append` dopisuje tylko nowe rekordy wynikowe. Tryb `update` aktualizuje tylko te wyniki, które zmieniły się od poprzedniego mikro-batcha. Tryb `complete` wypisuje cały aktualny wynik po każdym mikro-batchu i jest często używany przy agregacjach. W tym zadaniu zastosowano tryb `append`, ponieważ zapisywane były przetworzone rekordy, a nie pełna tabela agregacji.

Zadanie potwierdziło, że Spark Structured Streaming potrafi zapisywać wyniki przetwarzania do plików, korzystać z checkpointingu oraz poprawnie kontynuować pracę po ponownym uruchomieniu aplikacji bez ponownego przetwarzania tych samych danych wejściowych.
