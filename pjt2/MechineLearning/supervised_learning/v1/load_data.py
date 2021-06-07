import pandas as pd
import numpy as np


def load_data(aladin = 0, naver_shopping = 0, naver_movie = 0):
    total_data = pd.DataFrame(columns=['ISBN13', 'rating', 'review'])

    # 알라딘 데이터 로드하기
    if aladin:
        aladin_data = pd.read_csv('./_reviews.csv')
        aladin_data['rating'] = aladin_data['rating'].replace(8.0, np.nan) # 8점 제거
        aladin_data['label'] = np.select([aladin_data.rating >= 8.], [1], default=0) # total_data['label'] = total_data['rating'].apply(lambda x: 1 if int(x) == 10 or int(x) == 8 else 0)
        total_data = total_data.append(aladin_data)


    # 네이버 쇼핑 데이터 추가
    if naver_shopping:
        naver_shopping_data = pd.read_table('naver_shopping_ratings.txt', names=['rating', 'review'])
        naver_shopping_data['label'] = np.select([naver_shopping_data.rating > 3], [1], default=0)
        total_data = total_data.append(naver_shopping_data)


    # 네이버 영화 데이터 추가
    if naver_movie:
        naver_movie_data = pd.read_table('naver_movie_ratings.txt', names=['ISBN13', 'review', 'label'])
        naver_movie_data['label'] = naver_movie_data['label'].apply(lambda x: 1 if x == '1' else 0)
        total_data = total_data.append(naver_movie_data)


    # 중복 제거, null 제거
    total_data.drop_duplicates(subset=['review'], inplace=True)
    total_data['review'].replace('', np.nan, inplace=True)
    total_data['review'].dropna(how = 'any', inplace=True)

    total_data = total_data.astype({'label': 'int'})

    return total_data
