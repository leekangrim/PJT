import pandas as pd


df = pd.read_csv("./csv/2_cleaned_reviews.csv")
cleaned_reviews = df.values


# 구두점 제거
import re


def clean_text(texts):
    corpus = []
    for i in range(0, len(texts)):
        # review = re.sub(r'[@%\\*=()/~#&\+á?\xc3\xa1\-\|\.\:\;\!\-\,\_\~\$\'\"]', '',str(texts[i])) #remove punctuation
        # review = re.sub(r'\d+','', review)# remove number
        # review = review.lower() #lower case
        # review = re.sub(r'\s+', ' ', review) #remove extra space
        # review = re.sub(r'<[^>]+>','',review) #remove Html tags
        review = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣]', ' ', str(texts[i])) #remove space from the end
        review = re.sub(r'\s+', ' ', review) #remove spaces
        review = re.sub(r"^\s+", '', review) #remove space from start
        review = re.sub(r'\s+$', '', review) #remove space from the end
        corpus.append(review)
    return corpus


basic_preprocessed_reviews = []
for cleaned_review in cleaned_reviews:
    basic_preprocessed_reviews.append(clean_text(cleaned_review))


df = pd.DataFrame(basic_preprocessed_reviews)
df.to_csv("./csv/3_basic_preprocessed_reviews.csv", index=False)