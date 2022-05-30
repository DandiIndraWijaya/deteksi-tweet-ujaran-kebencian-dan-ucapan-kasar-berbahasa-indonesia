from fileinput import filename
import pandas as pd
import nltk
import os
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger') 
from nltk import word_tokenize
from nltk.corpus import stopwords
from numpy import array
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.model_selection import train_test_split
import joblib


def import_dataset():
  df = pd.read_csv(os.path.abspath("api_app/data.csv"),  encoding='latin-1')
  return df

def preprocess_data(df):
  #Case Folding
  df['Tweet'] = df['Tweet'].str.lower()

  #Punctuation Removal
  df['Tweet'] = df['Tweet'].str.replace('[^\w\s]','')

  #Tokenization
  df_without_stopword = df['Tweet'].apply(word_tokenize)

  #Stopword Removal
  list_stopwords = stopwords.words('indonesian')
  list_stopwords = set(list_stopwords)

  #remove stopword pada list token
  def stopwords_removal(words):
      return [word for word in words if word not in list_stopwords]

  df_with_stopword = df_without_stopword.apply(stopwords_removal)
  return df_with_stopword
  
def normalize_text(preprocessed_data):
  normalized_text = []
  for tokens in preprocessed_data:
    tokens_sent = ' '.join(tokens)
    normalized_text.append(tokens_sent)
  return normalized_text

def stemming_data(normalized_text):
  factory = StemmerFactory()
  stemmer = factory.create_stemmer()
  stemmed_text_list = []

  for i in range(len(normalized_text)):
    text = normalized_text[i]
    text = stemmer.stem(text)
    stemmed_text_list.append(text)

  with open(r"C:\Users\ACER\Documents\SKRIPSI\THIS\Dataset\stemmedTextList3.txt", "w") as txt_file:
      for line in stemmed_text_list:
          txt_file.write(line + "\n")
          
  return stemmed_text_list

def import_stemmed_dataset():
  file =  open(r"C:\Users\ACER\Documents\SKRIPSI\THIS\FOR DOSEN\code\deteksi_tweet\api_app\stemmedTextList.txt")
  lines = file.readlines()
  lines = [line.rstrip() for line in lines]

  stemmed_text_list = lines
  return stemmed_text_list

def process_data(algoritma, ekstraksi_fitur, dataset, stemmed_text_list):
  from sklearn.pipeline import make_pipeline
  from sklearn.ensemble import RandomForestClassifier, VotingClassifier
  from sklearn import svm
  from sklearn.feature_extraction.text import TfidfVectorizer
  from sklearn.model_selection import cross_val_score
  from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report, confusion_matrix
  import time
  import datetime
  
  target = dataset['HS']

  for i in range(len(dataset)):
    if(dataset['HS'][i] == 0 and dataset['Abusive'][i] == 1):
      target[i] = 2
      
  x_train,x_test,y_train,y_test = train_test_split(stemmed_text_list, target, test_size=0.20, random_state=0)
  
  svm = svm.SVC(probability=True)
  random_forest = RandomForestClassifier()
  voting_classifier = VotingClassifier(estimators=[('svm', svm), ('rf', random_forest)], voting='soft')

  if algoritma == 'svm':
    selected_algoritma = svm
    algm = 'svm'
  elif algoritma == 'rf':
    selected_algoritma = random_forest
    algm = 'rf'
  elif algoritma == 'vc':
    selected_algoritma = voting_classifier
    algm = 'vc'
  
  if ekstraksi_fitur == 'tfidf_unigram':
    vec = TfidfVectorizer(ngram_range=(1, 1))
    ef = 'tfidf-unigram'
  elif ekstraksi_fitur == 'tfidf_bigram':
    vec = TfidfVectorizer(ngram_range=(1, 2))
    ef = 'tfidf-bigram'
  elif ekstraksi_fitur == 'tfidf_trigram':
    vec = TfidfVectorizer(ngram_range=(1, 3))
    ef = 'tfidf-trigram'
  
  print('TRAINING MODEL')
  print('ALGORITMA : ', algm)
  print('EKSTRAKSI FITUR : ', ef)
  model = make_pipeline(vec, selected_algoritma)
  start = time.time()
  model.fit(x_train, y_train.values.astype('U'))
  stop = time.time()
  model_prediction = model.predict(x_test)
  ac = accuracy_score(y_test.values.astype('U'), model_prediction)
  # k_cross_val = 10
  # train_ac = cross_val_score(model, x_train, y_train.values.astype('U'), cv=k_cross_val, scoring="accuracy", verbose=2)
  # ac = train_ac.mean()
  print(f"Training time: {stop - start}s")
  timeInHour = str(datetime.timedelta(seconds=stop-start))
  print('Time in hour: ', timeInHour)
  print("Akurasi : ", ac * 100,'%')
  # print(classification_report(y_test.values.astype('U'), model_prediction))
  filename = algoritma + '_' + ekstraksi_fitur
  joblib.dump(model, filename)
  
  return {
    "model": algoritma,
    "ekstraksi_fitur": ekstraksi_fitur,
    "akurasi": f"{ac * 100}",
    "durasi": timeInHour
  }
  
def start_train_model(algoritma, ekstraksi_fitur):
  dataframe = import_dataset()
  preprocessed_data = preprocess_data(dataframe)
  normalized_text = normalize_text(preprocessed_data)
  # stemmed_data = stemming_data(normalized_text)
  stemmed_data = import_stemmed_dataset()
  result = process_data(algoritma, ekstraksi_fitur, dataframe, stemmed_data)
  return result
  
