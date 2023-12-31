# -*- coding: utf-8 -*-
"""Offense.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OcHN_KJBChfxZm2CzU9SAD0Ew21U2-Rv
"""

import pandas as pd
import numpy as np
train_df = pd.read_csv('/content/train.csv')
test_df = pd.read_csv('/content/valid.csv')
valid_df = pd.read_csv('/content/valid.csv')
print("Train Dataset:")
print(train_df.head())
print("\nValid Dataset:")
print(valid_df.head())
print("\nTest Dataset:")
print(test_df.head())
train_label_counts = train_df['label'].value_counts()
valid_label_counts = valid_df['label'].value_counts()
test_label_counts = test_df['label'].value_counts()
print("\nTrain Dataset Label Distribution:")
print(train_label_counts)
print("\nValid Dataset Label Distribution:")
print(valid_label_counts)
print("\nTest Dataset Label Distribution:")
print(test_label_counts)

import re
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

# Optional: Download NLTK data
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
def preprocess_text(text):
    # Tokenization: Split text into words or tokens
    words = word_tokenize(text)
    # Lowercasing: Convert all text to lowercase
    words = [word.lower() for word in words]
    # Remove special characters, punctuation, and numbers using regex
    words = [re.sub(r'[^a-zA-Z]', '', word) for word in words]
    # Optional: Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    preprocessed_text = ' '.join(words)
    return preprocessed_text

# Apply text preprocessing to your dataframes
train_df['tweet'] = train_df['tweet'].apply(preprocess_text)
valid_df['tweet'] = valid_df['tweet'].apply(preprocess_text)
test_df['tweet'] = test_df['tweet'].apply(preprocess_text)

# Label Encoding: Encode the labels into numerical format
label_encoder = LabelEncoder()
train_df['label'] = label_encoder.fit_transform(train_df['label'])
valid_df['label'] = label_encoder.transform(valid_df['label'])
test_df['label'] = label_encoder.transform(test_df['label'])

# Display the preprocessed data
print("Preprocessed Train Dataset:")
print(train_df.head())
print("\nPreprocessed Valid Dataset:")
print(valid_df.head())
print("\nPreprocessed Test Dataset:")
print(test_df.head())

import matplotlib.pyplot as plt
from wordcloud import WordCloud
label_counts = train_df['label'].value_counts()

# Plot label distribution
plt.figure(figsize=(6, 6))
plt.bar(label_counts.index, label_counts.values, tick_label=['Non-Offensive', 'Offensive'])
plt.title('Label Distribution in Training Dataset')
plt.xlabel('Label')
plt.ylabel('Count')
plt.show()
all_text = " ".join(train_df['tweet'])
# Create a WordCloud object
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)

# Display the WordCloud
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.title('Word Cloud of Common Terms in Tweets')
plt.axis('off')
plt.show()

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer(max_features=5000,
                                   stop_words='english',
                                   ngram_range=(1, 2))

# Fit and transform the vectorizer on the training data
X_train_tfidf = tfidf_vectorizer.fit_transform(train_df['tweet'])

# Transform the validation and test data using the same vectorizer
X_valid_tfidf = tfidf_vectorizer.transform(valid_df['tweet'])
X_test_tfidf = tfidf_vectorizer.transform(test_df['tweet'])

# Display the shape of the transformed data
print("Shape of Training Data (TF-IDF):", X_train_tfidf.shape)
print("Shape of Validation Data (TF-IDF):", X_valid_tfidf.shape)
print("Shape of Test Data (TF-IDF):", X_test_tfidf.shape)

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
# Fit the vectorizer on the training data
tfidf_vectorizer.fit(train_df['tweet'])

# Transform the training and test data
X_train_tfidf = tfidf_vectorizer.transform(train_df['tweet'])
X_test_tfidf = tfidf_vectorizer.transform(test_df['tweet'])
X_valid_tfidf = tfidf_vectorizer.transform(valid_df['tweet'])
from sklearn.naive_bayes import MultinomialNB

print(X_train_tfidf.shape)
classifier = MultinomialNB()

# Fit the classifier on the TF-IDF features and labels
classifier.fit(X_train_tfidf, train_df['label'])

# Make predictions on the test data
predictions = classifier.predict(X_test_tfidf)

# Calculate and print the accuracy
accuracy = accuracy_score(test_df['label'], predictions)
print("Test Accuracy:", accuracy)

from sklearn.ensemble import RandomForestClassifier

# Create a Random Forest classifier instance
rf_classifier = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=42)

# Fit the classifier on the training data
rf_classifier.fit(X_train_tfidf, train_df['label'])

from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# Predict labels on the validation set
valid_predictions = rf_classifier.predict(X_valid_tfidf)

# Evaluate the model
accuracy = accuracy_score(valid_df['label'], valid_predictions)
report = classification_report(valid_df['label'], valid_predictions)
confusion = confusion_matrix(valid_df['label'], valid_predictions)

print("Accuracy:", accuracy)
print("Classification Report:\n", report)
print("Confusion Matrix:\n", confusion)

# Transform the test data using the TF-IDF vectorizer
X_test_tfidf = tfidf_vectorizer.transform(test_df['tweet'])

# Predict labels on the test set
test_predictions = rf_classifier.predict(X_test_tfidf)
combined_train_data = pd.concat([train_df, valid_df], axis=0)
# Transform the combined training data using the TF-IDF vectorizer
X_combined_tfidf = tfidf_vectorizer.transform(combined_train_data['tweet'])
from sklearn.ensemble import RandomForestClassifier

# Create a Random Forest classifier instance
rf_classifier = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=42)

# Fit the classifier on the combined training data
rf_classifier.fit(X_combined_tfidf, combined_train_data['label'])

# Predict labels on the validation set during training
valid_predictions = rf_classifier.predict(X_valid_tfidf)

# Evaluate the model's performance on the validation set
accuracy = accuracy_score(valid_df['label'], valid_predictions)
report = classification_report(valid_df['label'], valid_predictions)
confusion = confusion_matrix(valid_df['label'], valid_predictions)

print("Accuracy during training:", accuracy)
print("Classification Report during training:\n", report)
print("Confusion Matrix during training:\n", confusion)

import joblib

#save the model
joblib.dump(rf_classifier, 'text classifier_model.pkl')

# Preprocess the test data
test_df['tweet'] = test_df['tweet'].apply(preprocess_text)

#Transform the test data using the same TF-IDF vectoriezer
X_test_tfidf = tfidf_vectorizer.transform(test_df['tweet'])

test_predictions = rf_classifier.predict(X_test_tfidf)

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Calculate accuracy
accuracy = accuracy_score(test_df['label'], test_predictions)

# Generate a classification report
report = classification_report(test_df['label'], test_predictions)

# Generate a confusion matrix
confusion = confusion_matrix(test_df['label'], test_predictions)

print("Accuracy on the test dataset:", accuracy)
print("Classification Report on the test dataset:\n", report)
print("Confusion Matrix on the test dataset:\n", confusion)

pip install Flask

