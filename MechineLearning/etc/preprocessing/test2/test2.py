import pandas as pd
import numpy as np


df = pd.read_csv("./test/1_basic_preprocessed_reviews.csv")
df['review'].replace('', np.nan, inplace=True)
df.dropna(subset=['review'], inplace=True)


# import re
from pykospacing import spacing
from hanspell import spell_checker
from soynlp.normalizer import repeat_normalize


def spell_check_text(texts):
    corpus = []
    for sent in texts:
        try:
            # sent = re.sub(r'\s+', ' ', sent) #remove spaces
            # sent = re.sub(r"^\s+", '', sent) #remove space from start
            # sent = re.sub(r'\s+$', '', sent) #remove space from the end

            spaced_text = spacing(sent)
            spelled_sent = spell_checker.check(spaced_text)
            checked_sent = spelled_sent.checked
            normalized_sent = repeat_normalize(checked_sent)
            corpus.append(normalized_sent)
        except:
            corpus.append('')
    return corpus


df['review'] = spell_check_text(df['review'])
df.to_csv("./test/2_spell_preprocessed_reviews.csv", index=False)