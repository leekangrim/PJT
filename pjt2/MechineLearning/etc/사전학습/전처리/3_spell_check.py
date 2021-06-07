# pip install git+https://github.com/haven-jeon/PyKoSpacing.git; pip install git+https://github.com/ssut/py-hanspell.git; pip install soynlp
from pykospacing import spacing 
from hanspell import spell_checker
from soynlp.normalizer import repeat_normalize
def spell_check(reviews):
    corpus = []
    for review in reviews:
        review = spacing(str(review))
        # review = spell_checker.check(str(review))
        review = review.checked
        review = repeat_normalize(str(review))
        corpus.append(review)
    return corpus


import pandas as pd
filepath = '"./_reviews.csv"'
df = pd.read_csv(filepath)

df['review'] = spell_check(df['review'])
df.to_csv("3" + filepath, index=False)