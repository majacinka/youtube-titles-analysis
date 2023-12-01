# pip install pandas textstat textblob nltk

import pandas as pd
import textstat
import nltk
from textblob import TextBlob
from nltk.corpus import stopwords

# Download NLTK stopwords
nltk.download('stopwords')

# Load the set of Enlgish stopwords
stop_words = set(stopwords.words('english'))

# Load the CSV file into a DataFrame
df = pd.read_csv('yd.csv').copy()  # Replace with your file path

"""# check and remove pontential duplicates 
duplicates = df_raw.duplicated(subset='title', keep='first')
print(f"Duplicate titles: {df_raw[duplicates]}")
df = df_raw.drop_duplicates(subset='title', keep='first')
"""
# Extract word, character and similar counts
def count_digits(s):
  return sum(1 for char in s if char.isdigit())

def count_uppercase(s):
  return sum(1 for char in s if char.isupper())

def count_lowercase(s):
  return sum(1 for char in s if char.islower())

def count_words(s):
  return len(s.split())

def count_question_marks(s):
  return s.count('?')

def has_question_marks(s):
  return s.count('?') > 0

def count_dollars(s):
  return s.count('$') > 0

# Calculate readability of the title
def calculate_readability(title):
  return textstat.flesch_reading_ease(title)

# Function to Calculate sentiment polarity
def calculate_sentiment(title):
  return TextBlob(title).sentiment.polarity

# Count stopwords in a string
def count_stopwords(s):
  words = s.split()
  return sum(word.lower() in stop_words for word in words)

def contains_digits(s):
    return any(char.isdigit() for char in s)

def percentage_uppercase_words(title):
  words = title.split()
  uppercase_count = sum(1 for word in words if word.istitle())
  percentage =  (uppercase_count / len(words)) * 100 if words else 0
  if percentage == 100:
        return 100
  return int(percentage // 20) * 20

df['title_length'] = df['title'].apply(len)
df['uppercase_count'] = df['title']. apply(count_uppercase)
df['lowercase_count'] = df['title'].apply(count_lowercase)
df['digit_count'] = df['title'].apply(count_digits)
df['word_count'] = df['title'].apply(count_words)
df['question_mark_count'] = df['title'].apply(count_question_marks)
df['flesch_reading_ease'] = df['title'].apply(calculate_readability)
df['sentiment_polarity'] = df['title'].apply(calculate_sentiment)
df['stopword_count'] = df['title'].apply(count_stopwords)
df['has_currency'] = df['title'].apply(count_dollars)
df['has_qmark'] = df['title'].apply(has_question_marks)
df['has_digit'] = df['title'].apply(contains_digits)
df['percentage_uppercase_words'] = df['title']. apply(percentage_uppercase_words)

# Optionally, save the updated DataFrame back to a CSV file
df.to_csv('data_3.csv', index=False)  # Replace with your desired file path
