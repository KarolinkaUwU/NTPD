## Zadanie 1. Przygotowanie środowiska

W ramach zadania przygotowano środowisko do pracy z narzędziem Business Intelligence Metabase oraz bazą danych PostgreSQL. Środowisko zostało uruchomione lokalnie z wykorzystaniem Dockera oraz Docker Compose.

Na początku sprawdzono dostępność Dockera i Docker Compose w systemie. W terminalu wykonano polecenia `docker --version` oraz `docker compose version`. Wynik potwierdził, że Docker jest zainstalowany w wersji `29.3.1`, a Docker Compose w wersji `v5.1.1`.

Następnie utworzono plik `docker-compose.yml`, w którym zdefiniowano dwa serwisy. Pierwszym serwisem był `postgres`, pełniący rolę bazy danych analitycznych. Do jego uruchomienia wykorzystano obraz `postgres:16`. Drugim serwisem był `metabase`, czyli narzędzie BI dostępne z poziomu przeglądarki. Do jego uruchomienia wykorzystano obraz `metabase/metabase:latest`.

Środowisko uruchomiono poleceniem:

```powershell
docker compose up -d
```

Po uruchomieniu sprawdzono stan kontenerów za pomocą polecenia:

```powershell
docker compose ps
```

Wynik pokazał, że kontenery `lab12_postgres` oraz `lab12_metabase` zostały poprawnie uruchomione. Kontener PostgreSQL udostępniał port `5432`, natomiast kontener Metabase port `3000`.

Dodatkowo sprawdzono użyte obrazy poleceniem:

```powershell
docker compose images
```

Wynik potwierdził wykorzystanie obrazów `postgres:16` oraz `metabase/metabase:latest`.

Na końcu otwarto interfejs Metabase w przeglądarce pod adresem `http://localhost:3000`. Panel Metabase uruchomił się poprawnie, a po przejściu przez konfigurację początkową utworzono konto administratora. Widoczny panel główny Metabase potwierdził, że narzędzie BI działa lokalnie i jest gotowe do połączenia z bazą danych PostgreSQL w kolejnych zadaniach.

## Zadanie 2. Załadowanie danych do bazy analitycznej

W ramach zadania przygotowano dane wejściowe w postaci zbioru transakcji zapisanych w pliku `data/transactions.csv`. Dane zawierały kolumny wymagane w poleceniu: `event_time`, `user_id`, `category`, `amount` oraz `status`. Zbiór obejmował przykładowe transakcje z różnych dni, kategorii oraz statusów, takich jak `paid`, `cancelled` i `pending`.

Do załadowania danych do bazy PostgreSQL przygotowano skrypt `load_data.py`. W skrypcie wykorzystano biblioteki `pandas`, `sqlalchemy` oraz `psycopg2-binary`. Dane zostały wczytane z pliku CSV, a następnie kolumna `event_time` została przekonwertowana na typ daty i czasu, natomiast kolumna `amount` na typ liczbowy.

Połączenie z bazą PostgreSQL zostało wykonane z poziomu skryptu Python. Ponieważ skrypt był uruchamiany lokalnie z systemu Windows, użyto adresu `127.0.0.1` oraz portu udostępnionego przez kontener PostgreSQL. Dane zostały zapisane do tabeli `transactions` w bazie danych `ntpd`.

Skrypt uruchomiono poleceniem:

```powershell
python load_data.py
```

Po uruchomieniu program wyświetlił informację, że dane zostały poprawnie załadowane do tabeli `transactions`. Wczytano 20 wierszy, a tabela zawierała kolumny `event_time`, `user_id`, `category`, `amount` oraz `status`.

Następnie w narzędziu Metabase dodano połączenie do bazy danych PostgreSQL. Jako typ bazy wybrano `PostgreSQL`, a połączenie skonfigurowano dla bazy `ntpd`. Ponieważ Metabase działa w kontenerze Docker, jako host wykorzystano nazwę serwisu `postgres`, port `5432`, użytkownika `bi` oraz hasło `bi`.

