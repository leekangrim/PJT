import pandas as pd
total_data = pd.read_csv('./tokenized_data.csv')
print(len(total_data))
print(total_data.groupby('label').size().reset_index(name = 'count'))

# total_data['tokenized'] = total_data['tokenized'].replace('', np.nan)
# total_data = total_data.dropna()
# print(len(total_data))

total_data['tokenized'] = total_data['tokenized'].apply(lambda x: str(x).split())


# 훈련 데이터와 테스트 데이터 분리
from sklearn.model_selection import train_test_split
train_data, test_data = train_test_split(total_data, test_size = 0.2, random_state = 42)

X_train = train_data['tokenized'].values
y_train = train_data['label'].values
X_test = test_data['tokenized'].values
y_test = test_data['label'].values


# 정수형 인코딩
from below_threshold import below_threshold_freq
min_freq = 2
vocab_size = below_threshold_freq(X_train, min_freq)
# vocab_size = 39684

from tensorflow.keras.preprocessing.text import Tokenizer
tokenizer = Tokenizer(vocab_size, oov_token = 'OOV') 
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)

# drop_train = [index for index, sentence in enumerate(X_train) if len(sentence) < 1]
# X_train = np.delete(X_train, drop_train, axis=0)
# y_train = np.delete(y_train, drop_train, axis=0)
# print(len(X_train))


# 패딩
max_len = 100
from below_threshold import below_threshold_len
below_threshold_len(X_train, max_len)

from tensorflow.keras.preprocessing.sequence import pad_sequences
X_train = pad_sequences(X_train, maxlen = max_len)
X_test = pad_sequences(X_test, maxlen = max_len)


# 학습
from tensorflow.keras.layers import Embedding, Dense, GRU
from tensorflow.keras.models import Sequential
# from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow as tf

model = Sequential()
model.add(Embedding(vocab_size, 100))
model.add(GRU(128))
model.add(Dense(1, activation='sigmoid'))

# es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
mc = ModelCheckpoint('gru_best_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc', tf.keras.metrics.Recall(), tf.keras.metrics.Precision()])
# history = model.fit(X_train, y_train, epochs=20, callbacks=[es, mc], batch_size=60, validation_split=0.2)
history = model.fit(X_train, y_train, epochs=20, callbacks=[mc], batch_size=60, validation_split=0.2)


# 시각화
import matplotlib.pyplot as plt
plt.figure(figsize=(25, 6))
plt.subplot(1, 4, 1)
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(['Train', 'Val'], loc='upper left')

plt.subplot(1, 4, 2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(['Train', 'Val'], loc='upper left')

plt.subplot(1, 4, 3)
plt.plot(history.history['recall'])
plt.plot(history.history['val_recall'])
plt.title('Recall')
plt.xlabel('Epoch')
plt.ylabel('Recall')
plt.legend(['Train', 'Val'], loc='upper left')

plt.subplot(1, 4, 4)
plt.plot(history.history['precision'])
plt.plot(history.history['val_precision'])
plt.title(' Precision')
plt.xlabel('Epoch')
plt.ylabel('Precision')
plt.legend(['Train', 'Val'], loc='upper left')

plt.savefig('./gru.png')


# 평가
from tensorflow.keras.models import load_model
loaded_model = load_model('gru_best_model.h5')

evaluate_list = loaded_model.evaluate(X_test, y_test)
print("\n 테스트 정확도: %.4f" % evaluate_list[1])
for eval in evaluate_list:
    print("\n 평과 결과 리스트 정확도: %.4f" % eval)


# 문서화
def predict(tokenized_reviews):    
    corpus = []
    for tokenized_review in tokenized_reviews:
        corpus.append(sentiment_predict(tokenized_review))
    return corpus


def sentiment_predict(tokenized_review):
    # 정수 인코딩
    encoded_review = tokenizer.texts_to_sequences([tokenized_review])

    # 패딩
    padded_review = pad_sequences(encoded_review, maxlen = max_len)
    
    # 예측
    score = float(loaded_model.predict(padded_review))
    predicted_review = "{:.2f}% 확률 긍정".format(score * 100) if(score > 0.5) else "{:.2f}% 확률 부정".format((1 - score) * 100)
    return predicted_review


test_data['predicted'] = predict(test_data['tokenized'][:100])
test_data.to_csv('./predicted_reviews.csv', index=False)