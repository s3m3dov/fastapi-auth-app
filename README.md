# Task: Fast API, JWT Authentication, async workers #


## Further Details ##
* This repository contains the solution for the interview task which is given by company Whelp.
* [Go to task](https://whelp.slite.com/p/note/MiWSksjtRXX8nW8h7rX9ms)


## Initial Set-up ##
### Virtual Environment ###
```
virtualenv .env
```
```
source .env/bin/activate
```

### Run using docker-compose ###
* Make sure docker is running on your hardware
```
docker-compose up -d --build
```
* Go to [localhost](http://localhost:8000)

### Install & Run Fast Api ###
```
pip install fastapi
```
```
pip install "uvicorn[standard]"
```
```
uvicorn main:app --reload
```