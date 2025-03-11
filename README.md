# Task Manager API

## Автор

Бондаренко Алексей Олегович
- Telegram: [@alovsemprivet](https://t.me/alovsemprivet)
- GitHub: [Pr1ority](https://github.com/Pr1ority)

## Описание
Telegram_bot — это телеграм-бот и веб-сервис для управления задачами с поддержкой категорий, и работой с API из телеграм-бота. Пользователь может создавать и удалять свои задачи.
## Требования
- Docker
- Docker Compose
- Python 3.10+

## Запуск проекта

```bash
git clone https://github.com/Pr1ority
cd telegram_bot
```

Настройте виртуальное окружение
```bash
python -m venv venv
```

Для macOS/Linux
```bash
source venv/bin/activate
```
Для Windows
```bash
source venv/Scripts/activate
```

Заполните .env
Пример:
```example.env
SECRET_KEY=YOUR_SECRET_KEY
TOKEN=YOUR_TG_TOKEN
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=bot
DB_NAME=bot
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1,telegram-bot-service
```

Поднимите контейнеры в Докере
```bash
docker-compose up --build
```

Подготовьте базу данных
```bash
docker-compose exec web python manage.py migrate
```

```bash
docker-compose exec web python manage.py createsuperuser
```

После этого API будет доступен по адресу: `http://localhost:8080`

## API

### 🔑 Аутентификация
- `POST /api/register/` — регистрация нового пользователя
- `POST /api/token/` — получение JWT токена

### 📆 Задачи
- `GET /api/tasks/` — список задач пользователя
- `POST /api/tasks/` — создать задачу
- `PUT /api/tasks/<id>/` и `PATCH /api/tasks/<id>/` — обновить задачу
- `DELETE /api/tasks/<id>/` — удалить задачу

### 📄 Категории
- `GET /api/categories/` — получить все категории
- `POST /api/categories/` — добавить категории
- `PUT /api/categories/<id>/` / `PATCH /api/comments/<id>/` - обновить категорию
- `DELETE /api/categories/<id>/` - удалить категорию

## Telegram Bot

[Ссылка на бота](https://t.me/Tasksd0_bot)

### Создание задачи
- `/add_task`

### Список задач
- `/tasks`

### Удалить задачу
- `/delete_task`

### Редактировать задачу
- `/edit_task`

### Группировать задачи по категориям
- `/tasks_by_category`

## Архитектура
- Django + Django REST Framework
- JWT-аутентификация
- Docker + docker-compose для создания изолированной среды
- Telegram Bot общается с API через HTTP
- Все операции CRUD доступны только для авторизованных пользователей

## Трудности
- Вопросы к логике регистрации и аутентификации через DRF JWT были решены созданием отдельного RegisterView

---

Если вы запустили проект и хотите протестить через Postman или Swagger:
- сначала создайте пользователя (регистрация)
- затем получите JWT-токен
- и передавайте `Authorization: Bearer <token>` в заголовках

---


