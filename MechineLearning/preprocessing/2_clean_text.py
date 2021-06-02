import re
def clean_text(reviews):
    corpus = []
    for review in reviews:
        # review = re.sub(r'[@%\\*=()/~#&\+á?\xc3\xa1\-\|\.\:\;\!\-\,\_\~\$\'\"]', '',str(review)) #remove punctuation
        # review = re.sub(r'\d+','', str(review))# remove number
        # review = re.sub(r'[a-z]','', str(review).lower())# remove number
        review = re.sub(r'<[^>]+>','',review) #remove Html tags
        # review = re.sub(r'\[[^>]+\]','',review) #remove Html tags
        # review = re.sub(r'\{[^>]+\}','',review) #remove Html tags
        # review = re.sub(r'\([^>]+\)','',review) #remove Html tags

        review = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣0-9\?\!\.\,\'\"]', ' ', str(review)) #한글, 숫자, 기본 구두점 제외

        review = re.sub(r'\s+', ' ', str(review)) #remove spaces
        review = re.sub(r"^\s+", '', str(review)) #remove space from start
        review = re.sub(r'\s+$', '', str(review)) #remove space from the end
        corpus.append(review)
    return corpus


import pandas as pd
filepath = '"./_reviews.csv"'
df = pd.read_csv(filepath)

df['review'] = clean_text(df['review'])
df.to_csv("2" + filepath, index=False)