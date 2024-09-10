from django.urls import path
from llmpredictor.views import *
app_name='llmpredictor'
urlpatterns=[
    path('llmpredict/',Predictor.as_view()),
]
