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
from datetime import datetime as dt

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
    def all_responses(cls):
        url = 'https://aqueous-caverns-33840.herokuapp.com/api/v1/responses'
        # url = 'http://localhost:9393/api/v1/responses'
        raw_data = cls.__get_json(url=url)
        df = pd.DataFrame([r['attributes'] for r in raw_data])

        # data_array = []
        # for record in data:
        #     data_array.append(record['attributes'])
        # df = json_normalize(data_array)
        # df = df[['question_id','course_id','student_id', 'created_at','choice_id']]
        df['created_at'] = pd.to_datetime(df['created_at'], format='%Y%m%d %H:%M:%S')
        df['choice_id'] = df['choice_id'].astype('float64')
        df['student_id'] = df['student_id'].astype('int64')
        return df

    @classmethod
    def __get_json(cls, url):
        response = requests.get(url)
        return json.loads(response.text)['data']

class ParseSurveyData(SinatraApi):

    def all_data():
        return SinatraApi.all_responses()

    @staticmethod
    def to_proportions(df, question_ids = [1,2], to_drop = [2,3]):
        dfs = [] # Aggregator
        for q_id in question_ids: # For each question you want to aggregate
            col_dat = df.loc[df['question_id'] == q_id] # Subset DF with only that question

            # Count number of times student made each choice
            counts = col_dat.groupby('student_id')['choice_id'].value_counts()
            counts.name = 'count'
            counts = counts.reset_index()

            # Count total number of choices each student made
            total = counts.groupby('student_id')['count'].sum()

            # Separate out choices to columns and student ids as index
            pivot = counts.pivot(index = 'student_id', columns = 'choice_id')
            pivot.columns = pivot.columns.levels[1]

            # Divide each count by the total for proportion
            for c in pivot:
                pivot[c] = pivot[c]/total

            # Fill with 0s
            pivot = pivot.fillna(0)

            dfs.append(pivot)

        # Concat, and drop unwanted columns (choice numbers)
        df = pd.concat(dfs, axis = 1).fillna(0)

        df = df[[1.0, 4.0, 5.0, 6.0, 7.0]]
        return df

    @classmethod
    def student_data(cls, df, student_id):
        if student_id in df.index:
            return [True, df[df.index == student_id]]
        else:
            return [False]

    # @classmethod
    # def parse_data(cls):
    #     df = cls.all_responses()
    #     dataset = []
    #     for s in df.student_id.unique():
    #         student_data = cls.data_parse(quiz_data(s, df), survey_data(s, df))
    #         for record in student_data:
    #             dataset.append(record)
    #     return dataset
    #
    # @classmethod
    # def data_parse(cls, quiz_data, survey_data):
    #     student_array = []
    #     for index, row in quiz_data.iterrows():
    #         columns = ['choice_id','choice_id_4.0','choice_id_5.0','choice_id_6.0','choice_id_7.0']
    #         if index == 0:
    #             survey_date = survey_data[(survey_data.created_at <= row.created_at)]
    #             percent_survey = []
    #             for col in columns:
    #                 try:
    #                     x = survey_date[col].value_counts(normalize=True).loc[1]
    #                 except: # doesn't account for if there are no surveys
    #                     x = 0.0
    #                 percent_survey.append(x)
    #
    #             student_array.append({'score':row['choice_id'],
    #                                   'data': percent_survey})
    #         else:
    #             survey_date = survey_data[(survey_data.created_at <= row.created_at)
    #                                       & (survey_data.created_at > quiz_data.iloc[index - 1].created_at) ]
    #             percent_survey = []
    #             for col in columns:
    #                 try:
    #                     x = survey_date[col].value_counts(normalize=True).loc[1]
    #                 except: # doesn't account for if there are no surveys
    #                     x = 0.0
    #                 percent_survey.append(x)
    #
    #             student_array.append({'score':row['choice_id'],
    #                                   'data': percent_survey})
    #     return student_array
    #
    # @classmethod
    # def survey_data(cls, s, df):
    #     survey_data = pd.concat([cls.food_data(s, df), cls.sleep_data(s, df)], sort=False)
    #     survey_data = survey_data.sort_values(['created_at'])
    #     return survey_data
    #
    # @classmethod
    # def food_data(cls, s, df):
    #     food_data = df[(df.student_id == s) & (df.question_id == 1)] # food data for student
    #     food_data = food_data[['created_at', 'choice_id']]
    #     idx = (food_data['choice_id'] == 2)
    #     food_data.loc[idx,['choice_id']] = food_data.loc[idx,['choice_id']] - 2
    #     return food_data
    #
    # @classmethod
    # def sleep_data(cls, s, df):
    #     sleep_data = cls.sleep_dummies(df)[(cls.sleep_dummies(df).student_id == s)] # sleep data for student
    #     sleep_data = sleep_data[['created_at','choice_id_4.0','choice_id_5.0', 'choice_id_6.0', 'choice_id_7.0']]
    #     return sleep_data
    #
    # @staticmethod
    # def sleep_dummies(df):
    #     return pd.get_dummies(df[(df.question_id == 2)],
    #                           drop_first=True,
    #                           columns=['choice_id'])
    #
    # @classmethod
    # def quiz_data(cls, s, df):
    #     quiz_data = df[(df.student_id == s) & (df.question_id == 3)]
    #     quiz_data = quiz_data.sort_values(['created_at'])[['choice_id', 'created_at']].reset_index()
    #     return quiz_data

    @classmethod
    def score_prediction(cls, raw_info):
        best_model = cls.model_extraction()
        prediction = best_model.predict(raw_info)
        prediction = round(prediction[0], 2)
        raw_info = round((raw_info * 100), 2)
        return {
                'score': prediction,
                'meals_missed': raw_info[1.0].values[0],
                'sleep_quality':
                    { 'none': abs(100 - raw_info[[4.0, 5.0, 6.0, 7.0]].sum(axis=1).values[0]),
                    'less_than': raw_info[4.0].values[0],
                    'usual': raw_info[5.0].values[0],
                    'more_than': raw_info[6.0].values[0],
                    'way_more': raw_info[7.0].values[0]
                    }
                }

    @classmethod
    def model_extraction(cls, file_path='./data/models/grade_prediction_gbr_model.pickle'):
        with open(file_path, "rb") as f:
            best_model = pickle.load(f)
        return best_model

    # @classmethod
    # def student_data(cls, student_id, df = all_data()):
    #     student_id = int(student_id)
    #     student_survey_data = cls.survey_data(student_id, df)
    #     student_quiz_data = cls.quiz_data(student_id, df)
    #     if len(student_survey_data) > 0:
    #         all_student_data =  cls.data_parse(student_quiz_data, student_survey_data)
    #         return [all_student_data[0]['data']]
    #     else:
    #         return None
