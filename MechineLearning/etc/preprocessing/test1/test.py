# import glob
# import re
# import pandas as pd
# import numpy as np
# filenames = glob.glob('./월간베스트리뷰평점/*.csv')
# test_filenames = filenames[21:]

# test_data = pd.DataFrame(columns=["ISBN13", "rating", "review"])

# for test_filename in test_filenames:
#     temp_data = pd.read_csv(test_filename)
#     test_data = pd.concat([test_data, temp_data], axis = 0, ignore_index=True)
# test_data = test_data.dropna(how = 'any')

# test_data['review'] = test_data['review'].apply(lambda x: re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", x))
# test_data['review'].replace('', np.nan, inplace=True)
# test_data = test_data.dropna(how = 'any')
# print(len(test_data))

# test_data = test_data.drop(['ISBN13'], axis=1)
# test_data.to_csv('res2.csv', index=False)


# # csv 합치기
# res1 = pd.read_csv('./res1.csv')
# print(len(res1))
# res2 = pd.read_csv('./res2.csv')
# print(len(res2))
# res3 = pd.concat([res1, res2], axis=1)
# res3.to_csv("./res3.csv", index=False)


# # 10점인데 부정
# res3 = pd.read_csv('./res3.csv')
# high_res3 = res3[res3['rating'].isin([10])]
# posivite_high_res3 = [(high_res3.iloc[i]['review'], high_res3.iloc[i]['predict']) for i in range(len(high_res3)) if str(high_res3.iloc[i]['predict']).find("부정 리뷰입니다.") != -1]

# print(*posivite_high_res3, sep='\n')


# # 2점인데 긍정
# res3 = pd.read_csv('./res3.csv')
# high_res3 = res3[res3['rating'].isin([2])]
# posivite_high_res3 = [(high_res3.iloc[i]['review'], high_res3.iloc[i]['predict']) for i in range(len(high_res3)) if str(high_res3.iloc[i]['predict']).find("긍정 리뷰입니다.") != -1]

# print(*posivite_high_res3, sep='\n')

str().issp