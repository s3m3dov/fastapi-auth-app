# Task: Fast API, JWT Authentication, async workers #


## Further Details ##
* This repository contains the solution for the interview task which is given by company Whelp.
* [Go to task](https://whelp.slite.com/p/note/MiWSksjtRXX8nW8h7rX9ms)


## Initial Set-up ##
### Using docker-compose ###
* Make sure docker is running on your hardware
* Make sure to change `IPDATA_API_KEY` on `docker-compose.yml` file.
```
docker-compose up -d --build
```
or
```
docker-compose -f docker-compose-local.yml up -d --build
```
* Go to [API Docs](http://localhost:8000/docs)

## Testing ##
```
docker-compose exec web pytest -vv
```
```
docker-compose exec web pytest --cov --cov-config=.coveragerc
```
