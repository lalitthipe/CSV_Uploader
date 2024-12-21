# analysis/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.data_analysis_view, name='data_analysis'),  # This maps the root of the 'analysis' app to the view
]

