from django.urls import path
from . import views

urlpatterns = [
    path('basic-research/', views.run_basic_research_workflow_view, name='basic-research'),
    path('historical-stock-data/', views.get_historical_data, name='historical-data')
]