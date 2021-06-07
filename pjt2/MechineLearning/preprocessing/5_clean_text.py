import re
def clean_text(reviews):
    corpus = []
    for review in reviews:
        review = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣]', ' ', str(review)) #remove space from the end

        review = re.sub(r'\s+', ' ', str(review)) #remove spaces
        review = re.sub(r"^\s+", '', str(review)) #remove space from start
        review = re.sub(r'\s+$', '', str(review)) #remove space from the end
        corpus.append(review)
    return corpus


import pandas as pd
filepath = '"./_reviews.csv"'
df = pd.read_csv(filepath)

df['review'] = clean_text(df['review'])
df.to_csv("5" + filepath, index=False)