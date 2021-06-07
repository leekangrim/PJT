# BERT

- SKT
  - https://www.youtube.com/watch?v=S42vDzJExIA&list=PL9mhQYIlKEhcIxjmLgm9X5BUtW5jMLbZD&index=5 (47:05 = 네이버 분류)
    - 학습 빨리 시키는 방법
      - 두 문장의 합친 단어의 개수인 max_seq_length=128 로 90% 학습시키고, 나머지 10%를 512로 학습 > 512와 비슷한 성능
      - 주의 : preprocessed 데이터를 만들 때와 학습시킬 때 max_seq_length를 일치시켜야함
        - 90%를 128 데이터로 만들어 놓고 10%를 512 데이터를 만들어 놓는다.
        - 128로 학습시키고 끝나면 512로 연장학습  
    - https://drive.google.com/drive/u/0/folders/1AcFPk1TqjrpCf1yslDbvpc5u-a5yeoXO
    - https://colab.research.google.com/drive/1Yr71eroueU9zqOE4ce0WejL-uKRh5O7G
- https://github.com/SKTBrain/KoBERT
  - https://colab.research.google.com/github/SKTBrain/KoBERT/blob/master/scripts/NSMC/naver_review_classifications_pytorch_kobert.ipynb

- ratsgo (KoBERT 흡사)
  - https://github.com/ratsgo/embedding



- HuggingFace BERT (bert-base-multilingual-cased)
  - https://github.com/deepseasw/bert-naver-movie-review
    - https://colab.research.google.com/drive/1tIf0Ugdqg4qT7gcxia3tL7und64Rv1dP
  - 경량화
    - https://zzaebok.github.io/



- Jangwon Park (ELECTRA)
  - https://monologg.kr/
    - https://github.com/monologg/KoELECTRA



- ETRI KorBERT 
  - https://github.com/snunlp/KR-BERT (NSMC 분류)
  
    <hr>
  - https://github.com/domyounglee/korbert-mecab-multigpu (KorQuard 분류)



- 카카오 개발자 박상길님 http://docs.likejazz.com/bert/
  - [카카오 브레인 이동현님의 PyTorch 구현](https://github.com/dhlee347/pytorchic-bert)  을 이용해 MRPC 태스크(두 문장의 유사도 판별)에 대해 Fine-tuning하고 성능을 측정했다.
  - 추천 시스템에 활용할 수 있을 것 같다..