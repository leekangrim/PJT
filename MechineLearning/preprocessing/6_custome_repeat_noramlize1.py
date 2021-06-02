def custom_repeat_noramlize1(review):
    sent = review[:]
    i = 0
    while i < len(sent) - 1:
      if sent[i] == sent[i + 1]:
          sent = sent[:i] + sent[i + 1:]
      else:
          i += 1
    return sent


def repeat_noramlize1(reviews):
    corpus = []
    for review in reviews:
        normalized_sent = custom_repeat_noramlize1(str(review))
        corpus.append(normalized_sent)
    return corpus


import pandas as pd
filepath = '"./_reviews.csv"'
df = pd.read_csv(filepath)

df['review'] = repeat_noramlize1(df['review'])
df.to_csv("6" + filepath, index=False)