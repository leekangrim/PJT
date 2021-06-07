from nltk.tokenize import word_tokenize


example = "고기를 아무렇게나 구우려고 하면 안 돼. 고기라고 다 같은 게 아니거든. 예컨대 삼겹살을 구울 때는 중요한 게 있지."
stop_words = "아무거나 아무렇게나 어찌하든지 같다 비슷하다 예컨대 이럴정도로 하면 아니거든".split()

token_words = word_tokenize(example)
result_words = [word for word in token_words if not word in stop_words]

print(token_words) 
print(result_words)