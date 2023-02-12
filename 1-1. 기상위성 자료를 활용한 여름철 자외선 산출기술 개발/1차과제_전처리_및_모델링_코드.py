# -*- coding: utf-8 -*-
"""1차과제_전처리_및_모델링_코드.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tb_SJcTCe_uKXshfNNTEfUZPq9eXBpAI

# 데이터 전처리

## 1) 월별 데이터 정렬 및 결측치 처리
- 2020.03월~ 2020.08월 , 2021.03월 ~ 2021.08월, 2022.06월 데이터 각각 처리  
- 예시: 202105 data

### Hive에서 다운받은 원본데이터 불러오기
"""

data = pd.read_csv('202105_uv.csv')

data = data.iloc[:,1:]

"""### 지역별, 날짜별, 시간별로 정렬"""

data = data.sort_values(['202105_uv.stn', '202105_uv.yyyymmdd', '202105_uv.hhnn'])

"""### 이상치(-999) 결측치로 변환"""

data.replace(-999, np.nan, inplace=True)

"""### 3차 스플라인 보간법을 이용하여 결측치 처리"""

data = data.fillna(data.interpolate(method='cubic'))

"""### 정렬 및 결측치 처리된 data csv파일로 저장"""

data.to_csv('202105.csv',encoding='utf-8-sig')

"""## 2) 데이터 통합

### 정렬 및 결측치 처리된 월별 데이터 통합
"""

import pandas as pd
from glob import glob

file_names = glob("C:\\Users\\82109\\Desktop\\결측치제거data*.csv") 
total = pd.DataFrame()

for file_name in file_names:
  temp = pd.read_csv(file_name) 
  temp.rename(columns = lambda x: x.split('_')[-1], inplace = True)
  total = pd.concat([total, temp])

total.to_csv('2003_2206.csv', encoding='utf-8-sig')

"""## 3) 데이터에 추가 변수 추가

- 13 : 제주 황해 (한경면)
- 105 : 강원도 강릉시 중앙동 63-3
- 108 : 서울특별시 종로구 송월동 11-2 (사직동)
- 112 : 인천광역시 중구 동인천동 25-59
- 115 : 경상북도 울릉군 울릉읍 사동리 57
- 131 : 충청북도 청주시 흥덕구 복대1동 265-22
- 132 : 충청남도 태안군 안면읍 승언리 산12-1
- 133 : 대전광역시 유성구 온천2동 20-4
- 138 : 경상북도 포항시 남구 송도로
- 143 : 대구광역시 동구 효목1동 산234-26
- 146 : 전라북도 전주시 덕진구 덕진동1가 1416-1
- 152 : 울산광역시 중구 병영2동 산8
- 156 : 광주광역시 북구 운암2동 32-25
- 159 : 부산광역시 중구 대청동 9-305
- 165 : 전라남도 목포시 고하대로 815 (연산동)

### 지역별 추가데이터 병합 후 원본데이터에 병합  
예시: stn-13(한경면), 2020년 data 병합

### 한경면의 2020년 추가 data
"""

import pandas as pd
from glob import glob

file_names=glob("C:\\Users\\82109\\Desktop\\기상청_추가 데이터(2)\\한경면\\2021\\*.csv") 
extra = pd.DataFrame() 

for file_name in file_names:
  temp = pd.read_csv(file_name)
  temp.rename(columns = lambda x: x.split('_')[-1], inplace = True)
  extra = pd.concat([extra, temp], axis=1)

extra.columns = [' format: day', 'hour', 'precipitation', ' format: day', 'hour',
       'precipitation_form', ' format: day', 'hour', 'temperature',
       ' format: day', 'hour', 'humidity', ' format: day', 'hour',
       'wind_dir', ' format: day', 'hour', 'velocity']

extra_2 = extra.drop([' format: day', 'hour'], axis=1, inplace=False)
extra_2 = extra_2.iloc[:4421, :]
extra_3 = extra.iloc[:, :2]
extra_4 = pd.concat([extra_3, extra_2], axis=1)
extra_4 = extra_4.rename(columns = {' format: day':'uv.yyyymmdd', 'hour':'uv.hhnn'})

"""### 한경면 2020년 data에서 각 월 추출 후 년도월일 변환  
- 예시: 2020 3월 
"""

