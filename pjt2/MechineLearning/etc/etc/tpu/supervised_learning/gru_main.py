# from load_data import load_data
# total_data = load_data(0, 0, 1)


# from gru_model import gru_model
# max_len, X_train, vocab_size = gru_model(
#     total_data, test_size=0.25, max_freq=2, max_len=80
# )


# from gru_predict import sentiment_predict
# sentiment_predict(
#     '뭐 이런 걸 상품이라고 만듬? 비추합니다.', 
#     max_len = 80, X_train=X_train, vocab_size = vocab_size
# )


from gru_predict import sentiment_predict
sentiment_predict(
    'ㅋㅋ 뭘 보라고 만듬? 비추합니다.', 
    max_len = 80, vocab_size = 29676
)