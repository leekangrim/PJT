import glob

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import re
# import urllib.request
from eunjeon import Mecab
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


# 1. 데이터 로드
filenames = glob.glob('./월간베스트리뷰평점/*.csv')

train_filenames= filenames[:21]
test_filenames = filenames[21:]

train_data = pd.DataFrame(columns=["ISBN13", "rating", "review"])
test_data = pd.DataFrame(columns=["ISBN13", "rating", "review"])

for train_filenames in train_filenames:
    temp_data = pd.read_csv(train_filenames)
    train_data = pd.concat([train_data, temp_data], axis = 0, ignore_index=True)
train_data = train_data.dropna(how = 'any')
print(len(train_data))

for test_filename in test_filenames:
    temp_data = pd.read_csv(test_filename)
    test_data = pd.concat([test_data, temp_data], axis = 0, ignore_index=True)
test_data = test_data.dropna(how = 'any')
print(len(test_data))


# 2. 데이터 정제 .apply(lambda x: re.sub('[^a-zA-Z]',' ',x))
train_data['review'] = train_data['review'].apply(lambda x: re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", x))
train_data['rating'] = train_data['rating'].apply(lambda x: 1 if x == 10 else 0)
train_data['review'].replace('', np.nan, inplace=True)
train_data = train_data.dropna(how = 'any')
print(len(train_data))

test_data['review'] = test_data['review'].apply(lambda x: re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", x))
test_data['rating'] = test_data['rating'].apply(lambda x: 1 if x == 10 else 0)
test_data['review'].replace('', np.nan, inplace=True)
test_data = test_data.dropna(how = 'any')
print(len(test_data))

# train_data['label'].value_counts().plot(kind = 'bar')
# print(train_data.groupby('label').size().reset_index(name = 'count'))
# test_data['label'].value_counts().plot(kind = 'bar')
# print(test_data.groupby('label').size().reset_index(name = 'count'))


# 3. 토큰화

# 한국어의 조사, 접속사 등의 보편적인 불용어를 사용할 수도 있겠지만 결국 풀고자 하는 문제의 데이터를 지속 검토하면서 계속해서 추가
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
Mecab = Mecab()
X_train = []
for sentence in train_data['review']:
    temp_X = []
    temp_X = Mecab.morphs(sentence) # 토큰화, 정규화
    temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
    X_train.append(temp_X)


# 4. 정수형 인코딩
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)


# 등장 빈도수가 3회 미만인 단어들이 이 데이터에서 얼만큼의 비중을 차지하는지 확인
threshold = 4
total_cnt = len(tokenizer.word_index) # 단어의 수
rare_cnt = 0 # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
total_freq = 0 # 훈련 데이터의 전체 단어 빈도수 총 합
rare_freq = 0 # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

# 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
for key, value in tokenizer.word_counts.items():
    total_freq = total_freq + value

    # 단어의 등장 빈도수가 threshold보다 작으면
    if(value < threshold):
        rare_cnt = rare_cnt + 1
        rare_freq = rare_freq + value
print('단어 집합(vocabulary)의 크기 :',total_cnt)
print('등장 빈도가 %s번 이하인 희귀 단어의 수: %s'%(threshold - 1, rare_cnt))
print("단어 집합에서 희귀 단어의 비율:", (rare_cnt / total_cnt)*100)
print("전체 등장 빈도에서 희귀 단어 등장 빈도 비율:", (rare_freq / total_freq)*100)


# 전체 단어 개수 중 빈도수 0이하인 단어 개수는 제거
# 0번 패딩 토큰과 1번 OOV 토큰을 고려하여 +2
vocab_size = total_cnt - rare_cnt + 2
print('단어 집합의 크기 :',vocab_size)


# 전체 단어 개수 중 빈도수 4이하인 단어 개수는 제거
# 정수 인코딩 과정에서 이보다 큰 숫자가 부여된 단어들은 OOV로 변환, 즉 1번으로 할당
tokenizer = Tokenizer(vocab_size, oov_token = 'OOV') 
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)
y_train = np.array(train_data['rating'])


# 5. 빈 샘플(empty samples) 제거
drop_train = [index for index, sentence in enumerate(X_train) if len(sentence) < 1]

X_train = np.delete(X_train, drop_train, axis=0)
y_train = np.delete(y_train, drop_train, axis=0)
print(X_train.shape)
print(y_train.shape)


# 6. 패딩
print('리뷰의 최대 길이 :',max(len(l) for l in X_train))
print('리뷰의 평균 길이 :',sum(map(len, X_train))/len(X_train))
# plt.hist([len(s) for s in X_train], bins=50)
# plt.xlabel('length of samples')
# plt.ylabel('number of samples')
# plt.show()


def below_threshold_len(max_len, nested_list):
    cnt = 0
    for s in nested_list:
        if(len(s) <= max_len):
            cnt = cnt + 1
    print('전체 샘플 중 길이가 %s 이하인 샘플의 비율: %s'%(max_len, (cnt / len(nested_list))*100))

max_len = 60
below_threshold_len(max_len, X_train)

X_train = pad_sequences(X_train, maxlen = max_len)


# 7. LSTM으로 알라딘 리뷰 감성 분류하기
from tensorflow.keras.layers import Embedding, Dense, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

model = Sequential()
model.add(Embedding(vocab_size, 100))
model.add(LSTM(128))
model.add(Dense(1, activation='sigmoid'))

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
mc = ModelCheckpoint('best_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
history = model.fit(X_train, y_train, epochs=5, callbacks=[es, mc], batch_size=60, validation_split=0.2)


# 8. 테스트 예측하기
loaded_model = load_model('best_model.h5')

# #  토큰화
# X_test = []
# for sentence in test_data['review']:
#     temp_X = []
#     temp_X = Mecab.morphs(sentence) # 토큰화, 정규화
#     temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
#     X_test.append(temp_X)

# # 인코딩
# X_test = tokenizer.texts_to_sequences(X_test)
# y_test = np.array(test_data['rating'])

# # 패딩
# X_test = pad_sequences(X_test, maxlen = max_len)

# print("\n 테스트 정확도: %.4f" % (loaded_model.evaluate(X_test, y_test)[1]))


def sentiment_predict(new_sentence):
    new_sentence = Mecab.morphs(new_sentence) # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
    score = float(loaded_model.predict(pad_new)) # 예측
    if(score > 0.5):
        return "{:.2f}% 확률로 긍정 리뷰입니다.".format(score * 100)
    else:
        return "{:.2f}% 확률로 부정 리뷰입니다.".format((1 - score) * 100)


res = []
for review in test_data['review']:
    res.append(sentiment_predict(review))

df = pd.DataFrame(res)
df.to_csv('res.csv', mode='w')