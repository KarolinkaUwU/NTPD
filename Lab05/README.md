## Zadanie 1. Przygotowanie lokalnego środowiska

W ramach zadania przygotowano lokalne środowisko do wdrożenia aplikacji ML w modelu serverless. W projekcie wykorzystano aplikację API z poprzednich zajęć, opartą o bibliotekę `Flask`. Aplikacja zawiera endpoint główny `/`, endpoint predykcji `/predict`, endpoint informacyjny `/info` oraz endpoint kontrolny `/health`.

W projekcie znajdowały się pliki `app.py`, `Dockerfile`, `requirements.txt` oraz `.dockerignore`. Plik `requirements.txt` zawierał biblioteki potrzebne do działania aplikacji: `flask`, `scikit-learn`, `numpy` oraz `waitress`.

Sprawdzono również dostępność wymaganych narzędzi. W terminalu potwierdzono działanie Dockera za pomocą polecenia `docker --version`. Zainstalowana wersja to `Docker version 29.3.1`. Następnie sprawdzono instalację Google Cloud SDK za pomocą polecenia `gcloud --version`. Terminal zwrócił wersję `Google Cloud SDK 567.0.0`, co potwierdza poprawną instalację pakietu `gcloud`.

Przygotowano także plik `Dockerfile`, który umożliwia zbudowanie obrazu z aplikacją. Obraz bazuje na `python:3.9-slim`, kopiuje plik `requirements.txt`, instaluje wymagane biblioteki, kopiuje plik `app.py`, wystawia port `5000` oraz uruchamia aplikację poleceniem `python app.py`.

Dodatkowo utworzono minimalny plik `.dockerignore`, aby do obrazu Dockera nie kopiować zbędnych plików. Wykluczono między innymi katalog `.venv`, pliki cache Pythona, katalog `.git`, plik `.env` oraz folder `Screenshots`.

W drugim podpunkcie sprawdzono konto Google Cloud. Za pomocą polecenia `gcloud auth list` potwierdzono, że użytkownik jest zalogowany do Google Cloud CLI. Oznacza to, że środowisko jest przygotowane do dalszej konfiguracji projektu Google Cloud oraz późniejszego wdrożenia aplikacji na Cloud Run.

## Zadanie 2A. Publikacja obrazu w Google Container Registry

W ramach zadania skonfigurowano narzędzie `gcloud` do pracy z projektem Google Cloud. Aktywny projekt sprawdzono za pomocą polecenia `gcloud config get-value project`. Terminal zwrócił identyfikator projektu `ntpd05-500317`, co potwierdza poprawną konfigurację projektu.

Następnie włączono usługę Google Container Registry za pomocą polecenia `gcloud services enable containerregistry.googleapis.com`. Operacja zakończyła się poprawnie, dzięki czemu projekt został przygotowany do przechowywania obrazów kontenerów.

W kolejnym kroku skonfigurowano logowanie Dockera do rejestrów Google za pomocą polecenia `gcloud auth configure-docker`. Po zatwierdzeniu operacji konfiguracja Dockera została zaktualizowana, co umożliwiło wypychanie obrazów do Google Container Registry.

Następnie zbudowano obraz Dockera aplikacji poleceniem `docker build -t gcr.io/ntpd05-500317/my-ml-app:v1 .`. Obraz otrzymał tag zgodny z formatem `gcr.io/<PROJECT_ID>/<IMAGE_NAME>:<TAG>`.

Na końcu obraz został wypchnięty do Google Container Registry za pomocą polecenia `docker push gcr.io/ntpd05-500317/my-ml-app:v1`. Terminal potwierdził przesłanie warstw obrazu oraz wyświetlił identyfikator `digest`, co oznacza, że obraz został poprawnie opublikowany w rejestrze. Dodatkowo polecenie `docker images` potwierdziło obecność obrazu `gcr.io/ntpd05-500317/my-ml-app:v1` w lokalnym środowisku.

## Zadanie 3A. Wdrożenie aplikacji na Google Cloud Run

W ramach zadania wdrożono aplikację ML na platformie Google Cloud Run. Do wdrożenia wykorzystano wcześniej zbudowany i opublikowany obraz Dockera `gcr.io/ntpd05-500317/my-ml-app:v1`.

Przed wdrożeniem włączono usługę Cloud Run za pomocą polecenia `gcloud services enable run.googleapis.com`. Następnie utworzono usługę `lab05-ml-api` poleceniem `gcloud run deploy`, wskazując obraz z Google Container Registry, region `europe-central2`, platformę `managed`, port `5000` oraz opcję `--allow-unauthenticated`, aby możliwe było publiczne testowanie API.

Po zakończeniu wdrożenia Cloud Run utworzył nową rewizję usługi i przekierował na nią cały ruch. W terminalu wyświetlony został adres URL usługi, co potwierdza poprawne uruchomienie aplikacji w chmurze.

Następnie skonfigurowano zmienną środowiskową `APP_ENV=production` oraz podstawowe parametry skalowania. Ustawiono `--min-instances 0`, dzięki czemu usługa może skalować się do zera, gdy nie jest używana, oraz `--max-instances 2`, aby ograniczyć maksymalną liczbę instancji. Dodatkowo ustawiono zasoby kontenera: `512Mi` pamięci oraz `1` CPU.