Po zapisaniu połączenia sprawdzono, czy baza danych jest widoczna w Metabase. W sekcji baz danych pojawiła się baza `PostgreSQL NTPD`, a w niej tabela `Transactions`. Następnie otwarto podgląd tabeli i sprawdzono, że dane zostały poprawnie wyświetlone w interfejsie Metabase.

Zadanie potwierdziło, że dane transakcyjne zostały poprawnie przygotowane, załadowane do PostgreSQL oraz udostępnione w narzędziu Metabase do dalszej analizy Business Intelligence.

## Zadanie 3. Pierwsze pytania i wykresy

W ramach zadania utworzono pierwsze pytania analityczne w narzędziu Metabase na podstawie tabeli `transactions` załadowanej wcześniej do bazy PostgreSQL. Celem było sprawdzenie, czy dane mogą być analizowane zarówno za pomocą wizualnego kreatora zapytań, jak i ręcznie napisanego zapytania SQL.

Pierwsze pytanie zostało utworzone za pomocą wizualnego kreatora zapytań, bez pisania kodu SQL. Jako źródło danych wybrano tabelę `Transactions`, a następnie dodano filtr `Status is paid`. Dzięki temu wynik zawierał tylko transakcje opłacone. Dla tego pytania wybrano wizualizację w formie tabeli, ponieważ najlepiej nadaje się ona do prezentacji pojedynczych rekordów, takich jak czas zdarzenia, identyfikator użytkownika, kategoria, kwota oraz status transakcji.

Drugie pytanie również przygotowano w kreatorze Metabase. Tym razem zastosowano agregację danych według kategorii. Dla rekordów ze statusem `paid` obliczono liczbę transakcji oraz sumę wartości `amount`, a następnie pogrupowano wynik według kolumny `category`. Do prezentacji wyniku użyto wykresu słupkowego, ponieważ taki wykres dobrze pokazuje porównanie wartości między kategoriami. Na wykresie można łatwo zauważyć, które kategorie mają największą liczbę transakcji i największą sumę przychodów.

Trzecie pytanie zostało przygotowane jako zapytanie SQL. Zapytanie obliczało liczbę zdarzeń oraz sumę przychodu dla każdej kategorii, uwzględniając tylko transakcje ze statusem `paid`.

```sql
SELECT
    category,
    COUNT(*) AS events,
    SUM(amount) AS revenue
FROM transactions
WHERE status = 'paid'
GROUP BY category
ORDER BY revenue DESC;
```

Wynik zapytania pokazał, że największy przychód wygenerowała kategoria `electronics`. Dla tego pytania zastosowano wykres słupkowy, ponieważ pozwala on w czytelny sposób porównać przychód i liczbę zdarzeń pomiędzy kategoriami.

Dodatkowo utworzono czwarte pytanie pokazujące trend sprzedaży w czasie. W tym celu wykorzystano zapytanie SQL grupujące transakcje według dnia.

```sql
SELECT
    DATE(event_time) AS day,
    COUNT(*) AS events,
    SUM(amount) AS revenue
FROM transactions
WHERE status = 'paid'
GROUP BY DATE(event_time)
ORDER BY day;
```

Dla tego pytania wybrano wykres liniowy. Ten typ wizualizacji pasuje do danych czasowych, ponieważ pokazuje zmianę liczby zdarzeń oraz przychodu w kolejnych dniach. Dzięki temu można obserwować, jak zmieniała się sprzedaż w analizowanym okresie.

Zadanie potwierdziło, że Metabase umożliwia analizę danych zarówno z użyciem prostego kreatora wizualnego, jak i zapytań SQL. Utworzone pytania mogą zostać wykorzystane w kolejnym zadaniu jako karty dashboardu.

## Zadanie 4. Budowa dashboardu

