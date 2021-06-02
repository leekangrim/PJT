from os import error
import re
from konlpy.tag import Mecab
from soynlp.normalizer import repeat_normalize
mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")
stopwords = [
    '의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다',
    '것','라고','에게','라면','게','을','이라','라니','있다','아','랑','쯤된','에서','에선','어','이지만','으로나','때','때는','때라면','때라서','라','이다','있',
    '죠','고','니','로','있','같','어서','어요','는데','습니다','면서'
]
def simple_preprocess(reviews):
    corpus = []
    for review in reviews:
        review = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣]', '', str(review))
        review = mecab.morphs(review) # 토큰화
        review = [word for word in review if not word in stopwords] # 불용어 제거
        corpus.append(review)
    return corpus


def complex_preprocess(reviews):
    
    reviews = spell_check_text(reviews)
    reviews = clean_text(reviews)
    reviews = custom_pos_text(reviews)
    reviews = clean_stopword_text(reviews)

    return reviews


def opensource_preprocess(reviews):
    
    reviews = spell_check_text(reviews)
    reviews = clean_text(reviews)
    reviews = pos_text(reviews)
    reviews = stemming_text(reviews)
    reviews = clean_stopword_text(reviews)

    return reviews



def custom_preprocess(reviews):

    reviews = clean_text(reviews)
    reviews = custom_nomalize(reviews)
    reviews = custom_pos_text(reviews)
    reviews = clean_stopword_text(reviews)

    return reviews


# 정제
import re
def clean_punc(reviews):
    corpus = []
    for review in reviews:

        review = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣"]', ' ', str(review)) #한글, 숫자, 기본 구두점 제외
        
        corpus.append(review)
    return corpus


def cleansing(text):
    pattern = "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+)"  # e-mail 주소 제거
    text = re.sub(pattern=pattern, repl=" ", string=text)

    pattern = "(http|ftp|https)://(?:[-\w.]|(?:\da-fA-F]{2}))+"  # url 제거
    text = re.sub(pattern=pattern, repl=" ", string=text)

    pattern = "([ㄱ-ㅎㅏ-ㅣ])+"  # 한글 자음, 모음 제거
    text = re.sub(pattern=pattern, repl=" ", string=text)

    # ㄷ, ㅋ, ㅎ, ㅜ, ㅠ

    pattern = "<[^>]*>"  # html tag 제거
    text = re.sub(pattern=pattern, repl=" ", string=text)

    pattern = "[\r|\n]"  # \r, \n 제거
    text = re.sub(pattern=pattern, repl=" ", string=text)

    pattern = "[^\w\s]"  # 특수기호 제거
    text = re.sub(pattern=pattern, repl=" ", string=text)

    pattern = re.compile(r"\s+")  # 이중 space 제거
    text = re.sub(pattern=pattern, repl=" ", string=text)

    # review = re.sub(r"^\s+", '', str(review)) #remove space from start
    # review = re.sub(r'\s+$', '', str(review)) #remove space from the end

    return text


import re
def clean_space(reviews):
    corpus = []
    for review in reviews:
        review = re.sub(r'\s+', ' ', str(review)) #remove spaces
        review = re.sub(r"^\s+", '', str(review)) #remove space from start
        review = re.sub(r'\s+$', '', str(review)) #remove space from the end
        corpus.append(review)
    return corpus


import re
def clean_text(reviews):
    corpus = []
    for review in reviews:
        review = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣"]', ' ', str(review)) #한글, 숫자, 기본 구두점 제외

        review = re.sub(r'\s+', ' ', str(review)) #remove spaces
        review = re.sub(r"^\s+", '', str(review)) #remove space from start
        review = re.sub(r'\s+$', '', str(review)) #remove space from the end
        corpus.append(review)
    return corpus


# 외래어 사전 로드
import pandas as pd
lownword_data = pd.read_table('./loanwords.txt', sep='\t', header=None)
lines = lownword_data.values
lownword_map = {}
for line in lines:
    miss_spell = line[0]
    ori_word = line[1]
    lownword_map[miss_spell] = ori_word


def custom_repeat_noramlize(review):
    sent = review[:]
    i = 0
    while i < len(sent) - 1:
        if sent[i] == sent[i + 1]:
            sent = sent[:i] + sent[i + 1:]
        else:
            i += 1
    return sent

# total_data['cleaned'] = clean_text(total_data['review'])
# for sent in total_data['cleaned'][:10]:
#     print(sent)


from soynlp.normalizer import repeat_normalize
def custom_nomalize(reviews):
    corpus = []
    for review in reviews:
        review = custom_repeat_noramlize(review)
        # review = repeat_normalize(review)
        # for lownword in lownword_map:
        #     review = re.sub(lownword, lownword_map[lownword], review)
        corpus.append(review)
    return corpus

# total_data['nomalized'] = nomalize(total_data['cleaned'])
# for sent in total_data['nomalized'][:10]:
#     print(sent)


