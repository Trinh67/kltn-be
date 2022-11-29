# kltn-be
Backend for KLTN

## Migrations
### Create migration versions
```
$ alembic revision --autogenerate
```
### Upgrade head migration
```
alembic upgrade head
```

## Install and running app
### Run web app
```
$ uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```


### Usage
To run test
```
    py.test --cov=app
```


### Run Job
```
    python command.py background-job upload-file-to-elastic-search
```
