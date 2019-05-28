from django.db import models
from django.http import JsonResponse

# Analysis Suite
import sys
import scipy
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import sklearn
from IPython import embed
import seaborn as sns

# Development Suite
import datetime as dt
import IPython
from IPython import embed
import csv
from datetime import timedelta

# HTTP Suite
from pandas.io.json import json_normalize
import requests
import json
import dateutil.parser

# sklearn Analysis Suite
from sklearn import model_selection
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import median_absolute_error

# sklearn Model Suite
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

import pickle

class SinatraApi(models.Model):
    class Meta:
        abstract = True

        def all_answers(self):
            data = get_json('http://localhost:9393/api/v1/answers')

            data_array = []
            for record in data:
                data_array.append(record['attributes'])

            df_answer = pd.DataFrame(data_array)
            df_answer = df_answer[['question_id','course_id','student_id', 'created_at','text_answer']]
            df_answer['created_at'] = pd.to_datetime(df_answer['created_at'], format='%Y%m%d %H:%M:%S')
            df_answer = df_answer.rename({'text_answer': 'choice_id'}, axis='columns')
            return df_answer

        def all_responses(self):
            data = get_json('http://localhost:9393/api/v1/responses')

            data_array = []
            for record in data:
                data_array.append(record['attributes'])

            df_response = json_normalize(data_array)
            df_response = df_response[['question_id','course_id','student_id', 'created_at','choice_id']]
            df_response['created_at'] = pd.to_datetime(df_response['created_at'], format='%Y%m%d %H:%M:%S')
            return df_response

        def all_data(self):
            df = pd.concat([all_responses(), all_answers()])
            df['choice_id'] = df['choice_id'].astype('float64')
            df['student_id'] = df['student_id'].astype('int64')
            return df

        @memoized
        def __get_json(self, url):
            response = requests.get(url)
            return json.loads(response.text)['data']

class ParseSurveyData(SinatraApi):
    class Meta:
        abstract = True

        @memoized
        def get_data():
            return all_data()

        def parse_data(self):
            df = get_data()
            dataset = []
            for s in df.student_id.unique():
                student_data = data_parse(quiz_data(s, df), survey_data(s, df))

                for record in student_data:
                    dataset.append(record)
            return dataset

        def survey_data(self, s, df):
            survey_data = pd.concat([food_data(s, df), sleep_data(s, df)], sort=False)
            survey_data = survey_data.sort_values(['created_at'])
            return survey_data

        def food_data(self, s, df):
            food_data = df[(df.student_id == s) & (df.question_id == 1)] # food data for student
            food_data = food_data[['created_at', 'choice_id']]
            idx = (food_data['choice_id'] == 2)
            food_data.loc[idx,['choice_id']] = food_data.loc[idx,['choice_id']] - 2
            return food_data

        def sleep_data(self, s, df):
            sleep_data = sleep_dummies(df)[(sleep_dummies.student_id == s)] # sleep data for student
            sleep_data = sleep_data[['created_at','choice_id_4.0','choice_id_5.0', 'choice_id_6.0', 'choice_id_7.0']]
            return sleep_data

        def sleep_dummies(self, df):
            return pd.get_dummies(df[(df.question_id == 2)],
                                  drop_first=True,
                                  columns=['choice_id'])

        def quiz_data(self, s, df):
            quiz_data = df[(df.student_id == s) & (df.question_id == 3)]
            quiz_data = quiz_data.sort_values(['created_at'])[['choice_id', 'created_at']].reset_index()
            return quiz_data

        def score_prediction(self, student_data): # use with student_data fxn
            best_model = model_extraction()
            return { 'score': best_model.predict(data) }

        def model_extraction(self, file_path='./data/models/grade_prediction_gbr_model.pickle'):
            with open(file_path, "rb") as f:
                best_model = pickle.load(f)
            return best_model

        def student_data(self, student_id, df=get_data()):
            return survey_data(student_id, df)

class StudentAnalysis(ParseSurveyData):
    def 
    student_id = request.GET.get('student_id', '')
    data = StudentAnalsis.score_prediction(self.student_data(request.GET.get('student_id', '')))
    return JsonResponse(data, safe=False)
