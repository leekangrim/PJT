import re
from konlpy.tag import Mecab


def preprocess(reviews):
    mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")
    stopwords = {
        '도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임', '게',
        '의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다'
    }

    corpus = []
    for review in reviews:
        review = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣]', '', str(review))
        review = mecab.morphs(review) # 토큰화
        review = [word for word in review if not word in stopwords] # 불용어 제거
        corpus.append(review)
    return corpus