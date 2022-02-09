from datetime import datetime
from statistics import mode
from unittest import result
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article, ModelResult
from .serializers import ArticleSerializer, ModelResultSerializer
from django.views.decorators.csrf import csrf_exempt
from .deteksi import start_train_model
# Create your views here.

@csrf_exempt
def article_list(request):
  
  if request.method == 'GET':
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return JsonResponse(serializer.data, safe = False)
  
  elif request.method == 'POST':
    data = JSONParser().parse(request)
    serializer = ArticleSerializer(data=data)
    
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def article_detail(request, pk):
  try:
    article = Article.objects.get(pk=pk)
  
  except Article.DoesNotExist:
    return HttpResponse(status=404)
  
  if request.method == 'GET':
    serializer = ArticleSerializer(article)
    return JsonResponse(serializer.data)
  
  elif request.method == 'PUT':
    data = JSONParser().parse(request)
    serializer = ArticleSerializer(article, data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)
    
  elif request.method == 'DELETE':
    article.delete()
    return HttpResponse(status=204)
  
@csrf_exempt
def train_model(request):
  
  if request.method == 'GET':
    train_model = ModelResult.objects.all()
    serializer =ModelResultSerializer(train_model, many=True)
    return JsonResponse(serializer.data, safe = False)
  
  elif request.method == 'POST':
    data = JSONParser().parse(request)
    if data['algoritma'] != 'svm' and data['algoritma'] != 'rf' and data['algoritma'] != 'vc':
      return HttpResponse(content='algoritma tidak ditemukan di sistem', status=404)
    
    model_result = start_train_model(data['algoritma'], data['ekstraksi-fitur'])
    
    model_result = ModelResult.objects.get(model=data['algoritma'])
    # Update model
    updated_model = ModelResultSerializer(model_result, data={
      "model": data['algoritma'], 
      "updated_at" :datetime.now()
    })
    if updated_model.is_valid():
      updated_model.save()
      trained_model = ModelResult.objects.all()
      object_result = {
        'svm': {
          'tfidf_unigram_acc': '3'
        },
        'rf': {
          'tfidf_unigram_acc': '4'
        },
        'vc': {
          'tfidf_unigram_acc': '5'
        }
      }
      for model in trained_model:
        object_result[model.model]['tfidf_unigram_acc'] =  model.tfidf_unigram_acc
      return JsonResponse(object_result, status=200)
    # End update model
    
    return JsonResponse(updated_model.errors, status=400)