from django.shortcuts import render

from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

class IndexView(generic.TemplateView):
    template_name = 'machinelearning/index.html'
    context_object_name = 'latest_question_list'

class ShowView()
