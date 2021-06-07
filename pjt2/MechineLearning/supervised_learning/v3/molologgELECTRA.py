import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

import torch
from torch.nn import functional as F
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, ElectraForSequenceClassification, AdamW
from tqdm.notebook import tqdm

# GPU 사용
device = torch.device("cuda")

# =========================
# Dataset 만들어서 불러오기
# =========================

total_dataset = pd.read_csv('molologgELECTRA_data.csv')

# Nan 제거
total_dataset.replace('', np.nan, inplace=True)
total_dataset.dropna(inplace=True) 
# 중복 제거
total_dataset.drop_duplicates(subset=['document'], inplace=True)

train_dataset, test_dataset = train_test_split(total_dataset, test_size = 0.2, random_state = 42)

print(train_dataset.shape)
print(test_dataset.shape)


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


train_dataset = ReviewDataset(train_dataset)
test_dataset = ReviewDataset(test_dataset)


# =========
# 모델 생성
# =========

model = ElectraForSequenceClassification.from_pretrained("monologg/koelectra-base-v3-discriminator").to(device)


# =========
# 모델 학습
# =========

epochs = 2
batch_size = 64

optimizer = AdamW(model.parameters(), lr=1e-5)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=16, shuffle=True)


losses = []
accuracies = []

for i in range(epochs):
    total_loss = 0.0
    correct = 0
    total = 0
    batches = 0

    model.train()

    for input_ids_batch, attention_masks_batch, y_batch in tqdm(train_loader):
        optimizer.zero_grad()
        y_batch = y_batch.to(device)
        y_pred = model(input_ids_batch.to(device), attention_mask=attention_masks_batch.to(device))[0]
        loss = F.cross_entropy(y_pred, y_batch)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

        _, predicted = torch.max(y_pred, 1)
        correct += (predicted == y_batch).sum()
        total += len(y_batch)

        batches += 1
        if batches % 100 == 0:
            print("Batch Loss:", total_loss, "Accuracy:", correct.float() / total)
  
    losses.append(total_loss)
    accuracies.append(correct.float() / total)
    print("Train Loss:", total_loss, "Accuracy:", correct.float() / total)

print("losses: ", losses)
print("accuracies: ", accuracies)


# ===============================
# 테스트 데이터셋 정확도 확인하기
# ===============================

model.eval()

test_correct = 0
test_total = 0

for input_ids_batch, attention_masks_batch, y_batch in tqdm(test_loader):
    y_batch = y_batch.to(device)
    y_pred = model(input_ids_batch.to(device), attention_mask=attention_masks_batch.to(device))[0]
    _, predicted = torch.max(y_pred, 1)
    test_correct += (predicted == y_batch).sum()
    test_total += len(y_batch)

print("Accuracy:", test_correct.float() / test_total)

# 모델 저장하기
torch.save(model.state_dict(), "koelectra_small_v3.pt")