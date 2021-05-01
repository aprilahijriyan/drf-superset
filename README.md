# Django REST Framework SuperSet

**Status is in progress, feel free if anyone wants to add features or anything!** <br>
For more details, see our contribution guidelines [here](https://github.com/aprilahijriyan/drf-superset/blob/main/CONTRIBUTING.md).

* Read more: https://drf-superset.readthedocs.io/en/latest/


# Quickstart

First you have to fork and clone this repository:

```
git clone https://github.com/<username>/drf-superset
```

Initialize virtual environment using python version 3.7 (in this case I am using [poetry](https://python-poetry.org/) as package manager):

```
poetry env use $(which python3.7)
```

And install all required dependency packages:

```
poetry install --no-dev
```

Create migrations for `drf_superset` app:

```
python manage.py makemigrations drf_superset
python manage.py migrate
```

Run it:

```
python manage.py runserver
```

Go to http://127.0.0.1:8000/docs/


**NOTE: If you want to test the endpoint on the `jwt` tag, don't forget to run the local SMTP server first.**

```
python -m smtpd -c DebuggingServer -n -d
```
