from django.urls import path
from .views import train_model, test_model

urlpatterns = [
    path('model', train_model),
    path('test/model', test_model)
]
