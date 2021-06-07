stopwords = ['데/NNB', '좀/MAG', '수/NNB', '등/NNB']
def clean_stopword_text(reviews):
    corpus = []
    for review in reviews:
        modi_sent = []
        for word in str(review).split(' '):
            if word not in stopwords:
                modi_sent.append(word)
        corpus.append(' '.join(modi_sent))
    return corpus


import pandas as pd
filepath = '"./_reviews.csv"'
df = pd.read_csv(filepath)

df['review'] = clean_stopword_text(df['review'])
df.to_csv("9" + filepath, index=False)