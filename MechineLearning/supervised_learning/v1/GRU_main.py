from load_data import load_data
total_data = load_data(1, 0, 1)


from GRU_model import GRU_model
X_train = GRU_model(total_data)


from GRU_predict import sentiment_predict
sentiment_predict('이 상품 진짜 좋아요... 저는 강추합니다. 대박', X_train)
sentiment_predict('진짜 배송도 늦고 개짜증나네요. 뭐 이런 걸 상품이라고 만듬?', X_train)
sentiment_predict('판매자님... 너무 짱이에요.. 대박나삼', X_train)
sentiment_predict('ㅁㄴㅇㄻㄴㅇㄻㄴㅇ리뷰쓰기도 귀찮아', X_train)