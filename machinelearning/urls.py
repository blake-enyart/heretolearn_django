from django.urls import path

from machinelearning.views import IndexView, StudentAnalysis

app_name = 'machinelearning'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('results/', StudentAnalysis.as_view(), name='score'),
]
