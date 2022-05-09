from django.urls import path
from .views import train_model, train_model_ten_times

urlpatterns = [
    path('model', train_model),
    path('model/train-ten', train_model_ten_times)
]
