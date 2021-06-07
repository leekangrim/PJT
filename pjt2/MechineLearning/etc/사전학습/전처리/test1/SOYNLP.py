# import urllib.request
# urllib.request.urlretrieve("https://raw.githubusercontent.com/lovit/soynlp/master/tutorials/2016-10-20.txt", filename="2016-10-20.txt")


# 토큰화
# WordExtractor
from soynlp import DoublespaceLineCorpus
from soynlp.word import WordExtractor

corpus = DoublespaceLineCorpus("2016-10-20.txt")

word_extractor = WordExtractor()
word_extractor.train(corpus)
word_score_table = word_extractor.extract()

print(word_score_table["반포한강공원"].cohesion_forward)
print(word_score_table["디스플"].right_branching_entropy)


# # LTokenizer
# from soynlp.tokenizer import LTokenizer

# scores = {word:score.cohesion_forward for word, score in word_score_table.items()}
# l_tokenizer = LTokenizer(scores=scores)
# l_tokenizer.tokenize("국제사회와 우리의 노력들로 범죄를 척결하자", flatten=False)


# # MaxScoreTokenizer
# from soynlp.tokenizer import MaxScoreTokenizer

# maxscore_tokenizer = MaxScoreTokenizer(scores=scores)
# maxscore_tokenizer.tokenize("국제사회와우리의노력들로범죄를척결하자")


# # 반복되는 문자 정제
# from soynlp.normalizer import *

# print(emoticon_normalize('앜ㅋㅋㅋㅋ이영화존잼쓰ㅠㅠㅠㅠㅠ', num_repeats=2))
# print(emoticon_normalize('앜ㅋㅋㅋㅋㅋㅋㅋㅋㅋ이영화존잼쓰ㅠㅠㅠㅠ', num_repeats=2))
# print(emoticon_normalize('앜ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ이영화존잼쓰ㅠㅠㅠㅠㅠㅠ', num_repeats=2))
# print(emoticon_normalize('앜ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ이영화존잼쓰ㅠㅠㅠㅠㅠㅠㅠㅠ', num_repeats=2))

# print(repeat_normalize('와하하하하하하하하하핫', num_repeats=2))
# print(repeat_normalize('와하하하하하하핫', num_repeats=2))
# print(repeat_normalize('와하하하하핫', num_repeats=2))