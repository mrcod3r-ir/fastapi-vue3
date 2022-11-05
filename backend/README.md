# FastAPI

## Version iteration

- `V1.0` FastAPI learning
- `V2.0` to build FastAPI scaffolding
- `V2.1` to create the required tables
- `V2.2` has successfully debugged Mysql, Sqlite, but not Postgresql
- `V2.3` initialization table data (debug)
- `V2.4` optimize the problem of creating tables
- `V2.5` initialize all table data
- `V2.6` package logging module
- `V2.7` encapsulates the multi-process log module (thread lock)
- `V2.8` optimized directory structure
- `V2.9` optimized the code && debugged the add, delete and query interface of the user table
- `V3.0` added to prevent cross-domain request code && debug interface
- `V3.1` removes the auto-increment of the test table
- `V3.2` added the interface of the department table
- `V3.3` added major table interface
- `V3.4` updated some code of major table interface
- `V3.5` replaced log module (loguru) && added backend data validation
- `V3.5` added teacher table interface
- `V3.6` added the interface of student table
- `V3.7` added the interface of course table and selectCourse table
- `V3.8` updated required packages
- `V3.9` modified the data for querying a single message
- `V4.0` removed methods to get all data and get individual data
- `V4.1` modified the validation rules
- `V4.1.1` removed the regular check rules for integer and floating point types
- `v4.2` is trying to deploy. . .
- `v4.3` has been deployed successfully, and some bugs have been fixed
- `v4.4` test token
- `v4.5` debug token success (admin, 123)
- `v4.6` refactored FastAPI
- `v4.7` add redis
- `v4.8` refactored backend
- `v4.9` supports PostgreSQL, and image upload
- `v5.0` implements permission management module in the background
- `v5.1` organizes the interface, and simply implements the rights management module
- `v5.2` adjust database structure

## Install

1.  Configure the virtual environment of <font color="red">Python3.9 (and above)</font>

2.  Install the required packages to run

    ```python
    # Mysql and ProgreSQL are installed by default
    pip install requirements.txt

    # or
    pip install fastapi
    pip install uvicorn[fastapi]
    pip install loguru
    pip install SQLAlchemy
    pip install aioredis
    pip install python-jose
    pip install passlib
    pip install bcrypt
    pip install python-multipart
    pip install orjson

    # To use Sqlite (asynchronous), please install the following bread
    pip install aiosqlite

    # Use MySQL (asynchronous), please install the following bread
    pip install asyncmy

    # To use ProgreSQL (asynchronous), please install the following bread
    pip install asyncpg
    ```

3.  Start the service

        + go to the `backend` project
        + find `main.py` right click to run
        + `core/config` configuration file (default database is sqlite)

    > Interface documentation: http://127.0.0.1:8000/docs

## Project screenshot

- picture of successful operation

  ![](https://gitee.com/zxiaosi/image/raw/master/Project/Vue+FastAPI/image-20211021164103094.png)

- interface diagram

  ![](https://gitee.com/zxiaosi/image/raw/master/Project/Vue+FastAPI/backend-%E6%8E%A5%E5%8F%A3.png)

## Project directory (to be sorted out)

```sh
|-- backend

		|-- api # interface
				|-- admin
						|-- __init__.py # Administrator interface
						|-- course.py # Curriculum interface
						|-- department.py # Department table interface
						|-- major.py # Professional watch interface
						|-- index.py # Admin home page
						|-- elective.py # Course elective table interface
						|-- student.py # Student table interface
						|-- teacher.py # Teacher table interface
				|-- common
						|-- __init__.py # common interface
						|-- login.py # login interface
						|-- redis_check.py # Check if redis is connected successfully
						|-- upload.py # image upload
				|-- __init__.py
				|-- deps.py # dependencies
				|-- api_router.py # admin interface summary

|-- core
|-- __init__.py # Core content
|-- config.py # configuration file
|-- security.py # security configuration

|-- crud
|-- __init__.py # Database addition, deletion, modification and query operations
|-- base.py # Encapsulate database addition, deletion, modification and query methods
|-- course.py # Course schedule
|-- department.py # Department table
|-- major.py # Major table
|-- elective.py # elective table
|-- teacher.py # teacher table
|-- student.py # Student table

 |-- db
 |-- __init__.py # Initial database and table data
|-- data.py # All data
		|-- init_data.py # Two ways to initialize table data
|-- init_db.py # Create and delete tables in base
|-- session.py # Create a database connection session
		|-- redis.py # Register Redis

		|-- logs # log module (automatically generated)
				|-- 2021-10-06_23-46-45.log
				|-- 2021-10-06_23-46-47.log
				|-- 2021-10-06_23-46-49.log

|-- models
|-- __init__.py # ORM model mapping
|-- base.py # Automatically generate table name
|-- index.py # Administrator table
|-- course.py # Course schedule
|-- department.py # Department table
|-- major.py # Major table
|-- elective.py # elective table
|-- student.py # Student table
|-- teacher.py # teacher table

|-- register
|-- __init__.py # Registration Center
|-- cors.py # Register cross-domain requests
|-- exception.py # Register global exceptions
|-- middleware.py # Registration request response interception
|-- router.py # Register routing

|-- schemas
|-- __init__.py # data model
|-- admin.py # Admin table model
|-- common.py # common table model
|-- course.py # Curriculum model
|-- department.py # Department table model
|-- login.py # login model
|-- major.py # Professional table model
|-- result.py # return data model
|-- elective.py # elective table model
|-- student.py # Student table model
|-- teacher.py # Teacher table model
|-- todo.py # todo model
|-- token.py # token model

|-- utils # Utilities
|-- __init__.py # Throw tool class
|-- create_dir.py # Create a folder class (do not move the location)
|-- custon_exc.py # custom exception
|-- ip_address.py # Get the location based on ip
|-- logger.py # log module
|-- permission_assign.py # permission management
|-- resp_code.py # Status code

|-- __init__.py
|-- main.py # main program
|-- Dockerfile # Dockerfile file
|-- README.md # Readme file
|-- requirements.txt # Required packages
|-- sql_app.db # sqlite database
```
