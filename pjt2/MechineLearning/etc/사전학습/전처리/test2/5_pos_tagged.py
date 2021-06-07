import pandas as pd
import numpy as np


df = pd.read_csv("./csv/4_spell_preprocessed_corpus.csv")
print(len(df))

df.replace('', np.nan, inplace=True)
df = df.dropna()
print(len(df))

spell_preprocessed_corpus = df['0']



from konlpy.tag import Mecab
mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")


significant_tags = ['NNG', 'NNP', 'NNB', 'VV', 'VA', 'VX', 'MAG', 'MAJ', 'XSV', 'XSA']


def pos_text(texts):
    corpus = []
    for i, sent in enumerate(texts):
        print(i, sent[:20])
        pos_tagged = ''
        for lex, tag in mecab.pos(sent):
            if tag in significant_tags:
                pos_tagged += lex + '/' + tag + ' '
        corpus.append(pos_tagged.rstrip())
    return corpus


pos_tagged_corpus = pos_text(spell_preprocessed_corpus)


df = pd.DataFrame(pos_tagged_corpus)
df.to_csv("./csv/5_pos_tagged_corpus.csv", index=False)