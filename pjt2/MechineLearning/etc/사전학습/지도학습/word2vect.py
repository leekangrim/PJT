def word2vect(train_data, size = 150, window = 5, min_count = 2, workers = 4, sg = 1):

    # 토큰화
    from preprocess import preprocess
    tokenized_data = preprocess(train_data['review'])


    # Word2Vec 훈련시키기
    from gensim.models import Word2Vec
    model = Word2Vec(
        sentences = tokenized_data, 
        size = size, 
        window = window, 
        min_count = min_count, 
        workers = workers, 
        sg = sg
    )


    # Word2Vec 모델 저장
    model.wv.save_word2vec_format('_kor_w2v') # 모델 저장