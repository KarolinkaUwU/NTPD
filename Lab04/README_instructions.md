Aplikacja została stworzona przy użyciu Flask oraz scikit-learn. Model LogisticRegression udostępniany jest przez API REST.

## Uruchomienie lokalne

Instalacja bibliotek:

```bash
pip install -r requirements.txt
```

Uruchomienie aplikacji:

```bash
python app.py
```

Aplikacja będzie dostępna pod adresem:

```text
http://127.0.0.1:5000
```

---

## Uruchomienie za pomocą Dockera

Budowanie obrazu:

```bash
docker build -t flask-ml-api .
```

Uruchomienie kontenera:

```bash
docker run -p 5000:5000 flask-ml-api
```

---

## Uruchomienie za pomocą Docker Compose

Uruchomienie wszystkich serwisów:

```bash
docker compose up --build
```

Docker Compose uruchamia:
- aplikację ML,
- serwis Redis,
- wspólną sieć dockerową.

---

## Test endpointu

Test endpointu `/predict`:

```bash
curl.exe -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d "{\"feature1\":9,\"feature2\":8}"
```

## Konfiguracja parametrów i wymagane zasoby

Aplikacja działa na porcie 5000. W przypadku uruchamiania przez Docker lub Docker Compose port kontenera jest mapowany na port 5000 hosta:

```bash
5000:5000
```

W pliku `docker-compose.yml` można skonfigurować zmienne środowiskowe, np. adres drugiego serwisu:

```yaml
environment:
  - REDIS_HOST=redis
```

Aplikacja wymaga środowiska Python 3.9 oraz bibliotek wymienionych w pliku `requirements.txt`:
- Flask
- scikit-learn
- numpy
- waitress

Do działania kontenerowego wymagany jest Docker Desktop.

Aplikacja ma niewielkie wymagania sprzętowe, ponieważ wykorzystuje prosty model LogisticRegression trenowany na małym zbiorze danych. Wystarczające zasoby to około:
- 1 CPU
- 512 MB RAM