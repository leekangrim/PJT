import re

r = re.compile('[ㄱ-ㅎㅏ-ㅣ]')
print(len(r.findall('ㄱㄴㄷ')))