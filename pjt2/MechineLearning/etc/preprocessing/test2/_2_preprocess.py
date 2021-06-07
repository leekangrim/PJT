import pandas as pd
import numpy as np


df = pd.read_csv("./test/1_spell_preprocessed_reviews.csv")
df['spell_preprocessed_reviews'].replace('', np.nan, inplace=True)
df.dropna(subset=['spell_preprocessed_reviews'], inplace=True)


import re


def clean_text(reviews):
    corpus = []
    for review in reviews:
        review = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣]', ' ', str(review)) #remove space from the end
        review = re.sub(r'\s+', ' ', review) #remove spaces
        review = re.sub(r"^\s+", '', review) #remove space from start
        review = re.sub(r'\s+$', '', review) #remove space from the end
        corpus.append(review)
    return corpus


df['simple_preprocessed_review'] = clean_text(df['spell_preprocessed_reviews'])
df.to_csv("./test/2_simple_preprocessed_review.csv", index=False)