W ramach zadania utworzono dashboard w narzędziu Metabase o nazwie `Dashboard sprzedaży LAB12`. Dashboard został przygotowany na podstawie pytań utworzonych w poprzednim zadaniu i służy do analizy sprzedaży oraz transakcji zapisanych w tabeli `transactions`.

Na dashboardzie umieszczono kilka kart analitycznych. Pierwszą kartą był wykres liniowy `04_Trend_sprzedazy_w_czasie`, pokazujący liczbę zdarzeń oraz przychód w kolejnych dniach. Taka wizualizacja pozwala obserwować zmiany sprzedaży w czasie. Kolejne karty przedstawiały przychód według kategorii. Wykorzystano między innymi wykres `02_Przychod_wedlug_kategorii`, przygotowany za pomocą kreatora Metabase, oraz kartę `03_SQL_przychod_kategorie`, utworzoną na podstawie zapytania SQL. Na dashboardzie umieszczono również tabelę `01_Opłacone transakcje`, która pokazuje szczegółowe rekordy transakcji ze statusem `paid`.

Dashboard został ułożony w taki sposób, aby najpierw widoczne były wykresy podsumowujące sprzedaż, a niżej szczegółowa tabela transakcji. Dzięki temu użytkownik może najpierw szybko ocenić ogólną sytuację sprzedażową, a następnie przejść do dokładniejszych danych.

Do dashboardu dodano filtr `Data`, który działa jako parametr czasu. Filtr został skonfigurowany jako selektor daty i połączony z kartami korzystającymi bezpośrednio z tabeli `Transactions`, między innymi z kartą przychodu według kategorii oraz tabelą opłaconych transakcji. Jako kolumnę filtrowania wybrano `Transactions.Event Time`.

Po zastosowaniu filtra ustawiono zakres od 3 maja 2026 do 5 maja 2026. Dashboard zaktualizował powiązane karty, a tabela opłaconych transakcji pokazała 7 rekordów z wybranego zakresu dat.

Na dashboardzie umieszczono także analizę trendu sprzedaży w czasie w formie wykresu liniowego. Jest to istotne, ponieważ pozwala ocenić, jak zmieniały się liczba transakcji oraz przychód w kolejnych dniach. Taki wykres jest bardziej czytelny dla danych czasowych niż tabela lub wykres kołowy.

Zadanie potwierdziło, że Metabase pozwala tworzyć interaktywne dashboardy BI złożone z wielu kart analitycznych, filtrów oraz różnych typów wizualizacji. Przygotowany dashboard może być wykorzystany do szybkiej analizy sprzedaży, porównania kategorii oraz obserwacji zmian przychodu w czasie.

## Zadanie 5. Wskaźniki, analiza i udostępnianie wyników

W ramach zadania zdefiniowano wskaźniki biznesowe KPI, przygotowano analizę przychodu według kategorii oraz pokazano sposób udostępniania wyników z poziomu Metabase.

Pierwszym wskaźnikiem KPI był łączny przychód z transakcji opłaconych. Wskaźnik został obliczony za pomocą zapytania SQL sumującego wartości z kolumny `amount` tylko dla rekordów o statusie `paid`.

```sql
SELECT
    SUM(amount) AS total_revenue
FROM transactions
WHERE status = 'paid';
```

Wynik wyniósł `4022.22`, co oznacza łączną wartość wszystkich opłaconych transakcji w analizowanym zbiorze danych.

Drugim wskaźnikiem KPI była średnia wartość opłaconej transakcji. Obliczono ją za pomocą funkcji `AVG`, również tylko dla rekordów ze statusem `paid`.

```sql
SELECT
    ROUND(AVG(amount)::numeric, 2) AS avg_transaction_value
FROM transactions
WHERE status = 'paid';
```

Wynik wyniósł `251.39`, co oznacza, że przeciętna opłacona transakcja miała wartość około 251,39.

