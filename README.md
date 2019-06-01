# Here To Learn on django

## Description
This Django application has trained a machine learning model with over 5000 data points to predict test outcomes based on eating and sleeping habits in order to assist students reach their full potential. HereToLearn, a Rails application works with this application to present the graphs, interact with teachers and students.

## Goals
* Work with two other applications, a Sinatra microservice and a Rails application
* Predict student test scores

## Configuration
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
psql
CREATE DATABASE heretolearn_production;
CREATE USER heretolearn WITH PASSWORD 'badgers';
GRANT ALL PRIVILEGES ON DATABASE heretolearn_production TO heretolearn;
\q
python manage.py migrate
python manage.py runserver
 ```
## Locations/Where to Find the applications
### Here To Learn
 ```
 development: localhost:3000
 production: https://young-anchorage-86985.herokuapp.com
 ```
### Surveys
 ```
 development: localhost:9393
 production: https://aqueous-caverns-33840.herokuapp.com
 ```
### Machine Learning Microservice
 ```
 development: localhost:8000
 production: http://lit-fortress-28598.herokuapp.com/
 ```
## Versioning
```
v1  5/30/2019
```
## Contributing
```https://github.com/blake-enyart/heretolearn_django
```
