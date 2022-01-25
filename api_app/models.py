from django.db import models

# Create your models here.


class Article(models.Model):
  title = models.CharField(max_length=100)
  author = models.CharField(max_length=100)
  email = models.EmailField(max_length=100)
  date = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.title

class ModelResult(models.Model):
  model = models.CharField(max_length=100)
  tfidf_unigram_acc = models.IntegerField()
  tfidf_brigram_acc = models.IntegerField()
  tfidf_trigram_acc = models.IntegerField()
  tfidf_unigram_time = models.CharField(max_length=100)
  tfidf_brigram_time = models.CharField(max_length=100)
  tfidf_trigram_time = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField()
  def __str__(self):
    return self.title
  