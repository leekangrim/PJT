# 외래어 사전 로드
import pandas as pd
lownword_data = pd.read_table('./content/confused_loanwords.txt', sep='\t', header=None)
lines = lownword_data.values
lownword_map = {}
for line in lines:
    miss_spell = line[0]
    ori_word = line[1]
    lownword_map[miss_spell] = ori_word


# 외래어 정규화
import re
def lownword_normalize(reviews):
    corpus = []
    for review in reviews:
        for lownword in lownword_map:
            normalized_sent = re.sub(lownword, lownword_map[lownword], str(review))
        corpus.append(normalized_sent)
    return corpus


import pandas as pd
filepath = '"./_reviews.csv"'
df = pd.read_csv(filepath)

df['review'] = lownword_normalize(df['review'])
df.to_csv("4" + filepath, index=False)