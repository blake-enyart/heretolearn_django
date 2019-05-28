from django.shortcuts import render

from django.http import HttpResponse
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from machinelearning.predict import ParseSurveyData
from IPython import embed

class IndexView(generic.TemplateView):
    template_name = 'machinelearning/index.html'
    context_object_name = 'latest_question_list'

def student_analysis(request):
    student_id = request.GET.get('student_id', '')
    student_data = ParseSurveyData.student_data(student_id = student_id)
    data = ParseSurveyData.score_prediction(student_data)
    return JsonResponse(data)
