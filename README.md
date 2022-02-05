# Task: Fast API, JWT Authentication, async workers #


## Further Details ##
* This repository contains the solution for the interview task which is given by company Whelp.
* [Go to task](https://whelp.slite.com/p/note/MiWSksjtRXX8nW8h7rX9ms)


## Initial Set-up ##
### Using docker-compose ###
* Make sure docker is running on your hardware
```
docker-compose up -d --build
```
or
```
docker-compose -f docker-compose-local.yml up -d --build
```
* Go to [localhost](http://localhost:8000)

### Issue: MySQL ###
* In case you face with this issue `(2003, "Can't connect to MySQL server on 'db' ([Errno 111] Connection refused)")`
* Run docker-compose build command above (I couldn't fix the root cause of the problem)


## Testing ##
```
docker-compose exec web pytest -vv
```
```
docker-compose exec web pytest --cov --cov-config=.coveragerc
```
