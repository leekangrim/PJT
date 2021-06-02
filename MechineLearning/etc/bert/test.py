import re
from soynlp.normalizer import repeat_normalize

import pandas as pd
import numpy as np
import torch
from torch.nn import functional as F
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, ElectraForSequenceClassification, AdamW
from tqdm.notebook import tqdm


# =================
# 새로운 문장 테스트
# =================

# GPU 사용
device = torch.device("cuda")

# 문장 테스트
model = ElectraForSequenceClassification.from_pretrained("monologg/koelectra-base-v3-discriminator").to(device)
model.load_state_dict(torch.load("koelectra_base_v3.pt"))
tokenizer = AutoTokenizer.from_pretrained("monologg/koelectra-base-v3-discriminator")
print('load...')


def preprocessing(review):

    review = re.sub('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+)', '', str(review)) # remove e-mail
    review = re.sub('(http|ftp|https)://(?:[-\w.]|(?:\da-fA-F]{2}))+', '', str(review)) # remove url
    review = re.sub(r'<[^>]+>','',review) #remove Html tags
    review = re.sub(r'\[[^>]+\]','',review) #remove Html tags
    review = re.sub(r'\{[^>]+\}','',review) #remove Html tags
    review = re.sub(r'\([^>]+\)','',review) #remove Html tags

    review = re.sub(r'[^ .,?!/@$%~％·∼()\x00-\x7F가-힣]+', '', str(review)) # 한글, 숫자, 알파벳, 기본구두점 제외
    # review = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣0-9a-zA-Z]', ' ', str(review)) # 한글, 숫자, 알파벳, 기본구두점 제외

    review = re.sub(r'\s+', ' ', str(review)) #remove spaces
    review = re.sub(r"^\s+", '', str(review)) #remove space from start
    review = re.sub(r'\s+$', '', str(review)) #remove space from the end
    
    review = repeat_normalize(str(review))

    return review


def test_sentences(sentences):

    sentences = preprocessing(sentences)
    
    inputs = tokenizer(
        sentences, 
        return_tensors='pt',
        truncation=True,
        max_length=64,
        pad_to_max_length=True,
        add_special_tokens=True
    )
    input_ids = inputs['input_ids'][0]
    attention_mask = inputs['attention_mask'][0]

    y_pred = model(
        input_ids.unsqueeze(0).to(device), 
        attention_mask=attention_mask.unsqueeze(0).to(device)
    )

    return y_pred[0].detach().cpu().numpy()


# 평가모드로 변경
model.eval()

logits = test_sentences(['연기는 별로지만 재미 하나는 끝내줌!'])
print(logits)
print(np.argmax(logits))

logits = test_sentences(['주연배우가 아깝다. 총체적 난국...'])
print(logits)
print(np.argmax(logits))