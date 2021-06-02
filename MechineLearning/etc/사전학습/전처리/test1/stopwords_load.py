import pandas as pd
from nltk.tokenize import word_tokenize

example = "고기를 아무렇게나 구우려고 하면 안 돼. 고기라고 다 같은 게 아니거든. 예컨대 삼겹살을 구울 때는 중요한 게 있지."
stop_words = pd.read_csv('stopwords.txt', engine='python', header=None, names=["불용어"])

token_words = word_tokenize(example)
result_words = [word for word in token_words if not word in stop_words]

print(token_words) 
print(result_words)