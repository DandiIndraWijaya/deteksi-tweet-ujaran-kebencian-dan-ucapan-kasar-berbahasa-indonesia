from dataclasses import fields
from statistics import mode
from rest_framework import serializers
from .models import Article, ModelResult

class ArticleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Article
    fields = ['id', 'title', 'author', 'date']

class ModelResultSerializer(serializers.ModelSerializer):
  class Meta:
    model = ModelResult
    fields = ['id', 
             'model',
             'tfidf_unigram_acc', 
             'tfidf_bigram_acc',
             'tfidf_trigram_acc',
             'tfidf_unigram_time',
             'tfidf_bigram_time',
             'tfidf_trigram_time',
             'updated_at'
             ]