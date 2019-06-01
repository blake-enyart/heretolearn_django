# Here To Learn - django

## Description
 This [Django application](http://lit-fortress-28598.herokuapp.com/) utilizes a machine learning model trained with over 300,000 data points to predict test outcomes for 5,000 mock students based on eating and sleeping habits for each student. The goal is to assist students reach their full potential. 

 [HereToLearn](https://young-anchorage-86985.herokuapp.com), a Rails application, works with this application to present the graphs, interact with teachers and students.
 
 The [Jupyter Notebook](https://github.com/blake-enyart/heretolearn_django/blob/master/jupyter_notebook/ml-generator.ipynb). demonstrates how the model was selected and trained.

**Jupyter Notebook Highlights:**
* Microservice JSON API conversion into pandas DataFrame
* Dummy variable implementation for nominal categorical sleep data
* model selection through k-fold cross validation in RandomSearchCV
* Hyperparameter optimization
* Gradient boosted model training
* matplotlib and seaborn visualization

**Rails App Integration:**
* chart.js presentation

## Goals
* Work with two other applications, a [Sinatra microservice](https://aqueous-caverns-33840.herokuapp.com) and a [Rails application](https://young-anchorage-86985.herokuapp.com)
* Predict student test scores using machine learning model developed [here](https://github.com/blake-enyart/heretolearn_django/blob/master/jupyter_notebook/ml-generator.ipynb)

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
#### Here To Learn
 ```
 development: localhost:3000
 production: https://young-anchorage-86985.herokuapp.com
 ```
#### Surveys
 ```
 development: localhost:9393
 production: https://aqueous-caverns-33840.herokuapp.com
 ```
#### Machine Learning Microservice
 ```
 development: localhost:8000
 production: http://lit-fortress-28598.herokuapp.com/
 ```

## Contributing

* [Blake Enyart](https://github.com/blake-enyart) - django app, data visualization (chart.js, seaborn, matplotlib), machine learning implementation
* [William Peterson](https://github.com/wipegup) - Provided input and mentoring on the machine learning model development
