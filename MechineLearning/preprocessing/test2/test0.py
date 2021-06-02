import pandas as pd
import numpy as np


df = pd.read_csv("./test/original_reviews.csv")
df['review'].replace('', np.nan, inplace=True)
df.dropna(subset=['review'], inplace=True)


import re


def clean_text(reviews):
    corpus = []
    for review in reviews:
        review = re.sub(r'\s+', ' ', str(review)) #remove spaces
        review = re.sub(r"^\s+", '', review) #remove space from start
        review = re.sub(r'\s+$', '', review) #remove space from the end
        corpus.append(review)
    return corpus


df['review'] = clean_text(df['review'])
df.to_csv("./test/0_remove_spaces_reviews.csv", index=False)