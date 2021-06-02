import pandas as pd


df = pd.read_csv("./reviews/2_spell_preprocessed_reviews.csv")


from konlpy.tag import Mecab
mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")


significant_tags = ['NNG', 'NNP', 'NNB', 'VV', 'VA', 'VX', 'MAG', 'MAJ', 'XSV', 'XSA']


def pos_text(texts):
    corpus = []
    for sent in texts:
        pos_tagged = ''
        for lex, tag in mecab.pos(str(sent)):
            if tag in significant_tags:
                pos_tagged += lex + '/' + tag + ' '
        corpus.append(pos_tagged.rstrip())
    return corpus


df['review'] = pos_text(df['review'])
df.to_csv("./reviews/3_pos_tagged_reivews.csv", index=False)