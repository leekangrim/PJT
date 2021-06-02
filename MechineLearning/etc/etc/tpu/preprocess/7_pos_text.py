from konlpy.tag import Mecab # pip install konlpy; pip install mecab_python-0.996_ko_0.9.2_msvc-cp37-cp37m-win_amd64
mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")
significant_tags = ['NNG', 'NNP', 'NNB', 'VV', 'VA', 'VX', 'MAG', 'MAJ', 'XSV', 'XSA']
def pos_text(reviews):
    corpus = []
    for review in reviews:
        pos_tagged = ''
        for lex, tag in mecab.pos(str(review)):
            if tag in significant_tags:
                pos_tagged += lex + '/' + tag + ' '
        corpus.append(pos_tagged.rstrip())
    return corpus


import pandas as pd
filepath = '"./_reviews.csv"'
df = pd.read_csv(filepath)

df['review'] = pos_text(df['review'])
df.to_csv("7" + filepath, index=False)