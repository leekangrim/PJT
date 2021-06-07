import re
from pykospacing import spacing 
from hanspell import spell_checker
from soynlp.normalizer import repeat_normalize
from konlpy.tag import Mecab # pip install konlpy; pip install mecab_python-0.996_ko_0.9.2_msvc-cp37-cp37m-win_amd64


def clean_space(reviews):
    corpus = []
    for review in reviews:
        # review = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣]', ' ', str(review)) #remove space from the end
        review = re.sub(r'\s+', ' ', str(review)) #remove spaces
        review = re.sub(r"^\s+", '', str(review)) #remove space from start
        review = re.sub(r'\s+$', '', str(review)) #remove space from the end
        corpus.append(review)
    return corpus


def spell_check(reviews):
    corpus = []
    for review in reviews:
        spaced_text = spacing(str(review))
        spelled_sent = spell_checker.check(str(spaced_text))
        checked_sent = spelled_sent.checked
        normalized_sent = repeat_normalize(str(checked_sent))
        corpus.append(normalized_sent)
    return corpus


def clean_text(reviews):
    corpus = []
    for review in reviews:
        review = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣]', ' ', str(review)) #remove space from the end

        review = re.sub(r'\s+', ' ', str(review)) #remove spaces
        review = re.sub(r"^\s+", '', str(review)) #remove space from start
        review = re.sub(r'\s+$', '', str(review)) #remove space from the end
        corpus.append(review)
    return corpus


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


def preprocess(reviews):
    corpus = clean_space(reviews)
    print(corpus)
    corpus = spell_check(corpus)
    print(corpus)
    corpus = clean_text(corpus)
    print(corpus)
    corpus = pos_text(corpus)
    print(corpus)
    corpus = stemming_text(corpus)
    print(corpus)
    corpus = clean_stopword_text(corpus)
    print(corpus)
    return corpus
