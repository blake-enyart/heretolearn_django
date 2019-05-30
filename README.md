# Here To Learn on django
## Description
```django microservice for machine learning component of HereToLearn app
```
## Goals
```
The Django application that has trained a machine learning model on over 5000 data points to predict test outcomes based on eating and sleeping habits in order to help.
```
## Configuration
```python3 -m venv env
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
 ```development: localhost:8000
 production: http://lit-fortress-28598.herokuapp.com/
 ```
## Versioning
```v1  5/30/2019
```
## Contributing
```https://github.com/blake-enyart/heretolearn_django
```
