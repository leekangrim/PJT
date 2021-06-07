# 분류성능평가지표 - Precision(정밀도), Recall(재현율) and Accuracy(정확도)

> https://sumniya.tistory.com/26



|           |       | 실제 정답      |                |
| --------- | ----- | -------------- | -------------- |
| 분류 결과 |       | True           | False          |
|           | True  | True Positive  | False Positive |
|           | False | False Negative | True Negative  |





# 1. Precision(정밀도)

**정밀도**란 모델이 True라고 분류한 것 중에서 실제 True인 것의 비율입니다.  (Positive 중 True)

(즉, True예측 중 맞춘 비율 === Positive 중 True)

**Positive 정답률**, **PPV(Positive Predictive Value)**라고도 불립니다.

날씨 예측 모델이 맑다로 예측했는데, 실제 날씨가 맑았는지를 살펴보는 지표라고 할 수 있겠습니다.



아래와 같은 식으로 표현할 수 있습니다.

![image-20210318091953299](%EB%B6%84%EB%A5%98%EC%84%B1%EB%8A%A5%ED%8F%89%EA%B0%80%EC%A7%80%ED%91%9C%20-%20Precision(%EC%A0%95%EB%B0%80%EB%8F%84),%20Recall(%EC%9E%AC%ED%98%84%EC%9C%A8)%20and%20Accuracy(%EC%A0%95%ED%99%95%EB%8F%84).assets/image-20210318091953299.png)



# 2. Recall(재현율)

**재현율**이란 실제 True인 것 중에서 모델이 True라고 예측한 것의 비율입니다. 

(즉, 실제 True 중 맞춘 비율 === 실제 True 중 Positive)

통계학에서는 **sensitivity**으로, 그리고 다른 분야에서는 **hit rate**라는 용어로도 사용합니다.

실제 날씨가 맑은 날 중에서 모델이 맑다고 예측한 비율을 나타낸 지표



아래와 같은 식으로 표현할 수 있습니다.

![image-20210318092210554](%EB%B6%84%EB%A5%98%EC%84%B1%EB%8A%A5%ED%8F%89%EA%B0%80%EC%A7%80%ED%91%9C%20-%20Precision(%EC%A0%95%EB%B0%80%EB%8F%84),%20Recall(%EC%9E%AC%ED%98%84%EC%9C%A8)%20and%20Accuracy(%EC%A0%95%ED%99%95%EB%8F%84).assets/image-20210318092210554.png)



<hr>



Precision은 모델의 입장 
Recall은 실제 정답(data)의 입장
정답을 정답이라고 맞춘 경우를 바라봄

*"어떤 요소에 의해, 확실히 맑은 날을 예측할 수 있다면 해당하는 날에만 맑은 날이라고 예측하면 되겠다."*

이 경우에는 확실하지 않은 날에는 아에 예측을 하지 않고 보류하여 FP의 경우의 수를 줄여, Precision을 극도로 끌어올리는 일종의 편법입니다. 

예를 들어 한달 30일 동안 맑은 날이 20일이었는데, 확실한 2일만 맑다고 예측한다면, 당연히 맑다고 한 날 중에 실제 맑은 날(Precision)은 100%가 나오게 됩니다. 하지만 과연, 이러한 모델이 이상적인 모델일까요?따라서, 우리는 실제 맑은 20일 중에서 예측한 맑은 날의 수도 고려해 보아야합니다. 이 경우에는 Precision만큼 높은 결과가 나오지 않습니다. 

Precision과 함께 Recall을 함께 고려하면 실제 맑은 날들(즉, 분류의 대상이 되는 정의역, 실제 data)의 입장에서 우리의 모델이 맑다고 예측한 비율을 함께 고려하게 되어 제대로 평가할 수 있습니다. 

Precision과 Recall은 상호보완적
두 지표가 모두 높을 수록 좋은 모델입니다.



# 3. Precision-Recall Trade-off

![image-20210322134511404](%EB%B6%84%EB%A5%98%EC%84%B1%EB%8A%A5%ED%8F%89%EA%B0%80%EC%A7%80%ED%91%9C%20-%20Precision(%EC%A0%95%EB%B0%80%EB%8F%84),%20Recall(%EC%9E%AC%ED%98%84%EC%9C%A8)%20and%20Accuracy(%EC%A0%95%ED%99%95%EB%8F%84).assets/image-20210322134511404.png)

A는 실제 날씨가 맑은 날입니다. 그리고 B는 모델에서 날씨가 맑은 날이라고 예측한 것

b의 영역은 TP로 실제 맑은 날씨를 모델이 맑다고 제대로 예측한 영역

![image-20210322134635435](%EB%B6%84%EB%A5%98%EC%84%B1%EB%8A%A5%ED%8F%89%EA%B0%80%EC%A7%80%ED%91%9C%20-%20Precision(%EC%A0%95%EB%B0%80%EB%8F%84),%20Recall(%EC%9E%AC%ED%98%84%EC%9C%A8)%20and%20Accuracy(%EC%A0%95%ED%99%95%EB%8F%84).assets/image-20210322134635435.png)

모델의 입장에서 모두 맑은 날이라고만 예측하는 경우를 생각해봅시다. 

그렇게 되면 TN(d)의 영역이 줄어들게 되고 그에 따라 FN(a)의 영역 또한 줄게 됩니다. 

그러므로 Recall은 분모의 일부인 FN(a)영역이 줄기 때문에 Recall은 100%가 됩니다. 

즉, 여기서 A⊂B인 관계를 형성합니다. 

하지만, 주의할 것은 단순히 a의 영역만 줄어드는 것이 아니라 d의 영역과 a의 영역이 모두 c로 흡수된다는 것입니다. 

Precision의 경우에는 기존보다 FP(c)의 영역이 커져 Precision은 줄게 됩니다. 





# 결론
### 정밀도가 낮은 재현율이 높으면, True 예측 남발(True 적극적, False 소극적) : False 학습에 문제가 있는 것으로 예상됨, False 학습이 제대로 되지 않고 True 위주로 학습됨, 즉 False에 대한 데이터의 전처리를 분석해야한다!
