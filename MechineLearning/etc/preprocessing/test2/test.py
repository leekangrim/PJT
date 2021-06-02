import pandas as pd


df = pd.read_csv("./test/0_remove_spaces_reviews.csv")


df['review'] = pd.read_csv("./csv/1_simple_preprocessed.csv")['0']
df.to_csv("./reviews/1_basic_preprocessed_reviews.csv", index=False)

df['review'] = pd.read_csv("./csv/4_spell_preprocessed_corpus.csv")['0']
df.to_csv("./reviews/2_spell_preprocessed_reviews.csv", index=False)