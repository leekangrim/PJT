import pandas as pd


loaded_data = pd.read_csv('labeled_reviews.csv')


negative_data = loaded_data[loaded_data['label'] == 0]
print(negative_data.groupby('label').size().reset_index(name = 'count'))

posivite_data = loaded_data[loaded_data['label'] == 1]
print(posivite_data.groupby('label').size().reset_index(name = 'count'))


total_data = negative_data + posivite_data[:(len(negative_data) << 1)]
total_data.to_csv('2vs1_total_data.csv')

remain_data = posivite_data[(len(negative_data) << 1):]
remain_data.to_csv('remain_pos_data.csv')
