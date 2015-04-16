# http-tracking-bg-jobs
simple HTTP service for tracking progress of background tasks
using flask and sqlalchemy (via sqlite)
### Instalation
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

### Setup db
```
./manage.py db upgrade
```
optionally you can add some dummy data
```
./manage.py init_dummy_data

```
### Run tests
```
./manage.py test
```
### Run server
```
./manage.py runserver
```
### Availiable endpoints

```'/' (GET)``` - returns app version  
```'/tasks' (GET)``` - returns list of tasks  
```'/task', (POST)``` - creates new task accepts total parameter  
```'/task/task_id' (GET)``` - returns task info  
```'/task/task_id' (PUT)``` - updates task, accepts progress parameter  
```'/task/task_id/progress' (PUT)``` - updates task, by adding progress in url to current task progress  
```'/task/task_id' (DELETE)``` - removes task  
