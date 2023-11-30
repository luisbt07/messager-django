#### Django app installation https://dockerize.io/guides/python-django-guide

    mkdir messager-django
    cd messager-django

#### Install specific python into virtua env
    sudo apt-get install python3.11-venv
    python3.11 -m venv env
#### Activate virtual env - For installing django in Virtual Environment not in your machine
    source env/bin/activate # deactivate only, to turn out 
#### Create requirements.txt file add latest django-app Django==4.2.7
    cat requirements.txt
    pip install -r requirements.txt

#### Create the django project 
    django-admin startproject messager
 to run server "python manage.py runserver"

#### create a django application
    python manage.py startapp hello_world
After that you need to add on settings.py in the INSTALLED_APPS

WARNING: These are first steps creating a django project. After the project setup we started
containerizing the application with Docker.