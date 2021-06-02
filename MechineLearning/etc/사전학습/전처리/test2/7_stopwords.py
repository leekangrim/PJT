import pandas as pd
import numpy as np


df = pd.read_csv("./csv/6_stemming_corpus.csv")
print(len(df))

df.replace('', np.nan, inplace=True)
df = df.dropna()
print(len(df))

stemming_corpus = df['0']


stopwords = ['데/NNB', '좀/MAG', '수/NNB', '등/NNB']


def remove_stopword_text(text):
    corpus = []
    for sent in text:
        modi_sent = []
        for word in sent.split(' '):
            if word not in stopwords:
                modi_sent.append(word)
        corpus.append(' '.join(modi_sent))
    return corpus


removed_stopword_corpus = remove_stopword_text(stemming_corpus)


df = pd.DataFrame(removed_stopword_corpus)
df.to_csv("./csv/7_removed_stopword_corpus.csv", index=False)