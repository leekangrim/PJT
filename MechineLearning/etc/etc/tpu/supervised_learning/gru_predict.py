from preprocess import preprocess
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
import ast

from below_threshold import below_threshold_freq


def sentiment_predict(new_sentence, X_train=None, max_freq=2, vocab_size = 0, max_len = 80):

    X_train = X_train if X_train else pd.read_csv('gru_x_train.csv')
    X_train = X_train['0'].apply(ast.literal_eval).values

    vocab_size = vocab_size if vocab_size else below_threshold_freq(X_train, max_freq)
    tokenizer = Tokenizer(vocab_size, oov_token = 'OOV') 
    tokenizer.fit_on_texts(X_train)

    # 전처리
    new_sentence = preprocess([new_sentence])
    new_sentence = new_sentence[0]

    # 정수 인코딩
    encoded = tokenizer.texts_to_sequences([new_sentence])

    # 패딩
    pad_new = pad_sequences(encoded, maxlen = max_len) 
    
    # 예측
    loaded_model = load_model('gru_best_model.h5')
    score = float(loaded_model.predict(pad_new))
    if(score > 0.5):
        print("{:.2f}% 확률로 긍정 리뷰입니다.".format(score * 100))
    else:
        print("{:.2f}% 확률로 부정 리뷰입니다.".format((1 - score) * 100))