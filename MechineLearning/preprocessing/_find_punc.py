import pandas as pd
df = pd.read_csv("./_reviews.csv")


import re
def find_punc(reviews):
    punc = set()
    for review in reviews:
        punc.update(re.findall('[^ㄱ-ㅎㅏ-ㅣ가-힣]', review))
    return punc


s = set()
for ps in find_punc(df['review']):
    for p in ps:
        s.add(p)
for e in s:
    print(f"'{e}',")