import pandas as pd


df = pd.read_csv("./csv/1_sentence_tokenized_reviews.csv")
sentence_tokenized_reviews = df.values


# 구두점 정제
import re


punct = "/-'?!.,#$%\'()*+-/:;<=>@[\\]^_`{|}~" + '""“”’' + '∞θ÷α•à−β∅³π‘₹´°£€\×™√²—–&'
punct_mapping = {"‘": "'", "₹": "e", "´": "'", "°": "", "€": "e", "™": "tm", "√": " sqrt ", "×": "x", "²": "2", "—": "-", "–": "-", "’": "'", "_": "-", "`": "'", '“': '"', '”': '"', '“': '"', "£": "e", '∞': 'infinity', 'θ': 'theta', '÷': '/', 'α': 'alpha', '•': '.', 'à': 'a', '−': '-', 'β': 'beta', '∅': '', '³': '3', 'π': 'pi', }


def clean_punc(text, punct, mapping):
    for p in mapping:
        text = re.sub(p, mapping[p], text)
    
    # for p in punct:
    #     text = re.sub(p, f' {p} ', text)
    
    specials = {'\u200b': ' ', '…': ' ... ', '\ufeff': '', 'करना': '', 'है': ''}
    for s in specials:
        text = re.sub(s, specials[s], text)
    
    return text.strip()


cleaned_reviews = []
for sentence_tokenized_review in sentence_tokenized_reviews:

    cleaned_review = []
    for sent in sentence_tokenized_review:
        cleaned_review.append(clean_punc(str(sent), punct, punct_mapping))

    cleaned_reviews.append(cleaned_review)


df = pd.DataFrame(sentence_tokenized_reviews)
df.to_csv("./csv/2_cleaned_reviews.csv", index=False)