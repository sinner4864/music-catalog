# NeedleDrop — каталог музыкальных альбомов

Тестовое full-stack приложение для вакансии Qortex. Проект сделан по SDD:
сначала зафиксированы доменная модель, REST-контракты и критерии приёмки в
[`specs/001-music-catalog.md`](specs/001-music-catalog.md), затем реализованы API
и интерфейс.

Одна песня может входить в разные альбомы под разными номерами: это выражено
явной связью `AlbumTrack(album, song, track_number)`, а не полем номера у песни.

## Стек

- Django 5 + Django REST Framework + SQLite;
- Vue 3 Composition API + Vite + Pinia;
- Docker Compose + nginx;
- Django API tests и GitHub Actions.

## Безопасность

Проект рассчитан на локальный запуск тестового задания. API намеренно не имеет
регистрации и аутентификации, поэтому его нельзя публиковать в интернет как
многопользовательский сервис без добавления авторизации.

- контейнер backend работает без root и без Linux capabilities;
- nginx выставляет CSP, anti-clickjacking и MIME-sniffing заголовки;
- API ограничен 120 анонимными запросами в минуту;
- секрет Django генерируется при запуске и не хранится в репозитории;
- `pip-audit`, Bandit и `npm audit` выполняются в CI;
- версии GitHub Actions и базовые Docker-образы закреплены по commit/digest.

Для внешнего HTTPS-развёртывания задайте постоянный `DJANGO_SECRET_KEY`, точный
`DJANGO_ALLOWED_HOSTS` и настройте TLS на reverse proxy.

## Быстрый запуск

Нужен Docker с Compose plugin:

```bash
docker compose up --build
```

Откройте <http://localhost:8080>. База хранится в Docker volume
`catalog-data`. Остановка: `docker compose down` (без `-v`, если данные нужны).

## Запуск для разработки

Backend (Python 3.11+):

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Frontend (Node.js 20+), в другом терминале:

```bash
cd frontend
npm install
npm run dev
```

Интерфейс будет доступен на <http://localhost:5173>, API — на
<http://localhost:8000/api/>.

## Проверки

```bash
cd backend && python manage.py test
cd frontend && npm test && npm run build
```

## API

Ресурсы находятся в `/api/artists/`, `/api/songs/`, `/api/albums/`. Добавление
трека: `POST /api/albums/{id}/tracks/` с `song_title` или `song_id` и
`track_number`. Поиск: `GET /api/albums/?search=...`.

## Принятые решения

- SQLite делает тестовое полностью автономным; ORM позволяет перейти на
  PostgreSQL без изменения предметной модели.
- Удаление исполнителя каскадно удаляет его альбомы, но песни сохраняются, пока
  их не удалят явно.
- Названия исполнителей и песен уникальны без учёта регистра; в пределах одного
  альбома уникальны и песня, и номер дорожки.
