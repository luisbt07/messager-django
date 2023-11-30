# messager-django
1. [Features](#features)
2. [Technologies Used](#technologies-used)
    - [Celery - Async Tasks](#celery---async-tasks)
    - [Redis](#redis)
    - [Redis integrated with Celery](#redis-integrated-with-celery)
3. [Running - Application](#running---application)
    - [Requirements](#requirements)
    - [Setup](#setup)
    - [Monitoring Containers](#monitoring-containers)
4. [Entity Relational Diagram](#entity-relational-mapping)
5. [Test Suggestion](#test-suggestion)
6. [References](#references)

This project was developed to serve the Instructional Self project for both **Backend and Distributed Systems Development**.
Students: 

    - Luís Brandão Teixeira (Backend - DSD - class)
    - Guilherme Moraes(Backend - Class) 
    - Henrique Cravez(DSD - class)
![DjangoMessager - Overview](https://github.com/luisbt07/messager-django/assets/57811501/6644fc79-a098-4a01-be7c-4064baca176a)
### Django framework
This is a simple messager chat django-project, but with a lot of modern concepts using Docker Containers, Celery for async task queue configured with Redis(as Broker and Backend).   
#### Features:

- **Simple User Management** - User registration and login functionalities using Django's authentication system, assigns unique usercodes to new users for identification.
- **Messaging**:
  - Allows sending messages to specific recipients or broadcasting messages to all online users.
  - Displays the sender's information along with the message content in the UI.
- **Online Users**
  - Fetches and displays online users periodically, using polling strategy
- **Message History**
  - Fetches historical messages (sent or received) for display when the page loads.
  - Limited historical message retrieval.
## Technologies Used
I'm running up separate containers using docker-compose.yaml for the django-application itself, Redis - Broker and the Celery
### Celery - Async Tasks
Celery is an asynchronous task queue/job queue that allows you to run tasks in the background, separate from the main application flow. It's commonly used in web applications to handle time-consuming or recurring tasks without blocking the application.
Async Processing: Celery allows you to execute tasks asynchronously. Instead of executing tasks immediately when called, it puts them into a queue, allowing other parts of the application to continue working without waiting for the task to finish.

- **Task Execution**: Tasks are units of work represented as functions or methods. These tasks can be scheduled to run at a specific time or triggered by events.
- **Distributed System**: Celery operates as a distributed system, allowing tasks to be executed on multiple worker nodes. This enables scalability and load balancing.
- **Broker System**: It relies on a message broker (e.g., Redis, RabbitMQ) to handle the passing of messages between the application and the Celery workers. The broker acts as a mediator, enabling communication between different parts of the application.
- **Result Backend**: Celery supports result backends where the task results can be stored (e.g., in a database or cache) for retrieval or monitoring purposes.
- **Monitoring and Management**: Tools like Flower offer a web-based monitoring dashboard for managing Celery tasks and workers, providing insights into the task execution process.

Celery greatly enhances the scalability and performance of applications by handling time-consuming tasks efficiently and asynchronously, ensuring a smoother user experience.

### Redis
**Redis** is an open-source, in-memory data structure store that acts as a database, cache, and message broker. It's known for its speed, versatility, and support for various data structures.

- Data Structures: Redis supports various data structures like strings, hashes, lists, sets, and sorted sets. This versatility allows it to be used for caching, queuing, and storing data.
- In-memory Storage: Being an in-memory store, Redis keeps the entire dataset in memory. This results in faster data retrieval and storage compared to disk-based databases.
- Pub/Sub Messaging: Redis has a Pub/Sub (Publish/Subscribe) feature that allows message passing between different parts of an application. Publishers send messages to specific channels, and subscribers receive messages from these channels.
- Message Broker: In the context of Celery, Redis is commonly used as a message broker. It acts as the intermediary between the Celery client (which sends tasks) and the Celery workers (which execute the tasks). When a task is initiated by the client, it's placed into a Redis queue to be picked up by available Celery workers.
- Caching and Session Store: Redis is also widely used for caching frequently accessed data and as a session store for web applications, enhancing performance and scalability.

#### Redis integrated with Celery:

- **Broker Configuration**: Celery needs a message broker to handle the passing of messages between the client and the workers. Redis serves as this broker, efficiently managing the queue of tasks waiting to be executed.
- **Task Queue**: Celery uses Redis as a task queue. Tasks sent by the Celery client are stored in Redis, waiting to be processed by available Celery workers.
- **Scalability and Performance**: Redis's fast in-memory storage and Pub/Sub features enhance Celery's scalability, allowing multiple Celery workers to process tasks concurrently and ensuring efficient message passing.

Overall, Redis plays a crucial role in the Celery ecosystem by providing a fast and reliable message broker and task queue, enabling distributed task execution and efficient communication between components in asynchronous task processing.

### Running - Application
#### Requirements
* [Docker](https://docs.docker.com/engine/install/)
* [Docker-Compose](https://docs.docker.com/compose/)
#### Setup
 The DockerFile and docker-compose.yaml are already configured to run the application, so you just need to run the following command:

    docker compose up -d --build

To shutdown application:

    docker compose down

If you want to access the application, just go to http://0.0.0.0:8000/messager \
#### Monitoring
You may want to monitor the other containers: 

    docker logs -f messager-redis
    docker logs -f messaging-worker
    docker logs -f messager-app
![Screenshot from 2023-11-25 17-52-06](https://github.com/luisbt07/messager-django/assets/57811501/d9e4418d-10e5-4dea-9af5-1525db71ab26)
### Entity Relational Mapping
![image](https://github.com/luisbt07/messager-django/assets/57811501/2a3571fc-448d-42f3-8306-8456234638cb)

**Models**

 - **CustomUser** model extends from django User model and adds the unique usercode.
 - **Message** models holds general message information, such as the sender, content, and whether it's a broadcast.
 - **MessageRecipient** model acts as an Intermediary to link each message to its recipients. This allows for multiple users to be associated with a single message.

This intermediate model enables us to handle more complex scenarios, such as:

 - Storing read/unread status per usaer for each message.
 - Adding more metadata per recipient-message(e.g., timestamps, flags).
 - Facilitating more advanced querying or filtering based on recipients
This design pattern gives us more flexibility to manage messages and recipients separately, providing clearer and more maintainable code as the application evolves.
### Test Suggestion
Happy path
1. Run the application with the docker commands | open in different terminals the Monitoring containers
2. Open the application in three different browsers Chrome, Chrome(private mode ctrl + shift + n), Firefox
3. Register different users and login with them - Ex: users(luis, lanaro, paper)
![image](https://github.com/luisbt07/messager-django/assets/57811501/4d675a28-e841-47cd-8119-6e8321929dab)
4. Send a broadcast message - Refresh all pages(the polling was not implemented for reaching new messages)
![image](https://github.com/luisbt07/messager-django/assets/57811501/599024fe-e5ea-4111-82fc-b79711aa425b)
5. Take the code of one user online in the Online Users columen - send a message for this user - refresh all pages - you must see that only the recipient received the message
![image](https://github.com/luisbt07/messager-django/assets/57811501/29dd471f-11af-4b04-89d4-33c67a6ed439)
6. Take the code of the other user online and send only for him - refresh all pages - you must see that only the recipient received the message 
![image](https://github.com/luisbt07/messager-django/assets/57811501/6f410534-e5e6-4546-bde1-68c93f3e74b8)
7. Close all pages and open again - you must see the sessions are maintened and historical messages are retrieved and written again to the text-area 


#### References

- https://dockerize.io/guides/python-django-guide
- https://semaphoreci.com/community/tutorials/dockerizing-a-python-django-web-application
- https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#application
- https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html#installation
- https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html#broker-toc
- https://devchecklists.com/en/checklist/celery-tasks-checklist.html
- https://denibertovic.com/posts/celery-best-practices/
- https://engineering.instawork.com/celery-eta-tasks-demystified-424b836e4e94
- https://python.plainenglish.io/how-to-implement-user-login-with-jwt-authentication-in-django-rest-framework-d56ae51a1fea
