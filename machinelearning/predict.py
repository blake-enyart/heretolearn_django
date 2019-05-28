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

class SinatraApi:

    @classmethod
    def all_answers(cls):
        data = cls.__get_json(url='https://aqueous-caverns-33840.herokuapp.com/api/v1/answers')
        data_array = []
        for record in data:
            data_array.append(record['attributes'])
        df_answer = pd.DataFrame(data_array)
        df_answer = df_answer[['question_id','course_id','student_id', 'created_at','text_answer']]
        df_answer['created_at'] = pd.to_datetime(df_answer['created_at'], format='%Y%m%d %H:%M:%S')
        df_answer = df_answer.rename({'text_answer': 'choice_id'}, axis='columns')
        return df_answer

    @classmethod
    def all_responses(cls):
        data = cls.__get_json(url='https://aqueous-caverns-33840.herokuapp.com/api/v1/responses')
        data_array = []
        for record in data:
            data_array.append(record['attributes'])
        df_response = json_normalize(data_array)
        df_response = df_response[['question_id','course_id','student_id', 'created_at','choice_id']]
        df_response['created_at'] = pd.to_datetime(df_response['created_at'], format='%Y%m%d %H:%M:%S')
        return df_response

    @classmethod
    def all_data(cls):
        df = pd.concat([cls.all_responses(), cls.all_answers()])
        df['choice_id'] = df['choice_id'].astype('float64')
        df['student_id'] = df['student_id'].astype('int64')
        return df

    @classmethod
    def __get_json(cls, url):
        response = requests.get(url)
        return json.loads(response.text)['data']

class ParseSurveyData(SinatraApi):

    def get_data():
        return SinatraApi.all_data()

    @classmethod
    def parse_data(cls):
        df = cls.get_data()
        dataset = []
        for s in df.student_id.unique():
            student_data = cls.data_parse(quiz_data(s, df), survey_data(s, df))
            for record in student_data:
                dataset.append(record)
        return dataset

    @classmethod
    def data_parse(cls, quiz_data, survey_data):
        student_array = []
        for index, row in quiz_data.iterrows():
            columns = ['choice_id','choice_id_4.0','choice_id_5.0','choice_id_6.0','choice_id_7.0']
            if index == 0:
                survey_date = survey_data[(survey_data.created_at <= row.created_at)]
                percent_survey = []
                for col in columns:
                    try:
                        x = survey_date[col].value_counts(normalize=True).loc[1]
                    except: # doesn't account for if there are no surveys
                        x = 0.0
                    percent_survey.append(x)

                student_array.append({'score':row['choice_id'],
                                      'data': percent_survey})
            else:
                survey_date = survey_data[(survey_data.created_at <= row.created_at)
                                          & (survey_data.created_at > quiz_data.iloc[index - 1].created_at) ]
                percent_survey = []
                for col in columns:
                    try:
                        x = survey_date[col].value_counts(normalize=True).loc[1]
                    except: # doesn't account for if there are no surveys
                        x = 0.0
                    percent_survey.append(x)

                student_array.append({'score':row['choice_id'],
                                      'data': percent_survey})
        return student_array

    @classmethod
    def survey_data(cls, s, df):
        survey_data = pd.concat([cls.food_data(s, df), cls.sleep_data(s, df)], sort=False)
        survey_data = survey_data.sort_values(['created_at'])
        return survey_data

    @classmethod
    def food_data(cls, s, df):
        food_data = df[(df.student_id == s) & (df.question_id == 1)] # food data for student
        food_data = food_data[['created_at', 'choice_id']]
        idx = (food_data['choice_id'] == 2)
        food_data.loc[idx,['choice_id']] = food_data.loc[idx,['choice_id']] - 2
        return food_data

    @classmethod
    def sleep_data(cls, s, df):
        sleep_data = cls.sleep_dummies(df)[(cls.sleep_dummies(df).student_id == s)] # sleep data for student
        sleep_data = sleep_data[['created_at','choice_id_4.0','choice_id_5.0', 'choice_id_6.0', 'choice_id_7.0']]
        return sleep_data

    @staticmethod
    def sleep_dummies(df):
        return pd.get_dummies(df[(df.question_id == 2)],
                              drop_first=True,
                              columns=['choice_id'])

    @classmethod
    def quiz_data(cls, s, df):
        quiz_data = df[(df.student_id == s) & (df.question_id == 3)]
        quiz_data = quiz_data.sort_values(['created_at'])[['choice_id', 'created_at']].reset_index()
        return quiz_data

    @classmethod
    def score_prediction(cls, student_processed_data): # use with student_data fxn
        best_model = cls.model_extraction()
        prediction = best_model.predict(student_processed_data)
        prediction = round(prediction[0], 2)
        return { 'score': prediction }

    @classmethod
    def model_extraction(cls, file_path='./data/models/grade_prediction_gbr_model.pickle'):
        with open(file_path, "rb") as f:
            best_model = pickle.load(f)
        return best_model

    @classmethod
    def student_data(cls, student_id, df = get_data()):
        student_id = int(student_id)
        student_survey_data = cls.survey_data(student_id, df)
        student_quiz_data = cls.quiz_data(student_id, df)
        all_student_data =  cls.data_parse(student_quiz_data, student_survey_data)
        return [all_student_data[0]['data']]
