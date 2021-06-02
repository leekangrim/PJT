import pandas as pd



def GRU_model(_total_data, _test_size=0.25, _threshold=2, _max_len=80):

    total_data = _total_data

    # 훈련 데이터와 테스트 데이터 분리
    from sklearn.model_selection import train_test_split
    train_data, test_data = train_test_split(total_data, test_size = _test_size, random_state = 42)


    # 훈련데이터의 긍부정 비율 확인
    print(train_data.groupby('label').size().reset_index(name = 'count'))


    # 전처리, 토큰화
    from preprocess import preprocess
    train_data['tokenized'] = preprocess(train_data['review'])
    test_data['tokenized'] = preprocess(test_data['review'])


    # predict를 위해 저장
    df = pd.DataFrame(train_data['tokenized'])
    df.to_csv('_X_train.csv', index=None)


    # 정수형 인코딩
    X_train = train_data['tokenized'].values
    y_train = train_data['label'].values
    X_test= test_data['tokenized'].values
    y_test = test_data['label'].values


    from tensorflow.keras.preprocessing.text import Tokenizer
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X_train)


    threshold = _threshold
    total_cnt = len(tokenizer.word_index) # 단어의 수
    rare_cnt = 0 # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
    total_freq = 0 # 훈련 데이터의 전체 단어 빈도수 총 합
    rare_freq = 0 # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합


    # 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
    for key, value in tokenizer.word_counts.items():
        total_freq += value

        # 단어의 등장 빈도수가 threshold보다 작으면
        if(value < threshold):
            rare_cnt = rare_cnt + 1
            rare_freq = rare_freq + value


    print('단어 집합(vocabulary)의 크기 :',total_cnt)
    print('등장 빈도가 %s번 이하인 희귀 단어의 수: %s'%(threshold - 1, rare_cnt))
    print("단어 집합에서 희귀 단어의 비율:", (rare_cnt / total_cnt)*100)
    print("전체 등장 빈도에서 희귀 단어 등장 빈도 비율:", (rare_freq / total_freq)*100)


    # 전체 단어 개수 중 빈도수 2이하인 단어 개수는 제거.
    # 0번 패딩 토큰과 1번 OOV 토큰을 고려하여 +2
    vocab_size = total_cnt - rare_cnt + 2
    print('단어 집합의 크기 :',vocab_size)


    tokenizer = Tokenizer(vocab_size, oov_token = 'OOV') 
    tokenizer.fit_on_texts(X_train)
    X_train = tokenizer.texts_to_sequences(X_train)
    X_test = tokenizer.texts_to_sequences(X_test)


    # 패딩
    print('리뷰의 최대 길이 :',max(len(l) for l in X_train))
    print('리뷰의 평균 길이 :',sum(map(len, X_train))/len(X_train))


    def below_threshold_len(max_len, nested_list):
        cnt = 0
        for s in nested_list:
            if(len(s) <= max_len):
                cnt = cnt + 1
        print('전체 샘플 중 길이가 %s 이하인 샘플의 비율: %s'%(max_len, (cnt / len(nested_list))*100))


    max_len = _max_len
    below_threshold_len(max_len, X_train)


    from tensorflow.keras.preprocessing.sequence import pad_sequences
    X_train = pad_sequences(X_train, maxlen = max_len)
    X_test = pad_sequences(X_test, maxlen = max_len)


    # GRU로 감성 분류하기
    from tensorflow.keras.layers import Embedding, Dense, GRU
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.models import load_model
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint


    model = Sequential()
    model.add(Embedding(vocab_size, 100))
    model.add(GRU(128))
    model.add(Dense(1, activation='sigmoid'))


    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
    mc = ModelCheckpoint('best_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)


    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
    history = model.fit(X_train, y_train, epochs=15, callbacks=[es, mc], batch_size=60, validation_split=0.2)


    loaded_model = load_model('best_model.h5')
    print("\n 테스트 정확도: %.4f" % (loaded_model.evaluate(X_test, y_test)[1]))

    return train_data['tokenized'].values