Na końcu przetestowano działanie wdrożonej usługi za pomocą `curl.exe`. Najpierw sprawdzono endpoint główny `/`, który zwrócił komunikat `API działa poprawnie`. Następnie przetestowano endpoint `/health`, który zwrócił status `ok`.

Przetestowano również endpoint `/predict` metodą `POST`, wysyłając dane wejściowe w formacie JSON z pliku `body.json`. Aplikacja zwróciła odpowiedź zawierającą dane wejściowe `feature1 = 8.0`, `feature2 = 9.0` oraz predykcję `1`. Oznacza to, że wdrożone API działa poprawnie i wykonuje predykcje modelu ML w środowisku Google Cloud Run.

## Zadanie 4. Porównanie zalet i wad wdrożeń serverless vs własny serwer

Wdrożenie serverless, takie jak Google Cloud Run lub Render, pozwala uruchomić aplikację bez samodzielnego zarządzania serwerem. Programista przygotowuje aplikację, obraz Dockera i konfigurację usługi, a platforma chmurowa odpowiada za uruchamianie kontenerów, skalowanie, dostępność oraz obsługę ruchu.

Główną zaletą podejścia serverless jest prostsze wdrożenie i mniejsza liczba obowiązków administracyjnych. Nie trzeba ręcznie konfigurować systemu operacyjnego, serwera aplikacyjnego, certyfikatów HTTPS ani mechanizmów skalowania. W przypadku Google Cloud Run aplikacja może skalować się do zera, gdy nie jest używana, co pozwala ograniczyć koszty przy małym ruchu.

Serverless dobrze sprawdza się przy aplikacjach API, mikroserwisach i modelach ML udostępnianych przez endpoint `/predict`. W takim podejściu łatwo wdrożyć nową wersję aplikacji przez zbudowanie nowego obrazu Dockera i opublikowanie go jako kolejnej rewizji usługi.

Wadą serverless jest mniejsza kontrola nad infrastrukturą. Użytkownik jest zależny od ograniczeń danej platformy, takich jak limity czasu działania requestu, limity pamięci, liczba instancji czy sposób obsługi zimnego startu. Przy pierwszym wywołaniu po dłuższej przerwie aplikacja może uruchamiać się wolniej, ponieważ platforma musi wystartować nową instancję.

Wdrożenie na własnym serwerze daje większą kontrolę nad środowiskiem. Można samodzielnie dobrać system, konfigurację sieci, zabezpieczenia, wersje usług i sposób uruchamiania aplikacji. Jest to korzystne w projektach wymagających niestandardowej konfiguracji, stałej dostępności lub pełnej kontroli nad danymi.

Minusem własnego serwera jest większa odpowiedzialność za utrzymanie. Trzeba samodzielnie dbać o aktualizacje systemu, bezpieczeństwo, monitoring, backupy, skalowanie, certyfikaty oraz reakcję na awarie. W przypadku małych projektów lub prostych API może to być bardziej czasochłonne niż samo stworzenie aplikacji.

Podsumowując, serverless jest wygodniejszy przy szybkim wdrażaniu aplikacji ML i API, ponieważ ogranicza pracę administracyjną i automatyzuje skalowanie. Własny serwer daje większą kontrolę, ale wymaga więcej konfiguracji i utrzymania. W tym laboratorium lepszym wyborem było wdrożenie serverless, ponieważ aplikacja ML była niewielka, kontenerowa i mogła zostać łatwo uruchomiona jako usługa Google Cloud Run.

## Zadanie 5. Konfiguracja środowiska i obsługa zmiennych konfiguracyjnych w Google Cloud Run

W ramach zadania rozszerzono aplikację o obsługę zmiennej środowiskowej `APP_ENV`. Zmienna ta określa środowisko działania aplikacji i nie jest wpisana na stałe w kodzie jako konkretna wartość produkcyjna.

W aplikacji dodano odczyt zmiennej środowiskowej oraz endpoint `/config`, który zwraca aktualną wartość `APP_ENV`. Dzięki temu można sprawdzić, czy aplikacja poprawnie korzysta z konfiguracji przekazanej przez środowisko uruchomieniowe.

Następnie zmienną `APP_ENV` zdefiniowano w konfiguracji usługi Google Cloud Run za pomocą polecenia `gcloud run services update`. Ustawiono wartość `APP_ENV=cloud-run`, a następnie sprawdzono konfigurację usługi poleceniem `gcloud run services describe`. W wyniku widoczna była zmienna `APP_ENV` oraz jej wartość `cloud-run`.

Po zmianie kodu zbudowano nową wersję obrazu Dockera z tagiem `v2`, a następnie wypchnięto ją do Google Container Registry. Nowy obraz został wdrożony w Cloud Run jako kolejna rewizja usługi `lab05-ml-api`.

Na końcu przetestowano działanie aplikacji za pomocą `curl.exe`. Wywołanie endpointu `/config` zwróciło `{"APP_ENV":"cloud-run"}`, co potwierdza, że aplikacja poprawnie odczytuje zmienną środowiskową z konfiguracji Cloud Run. Dodatkowo endpoint główny `/` zwrócił odpowiedź zawierającą `"environment":"cloud-run"` oraz komunikat o poprawnym działaniu API.
