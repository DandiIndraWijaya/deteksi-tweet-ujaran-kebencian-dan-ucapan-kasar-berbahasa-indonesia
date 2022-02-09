from django.urls import path
from .views import article_list, article_detail, train_model

urlpatterns = [
    path('article', article_list),
    path('detail/<int:pk>', article_detail),
    path('model', train_model)
]
