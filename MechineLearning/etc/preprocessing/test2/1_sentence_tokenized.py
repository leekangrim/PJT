import pandas as pd
import numpy as np


df = pd.read_csv("./csv/0_original_reviews.csv")
df['review'].replace('', np.nan, inplace=True)
df.dropna(subset=['review'], inplace=True)
reviews = df['review']


# 문장 분리
import kss
import re


sentence_tokenized_reviews = []
for review in reviews:

    sentence_tokenized_text = []

    review = re.sub(r'\s+', ' ', review) #remove spaces
    review = re.sub(r"^\s+", '', review) #remove space from start
    review = re.sub(r'\s+$', '', review) #remove space from the end

    for sent in kss.split_sentences(review):
        sentence_tokenized_text.append(sent.strip())
    
    sentence_tokenized_reviews.append(sentence_tokenized_text)


df = pd.DataFrame(sentence_tokenized_reviews)
df.to_csv("./csv/1_sentence_tokenized_reviews.csv", index=False)