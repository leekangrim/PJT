from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize

example = "Family is not an important thing. It's everything."
stop_words = set(stopwords.words('english')) 

token_words = word_tokenize(example)
result_words = [word for word in token_words if word not in stop_words]

print(token_words) 
print(result_words) 