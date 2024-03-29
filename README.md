# Here To Learn - Django & Jupyter Notebook

 [Django application](http://lit-fortress-28598.herokuapp.com/) hosted on Heroku that utilizes a machine learning model trained with over 300,000 data points to predict test outcomes for 5,000 mock students based on eating and sleeping habits for each student.

 This [Jupyter Notebook](https://github.com/blake-enyart/heretolearn_django/blob/master/jupyter_notebook/ml-generator.ipynb) demonstrates:
* Data generation
* JSON API conversion to pandas DataFrame
* Data munging (dummy variables for nominal categorical sleep data)
* Hyperparameter optimization & model selection in RandomSearchCV
* Gradient boosted model training
* matplotlib and seaborn visualization

 This app is one-third of a Service Oriented Architecture (SOA) app called Here To Learn which integrates with a [Rails application](https://github.com/carriewalsh/HereToLearn) which presents the data and serves as the interface for teachers and students and a [Sinatra application](https://github.com/JennicaStiehl/surveys) which stores survey information gathered from students.

**Application Highlights:**
* 5 person team project
* SOA integration into Rails and Sinatra applications all hosted independently on Heroku
* Data munging, hyperparameter optimization & model selection
* Matplotlib, seaborn, chart.js data visualization

## Contributing
* [Blake Enyart](https://github.com/blake-enyart) - Django app, data visualization (chart.js, seaborn, matplotlib), machine learning implementation
* [William Peterson](https://github.com/wipegup) - Provided input and mentoring on the machine learning model development

### Location of Apps in Production
* [Here to Learn](https://young-anchorage-86985.herokuapp.com) - Rails based central app designed for user interface
* [Django application](http://lit-fortress-28598.herokuapp.com/) - Django based machine learning microservice
* [Surveys](https://aqueous-caverns-33840.herokuapp.com) - Sinatra based database microservice

## Tech Stack
<p align="center">
 <img src="media/README/tech_stack.png" width="600" height="auto"/>
</p>

## Data Visualization
<p align="center">
 <img src="media/README/joint_plot.png" width="400" height="auto"/>
</p>

## Local Configuration for Further Development

Use the following code to setup the code locally:
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
 Navigate to `localhost:8000` from your browser to see the app in development mode
 
## Django App Demo

Use the following endpoint to see the production app return data from the Sinatra app, make a prediction, and render data and prediction in JSON format:
```
https://lit-fortress-28598.herokuapp.com/machinelearning/results/?student_id=5
```