# 맞춤법 검사
from pykospacing import spacing
from hanspell import spell_checker
from soynlp.normalizer import repeat_normalize
def spell_check_text(reviews):
    corpus = []
    for review in reviews:
        try:
            review = spacing(str(review))
        except:
            print(review)

        try:
            review = spell_checker.check(str(review))
            review = review.checked
        except:
            print(review)

        review = repeat_normalize(str(review))
        
        # for lownword in lownword_map:
        #     review = str(review).replace(lownword, lownword_map[lownword])
        corpus.append(review)
    return corpus


from konlpy.tag import Mecab # pip install konlpy; pip install mecab_python-0.996_ko_0.9.2_msvc-cp37-cp37m-win_amd64
mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")
def custom_pos_text(reviews):
    corpus = []
    for review in reviews:
        pos_tagged = ''
        for lex, tag in mecab.pos(str(review)):
            pos_tagged += lex + '/' + tag + ' '
        corpus.append(pos_tagged.rstrip())
    return corpus

# total_data['tokenized'] = my_pos_text(total_data['nomalized'])
# for sent in total_data['tokenized'][:10]:
#     print(sent)


from konlpy.tag import Mecab # pip install konlpy; pip install mecab_python-0.996_ko_0.9.2_msvc-cp37-cp37m-win_amd64
mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")
significant_tags = ['NNG', 'NNP', 'NNB', 'VV', 'VA', 'VX', 'MAG', 'MAJ', 'XSV', 'XSA'] # 'EC'
def pos_text(reviews):
    corpus = []
    for review in reviews:
        pos_tagged = ''
        for lex, tag in mecab.pos(str(review)):
            if tag in significant_tags:
                pos_tagged += lex + '/' + tag + ' '
        review = pos_tagged.rstrip()
        corpus.append(review)
    return corpus

# total_data['tokenized'] = pos_text(total_data['nomalized'])
# for sent in total_data['tokenized'][:10]:
#     print(sent)


import re
p1 = re.compile('[가-힣A-Za-z0-9]+/NN. [가-힣A-Za-z0-9]+/XS.')
p2 = re.compile('[가-힣A-Za-z0-9]+/NN. [가-힣A-Za-z0-9]+/XSA [가-힣A-Za-z0-9]+/VX')
p3 = re.compile('[가-힣A-Za-z0-9]+/VV')
p4 = re.compile('[가-힣A-Za-z0-9]+/VX')
def stemming_text(reviews):
    corpus = []
    for review in reviews:
        ori_sent = str(review)
        mached_terms = re.findall(p1, ori_sent)
        for terms in mached_terms:
            ori_terms = terms
            modi_terms = ''
            for term in terms.split(' '):
                lemma = term.split('/')[0]
                tag = term.split('/')[-1]
                modi_terms += lemma
            modi_terms += '다/VV'
            ori_sent = ori_sent.replace(ori_terms, modi_terms)
        
        mached_terms = re.findall(p2, ori_sent)
        for terms in mached_terms:
            ori_terms = terms
            modi_terms = ''
            for term in terms.split(' '):
                lemma = term.split('/')[0]
                tag = term.split('/')[-1]
                if tag != 'VX':
                    modi_terms += lemma
            modi_terms += '다/VV'
            ori_sent = ori_sent.replace(ori_terms, modi_terms)

        mached_terms = re.findall(p3, ori_sent)
        for terms in mached_terms:
            ori_terms = terms
            modi_terms = ''
            for term in terms.split(' '):
                lemma = term.split('/')[0]
                tag = term.split('/')[-1]
                modi_terms += lemma
            if '다' != modi_terms[-1]:
                modi_terms += '다'
            modi_terms += '/VV'
            ori_sent = ori_sent.replace(ori_terms, modi_terms)

        mached_terms = re.findall(p4, ori_sent)
        for terms in mached_terms:
            ori_terms = terms
            modi_terms = ''
            for term in terms.split(' '):
                lemma = term.split('/')[0]
                tag = term.split('/')[-1]
                modi_terms += lemma
            if '다' != modi_terms[-1]:
                modi_terms += '다'
            modi_terms += '/VV'
            ori_sent = ori_sent.replace(ori_terms, modi_terms)
        corpus.append(ori_sent)
    return corpus

# total_data['stemmed'] = stemming_text(total_data['tokenized'])
# for sent in total_data['stemmed'][:100]:
#     print(sent)


stopwords = ['데/NNB', '좀/MAG', '수/NNB', '등/NNB']
def clean_stopword_text(reviews):
    corpus = []
    for review in reviews:
        modi_sent = []
        for word in str(review).split(' '):
            if word not in stopwords:
                modi_sent.append(word)
        corpus.append(' '.join(modi_sent))
    return corpus

# # total_data['stopword'] = clean_stopword_text(total_data['stemmed'])
# total_data['stopword'] = clean_stopword_text(total_data['tokenized'])
# for sent in total_data['stopword'][:10]:
#     print(sent)