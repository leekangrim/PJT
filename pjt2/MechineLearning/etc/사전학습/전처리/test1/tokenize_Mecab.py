from eunjeon import Mecab 
Mecab = Mecab()

sentence = '데이콘에서 다양한 컴피티션을 즐기면서 실력있는 데이터 분석가로 성장하세요!!.'

print("형태소 단위로 문장 분리")
print("----------------------")
print(Mecab.morphs(sentence))
print(" ")
print("문장에서 명사 추출")
print("----------------------")
print(Mecab.nouns(sentence))
print(" ")
print("품사 태킹(PoS)")
print("----------------------")
print(Mecab.pos(sentence))