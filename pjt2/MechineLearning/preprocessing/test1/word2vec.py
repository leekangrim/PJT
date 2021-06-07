# import urllib.request
# urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings.txt", filename="ratings.txt")

import pandas as pd
import matplotlib.pyplot as plt
from konlpy.tag import Okt
from gensim.models.word2vec import Word2Vec

train_data = pd.read_table('ratings.txt')

train_data['document'] = train_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")

train_data = train_data.dropna(how = 'any') # Null 값이 존재하는 행 제거

# 불용어 정의
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

# 형태소 분석기 OKT를 사용한 토큰화 작업 (다소 시간 소요)
okt = Okt()
tokenized_data = []
for sentence in train_data['document']:
    temp_data = okt.morphs(sentence, stem=True) # 토큰화
    temp_data = [word for word in temp_data if not word in stopwords] # 불용어 제거
    tokenized_data.append(temp_data)

# # 리뷰 길이 분포 확인
# print('리뷰의 최대 길이 :',max(len(l) for l in tokenized_data))
# print('리뷰의 평균 길이 :',sum(map(len, tokenized_data))/len(tokenized_data))
# plt.hist([len(s) for s in tokenized_data], bins=50)
# plt.xlabel('length of samples')
# plt.ylabel('number of samples')
# plt.show()


# from gensim.models import Word2Vec

# model = Word2Vec(sentences = tokenized_data, size = 100, window = 5, min_count = 5, workers = 4, sg = 0)