import pandas as pd


total_data = pd.read_csv('full_reviews.csv')
print(total_data.groupby('rating').size().reset_index(name = 'count'))