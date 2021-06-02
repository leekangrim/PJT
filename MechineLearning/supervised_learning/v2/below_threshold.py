from tensorflow.keras.preprocessing.text import Tokenizer


def below_threshold_freq(X_train, max_freq):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X_train)

    threshold = max_freq
    
    total_cnt = len(tokenizer.word_index)
    rare_cnt = 0
    total_freq = 0
    rare_freq = 0

    for key, value in tokenizer.word_counts.items():
        total_freq += value
        if(value < threshold):
            rare_cnt = rare_cnt + 1
            rare_freq = rare_freq + value

    print('단어 집합(vocabulary)의 크기 :',total_cnt)
    print('등장 빈도가 %s번 이하인 희귀 단어의 수: %s'%(threshold - 1, rare_cnt))
    print("단어 집합에서 희귀 단어의 비율:", (rare_cnt / total_cnt)*100)
    print("전체 등장 빈도에서 희귀 단어 등장 빈도 비율:", (rare_freq / total_freq)*100)
    

    vocab_size = total_cnt - rare_cnt + 2
    print('단어 집합의 크기 :',vocab_size)


    return vocab_size



def below_threshold_len(X_train, max_len):

    print('리뷰의 최대 길이 :',max(len(l) for l in X_train))
    print('리뷰의 평균 길이 :',sum(map(len, X_train))/len(X_train))

    cnt = 0
    for sent in X_train:
        if(len(sent) <= max_len):
            cnt = cnt + 1
    print('전체 샘플 중 길이가 %s 이하인 샘플의 비율: %s'%(max_len, (cnt / len(X_train))*100))