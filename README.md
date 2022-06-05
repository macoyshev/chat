# chat
Asynchronous chat. One shared chat room where users can send and 
receive messages to each other in real-time. 
When connecting, the user can request 50 recent messages.
Before start to chat, launch [redis](#run-redis), 
[fastapi-server](#run-server), and after that run the console 
[client](#run-console-client).
To see API, launch [fastapi-server](#run-server), and go to `http://127.0.0.1:8000/docs`

### Create venv:
    make venv

### Create venv for windows:
    make venv-win

### Run redis:
    make redis

### Run server:
    make up

### Run console client
    make console

### Create containers
    docker-compose build

### Run containers
    docker-compose up -d

### Run tests:
    make test

### Run linters:
    make lint

### Run formatters:
    make format