extra_2003 = extra_4.iloc[:744, :]
extra_2003

extra_2003['uv.yyyymmdd'] = extra_2003['uv.yyyymmdd'].astype(int)

for i in range(1, 32):
    extra_2003['uv.yyyymmdd'].replace(i, 20220300+i, inplace=True)
    
extra_2003

"""### 2020 3월과 동일하게 3~8월 진행 후 2020년 data로 통합"""

extra_2020 = pd.concat([extra_2003, extra_2004, extra_2005, 
                        extra_2006, extra_2007, extra_2008])
extra_2020['uv.stn'] = 13
extra_2020

"""### 추가변수 2020년data csv파일로 저장"""

extra_2020.to_csv('C:\\Users\\82109\\Desktop\\기상청_추가 데이터(2)\\extra_2020_13.csv')

"""### 2020,2021년, 202206 추가변수 동일하게 진행

### 지역별 추가변수 통합
"""

import pandas as pd
from glob import glob

file_names=glob("C:\\Users\\82109\\Desktop\\기상청_추가 데이터(2)\\추가데이터_모음\\*.csv") 
add = pd.DataFrame() 

for file_name in file_names:
  temp = pd.read_csv(file_name) 
  temp.rename(columns = lambda x: x.split('_')[-1], inplace = True)
  add = pd.concat([add, temp]) 
add

"""## 4)기존 data와 병합"""

add = add.iloc[:, 1:]

data = pd.read_csv("C:\\Users\\82109\\Desktop\\기상청_결합본\\2003_2206.csv")
data = data.iloc[:, 3:]
data

data_2 = pd.merge(data, add,how='outer',on=['uv.yyyymmdd', 'uv.hhnn', 'uv.stn'])
data_2

"""### 제공 데이터는 6월 25일까지 --> 26일~30일 데이터 제거"""

data_2 = data_2.iloc[:846735, :]
data_2

"""### 추가데이터는 1시간 단위, 기존 데이터는 10분 단위 따라서 10분 단위 부분 NaN으로 병합
### 결측치 3차 스플라인 보간법을 이용하여 채우기
"""

data_2 = data_2.fillna(data_2.interpolate(method='cubic'))

"""## 5)lon, lat, height column 제거

의미가 동일한 변수를 여러개 사용할 시 의도치 않은 가중치를 부여할 수 있음  
stn(지역)이 동일할 때 lon(경도), lat(위도), height(관측높이)가 동일하므로 제거
"""

total = data_2.drop(['uv.lon','uv.lat','uv.height'], axis=1, inplace=False)

total

"""## 6)정규화

### 정규화 진행하지 않을 colums
"""

total1 = total.iloc[:,[0,1,2,3]]

"""### 정규화 진행할 columns"""

total2 = total.iloc[:,4:]

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
total2[:] = scaler.fit_transform(total2[:])

data_re = pd.concat([total1,total2],axis=1)
data_re

"""## 7) 통합 데이터 나누기
- 학습데이터: 202003~ 202108 (202106~ 202107 제외)  
- 검증데이터: 202106~202107  
- 테스트데이터: 202206
"""

a = 20151102
yy = a//10000
yy

mm = a%10000//100
mm

dd = a%100
dd

l = '{}-{:02d}-{:02d}'.format(yy,mm,dd)
type(l)

def convert(n):
    yy = n//10000
    mm = n%10000//100
    dd = n%100
    l = '{}-{:02d}-{:02d}'.format(yy,mm,dd)
    return l

data['yyyymmdd'] = data['yyyymmdd'].apply(convert)

"""## train, test 나누기"""

def abc(n):
    n = n//100
    n= n%10000
    return n

"""### 학습데이터+ 검증데이터"""

train=data_re[data_re['uv.yyyymmdd'].apply(abc)!=2206]

"""### 테스트데이터"""

test2=data_re[data_re['uv.yyyymmdd'].apply(abc)==2206]

"""### 학습데이터"""

train_1=train[(train['uv.yyyymmdd'].apply(abc)!=2106) & 
              (train['uv.yyyymmdd'].apply(abc)!=2107)]

"""### 검증데이터"""

