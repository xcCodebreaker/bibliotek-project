# Bibliotek

A small library web app made with Django, where you can browse books by category.

## How to run it

1. Make a virtual environment and turn it on:

```
py -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install the packages:

```
pip install -r requirements.txt
```

3. Set up the database and start the server:

```
python manage.py migrate
python manage.py runserver
```

4. Open http://127.0.0.1:8000 in the browser.
