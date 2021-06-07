# import glob
# import pandas as pd


# foldername_list = glob.glob('csv_reviews/*')
# for foldername in foldername_list:
#     print(foldername)

#     write_csv = pd.DataFrame(columns=['ISBN13', 'rating', 'review'])

#     filename_list = glob.glob(f'{foldername}/*')
#     for filename in filename_list:
#         print(filename)

#         read_csv = pd.read_csv(filename)
#         write_csv = write_csv.append(read_csv)

#     foldername1, foldername2, filename = filename.split('\\')
#     # new_filename = foldername2[3:]
#     write_csv.to_csv(f'./connected/{foldername2}.csv', index=False)


import glob
import pandas as pd


write_csv = pd.DataFrame(columns=['ISBN13', 'rating', 'review'])

filename_list = glob.glob('csv_reviews_bindded/*.csv')
for filename in filename_list:
    print(filename)

    read_csv = pd.read_csv(filename)
    write_csv = write_csv.append(read_csv)

write_csv.to_csv('./csv_reviews_bindded/full_reviews.csv', index=False)