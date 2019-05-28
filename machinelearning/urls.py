from django.urls import path

from . import views

app_name = 'machinelearning'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('results/', views.student_analysis, name='score'),
]
