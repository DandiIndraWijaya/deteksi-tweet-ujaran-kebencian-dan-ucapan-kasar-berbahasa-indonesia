import pandas as pd
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger') 
from nltk import word_tokenize
from nltk.corpus import stopwords
from numpy import array
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

def import_dataset():
  df = pd.read_csv(r'C:\Users\ACER\Documents\SKRIPSI\THIS\Dataset\data.csv',  encoding='latin-1')
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

def main():
  data_frame = import_dataset()
  preprocessed_data = preprocess_data(data_frame)
  normalized_text = normalize_text(preprocessed_data)
  stemmed_data = stemming_data(normalized_text)
  print(len(normalized_text))

main()