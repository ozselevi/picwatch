# Képfeltöltő és Arcérzékelő Webalkalmazás

Ez a projekt egy FastAPI-alapú webalkalmazás, amely lehetővé teszi a felhasználók számára képek feltöltését leírással, azokon automatikus arcdetektálást, valamint e-mailes értesítések küldését a tartalmakról a feliratkozott felhasználóknak.

## 🚀 Funkciók

- Képfeltöltés leírással
- Arcok automatikus felismerése a képeken (`face_recognition`)
- Feltöltött képek fájlrendszerben történő tárolása
- Adatok mentése PostgreSQL adatbázisba
- Feliratkozás e-mail értesítésekre
- Háttérfeladatok kezelése Celery-vel és Redis-szel
- Tartós adatok és képek Kubernetes Persistent Volume segítségével

## 🛠️ Használt technológiák

- **FastAPI** – gyors és aszinkron webes backend
- **PostgreSQL** – megbízható relációs adatbázis-kezelő
- **Celery + Redis** – háttérfeladatok és értesítések kezelése
- **face-recognition** – Python csomag arcfelismeréshez
- **Docker** – konténerizált környezet minden komponenshez
- **Kubernetes (PVC)** – tartós adattárolás és skálázható futtatás
- **GitHub Actions** – automatikus CI/CD pipeline

