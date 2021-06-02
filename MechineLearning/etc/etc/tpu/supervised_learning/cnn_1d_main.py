# from load_data import load_data
# total_data = load_data(0, 0, 1)


# from cnn_1d_model import cnn_1d_model
# max_len, X_train, vocab_size = cnn_1d_model(
#     total_data, test_size=0.25, max_freq=3, max_len=50
# )


# from cnn_1d_predict import sentiment_predict
# sentiment_predict(
#     '뭐 이런 걸 상품이라고 만듬? 비추합니다.', 
#     max_len = 50, X_train=X_train, vocab_size = vocab_size
# )



from cnn_1d_predict import sentiment_predict
sentiment_predict(
    '정말 재미있어요. 추천합니다.', 
    max_len = 50, vocab_size = 22225
)
from cnn_1d_predict import sentiment_predict
sentiment_predict(
    '돈주고 보기 아깝다.', 
    max_len = 50, vocab_size = 22225
)
from cnn_1d_predict import sentiment_predict
sentiment_predict(
    '비추합니다. ㅋㅋㅋ', 
    max_len = 50, vocab_size = 22225
)