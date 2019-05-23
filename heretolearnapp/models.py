from django.db import models
import datetime
from django.utils import timezone

#Data Analysis Suite
import pandas as pd
import numpy as np
import scipy
import sklearn as sk
import seaborn as sns
import matplotlib.pyplot as plt

# HTTP
import requests
import json

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class SurveyData(models.Model):
    response = requests.get('http://localhost:3000/irises')
