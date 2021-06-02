import pandas as pd
import numpy as np


df = pd.read_csv("./csv/0_original_reviews.csv")
df['review'].replace('', np.nan, inplace=True)
df.dropna(subset=['review'], inplace=True)

reviews = df['review']
print(len(df))


import re


def clean_text(reviews):
    corpus = []
    for review in reviews:
        review = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣]', ' ', review) #remove space from the end
        review = re.sub(r'\s+', ' ', review) #remove spaces
        review = re.sub(r"^\s+", '', review) #remove space from start
        review = re.sub(r'\s+$', '', review) #remove space from the end
        corpus.append(review)
    return corpus


simple_preprocessed_corpus = clean_text(reviews)
print(len(simple_preprocessed_corpus))


simple_preprocessed_corpus_df = pd.DataFrame(simple_preprocessed_corpus)
simple_preprocessed_corpus_df.replace('', np.nan, inplace=True)
simple_preprocessed_corpus_df.dropna(subset=[0], inplace=True)
simple_preprocessed_corpus = simple_preprocessed_corpus_df[0]
print(len(simple_preprocessed_corpus))


# # from pykospacing import spacing
# from hanspell import spell_checker
# from soynlp.normalizer import repeat_normalize


# def custom_repeat_noramlize(sent):
#     temp = sent[:]
#     i = 0
#     while i < len(temp) - 1:
#       if temp[i] == temp[i + 1]:
#           temp = temp[:i] + temp[i + 1:]
#       else:
#           i += 1
#     return temp


# def spell_check_text(texts):
#     corpus = []
#     for i, sent in enumerate(texts):
#         print(i, sent[:50])
#         # spaced_text = spacing(str(sent))
#         spelled_sent = spell_checker.check(str(sent))
#         checked_sent = spelled_sent.checked
#         normalized_sent = custom_repeat_noramlize(checked_sent)
#         corpus.append(normalized_sent)
#     return corpus


# spell_preprocessed_reviews = spell_check_text(simple_preprocessed_corpus)


# df = pd.DataFrame(spell_preprocessed_reviews)
# df.to_csv("./csv/4_spell_preprocessed_corpus.csv", index=False)