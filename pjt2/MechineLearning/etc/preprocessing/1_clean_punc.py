import re
punct = "/-'?!.,#$%\'()*+-/:;<=>@[\\]^_`{|}~" + '""“”’' + '∞θ÷α•à−β∅³π‘₹´°£€\×™√²—–&'
punct_mapping = {
    "‘": "'", "₹": "e", "´": "'", "°": "", "€": "e", "™": "tm", "√": " sqrt ", "×": "x", "²": "2", "—": "-", "–": "-", "’": "'", "_": "-", "`": "'", '“': '"', '”': '"', '“': '"', "£": "e", '∞': 'infinity', 'θ': 'theta', '÷': '/', 'α': 'alpha', '•': '.', 'à': 'a', '−': '-', 'β': 'beta', '∅': '', '³': '3', 'π': 'pi', 
}
def clean_punc(reviews, punct, mapping):
    corpus = []
    for review in reviews:
        for p in mapping:
            review = re.sub(p, mapping[p], str(review))
        
        for p in punct:
            review = re.sub(p, f' {p} ', str(review))
        
        specials = {'\u200b': ' ', '…': ' ... ', '\ufeff': '', 'करना': '', 'है': ''}
        for s in specials:
            review = re.sub(s, specials[s], str(review))
        
        corpus.append(review.strip())
    return corpus


import pandas as pd
filepath = '"./_reviews.csv"'
df = pd.read_csv(filepath)

df['review'] = clean_punc(df['review'])
df.to_csv("1" + filepath, index=False)