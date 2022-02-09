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
    # model_result = start_train_model(data['algoritma'], data['ekstraksi-fitur'])
    
    try:
      model_result = ModelResult.objects.get(model=data['algoritma'])
      
      
    except ModelResult.DoesNotExist:
      newModel = ModelResult(model='svm', tfidf_unigram_acc='81.39711465451785', tfidf_unigram_time='0:01:10.873679', updated_at = datetime.now())
      newModel.save()
      trained_model = ModelResult.objects.all()
      serializer =ModelResultSerializer(trained_model, many=True)
      return JsonResponse(serializer.data, safe = False)
    
    # if serializer.is_valid():
    #   serializer.save()
    #   return JsonResponse(serializer.data, status=201)
    serializer = ModelResultSerializer(model_result, data={
      "model": 'svm', "tfidf_unigram_acc":'87.39711465451785', "tfidf_unigram_time": '0:01:10.873679', "updated_at" :datetime.now()
    })
    if serializer.is_valid():
      serializer.save()
      trained_model = ModelResult.objects.all()
      serializer =ModelResultSerializer(trained_model, many=True)
      return JsonResponse(serializer.data, safe = False)
    return JsonResponse(serializer.errors, status=400)
  
@csrf_exempt
def update_model(request, pk):
  try:
    model_result = ModelResult.objects.get(pk=pk)
  
  except ModelResult.DoesNotExist:
    return HttpResponse(status=404)
  
  if request.method == 'PUT':
    data = JSONParser().parse(request)
    serializer = ModelResultSerializer(model_result, data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)
    
  elif request.method == 'DELETE':
    model_result.delete()
    return HttpResponse(status=204)