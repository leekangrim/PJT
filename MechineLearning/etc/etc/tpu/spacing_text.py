import pandas as pd
total_data = pd.read_csv('cleansing_data.csv')
print(len(total_data))


import re
from pykospacing import spacing 
# from hanspell import spell_checker
# from soynlp.normalizer import repeat_normalize
def spacing_text(reviews):
    corpus = []
    for review in reviews:
        # review = re.sub(r'\s', '', str(review)) #remove spaces
        review = spacing(str(review))
        # review = spell_checker.check(str(review))
        # review = review.checked
        # review = repeat_normalize(str(review))
        corpus.append(review)
    return corpus


total_data['review'] = spacing_text(total_data['review'])
print(len(total_data))
total_data.to_csv('spacing_data2.csv', index=False)