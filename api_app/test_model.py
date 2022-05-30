import joblib
from sklearn.model_selection import train_test_split
import pandas as pd
import os
from sklearn.metrics import accuracy_score

def import_dataset():
  df = pd.read_csv(os.path.abspath("api_app/data.csv"),  encoding='latin-1')
  return df

def start_test_model(tweet, algoritma, ekstraksi_fitur):
  filename = algoritma + '_' + ekstraksi_fitur
  loaded_model = joblib.load(filename)
  
  model_prediction = loaded_model.predict([tweet])
  
  jenis_tweet = ''
  if model_prediction[0] == '0':
    jenis_tweet = "Tweet Netral"
  elif  model_prediction[0] == '1':
    jenis_tweet = "Tweet Ujaran Kebencian"
  elif  model_prediction[0] == '2':
    jenis_tweet = "Tweet Ucapan Kasar"
  
  return {
    "tweet": jenis_tweet
  }
  
def start_check_model_accuracy(algoritma, ekstraksi_fitur):
  filename = algoritma + '_' + ekstraksi_fitur
  loaded_model = joblib.load(filename)
  
  file =  open(r"C:\Users\ACER\Documents\SKRIPSI\THIS\FOR DOSEN\code\deteksi_tweet\api_app\stemmedTextList.txt")
  lines = file.readlines()
  lines = [line.rstrip() for line in lines]

  stemmed_text_list = lines
  
  dataset = import_dataset()
  target = dataset['HS']

  for i in range(len(dataset)):
    if(dataset['HS'][i] == 0 and dataset['Abusive'][i] == 1):
      target[i] = 2
      
  x_train,x_test,y_train,y_test = train_test_split(stemmed_text_list, target, test_size=0.20, random_state=0)
  model_prediction = loaded_model.predict(x_test)
  ac = accuracy_score(y_test.values.astype('U'), model_prediction)
  print(model_prediction)
  return {
    "accuracy": 'model_prediction'
  }