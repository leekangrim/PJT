from ckonlpy.tag import Twitter


twitter = Twitter()

twitter.morphs('은경이는 사무실로 갔습니다.')

twitter.add_dictionary('은경이', 'Noun')

twitter.morphs('은경이는 사무실로 갔습니다.')