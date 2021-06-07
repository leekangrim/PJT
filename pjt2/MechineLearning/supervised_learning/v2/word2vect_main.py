# from load_data import load_data
# train_data = load_data(1, 1, 1)


# from word2vect import word2vect
# word2vect(train_data)


# Word2Vec 모델 저장하고 로드하기
from gensim.models import KeyedVectors
loaded_model = KeyedVectors.load_word2vec_format("_kor_w2v")
print(loaded_model.most_similar("남자"))
print(loaded_model.most_similar("여자"))
print(loaded_model.most_similar("책"))
print(loaded_model.most_similar("강추"))
print(loaded_model.most_similar("비추"))