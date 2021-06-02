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


class ReviewDataset(Dataset):
  
    def __init__(self, dataset):
        self.dataset = dataset
        
        self.tokenizer = AutoTokenizer.from_pretrained("monologg/koelectra-base-v3-discriminator")

        print(self.dataset.describe())
  
    def __len__(self):
        return len(self.dataset)
  
    def __getitem__(self, idx):
        row = self.dataset.iloc[idx, 1:3].values
        text = row[0]
        y = row[1]

        inputs = self.tokenizer(
            text, 
            return_tensors='pt',
            truncation=True,
            max_length=128,
            pad_to_max_length=True,
            add_special_tokens=True
        )

        input_ids = inputs['input_ids'][0]
        attention_mask = inputs['attention_mask'][0]

        return input_ids, attention_mask, y


def test_sentences(sentences):
    df = pd.DataFrame([[0, sentences, 0]], columns=['id','document','label'])
    dataset = ReviewDataset(df)
    loader = DataLoader(dataset, batch_size=1)
    for input_ids_batch, attention_masks_batch, _ in tqdm(loader):
        y_pred = model(input_ids_batch.to(device), attention_mask=attention_masks_batch.to(device))[0]

    # 로스 구함
    logits = y_pred

    # CPU로 데이터 이동
    logits = logits.detach().cpu().numpy()

    return logits


 # 평가모드로 변경
model.eval()    

logits = test_sentences(['연기는 별로지만 재미 하나는 끝내줌!'])
print(logits)
print(np.argmax(logits))


logits = test_sentences(['주연배우가 아깝다. 총체적 난국...'])
print(logits)
print(np.argmax(logits))