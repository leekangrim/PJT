def word2vect(_train_data, _size = 150, _window = 5, _min_count = 2, _workers = 4, _sg = 1):
    train_data = _train_data
    # 토큰화
    from preprocess0 import preprocess
    tokenized_data = preprocess(train_data['review'])


    # Word2Vec 훈련시키기
    from gensim.models import Word2Vec
    model = Word2Vec(
        sentences = tokenized_data, 
        size = _size, 
        window = _window, 
        min_count = _min_count, 
        workers = _workers, 
        sg = _sg
    )


    # Word2Vec 모델 저장
    model.wv.save_word2vec_format('_kor_w2v') # 모델 저장