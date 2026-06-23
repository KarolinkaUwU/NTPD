## Zadanie 1. Zbieranie danych z produkcji i przygotowanie modelu do monitorowania

W ramach zadania przygotowano dwa sztucznie wygenerowane zbiory danych. Pierwszy zbiór reprezentował dane historyczne, czyli dane z okresu trenowania lub walidacji modelu. Drugi zbiór reprezentował dane produkcyjne, czyli nowsze próbki pojawiające się po wdrożeniu modelu.

Dane wygenerowano za pomocą funkcji `make_classification` z biblioteki `scikit-learn`. Zbiór historyczny zawierał `500` rekordów oraz `5` cech wejściowych, natomiast zbiór produkcyjny zawierał `300` rekordów oraz te same cechy. Do obu zbiorów dodano kolumnę `target`, czyli prawdziwą etykietę klasy.

Następnie wytrenowano model klasyfikacyjny `RandomForestClassifier` na danych historycznych. Model został nauczony na cechach `feature_0`–`feature_4`, a jako zmienną docelową wykorzystano kolumnę `target`.

Po treningu wykonano predykcję dla danych produkcyjnych. Wyniki predykcji zapisano w zbiorze produkcyjnym w dodatkowej kolumnie `prediction`. Dzięki temu dane produkcyjne zawierały zarówno prawdziwe etykiety `target`, jak i przewidywania modelu `prediction`.

Dane zostały następnie wczytane do środowiska Pythona i poddane wstępnej analizie. Sprawdzono liczbę rekordów i kolumn, typy zmiennych, liczbę braków danych, rozkład klas oraz podstawowe statystyki opisowe.

Zbiór historyczny miał rozmiar `(500, 6)`, ponieważ zawierał pięć cech oraz kolumnę `target`. Zbiór produkcyjny miał rozmiar `(300, 7)`, ponieważ oprócz pięciu cech i kolumny `target` zawierał również kolumnę `prediction`.

W obu zbiorach nie występowały braki danych. Zmiennymi wejściowymi były wartości typu `float64`, natomiast kolumny `target` i `prediction` miały typ `int64`. Rozkład klas w zbiorze historycznym był prawie równy: klasa `0` wystąpiła `251` razy, a klasa `1` `249` razy. W zbiorze produkcyjnym klasa `0` wystąpiła `151` razy, a klasa `1` `149` razy.

Rozkład predykcji modelu na danych produkcyjnych wynosił `171` predykcji klasy `0` oraz `129` predykcji klasy `1`. Oznacza to, że model częściej przewidywał klasę `0`, mimo że rzeczywisty rozkład klas w danych produkcyjnych był prawie zbalansowany.

## Zadanie 2. Wykrywanie driftu danych z biblioteką Evidently AI

W ramach zadania zainstalowano i zaimportowano bibliotekę `Evidently AI`, która służy do monitorowania modeli ML oraz wykrywania zmian w danych. Sprawdzono również wersję biblioteki z poziomu terminala. Wykorzystana wersja Evidently to `0.7.21`.

Następnie wygenerowano raport `Data Drift`, w którym porównano zbiór historyczny jako dane referencyjne oraz zbiór produkcyjny jako dane aktualne. Raport został zapisany w formacie HTML, dzięki czemu można go było otworzyć w przeglądarce i przeanalizować w formie interaktywnej.

Na podstawie raportu stwierdzono, że wystąpił drift danych na poziomie całego zbioru. Evidently wykazało, że spośród `5` analizowanych cech aż `4` cechy miały wykryty drift. Udział kolumn z driftem wyniósł `0.8`, czyli `80%`.

W dalszej części raportu sprawdzono drift dla poszczególnych cech wejściowych. Drift został wykryty dla cech `feature_0`, `feature_2`, `feature_3` oraz `feature_4`. Dla cechy `feature_1` drift nie został wykryty.

Oznacza to, że dane produkcyjne różnią się od danych historycznych pod względem rozkładu większości cech. Taka sytuacja może świadczyć o zmianie charakteru danych wejściowych po wdrożeniu modelu. W praktyce może to prowadzić do pogorszenia jakości predykcji, dlatego taki wynik powinien być sygnałem do dalszej analizy modelu, sprawdzenia jego metryk na danych produkcyjnych oraz ewentualnego ponownego trenowania modelu na nowszych danych.

## Zadanie 3. Analiza jakości predykcji po wdrożeniu

W ramach zadania przeprowadzono analizę jakości predykcji modelu po wdrożeniu. Do oceny wykorzystano dane produkcyjne, które zawierały zarówno prawdziwe etykiety `target`, jak i predykcje modelu zapisane w kolumnie `prediction`.

Za pomocą biblioteki Evidently wygenerowano raport jakości klasyfikacji. Raport pokazał podstawowe metryki modelu na danych produkcyjnych: accuracy, precision, recall oraz F1-score. Dla danych produkcyjnych uzyskano wyniki: accuracy `0.4733`, precision `0.4651`, recall `0.4027` oraz F1-score `0.4317`.

Następnie porównano jakość modelu na zbiorze referencyjnym, czyli historycznym, oraz na zbiorze aktualnym, czyli produkcyjnym. Na danych historycznych model osiągnął wyniki równe `1.0000` dla wszystkich analizowanych metryk. Na danych produkcyjnych wyniki były znacznie niższe.

Tak duży spadek jakości oznacza, że model nie radzi sobie dobrze z nowymi danymi. Accuracy spadło z `1.0000` do `0.4733`, a F1-score z `1.0000` do `0.4317`. Oznacza to, że model poprawnie klasyfikował mniej niż połowę próbek produkcyjnych.

Spadek jakości można uznać za znaczący. Wynik ten jest zgodny z wcześniejszą analizą driftu danych, w której wykryto drift dla `4 z 5` cech wejściowych. Oznacza to, że dane produkcyjne różnią się od danych historycznych, na których model był trenowany.

W takiej sytuacji zalecane jest zebranie większej liczby aktualnych danych produkcyjnych wraz z prawdziwymi etykietami. Następnie model powinien zostać ponownie wytrenowany z wykorzystaniem nowszych danych. Warto także regularnie monitorować drift danych oraz metryki jakości modelu, aby szybciej wykrywać pogorszenie działania modelu w środowisku produkcyjnym.
