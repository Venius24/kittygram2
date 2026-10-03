# Kittygram 2

Учебный Django REST API: коты, достижения и список пользователей. JWT аутентификация, уникальное имя кота у владельца, проверка года рождения и цвета.

## Локальный запуск

Нужен Python 3.9. В Windows:

```powershell
py -3.9 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python manage.py migrate
.venv\Scripts\python manage.py runserver
```

В Linux/macOS используйте `.venv/bin/python`. Переменные `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS` и необязательная `DJANGO_DB_PATH` описаны в `.env.example`; Django читает их из окружения, но не загружает `.env` сам. Для внешнего доступа установите собственный ключ, `DJANGO_DEBUG=0` и допустимые хосты.

Маршруты: `/cats/`, `/users/`, `/achievements/`, `/auth/jwt/create/`. Проверки: `python manage.py check`, `python manage.py test`. Старый ключ в истории Git требует отдельной ротации и очистки истории при развёртывании.
