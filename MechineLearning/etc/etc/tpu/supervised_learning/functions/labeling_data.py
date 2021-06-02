import pandas as pd
import numpy as np


total_data = pd.DataFrame(columns=['ISBN13', 'rating', 'review'])

load_data = pd.read_csv('full_reviews.csv')
print(len(load_data))

load_data = load_data[load_data['rating'] != 8]
print(len(load_data))


load_data['label'] = load_data['rating'].replace([10, 6, 4, 2], [1, 0, 0, 0])
print(load_data.groupby('label').size().reset_index(name = 'count'))


load_data.to_csv('labeld_reviews.csv')