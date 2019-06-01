from django.shortcuts import render

from django.http import HttpResponse
from django.http import Http404
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from machinelearning.predict import ParseSurveyData, SinatraApi
from IPython import embed

class IndexView(generic.TemplateView):
    def get(self, request):
        return HttpResponse()

class StudentAnalysis(View):
    def get(self, request):
        student_id = request.GET.get('student_id', '')
        student_id = int(student_id)
        raw_df = SinatraApi.all_responses()
        df = ParseSurveyData.to_proportions(raw_df)
        student_data = ParseSurveyData.student_data(df=df, student_id = student_id)
        if student_data[0]:
            results = ParseSurveyData.score_prediction(student_data[1])
            return JsonResponse(results)
        else:
            return JsonResponse({})