Dodatkowo przygotowano trzeci wskaźnik KPI, czyli udział transakcji opłaconych w całym zbiorze. Wartość tego wskaźnika wyniosła `80`, co oznacza, że 80% wszystkich transakcji miało status `paid`. Wskaźniki KPI zostały dodane do dashboardu jako osobne karty liczbowe, dzięki czemu najważniejsze informacje biznesowe są widoczne od razu po otwarciu pulpitu.

W ramach analizy biznesowej odpowiedziano na pytanie: które kategorie generują największy przychód? Do tego celu wykorzystano zapisane wcześniej pytanie `03_SQL_przychod_kategorie`.

```sql
SELECT
    category,
    COUNT(*) AS events,
    SUM(amount) AS revenue
FROM transactions
WHERE status = 'paid'
GROUP BY category
ORDER BY revenue DESC;
```

Analiza pokazała, że największy przychód wygenerowała kategoria `electronics`, której suma przychodu wyniosła `3096.89`. Kolejne kategorie osiągnęły znacznie niższe wartości: `clothes` uzyskało `499.88`, `beauty` `260.48`, a `books` `164.97`. Oznacza to, że kategoria `electronics` ma największy wpływ na całkowity wynik sprzedaży. Wynika to z wyższych wartości pojedynczych transakcji w tej kategorii.

Jako sposób udostępnienia wyników pokazano eksport danych z pytania `03_SQL_przychod_kategorie` do pliku CSV. Metabase umożliwia pobranie wyników zapytania w formatach takich jak `.csv`, `.xlsx` oraz `.json`. Eksport do CSV pozwala przekazać wynik analizy poza Metabase, na przykład do dalszego opracowania, przesłania innym osobom lub dołączenia do raportu. Dodatkowo pytania oraz dashboard zostały zapisane w kolekcji `Nasza analityka`, dzięki czemu mogą być ponownie otwierane i wykorzystywane w Metabase.

Przetwarzanie danych różni się od warstwy Business Intelligence tym, że przetwarzanie obejmuje przygotowanie danych, ich czyszczenie, transformację i zapis do bazy danych. Warstwa Business Intelligence służy natomiast do interpretacji danych, tworzenia wykresów, dashboardów, wskaźników KPI oraz raportów dla użytkownika biznesowego. W tym laboratorium dane zostały najpierw załadowane do PostgreSQL, a dopiero później analizowane i wizualizowane w Metabase.

Dashboard różni się od raportu statycznego tym, że dashboard jest interaktywny. Użytkownik może zmieniać filtry, zakres dat i analizować dane z różnych perspektyw. Raport statyczny jest natomiast gotowym zestawieniem, które zwykle przedstawia dane z jednego momentu i nie pozwala odbiorcy samodzielnie modyfikować widoku.

Zapytanie ad-hoc to jednorazowe pytanie tworzone w celu szybkiego sprawdzenia konkretnej informacji, na przykład przychodu według kategorii. Zdefiniowany wskaźnik KPI jest natomiast stałą metryką biznesową, która może być regularnie monitorowana. Przykładami KPI w tym zadaniu były łączny przychód, średnia wartość transakcji oraz udział transakcji opłaconych.

Metabase można porównać z Power BI. Metabase jest wygodny, gdy trzeba szybko podłączyć bazę danych, utworzyć pytania, wykresy i dashboard w aplikacji webowej. Dobrze sprawdza się w prostych projektach analitycznych i środowiskach opartych na bazach danych, takich jak PostgreSQL. Power BI jest bardziej rozbudowanym narzędziem, które lepiej sprawdza się przy zaawansowanych raportach, modelowaniu danych, integracji z Microsoft 365 oraz przygotowywaniu bardziej dopracowanych wizualnie raportów biznesowych. W tym laboratorium Metabase był wystarczający, ponieważ pozwolił szybko połączyć się z bazą PostgreSQL, utworzyć KPI, wykresy, dashboard i udostępnić wyniki analizy.
