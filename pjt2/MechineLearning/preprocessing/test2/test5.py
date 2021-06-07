import pandas as pd


df = pd.read_csv("./reviews/4_stemming_reivews.csv")


from konlpy.tag import Mecab
mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")


stopwords = ['데/NNB', '좀/MAG', '수/NNB', '등/NNB']


def remove_stopword_text(text):
    corpus = []
    for sent in text:
        modi_sent = []
        for word in str(sent).split(' '):
            if word not in stopwords:
                modi_sent.append(word)
        corpus.append(' '.join(modi_sent))
    return corpus


df['review'] = remove_stopword_text(df['review'])
df.to_csv("./reviews/5_stopword_reivews.csv", index=False)