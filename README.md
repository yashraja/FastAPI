# FastAPI

# Table of contents
1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [How to Run](#howtorun)
4. [Project Phases](#phases)
    1. [Docker](#docker)
    2. [Fast API](#fastapi)
    3. [Postgres](#db)
    4. [Test Cases](#tests)
    5. [Logging](#logs)
5. [Reference Materials](#ref)

## Introduction <a name="introduction"></a>
    This project is created for general purpose learning.


## Required softwares <a name="requirements"></a>
```text
Python3 + FastAPI + postgres + Docker + Test Cases
```

## How to Run <a name="howtorun"></a>
```commandline
    uvicorn main:app --reload // Start this server in main.py path
```

## Project Phases: <a name="phases"></a>

| S.No  | Module | Description | Branch | Status |
| ----- | ------ | ------ | ------ | ------ |
| 1.  | Docker  | Setup Docker File | Docker-101 | TBD |
| 2.  | Fast API  | Setup code for Fast API | FastAPI-102 | TBD |
| 3.  | Postgres  | Add tables to database | Postgres-103 | TBD |

### Docker <a name="docker"></a>
```text
Info on Docker
```

### Fast API <a name="fastapi"></a>

Needs UVICORN to be installed- This acts as a server

Install uvicorn
```commandline
    pip install uvicorn
```

Run uvicorn
```commandline
    uvicorn main:app --reload
```

URL:

Swagger: 
```text
         http://localhost:8000/docs#/
         http://localhost:8000/redoc
```

Response : http://localhost:8000/


### Postgres <a name="db"></a>
```text
Info on Postgres
```

### Test Cases <a name="tests"></a>
```commandline
   pytest -v
```
ABove pytest command will run the existing tests case scenarios.

### Logging <a name="logs"></a>
```text
   Default log level is set as INFO.
   Logging is handled in logger.py file
```


## References: <a name="ref"></a>

Dev: https://realpython.com/fastapi-python-web-apis/

Testing: https://fastapi.tiangolo.com/tutorial/testing/

