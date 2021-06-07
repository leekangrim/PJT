def cnn_1d_model(total_data, test_size=0.25, max_freq=2, vocab_size = 0, max_len=80):
  
    # 전처리, 토큰화
    from preprocess import preprocess
    total_data['tokenized'] = preprocess(total_data['review'])


    # 훈련 데이터와 테스트 데이터 분리
    from sklearn.model_selection import train_test_split
    train_data, test_data = train_test_split(total_data, test_size = test_size, random_state = 42)
    print(train_data.groupby('label').size().reset_index(name = 'count'))

    X_train = train_data['tokenized'].values
    y_train = train_data['label'].values
    X_test = test_data['tokenized'].values
    y_test = test_data['label'].values

    import pandas as pd
    pd.DataFrame(train_data['tokenized'].values).to_csv('cnn_1d_x_train.csv', index=None)


    # 정수형 인코딩
    from below_threshold import below_threshold_freq
    vocab_size = vocab_size if vocab_size else below_threshold_freq(X_train, max_freq)

    from tensorflow.keras.preprocessing.text import Tokenizer
    tokenizer = Tokenizer(vocab_size, oov_token = 'OOV') 
    tokenizer.fit_on_texts(X_train)
    X_train = tokenizer.texts_to_sequences(X_train)
    X_test = tokenizer.texts_to_sequences(X_test)


    # 패딩
    from below_threshold import below_threshold_len
    below_threshold_len(X_train, max_len)

    from tensorflow.keras.preprocessing.sequence import pad_sequences
    X_train = pad_sequences(X_train, maxlen = max_len)
    X_test = pad_sequences(X_test, maxlen = max_len)


    # 1D CNN 감성 분류하기
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Embedding, Dropout, Conv1D, GlobalMaxPooling1D, Dense
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
    from tensorflow.keras.models import load_model


    model = Sequential()
    model.add(Embedding(vocab_size, 100))
    model.add(Dropout(0.3))
    model.add(Conv1D(100, 3, padding='valid', activation='relu'))
    model.add(GlobalMaxPooling1D())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))


    es = EarlyStopping(monitor = 'val_loss', mode = 'min', verbose = 1, patience = 3)
    mc = ModelCheckpoint('cnn_1d_best_model.h5', monitor = 'val_acc', mode = 'max', verbose = 1, save_best_only = True)
    model.compile(optimizer='adam', loss = 'binary_crossentropy', metrics = ['acc'])
    history = model.fit(X_train, y_train, epochs = 20, validation_data = (X_test, y_test), callbacks=[es, mc])


    loaded_model = load_model('cnn_1d_best_model.h5')
    print("\n 테스트 정확도: %.4f" % (loaded_model.evaluate(X_test, y_test)[1]))