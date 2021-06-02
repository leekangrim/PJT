import pandas as pd
import numpy as np


df = pd.read_csv("./test/2_spell_preprocessed_reviews.csv")
df['review'].replace('', np.nan, inplace=True)
df.dropna(subset=['review'], inplace=True)


import re


# 외래어 사전 로드
lownword_data = pd.read_table('./content/confused_loanwords.txt', sep='\t', header=None)
lines = lownword_data.values
lownword_map = {}
for line in lines:
    miss_spell = line[0]
    ori_word = line[1]
    lownword_map[miss_spell] = ori_word


# 맞춤법 검사
def spell_check_text(texts):
    corpus = []
    for sent in texts:
        for lownword in lownword_map:
            normalized_sent = re.sub(lownword, lownword_map[lownword], str(sent))
        corpus.append(normalized_sent)
    return corpus


df['review'] = spell_check_text(df['review'])
df.to_csv("./test/2_2_loanword_reviews.csv", index=False)