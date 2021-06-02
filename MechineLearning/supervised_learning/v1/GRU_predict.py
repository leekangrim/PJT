from preprocess import preprocess
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
import ast


def sentiment_predict(_new_sentence, _X_train=None, _threshold=2, _max_len = 80):
    # _X_train.csv 로드하기
    if not _X_train:
        _X_train = pd.read_csv('./_X_train.csv')
        _X_train['tokenized'] = _X_train['tokenized'].apply(ast.literal_eval)

    # 정수 인코딩
    X_train = _X_train['tokenized']
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X_train)

    threshold = _threshold
    total_cnt = len(tokenizer.word_index)
    rare_cnt = 0
    total_freq = 0
    rare_freq = 0

    for key, value in tokenizer.word_counts.items():
        total_freq += value

        if(value < threshold):
            rare_cnt = rare_cnt + 1
            rare_freq = rare_freq + value

    vocab_size = total_cnt - rare_cnt + 2
    tokenizer = Tokenizer(vocab_size, oov_token = 'OOV') 
    tokenizer.fit_on_texts(X_train)

    # 전처리, 토큰화
    new_sentence = _new_sentence
    new_sentence = preprocess([new_sentence])
    new_sentence = new_sentence[0]

    encoded = tokenizer.texts_to_sequences([new_sentence])

    # 패딩
    pad_new = pad_sequences(encoded, maxlen = _max_len) 
    
    # 예측
    loaded_model = load_model('best_model.h5')
    score = float(loaded_model.predict(pad_new))
    if(score > 0.5):
        print("{:.2f}% 확률로 긍정 리뷰입니다.".format(score * 100))
    else:
        print("{:.2f}% 확률로 부정 리뷰입니다.".format((1 - score) * 100))