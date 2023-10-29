# Brandeis Courses API 
## Description
This is a RESTful API that provides information about Brandeis courses that was scraped from the course registrar website with Selenium. The API is built with Python Flask. The database is built with PostgreSQL deployed on AWS RDS.
## Table of Contents
- [API Endpoints](#api-endpoints)
- [Database Setup Process](#database-setup-process)
- [Challenges](#challenges)
- [Postgresql Notes](#postgresql-notes)

## API Endpoints
## Tech Stack
- Python
- Flask
- PostgreSQL
- AWS RDS
- Selenium

## Database Setup Process
### Install ODBC driver and connect to SQL server

- `pip install --no-binary :all: pyodbc` install error solution 
- `odbcinst -q -d`check if driver is installed
- `sqlcmd -S servername.database.windows.net,1433 -U "username" -P 'password' -Q "use mydb;"` connect to sql server with sqlcmd

### Challenges 
#### Cannot connect to the sql server 
- install pyodbc
- install pymssql but failed to install the library, seems like the library is not compatible with my environment
- checked the firewall setting, the port 1433 is open, and ip address is allowed
- checked the server name, username and password, all correct
- checked the odbc driver, the driver is installed
- tried increasing connection timeout, but still failed

#### Resorted to using postgresql instead
- installed postgresql with postgres.app
- installed psycopg2
- successfully connected to the database
- disadavantage: requries third party cloud service to host the database


## Postgresql Notes
### What is PostgreSQL
- A `server` process accepts connections from client applications, and performs database actions on behalf of the clients.
- A `server` program is called `postgres`.
- A `client` may be a text-oriented tool, a graphical application, a web server that accesses the database for information to be presented on a website.
- relational database management systems (RDBMS)
### Creating a database
- `createdb` is a wrapper around the SQL command `CREATE DATABASE`. 
- `dropdb` is a wrapper around the SQL command `DROP DATABASE`. 
```
cursor.execute('''CREATE TABLE course_data (
    id serial PRIMARY KEY,
    course varchar(255),
    courseTitle varchar(255),
    syllabus varchar(255),
    instructor varchar(255),
    term varchar(255),
    requirements varchar(255)[], -- Assuming it's an array
    description text
    );''')
```
Ran into an error when creating a database, the error message is 
```bash
createdb: error: connection to server on socket "/tmp/.s.PGSQL.5432" failed: No such file or directory Is the server running locally and accepting connections on that socket?
```
Solution: used postgres.app instead of homebrew to install postgresql, and it works
- Initialized databse cluster 
### Connecting to a database from python
- `psycopg2` is a PostgreSQL database adapter for the Python programming language.
```
connection = psycopg2.connect(
	host="localhost",         # Hostname or IP address of your database server
	database="courses",  # Name of your database
	user="minstonewang",     # Your PostgreSQL username
	password=""  # Your PostgreSQL password
)
cursor = connection.cursor()
    
```
### SQL types 
- `int` is a signed integer that has a maximum precision of 32 bits.
- `smallint` is a signed integer that has a maximum precision of 16 bits.
- `real` is a floating-point number that supports 6 decimal digits of precision.
- `double precision` is a floating-point number that supports 15 decimal digits of precision.
- `char(n)` is a fixed-length character string.
- `varchar(n)` is a variable-length character string with a maximum length of n.
- `date` stores the date.
- `time` stores the time of day.
- `timestamp` stores the date and time of day.
- `interval` stores an interval of time.
### Sqlalchemy - Object Relational Mapper
- `sqlalchemy` allows you to work with Python objects that map to database tables, which can make your code more Pythonic and object-oriented. 
### psql - terminal-based front-end to PostgreSQL
- `psql` is a terminal-based front-end to PostgreSQL. It enables you to type in queries interactively, issue them to PostgreSQL, and see the query results.
basic commands
- `\l` // list all databases
- `\c` // connect to a database
- `\dt` // list all tables in the current database
- `\q` // quit

