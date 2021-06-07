from pykospacing import spacing
from hanspell import spell_checker
from soynlp.normalizer import repeat_normalize

import pandas as pd


df = pd.read_csv("./csv/3_basic_preprocessed_reviews.csv")
basic_preprocessed_reviews = df.values


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
        spaced_text = spacing(str(sent))
        spelled_sent = spell_checker.check(spaced_text)
        checked_sent = spelled_sent.checked
        normalized_sent = repeat_normalize(checked_sent)
        for lownword in lownword_map:
            normalized_sent = normalized_sent.replace(lownword, lownword_map[lownword])
        corpus.append(normalized_sent)
    return corpus


spell_preprocessed_reviews = []
for basic_preprocessed_review in basic_preprocessed_reviews:
    spell_preprocessed_reviews.append(spell_check_text(basic_preprocessed_review))


df = pd.DataFrame(spell_preprocessed_reviews)
df.to_csv("./csv/4_spell_preprocessed_corpus.csv", index=False)