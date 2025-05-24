from django.urls import path

from .views import PredictCaloriesView


urlpatterns = [
    path('', PredictCaloriesView.as_view(), name='predict_calories'),
]
