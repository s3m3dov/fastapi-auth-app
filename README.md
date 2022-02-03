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