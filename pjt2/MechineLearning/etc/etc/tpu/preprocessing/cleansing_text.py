import pandas as pd
total_data = pd.read_csv('origin_data.csv')
print(len(total_data))


import re
def clean_text(reviews):
    corpus = []
    for review in reviews:
        # review = re.sub(r'[@%\\*=()/~#&\+á?\xc3\xa1\-\|\.\:\;\!\-\,\_\~\$\'\"]', '',str(review)) #remove punctuation
        # review = re.sub(r'\d+','', str(review))# remove number
        # review = re.sub(r'[a-z]','', str(review).lower())# remove number
        review = re.sub('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+)', '', str(review)) # remove e-mail
        review = re.sub('(http|ftp|https)://(?:[-\w.]|(?:\da-fA-F]{2}))+', '', review) # remove url
        review = re.sub(r'<[^>]+>','',review) #remove Html tags
        review = re.sub(r'\[[^>]+\]','',review) #remove Html tags
        review = re.sub(r'\{[^>]+\}','',review) #remove Html tags
        review = re.sub(r'\([^>]+\)','',review) #remove Html tags

        review = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣0-9a-zA-Z?\!\.\,\'\"]', ' ', str(review)) # 한글, 숫자, 알파벳, 기본구두점 제외

        review = re.sub(r'\s+', ' ', str(review)) #remove spaces
        review = re.sub(r"^\s+", '', str(review)) #remove space from start
        review = re.sub(r'\s+$', '', str(review)) #remove space from the end
        corpus.append(review)
    return corpus


total_data['review'] = clean_text(total_data['review'])
print(len(total_data))
total_data.to_csv('clean_data.csv', index=False)