train_2=train[(train['uv.yyyymmdd'].apply(abc)==2106) | 
              (train['uv.yyyymmdd'].apply(abc)==2107)

"""### 각 data csv파일로 저장"""

train_1.to_csv('train_추가본.csv',encoding='utf-8-sig')

train_2.to_csv('test_추가본.csv',encoding='utf-8-sig')

test2.to_csv('2206_추가본.csv',encoding='utf-8-sig')





"""# 회귀분석

### 예측할 202206 data를 제외한 나머지 data끼리 회귀분석 진행하여 유의하지 않은 변수들 찾기
"""

import pandas as pd

data = pd.read_csv('train_추가본.csv')
data2 = pd.read_csv('test_추가본.csv')

data3 = pd.concat([data,data2],axis=0)
data3 = data3.iloc[:, 1:]
data3.to_csv('202003-202108.csv', encoding='utf-8-sig')

data = pd.read_csv('202003-202108.csv', )
data

import statsmodels.api as sm
x = ['uv.yyyymmdd', 'uv.hhnn', 'uv.stn', 'uv.landtype', 'uv.band1',
       'uv.band2', 'uv.band3', 'uv.band4', 'uv.band5', 'uv.band6', 'uv.band7',
       'uv.band8', 'uv.band9', 'uv.band10', 'uv.band11', 'uv.band12',
       'uv.band13', 'uv.band14', 'uv.band15', 'uv.band16', 'uv.solarza',
       'uv.sateza', 'uv.esr', 'precipitation', 'form', 'temperature',
       'humidity', 'dir', 'velocity']
X = data[x]
X = sm.add_constant(X)
y = data['uv.uv']
res = sm.OLS(y, X).fit()
print(res.summary())

"""유의수준이 0.05일때  p-value가 유의수준보다 큰 변수는 회귀분석에서 유의하지 않은 변수이므로  
yyyymmdd, band15, precipitation 제거
"""





"""# 모델링

## 1) XGboost
## 2) LGBM
## 3) Randomforest

- 추가데이터 병합한 파일 사용  
- 다중공선성 있는 변수들 제거

#### 홈페이지 rmse검증을 통해 최적의 파라미터로 계속 수정

### 라이브러리 import 및 학습데이터 불러오기
"""

from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

from sklearn.model_selection import GridSearchCV  
from sklearn.model_selection import TimeSeriesSplit

from sklearn.metrics import mean_squared_error
from math import sqrt

import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')

from google.colab import drive
drive.mount('/content/drive')

train = pd.read_csv('/content/drive/MyDrive/공모전 모델링/train_추가본.csv', 
                    index_col=0)  
test = pd.read_csv('/content/drive/MyDrive/공모전 모델링/test_추가본.csv', index_col=0)  


trainX = train.drop(['uv.yyyymmdd', 'uv.band15', 'precipitation', 'uv.uv'], 
                    axis=1, inplace=False)
trainY = train['uv.uv']


testX = test.drop(['uv.yyyymmdd', 'uv.band15', 'precipitation', 'uv.uv'], 
                  axis=1, inplace=False)
testY = test['uv.uv']

"""### 1. XGBRegressor"""

cv = 4

paramGrid = {"subsample" : [0.5, 0.7, 0.9], 'max_depth' : [3, 5, 7, 9,11],
             'n_estimators' : [500, 1000, 10000], 'learning_rate' : [0.01, 0.1, 0.3]}

fit_params={"early_stopping_rounds":100, 
            "eval_metric" : "rmse", 
            "eval_set" : [[testX, testY]]}

model = XGBRegressor(random_state=42, tree_method='gpu_hist', gpu_id=0)

gridsearch = GridSearchCV(model, paramGrid, verbose=1,
                          cv=TimeSeriesSplit(n_splits=cv).get_n_splits([trainX, trainY]))

gridsearch.fit(trainX, trainY, **fit_params)

print(model)
print('GridSearchCV 최고 평균 정확도 수치: {:.4f}'.format(gridsearch.best_score_))
print('GridSearchCV 최적 하이퍼파라미터: ', gridsearch.best_params_)

scores_df = pd.DataFrame(gridsearch.cv_results_)
scores_df

"""### 최적의 파라미터로 다시 모델링"""

from sklearn.metrics import mean_squared_error
from math import sqrt

best_model_XGBR = gridsearch.best_estimator_
best_pred = best_model_XGBR.predict(testX)

rmse = sqrt(mean_squared_error(testY, best_pred))

print("훈련 세트 정확도: {:.4f}".format(best_model_XGBR.score(trainX, trainY)))
print("테스트 세트 정확도: {:.4f}".format(best_model_XGBR.score(testX, testY)))
print('{}\n rmse: {:.4f}'.format(best_model_XGBR, rmse))

"""### 예측할 data 불러오기 및 최적 파라미터 모델로 예측"""

real_test = pd.read_csv('/content/drive/MyDrive/공모전 모델링/2206_추가본.csv', 
                        index_col=0)  
real_testX = real_test.drop(['uv.yyyymmdd', 'uv.band15', 'precipitation', 
                             'uv.uv'], axis=1, inplace=False) 

real_pred = best_model_XGBR.predict(real_testX) 
print(real_pred)

"""### 2. LGBM"""

from lightgbm import LGBMRegressor

cv = 4

paramGrid = {"bagging_fraction" : [0.7], 'num_iterations' : [5000], 'max_depth':[7], 
             'min_data_in_leaf' : [8], 'learning_rate' : [0.03], 'colsample_bytree':[0.72], 
             'max_bin':[255]}

fit_params={"early_stopping_rounds":100,
            "eval_metric" : "rmse", 
            "eval_set" : [[testX, testY]]}


model_LGBMR = LGBMRegressor(random_state=42)


gridsearch_LGBMR = GridSearchCV(model_LGBMR, paramGrid, verbose=1,
                          cv=TimeSeriesSplit(n_splits=cv).get_n_splits([trainX, trainY]))

gridsearch_LGBMR.fit(trainX, trainY, **fit_params)

print(gridsearch_LGBMR)
print('gridsearch_RDFRCV 최고 평균 정확도 수치: {:.4f}'.format(gridsearch_LGBMR.best_score_))
print('gridsearch_RDFRCV 최적 하이퍼파라미터: ', gridsearch_LGBMR.best_params_)

# gridsearch_RDFRCV 객체의 cv_results_ 속성을 데이터 프레임으로 생성
scores_df = pd.DataFrame(gridsearch_LGBMR.cv_results_)
scores_df

"""### 최적의 파라미터로 다시 모델링"""

best_model_LGBMR = gridsearch_LGBMR.best_estimator_
best_pred = best_model_LGBMR.predict(testX)
rmse = sqrt(mean_squared_error(testY, best_pred)) 

print('{}\n rmse: {:.4f}'.format(best_model_LGBMR, rmse))

real_test = pd.read_csv('/content/drive/MyDrive/공모전 모델링/2206.csv', index_col=0)  

real_testX = real_test.drop(['uv.uv'], axis=1, inplace=False) 
real_pred = best_model_LGBMR.predict(real_testX)

"""### 예측할 data 불러오기 및 최적 파라미터 모델로 예측"""

real_test = pd.read_csv('/content/drive/MyDrive/공모전 모델링/2206_추가본.csv', 
                        index_col=0)  
real_testX = real_test.drop(['uv.yyyymmdd', 'uv.band15', 'precipitation', 
                             'uv.uv'], axis=1, inplace=False) 

real_pred = best_model_LGBMR.predict(real_testX) 
print(real_pred)

"""### 3. Random forest"""

from sklearn.ensemble import RandomForestRegressor
cv = 4
paramGrid = {"min_samples_leaf" : [8, 12, 18], 'min_samples_split' : [8, 16, 20], 
             'max_depth' : [6, 8, 10, 12], 'n_estimators' : [1000, 10000, 100000]}

model_RDFR = RandomForestRegressor(random_state=42)

gridsearch_RDFR = GridSearchCV(model_RDFR, paramGrid, verbose=1, 
                               cv=TimeSeriesSplit(n_splits=cv).get_n_splits([trainX, trainY]), 
                               scoring='neg_mean_squared_error', 
                               return_train_score=True,  n_jobs=-1)

gridsearch_RDFR.fit(trainX, trainY)

print(model_RDFR)
print('gridsearch_RDFRCV 최고 -mse 수치: {:.4f}'.format(gridsearch_RDFR.best_score_))
print('gridsearch_RDFRCV 최적 하이퍼파라미터: ', gridsearch_RDFR.best_params_)

scores_df = pd.DataFrame(gridsearch_RDFR.cv_results_)
scores_df

"""### 최적의 파라미터로 다시 모델링"""

best_model_RDFR = gridsearch_RDFR.best_estimator_
best_pred = best_model_RDFR.predict(testX)
rmse = sqrt(mean_squared_error(testY, best_pred))

print("훈련 세트 정확도: {:.4f}".format(best_model_RDFR.score(trainX, trainY)))
print("테스트 세트 정확도: {:.4f}".format(best_model_RDFR.score(testX, testY)))

print('{}\n rmse: {:.4f}'.format(best_model_RDFR, rmse))

"""### 예측할 data 불러오기 및 최적 파라미터 모델로 예측"""

real_test = pd.read_csv('/content/drive/MyDrive/공모전 모델링/2206_추가본.csv', 
                        index_col=0)  
real_testX = real_test.drop(['uv.yyyymmdd', 'uv.band15', 'precipitation', 
                             'uv.uv'], axis=1, inplace=False) 

real_pred = best_model_RDFR.predict(real_testX) 
print(real_pred)



"""### 여기부터 3가지 모델 모두 동일 과정

### rmse 검증을 위해 정규화 해제
"""

uv_min = -1.375246e+00
uv_max = 2.360000e+01

real_pred_final = real_pred * (uv_max - uv_min) + uv_min
real_pred_final

uv_df = pd.DataFrame(real_pred_final, columns=['uv.uv'])

"""### 기존 2206 data에 uv col 제거 후 예측한 uv col 병합"""

real_testX2 = real_testX.reset_index()
final = pd.concat([real_testX2, uv_df],axis=1)
final.drop(['index'], axis=1, inplace=True)

"""### 검증양식으로 예측data 변환

### 검증양식을 위해 제거했던 yyyymmdd column 병합

yymmdd = real_test['uv.yyyymmdd'].reset_index()
yymmdd = yymmdd.iloc[:,1]

final = pd.concat([final, yymmdd],axis=1)

### 양식에 맞게 정렬 후 uv column만 추출 및 csv파일로 저장
"""

data_2 = final.sort_values(['uv.yyyymmdd','uv.hhnn'])
data_2.tail(30)

uv = data_2['uv.uv']
uv = uv.reset_index()
uv = uv.iloc[:,1:]
test = pd.read_csv('/content/drive/MyDrive/공모전 모델링/검증양식.csv')
test = test.iloc[:,[0,1]]

final = pd.concat([test,uv],axis=1)
final.columns = ['YearMonthDayHourMinute', 'STN', 'UV']
final.to_csv('/content/drive/MyDrive/공모전 모델링/pred.csv', encoding='utf-8-sig')





"""## 최종모델 - LGBM

### 사용파라미터
* bagging_fraction : 0.72 
* num_iterations : 20000 
* max_depth:7 
* min_data_in_leaf : 8 
* learning_rate : 0.03
* colsample_bytree: 0.72
* scale_pos_weight: 1.5 
* lambda_l1: 0.1
* lambda_l2: 0.35
* early_stopping_rounds: 300
* n_splits : 4
"""

from lightgbm import LGBMRegressor

cv = 4

paramGrid = {"bagging_fraction" : [0.72], 'num_iterations' : [20000], 'max_depth':[7], 'min_data_in_leaf' : [8], 'learning_rate' : [0.03], 'colsample_bytree':[0.72],
              'scale_pos_weight': [1.5], 'lambda_l1':[0.1], 'lambda_l2':[0.35]}

fit_params={"early_stopping_rounds":300,
            "eval_metric" : "rmse", 
            "eval_set" : [[testX, testY]]}


model_LGBMR = LGBMRegressor(random_state=42)


gridsearch_LGBMR = GridSearchCV(model_LGBMR, paramGrid, verbose=1,
                          cv=TimeSeriesSplit(n_splits=cv).get_n_splits([trainX, trainY]))

gridsearch_LGBMR.fit(trainX, trainY, **fit_params)

print(gridsearch_LGBMR)
print('gridsearch_RDFRCV 최고 평균 정확도 수치: {:.4f}'.format(gridsearch_LGBMR.best_score_))
print('gridsearch_RDFRCV 최적 하이퍼파라미터: ', gridsearch_LGBMR.best_params_)

"""### 그 이후 최적파라미터로 모델링, 검증 데이터로 변환과정 동일"""