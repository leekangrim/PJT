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
model.load_state_dict(torch.load("C:/Users/multicampus/Desktop/bootcamp/koelectra_base_v3.pt"))
tokenizer = AutoTokenizer.from_pretrained("monologg/koelectra-base-v3-discriminator")
print('load...')


def test_sentences(sentences):
    
    inputs = tokenizer(
        sentences, 
        return_tensors='pt',
        truncation=True,
        max_length=128,
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