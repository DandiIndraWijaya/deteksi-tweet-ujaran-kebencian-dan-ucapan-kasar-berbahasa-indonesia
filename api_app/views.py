from datetime import datetime
from statistics import mode
from unittest import result
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import ModelResult
from .serializers import ModelResultSerializer
from django.views.decorators.csrf import csrf_exempt
from .deteksi import start_train_model
# Create your views here.

def make_data_to_store(model, ekstraksi_fitur, acc, time):
  if ekstraksi_fitur == 'tfidf_unigram':
    return {
      "model": model, 
      'tfidf_unigram_acc': acc,
      'tfidf_unigram_time': time,
      "updated_at" :datetime.now()
    }
  elif ekstraksi_fitur == 'tfidf_bigram':
    return {
      "model": model, 
      'tfidf_bigram_acc': acc,
      'tfidf_bigram_time': time,
      "updated_at" :datetime.now()
    }
  elif ekstraksi_fitur == 'tfidf_trigram':
    return {
      "model": model, 
      'tfidf_trigram_acc': acc,
      'tfidf_trigram_time': time,
      "updated_at" :datetime.now()
    }
    

@csrf_exempt
def train_model(request):
  
  if request.method == 'GET':
    trained_model = ModelResult.objects.all()
    object_result = {
      'svm': {
        'tfidf_unigram_acc': ''
      },
      'rf': {
        'tfidf_unigram_acc': ''
      },
      'vc': {
        'tfidf_unigram_acc': ''
      }
    }
    for model in trained_model:
      object_result[model.model]['tfidf_unigram_acc'] =  model.tfidf_unigram_acc
      object_result[model.model]['tfidf_bigram_acc'] =  model.tfidf_bigram_acc
      object_result[model.model]['tfidf_trigram_acc'] =  model.tfidf_trigram_acc
      object_result[model.model]['tfidf_unigram_time'] =  model.tfidf_unigram_time
      object_result[model.model]['tfidf_bigram_time'] =  model.tfidf_bigram_time
      object_result[model.model]['tfidf_trigram_time'] =  model.tfidf_trigram_time
      object_result[model.model]['updated_at'] =  model.updated_at
        
    return JsonResponse(object_result, status=200)
  
  elif request.method == 'POST':
    data = JSONParser().parse(request)
    if data['algoritma'] != 'svm' and data['algoritma'] != 'rf' and data['algoritma'] != 'vc':
      return HttpResponse(content='algoritma tidak ditemukan di sistem', status=404)
    
    trained_model_result = start_train_model(data['algoritma'], data['ekstraksi-fitur'])
    
    model = ModelResult.objects.get(model=data['algoritma'])
    # Update model
    data = make_data_to_store(data['algoritma'], data['ekstraksi-fitur'], trained_model_result['akurasi'], trained_model_result['durasi'])
    updated_model = ModelResultSerializer(model, data=data)
    if updated_model.is_valid():
      updated_model.save()
      trained_model = ModelResult.objects.all()
      object_result = {
        'svm': {
          'tfidf_unigram_acc': ''
        },
        'rf': {
          'tfidf_unigram_acc': ''
        },
        'vc': {
          'tfidf_unigram_acc': ''
        }
      }
      for model in trained_model:
        object_result[model.model]['tfidf_unigram_acc'] =  model.tfidf_unigram_acc
        object_result[model.model]['tfidf_bigram_acc'] =  model.tfidf_bigram_acc
        object_result[model.model]['tfidf_trigram_acc'] =  model.tfidf_trigram_acc
        object_result[model.model]['tfidf_unigram_time'] =  model.tfidf_unigram_time
        object_result[model.model]['tfidf_bigram_time'] =  model.tfidf_bigram_time
        object_result[model.model]['tfidf_trigram_time'] =  model.tfidf_trigram_time
        object_result[model.model]['updated_at'] =  model.updated_at
        
      return JsonResponse(object_result, status=200)
    # End update model
    
    return JsonResponse(updated_model.errors, status=400)