# messager-django

### Django
This is a simple project that intents to process some tasks asynchronously using Celery and Redis as broker.
For instance it doesn't control the users, it doesn't have authentication, nor it has a control of the sessions created.

What it really does is to process the tasks asynchronously and return the result of the task to the user.

I'm running up separate containers using docker-compose.yaml for the django-application itself, Redis - Broker and the Celery

### Redis - Broker
Redis is a in-memory data structure store, used as a database, cache and message broker.
### Celery - Async Tasks
Celery is a simple, flexible, and reliable distributed system to process vast amounts of messages, while providing operations with the tools required to maintain such a system. It’s a task queue with focus on real-time processing, while also supporting task scheduling.
### Running - Application
#### Requirements
* [Docker](https://docs.docker.com/engine/install/)
* [Docker-Compose](https://docs.docker.com/compose/)

 The DockerFile and docker-compose.yaml are already configured to run the application, so you just need to run the following command:

    docker compose up -d --build

To shutdown application:

    docker compose down

If you want to access the application, just go to http://0.0.0.0:8000/messager \
If you want to monitore the other containers: 

    docker logs -f messager-redis
    docker logs -f messaging-worker
    docker logs -f messager-app
![Screenshot from 2023-11-25 17-52-06](https://github.com/luisbt07/messager-django/assets/57811501/d9e4418d-10e5-4dea-9af5-1525db71ab26)
