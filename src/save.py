# 노트
'''
pip freeze > requirements.txt <br/>
pip install -r requirements.txt
'''

# EDA
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
plt.rc('font', family=font_name)
import matplotlib
matplotlib.rcParams['axes.unicode_minus'] = False

# API DATA LOAD
import time
import urllib.request
import json
from pandas.io.json import json_normalize
from pandas import ExcelWriter
import xlsxwriter

# HYPOTHESIS TEST
from scipy import stats

# FEATURE ENGINEERING & MODELLING
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from statsmodels.stats.outliers_influence import variance_inflation_factor
from xgboost import XGBRegressor
from xgboost import plot_importance
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV

##################### DATA LOAD #####################

# PART 1 : DATE LOAD
# 서울시 우리마을가게 상권분석서비스(상권배후지-추정매출) 2020 데이터 추출
'''
2020년 상권배후지-추정매출 데이터가 CSV로 추출이 불가
API를 이용 데이터 추출후 2019년 2020년 데이터를 엑셀에 병합
'''
점포_2019 = pd.DataFrame()
for i in range(1,191658-152,1000-1):
    url = 'http://openapi.seoul.go.kr:8088/{}/json/VwsmTrdhlSelngQq/{}/{}/2020'.format('api',i, i + 999)
    response = urllib.request.urlopen(url)
    json_str = response.read().decode("utf-8")

    json_object = json.loads(json_str)
    body = [json_object['VwsmTrdhlSelngQq']['row']]
    append_data = json_normalize(json_object['VwsmTrdhlSelngQq']['row'])
    점포_2019 = 점포_2019.append(append_data)

writer = pd.ExcelWriter('data/Book1.xlsx', engine='xlsxwriter')
점포_2019.to_excel(writer, index=False, header=True)
writer.save()

# PART 2 : CSV Load
상주인구 = pd.read_csv('data/001_상주인구.csv')
소득소비 = pd.read_csv('data/002_소득소비.csv')
아파트 = pd.read_csv('data/003_아파트.csv')
점포 = pd.read_csv('data/004_점포.csv')
직장인구 = pd.read_csv('data/005_직장인구.csv')
집객시설 = pd.read_csv('data/006_집객시설.csv')
추정매출 = pd.read_csv('data/007_추정매출.csv')
생활인구 = pd.read_csv('data/008_생활인구.csv')

# PART 3 : DEFINE FUNCTION
plot_range = ['2020Q1','2020Q2','2020Q3','2020Q4','2021Q1']

##################### EDA START #####################

# EDA PART 1 : 상주인구
'''
1.정의 
* 총_상주인구_수
의미 : 조사대상인구를 계속 거주하고 있는 지역에 귀속시켜 계상한 인구를 말한다. 조사대상인구를 결정하는 한 방법으로서, 현재인구와 대조되는 개념이다. 현재인구는 조사시점에 실제로 있었던 장소에 귀속시켜 계상한 인구를 말한다.
* 총_가구_수
의미 : 현재 지역에 거주하는 가구수

그래프 1 분기별 총 상주인구와 가구수(Million) : 인구수 확인
그래프 2 상권코드별 상위10 상주인구&가구수 : 상권코드와 가구수 중복여부확인
그래프 3 상권코드별 하위10 상주인구&가구수 : 상권코드와 가구수 중복여부확인
'''
상주인구['분기_코드'] = 상주인구['기준_년_코드'].astype(str) + 'Q' + 상주인구['기준_분기_코드'].astype(str)
eda_분기별_상주인구 = 상주인구.groupby(['기준_년_코드','기준_분기_코드','분기_코드']).agg(총_상주인구_수=('총_상주인구_수','sum'), 총_가구_수=('총_가구_수','sum')).reset_index()
eda_분기별_상주인구['총_상주인구_수'] = eda_분기별_상주인구['총_상주인구_수']/1000000
eda_분기별_상주인구['총_가구_수'] = eda_분기별_상주인구['총_가구_수']/1000000

eda_상권코드_상주인구 = 상주인구.groupby(['상권_코드','상권_코드_명']).agg(총_상주인구_수=('총_상주인구_수','sum'), 총_가구_수=('총_가구_수','sum')).reset_index()
eda_상권코드_상주인구['총_상주인구_수'] = eda_상권코드_상주인구['총_상주인구_수']/1000000
eda_상권코드_상주인구['총_가구_수'] = eda_상권코드_상주인구['총_가구_수']/1000000

edatop_상권코드_상주인구 = eda_상권코드_상주인구.sort_values(by='총_상주인구_수', ascending=False).head(10)
edabtm_상권코드_상주인구 = eda_상권코드_상주인구.sort_values(by='총_상주인구_수', ascending=False).tail(10)
edatop_상권코드_가구수 = eda_상권코드_상주인구.sort_values(by='총_가구_수', ascending=False).head(10)
edabtm_상권코드_가구수 = eda_상권코드_상주인구.sort_values(by='총_가구_수', ascending=False).tail(10)

# 직장인구(PART5)와의 비교를 위한 세팅
eda_상주인구 = edatop_상권코드_상주인구['상권_코드_명']
eda_상권별_상주인구 = 상주인구[상주인구['상권_코드_명'].isin(eda_상주인구)]
eda_상권별_상주인구 = eda_상권별_상주인구.groupby(['기준_년_코드','기준_분기_코드','분기_코드', '상권_코드_명']).agg(
    총_상주인구_수=('총_상주인구_수','sum'),
    총_가구_수=('총_가구_수','sum')
).reset_index()

# 그래프 1
fig, ax = plt.subplots()
ax.plot(eda_분기별_상주인구['분기_코드'], eda_분기별_상주인구['총_상주인구_수'], label='Total Residents')
ax.plot(eda_분기별_상주인구['분기_코드'], eda_분기별_상주인구['총_가구_수'], label='Total Households')
ax.set_title("분기별 총 상주인구와 가구수(Million)", fontsize=18)
ax.set_xlabel('분기')
ax.set_ylabel('인구(M)')
ax.grid(linewidth=0.3)
plt.axvline(x='2020Q1', color='darkred', linestyle='--')
plt.text('2019Q4',1,'COVID19',rotation=90, color='darkred')
plt.xticks(rotation=45)
plt.legend(loc="upper right")
plt.show()

# 그래프 2
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(edatop_상권코드_상주인구['상권_코드_명'].astype(str), edatop_상권코드_상주인구['총_상주인구_수'], color='blue')
ax1.grid(True)
ax1.set_title("상권코드별 상위10 상주인구", fontsize=15)
ax1.set_ylabel('인구(M)')
ax2.barh(edatop_상권코드_가구수['상권_코드_명'].astype(str), edatop_상권코드_가구수['총_가구_수'], color='skyblue')
ax2.grid(True)
ax2.set_title("상권코드별 상위10 가구수", fontsize=15)
ax2.set_ylabel('인구(M)')
fig.suptitle('상권코드별 상위10 상주인구&가구수', fontsize=20)
plt.show(block=True)

# 그래프 3
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(edabtm_상권코드_상주인구['상권_코드_명'].astype(str), edabtm_상권코드_상주인구['총_상주인구_수'], color='red')
ax1.grid(True)
ax1.set_title("상권코드별 하위10 상주인구", fontsize=15)
ax1.set_ylabel('인구(M)')
ax2.barh(edabtm_상권코드_가구수['상권_코드_명'].astype(str), edabtm_상권코드_가구수['총_가구_수'], color='pink')
ax2.grid(True)
ax2.set_title("상권코드별 하위10 가구수", fontsize=15)
ax2.set_ylabel('인구(M)')
fig.suptitle('상권코드별 하위 10 상주인구&가구수', fontsize=20)
plt.show(block=True)

# EDA PART 2 : 소득소비
'''
**** 2020Q1 이후로 데이터는 업데이트 되어 있지 않았다.
질문1 : 코로나 시기에 소득이 줄어들었는가 ?
그래프 1 [분기별 소득과 지출 그래프] : 아니다. 코로나시기 이전 2018Q4에 이미 소득금액은 급격하게 줄어들었다. 하지만, 
지출금액은 2018Q4에도 지속적으로 비슷한 경사를 유지.
질문2 : 코로나 시기에 데이터는 무엇을 의미하나.
그래프 2 [2020 분기별 소득과 지출 그래프] : 2020Q1부터 소득과 지출이 전혀 변화가 없다. 수치가 업데이트 되지 않는것으로 파악된다.
질문3 : 종류별 지출내역은 코로나시기에 무엇을 말해주는가?
그래프 3 [분기별 지출내역 그래프] : 동일하게 2020Q1 이후 업데이트가 되지않았으며, 그 이전에도 별다른 UP&DOWN이 없음
'''
소득소비['분기_코드'] = 소득소비['기준_년_코드'].astype(str) + 'Q' + 소득소비['기준_분기_코드'].astype(str)
# NOTE : Omission of '소득_구간_코드'
소득소비_columns = ['월_평균_소득_금액','지출_총금액', '식료품_지출_총금액','의류_신발_지출_총금액','생활용품_지출_총금액',
                '의료비_지출_총금액','교통_지출_총금액','여가_지출_총금액','문화_지출_총금액','교육_지출_총금액','유흥_지출_총금액']

eda_분기별_소득소비 = 소득소비.groupby(['기준_년_코드','기준_분기_코드','분기_코드']).agg(
    월_평균_소득_금액=('월_평균_소득_금액','sum'),
    지출_총금액=('지출_총금액', 'sum'),
    식료품_지출_총금액=('식료품_지출_총금액', 'sum'),
    의류_신발_지출_총금액=('의류_신발_지출_총금액', 'sum'),
    생활용품_지출_총금액=('생활용품_지출_총금액', 'sum'),
    의료비_지출_총금액=('의료비_지출_총금액', 'sum'),
    교통_지출_총금액=('교통_지출_총금액', 'sum'),
    여가_지출_총금액=('여가_지출_총금액', 'sum'),
    문화_지출_총금액=('문화_지출_총금액', 'sum'),
    교육_지출_총금액=('교육_지출_총금액', 'sum'),
    유흥_지출_총금액=('유흥_지출_총금액', 'sum'),
).reset_index()

eda_분기별_소득소비[소득소비_columns] = eda_분기별_소득소비[소득소비_columns]/100000000
eda_2020_소득소비 = eda_분기별_소득소비[eda_분기별_소득소비['분기_코드'].isin(plot_range)]

# 분기별 소득소비 (전체분기)
fig, (ax1,ax2) = plt.subplots(2,1)
ax1.plot(eda_분기별_소득소비['분기_코드'], eda_분기별_소득소비['월_평균_소득_금액'])
ax1.set_title("분기별 소득금액(억)", fontsize=15)
ax1.set_ylabel('소득금액(억)')
ax1.grid(linewidth=0.3)
ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(eda_분기별_소득소비['분기_코드'], eda_분기별_소득소비['지출_총금액'])
ax2.set_title("분기별 지출금액(억)", fontsize=15)
ax2.set_ylabel('지출금액(억)')
ax2.grid(linewidth=0.3)
ax2.axvline(x='2020Q1', color='darkred', linestyle='--')
plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
fig.subplots_adjust(wspace=0.2, hspace=0.5)
fig.suptitle('분기별 소득&지출 금액(억)', fontsize=20)
plt.show()

# 분기별 소득소비 (2020Q1부터)plot_range
fig, (ax1,ax2) = plt.subplots(2,1)
ax1.plot(eda_2020_소득소비['분기_코드'], eda_2020_소득소비['월_평균_소득_금액'])
ax1.set_title("2020분기 소득금액(억)", fontsize=15)
ax1.set_ylabel('소득금액(억)')
ax1.grid(linewidth=0.3)
ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(eda_2020_소득소비['분기_코드'], eda_2020_소득소비['지출_총금액'])
ax2.set_title("2020분기 지출금액(억)", fontsize=15)
ax2.set_ylabel('지출금액(억)')
ax2.grid(linewidth=0.3)
ax2.axvline(x='2020Q1', color='darkred', linestyle='--')
plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
fig.subplots_adjust(wspace=0.2, hspace=0.5)
fig.suptitle('2020분기 소득&지출 금액(억)', fontsize=20)
plt.show()

fig, ax = plt.subplots()
ax.plot(eda_분기별_소득소비['분기_코드'], eda_분기별_소득소비['식료품_지출_총금액'], label='식료품_지출_총금액')
ax.plot(eda_분기별_상주인구['분기_코드'], eda_분기별_소득소비['의류_신발_지출_총금액'], label='의류_신발_지출_총금액')
ax.plot(eda_분기별_상주인구['분기_코드'], eda_분기별_소득소비['생활용품_지출_총금액'], label='생활용품_지출_총금액')
ax.plot(eda_분기별_상주인구['분기_코드'], eda_분기별_소득소비['의료비_지출_총금액'], label='의료비_지출_총금액')
ax.plot(eda_분기별_상주인구['분기_코드'], eda_분기별_소득소비['교통_지출_총금액'], label='교통_지출_총금액')
ax.plot(eda_분기별_상주인구['분기_코드'], eda_분기별_소득소비['여가_지출_총금액'], label='여가_지출_총금액')
ax.plot(eda_분기별_상주인구['분기_코드'], eda_분기별_소득소비['문화_지출_총금액'], label='문화_지출_총금액')
ax.plot(eda_분기별_상주인구['분기_코드'], eda_분기별_소득소비['교육_지출_총금액'], label='교육_지출_총금액')
ax.plot(eda_분기별_상주인구['분기_코드'], eda_분기별_소득소비['유흥_지출_총금액'], label='유흥_지출_총금액')
ax.set_title("분기별 지출내역(억)", fontsize=18)
ax.set_xlabel('분기')
ax.set_ylabel('지출금액(억)')
ax.grid(linewidth=0.3)
plt.axvline(x='2020Q1', color='darkred', linestyle='--')
plt.text('2019Q4',1,'COVID19',rotation=90, color='darkred')
plt.xticks(rotation=45)
plt.legend(loc="upper right")
plt.show()

# EDA PART 3 : 아파트
'''
***** 2019Q3와 2019Q4까지의 데이터 없음. 나머지 데이터는 존재함.
분기별 아파트 평균시가(억)와 단지수 그래프 : 2019Q3와 2019Q4 데이터 소실
'''
아파트['분기_코드'] = 아파트['기준_년_코드'].astype(str) + 'Q' + 아파트['기준_분기_코드'].astype(str)
eda_분기별_아파트 = 아파트.groupby(['기준_년_코드','기준_분기_코드','분기_코드']).agg(
    아파트_단지_수=('아파트_단지_수','sum'),
    아파트_평균_시가=('아파트_평균_시가', 'sum')
).reset_index()

eda_분기별_아파트['아파트_평균_시가'] = eda_분기별_아파트['아파트_평균_시가']/100000000

fig, (ax1,ax2) = plt.subplots(2,1)
ax1.plot(eda_분기별_아파트['분기_코드'], eda_분기별_아파트['아파트_평균_시가'])
ax1.set_title("분기별 아파트 평균시가(억)", fontsize=15)
ax1.set_ylabel('아파트 시가(억)')
ax1.grid(linewidth=0.3)
ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(eda_분기별_아파트['분기_코드'], eda_분기별_아파트['아파트_단지_수'])
ax2.set_title("아파트 단지수)", fontsize=15)
ax2.set_ylabel('단지수')
ax2.grid(linewidth=0.3)
ax2.axvline(x='2020Q1', color='darkred', linestyle='--')
plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
fig.subplots_adjust(wspace=0.2, hspace=0.5)
fig.suptitle('분기별 아파트 평균시가(억)와 단지수', fontsize=20)
plt.show()

# EDA PART 4 : 점포
'''
***** 2019Q1부터 데이터 존재.
***** 중요한 데이터. 하지만 예)한식음식점이 증가하는것이 유동인구 혹은 골목상권에 어떠한 영향이 있을까?
질문 1 : 분기별 점포수는 코로나 이후 얼마 줄었을까? 폐업과 같이 확인
그래프 1 [2019-2021 분기별 점포수] : 코로나시기에 증가하는 점포수. 하지만 2020Q1이후로 줄어드는 트렌드. 

질문 2 : 상위 15 점포의 변화는 어떨까 ?
그래프 2 & 3 [상위15 서비스업종별 점포 & 프랜차이즈 수] [서비스업종별 상위15 점포 & 프랜차이즈 수] :
첫벗째, 점포수 & 프랜차이즈 점포수는 크게 눈에띄게 하락하지 않았다.
두번째, 눈에 띄지않지만 줄어드는 개업점포수와 2020Q2 이후 증가하는 폐업수. 코로나의 영향이라 할수 있을만함 움직임. 
세번째, 코로나 기간인 2020Q1 상위 15 서비스업종에서 보이는 폐업수

질문 3 : y-axis의 차이로 질문2에 대한 답변이 여러운관계로 %Change.
그래프 4 & 5 [점포수 기준 상위 15 서비스업종 폐업점포 수 (%Change)]:
-전자상거래업 12퍼센트 상승
-일반교습학원 10퍼센트상승
-호프간이주점 7퍼센트 상승
-분식전문저 5퍼센트 하락
'''
점포['분기_코드'] = 점포['기준_년_코드'].astype(str) + 'Q' + 점포['기준_분기_코드'].astype(str)

# 분기별 점포수
eda_분기별_점포 = 점포.groupby(['기준_년_코드','기준_분기_코드','분기_코드']).agg(
    점포_수=('점포_수', 'sum'),
    개업_점포_수=('개업_점포_수', 'sum'),
    폐업_점포_수=('폐업_점포_수', 'sum'),
    프랜차이즈_점포_수=('프랜차이즈_점포_수', 'sum')
).reset_index()

# 그래프 1
fig = plt.figure()
gs = gridspec.GridSpec(2, 2)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, :])

ax1.plot(eda_분기별_점포['분기_코드'], eda_분기별_점포['점포_수'], label='점포_수')
ax1.set_title("분기별 점포 수", fontsize=12)
ax1.set_xlabel('분기')
ax1.set_ylabel('점포수')
ax1.grid(which='major', linestyle='--', linewidth=0.5)
ax1.grid(which='minor', linestyle=':', linewidth=0.5)

ax2.plot(eda_분기별_점포['분기_코드'], eda_분기별_점포['프랜차이즈_점포_수'], label='프랜차이즈_점포_수')
ax2.set_title("분기별 프랜차이즈_점포 수", fontsize=12)
ax2.set_xlabel('분기')
ax2.set_ylabel('점포수')
ax2.grid(which='major', linestyle='--', linewidth=0.5)
ax2.grid(which='minor', linestyle=':', linewidth=0.5)

ax3.plot(eda_분기별_점포['분기_코드'], eda_분기별_점포['개업_점포_수'], label='개업_점포_수', color='teal')
ax3.plot(eda_분기별_점포['분기_코드'], eda_분기별_점포['폐업_점포_수'], label='폐업_점포_수', color='orange')
ax3.set_title("분기별 개업&폐업 수", fontsize=12)
ax3.set_xlabel('분기')
ax3.set_ylabel('점포수')
ax3.grid(which='major', linestyle='--', linewidth=0.5)
ax3.grid(which='minor', linestyle=':', linewidth=0.5)

plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
fig.subplots_adjust(wspace=0.1, hspace=0.4)
fig.suptitle('2019-2021 분기별 점포수', fontsize=20)
ax3.legend()
plt.show()

# 업종별 점포수
eda_업종별_점포 = 점포.groupby(['기준_년_코드','기준_분기_코드','분기_코드','서비스_업종_코드_명']).agg(
    점포_수=('점포_수', 'sum'),
    개업_점포_수=('개업_점포_수', 'sum'),
    폐업_점포_수=('폐업_점포_수', 'sum'),
    프랜차이즈_점포_수=('프랜차이즈_점포_수', 'sum')
).reset_index()

eda_점포수 = pd.pivot_table(eda_업종별_점포, values = ['점포_수'], index=['서비스_업종_코드_명']).reset_index()
eda_점포수 = eda_점포수.sort_values(by='점포_수', ascending=False).head(15)
eda_점포수 = eda_점포수['서비스_업종_코드_명']

eda_업종별_점포 = pd.pivot_table(eda_업종별_점포, values = ['점포_수','개업_점포_수','폐업_점포_수','프랜차이즈_점포_수'], index=['서비스_업종_코드_명', '분기_코드']).reset_index()
eda_업종별_점포 = eda_업종별_점포[eda_업종별_점포['서비스_업종_코드_명'].isin(eda_점포수)]
eda_업종별_점포['점포_수_pchange'] = eda_업종별_점포.groupby('서비스_업종_코드_명', sort=False)['점포_수'].apply(lambda x: x.pct_change()).to_numpy()
eda_업종별_점포['개업_점포_수_pchange'] = eda_업종별_점포.groupby('서비스_업종_코드_명', sort=False)['개업_점포_수'].apply(lambda x: x.pct_change()).to_numpy()
eda_업종별_점포['폐업_점포_수_pchange'] = eda_업종별_점포.groupby('서비스_업종_코드_명', sort=False)['폐업_점포_수'].apply(lambda x: x.pct_change()).to_numpy()
eda_업종별_점포['프랜차이즈_점포_수_pchange'] = eda_업종별_점포.groupby('서비스_업종_코드_명', sort=False)['프랜차이즈_점포_수'].apply(lambda x: x.pct_change()).to_numpy()

# 그래프 2 : 점포수 기준 상위15 서비스업종별 점포 & 프랜차이즈 수
fig, (ax1, ax2) = plt.subplots(2,1)
ax1.set_title("점포수 기준 상위 15 서비스업종 점포 수", fontsize=15)
ax1.set_xlabel('분기')
for label, grp in eda_업종별_점포.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '점포_수',ax = ax1, label = label, linestyle='-', marker='o')
ax.legend(loc="upper right", fontsize=7)
for label, grp in eda_업종별_점포.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '프랜차이즈_점포_수',ax = ax2, label = label, linestyle='-', marker='o')
ax1.legend(fontsize=7, loc="upper right")
ax2.legend(fontsize=7, loc="upper right")
fig.subplots_adjust(wspace=0.1, hspace=0.4)
fig.suptitle('점포수 기준 상위15 서비스업종별 점포 & 프랜차이즈 수', fontsize=20)

# 그래프 3 : 점포수 기준 서비스업종별 상위15 점포 & 프랜차이즈 수
fig, (ax1,ax2) = plt.subplots(2,1)
ax1.set_title("점포수 기준 상위15 점포 개업점포 수", fontsize=15)
ax1.set_xlabel('분기')
for label, grp in eda_업종별_점포.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '개업_점포_수',ax = ax1, label = label, linestyle='-', marker='o')
ax2.set_title("점포수 기준 상위15 점포 폐업 수", fontsize=15)
ax2.set_xlabel('분기')
for label, grp in eda_업종별_점포.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '폐업_점포_수',ax = ax2, label = label, linestyle='-', marker='o')
ax1.legend(fontsize=7, loc="upper right")
ax2.legend(fontsize=7, loc="upper right")
fig.subplots_adjust(wspace=0.1, hspace=0.4)
fig.suptitle('점포수 기준 서비스업종별 상위15 점포 & 프랜차이즈 수', fontsize=20)

# 그래프 4 : 점포수 기준 상위 15 서비스업종 점포수 (%Change)
fig, ax = plt.subplots()
ax.set_title("점포수 기준 상위 15 서비스업종 점포수 (%Change)", fontsize=15)
ax.set_xlabel('% Change')
for label, grp in eda_업종별_점포.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '점포_수_pchange',ax = ax, label = label, linestyle='-', marker='o')
ax.legend(loc="upper right", fontsize=7)

# 그래프 5 : 점포수 기준 상위 15 서비스업종 폐업점포 수 (%Change)
fig, ax = plt.subplots()
ax.set_title("점포수 기준 상위 15 서비스업종 폐업점포 수 (%Change)", fontsize=15)
ax.set_xlabel('% Change')
for label, grp in eda_업종별_점포.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '폐업_점포_수_pchange',ax = ax, label = label, linestyle='-', marker='o')
ax.legend(loc="upper right", fontsize=7)


# EDA PART 5 : 직장인구
'''
*** 2019Q4 이후의 데이터는 업데이되있지 않다.
질문1 : 골목상권의 직장인구는 늘어나는가? 줄어드는가 ?
그래프 1 [분기별 직장인구(만명)] : 2019Q4 이후의 데이터는 업데이트 되어있지 않다. 즉 코로나 시기에 데이터 변화를 분석이 불가능하다.
하지만 분기별 소득&지출 금액과 비슷한시기 (2018Q4)인 2019Q1에 급격하게 직장인구가 줄어들었다. 
질문2 : 코로나 시기의 직장인구는 어떻게 되었는가?
그래프 2 [2020년 분기별 직장인구(만명)] : 동일하게 2019Q4 이후의 데이터가 업데이트 되어있지 않으므로 파악이 불가능하다.
질문3 : 분기별 상권의 직장인구의 분기별 변화는? 상주인구와의 비교는 어떻게 되는가.
그래프 3 [분기별 직장인구와 상주&거주인구(만명)] : 별다른 연관관계는 찾기 힘들다
질문4 : 상위 10 상권의 직장인구의 분기별 변화는? 상주인구와의 비교는 
그래프 4 [상권별 직장 & 상주인구(명)] : 눈에띄는 연관성이나 기울기는 확인할수 없음.
'''
직장인구['분기_코드'] = 직장인구['기준_년_코드'].astype(str) + 'Q' + 직장인구['기준_분기_코드'].astype(str)
eda_분기별_직장인구 = 직장인구.groupby(['기준_년_코드','기준_분기_코드','분기_코드']).agg(
    총_직장_인구_수=('총_직장_인구_수', 'sum'),
    남성_직장_인구_수=('남성_직장_인구_수', 'sum'),
    여성_직장_인구_수=('여성_직장_인구_수', 'sum'),
).reset_index()

eda_분기별_직장인구['총_직장_인구_수'] = eda_분기별_직장인구['총_직장_인구_수']/10000
eda_분기별_직장인구['남성_직장_인구_수'] = eda_분기별_직장인구['남성_직장_인구_수']/10000
eda_분기별_직장인구['여성_직장_인구_수'] = eda_분기별_직장인구['여성_직장_인구_수']/10000
eda_2020_직장인구 = eda_분기별_직장인구[eda_분기별_직장인구['분기_코드'].isin(plot_range)]

# 직장인구 그래프 1
fig, (ax1,ax2) = plt.subplots(2,1)
ax1.plot(eda_분기별_직장인구['분기_코드'], eda_분기별_직장인구['총_직장_인구_수'])
ax1.set_title("분기별 직장인구(만명)", fontsize=15)
ax1.set_ylabel('직장인구(만명)')
ax1.grid(linewidth=0.3)
ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(eda_분기별_직장인구['분기_코드'], eda_분기별_직장인구['남성_직장_인구_수'], label='남성 직장인구')
ax2.plot(eda_분기별_직장인구['분기_코드'], eda_분기별_직장인구['여성_직장_인구_수'], label='여성 직장인구')
ax2.set_title("분기별 남성&여성 인구수 (만명)", fontsize=15)
ax2.set_ylabel('직장인구(만명)')
ax2.grid(linewidth=0.3)
ax2.axvline(x='2020Q1', color='darkred', linestyle='--')
plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
fig.subplots_adjust(wspace=0.2, hspace=0.5)
fig.suptitle('분기별 직장인구(만명)', fontsize=20)
plt.legend(loc="upper right")
plt.show()

# 직장인구 그래프 2
fig, (ax1,ax2) = plt.subplots(2,1)
ax1.plot(eda_2020_직장인구['분기_코드'], eda_2020_직장인구['총_직장_인구_수'])
ax1.set_title("2020년 분기별 직장인구(만명)", fontsize=15)
ax1.set_ylabel('직장인구(만명)')
ax1.grid(linewidth=0.3)
ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(eda_2020_직장인구['분기_코드'], eda_2020_직장인구['남성_직장_인구_수'], label='남성 직장인구')
ax2.plot(eda_2020_직장인구['분기_코드'], eda_2020_직장인구['여성_직장_인구_수'], label='여성 직장인구')
ax2.set_title("2020년 분기별 남성&여성 인구수 (만명)", fontsize=15)
ax2.set_ylabel('직장인구(만명)')
ax2.grid(linewidth=0.3)
ax2.axvline(x='2020Q1', color='darkred', linestyle='--')
plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
fig.subplots_adjust(wspace=0.2, hspace=0.5)
fig.suptitle('2020년 분기별 직장인구(만명)', fontsize=20)
plt.legend(loc="upper right")
plt.show()

# 직장인구 & 상주인구 그래프 3
fig, (ax1,ax2) = plt.subplots(2,1)
ax1.plot(eda_분기별_직장인구['분기_코드'], eda_분기별_직장인구['총_직장_인구_수'])
ax1.set_title("분기별 직장인구(만명)", fontsize=15)
ax1.set_ylabel('직장인구(만명)')
ax1.grid(linewidth=0.3)
ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(eda_분기별_상주인구['분기_코드'], eda_분기별_상주인구['총_상주인구_수']*100, label='총_상주인구_수')
ax2.plot(eda_분기별_상주인구['분기_코드'], eda_분기별_상주인구['총_가구_수']*100, label='총_가구_수')
ax2.legend(loc="upper right")
ax2.set_title("분기별 총 상주인구와 가구수(만명)", fontsize=18)
ax2.set_ylabel('인구(만명)')
ax2.grid(linewidth=0.3)
ax2.axvline(x='2020Q1', color='darkred', linestyle='--')
plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
fig.subplots_adjust(wspace=0.2, hspace=0.5)
fig.suptitle('분기별 직장인구와 상주&거주인구(만명)', fontsize=20)
plt.legend(loc="upper right")
plt.show()

# 상위10 직장인구 & 상주인구 그래프 4
eda_직장인구 = 직장인구.groupby(['상권_코드_명']).agg(총_직장_인구_수=('총_직장_인구_수', 'sum')).reset_index()
eda_직장인구 = eda_직장인구.sort_values(by='총_직장_인구_수', ascending=False).head(10)
eda_직장인구 = eda_직장인구['상권_코드_명']
eda_상권별_직장인구 = 직장인구[직장인구['상권_코드_명'].isin(eda_직장인구)]
eda_상권별_직장인구 = eda_상권별_직장인구.groupby(['기준_년_코드','기준_분기_코드','분기_코드','상권_코드_명']).agg(
    총_직장_인구_수=('총_직장_인구_수', 'sum'),
    남성_직장_인구_수=('남성_직장_인구_수', 'sum'),
    여성_직장_인구_수=('여성_직장_인구_수', 'sum'),
).reset_index()

fig, (ax1, ax2) = plt.subplots(2,1)
ax1.set_title("총직장인구 기준 상위10 상권별 직장인구(명)", fontsize=15)
ax1.set_xlabel('분기')
for label, grp in eda_상권별_직장인구.groupby('상권_코드_명'):
    grp.plot(x = '분기_코드', y = '총_직장_인구_수',ax = ax1, label = label, linestyle='-', marker='o')
ax2.set_title("총직장인구 기준 상위10 상권별 상주인구(명)", fontsize=15)
ax2.set_xlabel('분기')
for label, grp in eda_상권별_상주인구.groupby('상권_코드_명'):
    grp.plot(x = '분기_코드', y = '총_상주인구_수',ax = ax2, label = label, linestyle='-', marker='o')
ax1.legend(fontsize=7, loc="upper right")
ax2.legend(fontsize=7, loc="upper right")
fig.subplots_adjust(wspace=0.1, hspace=0.4)
fig.suptitle('총직장인구 기준 상권별 직장 & 상주인구(명)', fontsize=20)

# EDA PART 6 : 집객시설
'''
*** 모든 데이터를 이용할수 있을것 같다고 생각했지만 2018Q1 이후의 데이터는 전혀 변화가 없다.
*** 집객시설의 데이터는 이용할수 없다. 하지만 2017Q4 이후의 대학교의 급격한 상승은 데이터 신뢰성에 의심이 간다.

질문1 : 분기별 각 집객시설은 어떻게 변화 하였는가.
그래프 1 [분기별 집객시설 모음] : 2018Q1 이후의 변화가 없으므로 특별한 분석이 불가능 

질문2 : 분기별 집객시설 수에는 어떻게 변화 하였는가.
그래프 2 [분기별 전체 집객시설 수] : 2018Q1 이후의 변화가 없는것은 동일하나 2017Q4이후로 가파른 상승을 한 집객시설수.
가파른 집객시설의 이유는 대학교의 수가 약 1300개 한분기 사이만에 증가한 이유. 데이터 신뢰에 의문. 
'''
집객시설['분기_코드'] = 집객시설['기준_년_코드'].astype(str) + 'Q' + 집객시설['기준_분기_코드'].astype(str)
eda_분기별_집객시설 = 집객시설.groupby(['기준_년_코드','기준_분기_코드','분기_코드']).agg(
    집객시설_수=('집객시설_수', 'sum'), 관공서_수=('관공서_수', 'sum'), 은행_수=('은행_수', 'sum'),
    종합병원_수=('종합병원_수', 'sum'), 일반_병원_수=('일반_병원_수', 'sum'), 약국_수=('약국_수', 'sum'),
    유치원_수=('유치원_수', 'sum'), 초등학교_수=('초등학교_수', 'sum'), 중학교_수=('중학교_수', 'sum'),
    고등학교_수=('고등학교_수', 'sum'), 대학교_수=('대학교_수', 'sum'), 백화점_수=('백화점_수', 'sum'),
    슈퍼마켓_수=('슈퍼마켓_수', 'sum'), 극장_수=('극장_수', 'sum'), 숙박_시설_수=('숙박_시설_수', 'sum'),
    공항_수=('공항_수', 'sum'), 철도_역_수=('철도_역_수', 'sum'), 버스_터미널_수=('버스_터미널_수', 'sum'),
    지하철_역_수=('지하철_역_수', 'sum'), 버스_정거장_수=('버스_정거장_수', 'sum')
).reset_index()
eda_분기별_집객시설['집객시설_합계'] = eda_분기별_집객시설.iloc[:,4:].sum(axis=1)

# 그래프 1 : 분기별 집객시설 모음
fig, ax = plt.subplots()
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['관공서_수'], label='관공서_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['은행_수'], label='은행_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['종합병원_수'], label='종합병원_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['일반_병원_수'], label='일반_병원_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['약국_수'], label='약국_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['유치원_수'], label='유치원_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['초등학교_수'], label='초등학교_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['중학교_수'], label='중학교_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['고등학교_수'], label='고등학교_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['대학교_수'], label='대학교_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['백화점_수'], label='백화점_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['슈퍼마켓_수'], label='슈퍼마켓_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['극장_수'], label='극장_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['숙박_시설_수'], label='숙박_시설_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['공항_수'], label='공항_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['철도_역_수'], label='철도_역_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['버스_터미널_수'], label='버스_터미널_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['지하철_역_수'], label='지하철_역_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['버스_정거장_수'], label='버스_정거장_수')
ax.set_title("분기별 집객시설 모음", fontsize=20)
ax.set_xlabel('분기')
ax.set_ylabel('수')
ax.grid(linewidth=0.3)
plt.axvline(x='2020Q1', color='darkred', linestyle='--')
plt.text('2019Q4',1,'COVID19',rotation=90, color='darkred')
plt.xticks(rotation=45)
plt.legend(loc="upper right")
plt.show()

# 그래프 2 : 분기별 전체 집객시설 수(만)
fig, (ax1,ax2) = plt.subplots(2,1)
ax1.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['집객시설_수']/10000, label='집객시설_수')
ax1.set_title("분기별 집객시설 수(만)", fontsize=20)
ax1.set_xlabel('분기')
ax1.set_ylabel('수(만)')
ax1.grid(linewidth=0.3)
ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['집객시설_합계']/10000, label='집객시설_합계')
ax2.set_title("분기별 모든 집객시설 합계(만)", fontsize=20)
ax2.set_xlabel('분기')
ax2.set_ylabel('수(만)')
ax2.grid(linewidth=0.3)
ax2.axvline(x='2020Q1', color='darkred', linestyle='--')
fig.subplots_adjust(wspace=0.2, hspace=0.5)
plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
plt.show()

# EDA PART 7 : 추정매출
'''
질문 1 : 분기별 매출은 줄어들었을까 ? 남성매출건수, 여성매출건수로 보면은 차이가 있을까?
그래프 1 [분기당 매출금액(10억)과 남성&여성 매출건수(1만)] : 분기별 매출은 코로나시기에 줄어들었으나, 2019년과 비교하여서 
상대적으로 높은 매출의 그래프. 남성 & 여성 매출건수는 분기별 매출과 매우 비슷한 그래프 형태를 띄고 있음. 
 
질문 2 : 분기별 매출금액과 점포수는 동일하게 움직일까 ? 
그래프 2 [분기별 매출금액(10억)과 점포수] : 코로나시기에 줄어든 매출금액과 반대로 점포수는 반대로 증가하였음을 보여준다.
 
질문 3 : 상하위 서비스업종별 매출의 분기별 차이는 ? 2019년 매출이 2020년 매출보다 높은이유를 설명하기 위한 차트로 충분한가?  
그래프 3 [2020-2019년 매출차액 상,하위 10개 서비스업종별 매출금액] : 의료품의 상승세와 가장많은 점포수를 가지고 있는 한식점의 하락은
코로나시기에도 불구하고 2020년의 매출이 2019년보다 높은 이유를 설명해준다. 
'''
추정매출['분기_코드'] = 추정매출['기준_년_코드'].astype(str) + 'Q' + 추정매출['기준_분기_코드'].astype(str)
eda_분기별_추정매출 = 추정매출.groupby(['기준_년_코드','기준_분기_코드','분기_코드']).agg(
    분기당_매출_금액=('분기당_매출_금액', 'sum'),
    분기당_매출_건수=('분기당_매출_건수', 'sum'),
    점포수=('점포수', 'sum'),
    남성_매출_건수=('남성_매출_건수', 'sum'),
    여성_매출_건수=('여성_매출_건수', 'sum'),
).reset_index()

# 그래프 1 : 분기당 매출금액(10억)과 남성&여성 매출건수(1만)
fig, ax = plt.subplots()
ax.plot(eda_분기별_추정매출['분기_코드'], eda_분기별_추정매출['분기당_매출_금액']/1000000000, label='분기당_매출_금액(10억)')
ax.plot(eda_분기별_추정매출['분기_코드'], eda_분기별_추정매출['남성_매출_건수']/10000, label='남성_매출_건수(1만)')
ax.plot(eda_분기별_추정매출['분기_코드'], eda_분기별_추정매출['여성_매출_건수']/10000, label='여성_매출_건수(1만)')
ax.set_title("분기당 매출금액(10억)과 남성&여성 매출건수(1만)", fontsize=20)
ax.set_xlabel('분기')
ax.set_ylabel('매출금액(10억),매출건수(1만)')
ax.grid(linewidth=0.3)
plt.axvline(x='2020Q1', color='darkred', linestyle='--')
plt.text('2019Q4',1,'COVID19',rotation=90, color='darkred')
plt.xticks(rotation=45)
plt.legend(loc="upper right")
plt.show()

# 그래프 2 : 분기당 매출금액(10억)과 점포수
fig, (ax1,ax2) = plt.subplots(2,1)
ax1.plot(eda_분기별_추정매출['분기_코드'], eda_분기별_추정매출['분기당_매출_금액']/1000000000, label='분기당_매출_금액(10억)')
ax1.set_title("분기별 매출금액(10억)", fontsize=15)
ax1.set_ylabel('매출금액(10억)')
ax1.grid(linewidth=0.3)
ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(eda_분기별_추정매출['분기_코드'], eda_분기별_추정매출['점포수'], label='점포수', color='orange')
ax2.set_title("분기별 점포수", fontsize=18)
ax2.set_ylabel('점포수')
ax2.grid(linewidth=0.3)
ax2.axvline(x='2020Q1', color='darkred', linestyle='--')
plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
fig.subplots_adjust(wspace=0.2, hspace=0.5)
fig.suptitle('분기별 매출금액(10억)과 점포수', fontsize=20)
plt.show()

# 그래프 3 : 2020-2019년 매출차액 상,하위 10개 서비스업종별 매출금액
eda_추정매출 = pd.pivot_table(추정매출, values = ['분기당_매출_금액'], index=['서비스_업종_코드_명'], columns=['기준_년_코드'], aggfunc=sum).reset_index()
eda_추정매출 = eda_추정매출.droplevel(0,axis=1).reset_index().rename_axis(columns=None)
eda_추정매출 = eda_추정매출.rename(columns={'': '서비스_업종_코드_명'})
eda_추정매출['차액'] = eda_추정매출[2020] - eda_추정매출[2019]
edatop_추정매출 = eda_추정매출.sort_values(by='차액', ascending=False).head(10)
edabtm_추정매출 = eda_추정매출.sort_values(by='차액', ascending=False).tail(10)

edatop_상권별_추정매출 = 추정매출[추정매출['서비스_업종_코드_명'].isin(edatop_추정매출['서비스_업종_코드_명'])]
edabtm_상권별_상주인구 = 추정매출[추정매출['서비스_업종_코드_명'].isin(edabtm_추정매출['서비스_업종_코드_명'])]

edatop_상권별_추정매출 = edatop_상권별_추정매출.groupby(['기준_년_코드','기준_분기_코드','분기_코드', '서비스_업종_코드_명']).agg(
    분기당_매출_금액=('분기당_매출_금액', 'sum'),
    분기당_매출_건수=('분기당_매출_건수', 'sum'),
    점포수=('점포수', 'sum'),
    남성_매출_건수=('남성_매출_건수', 'sum'),
    여성_매출_건수=('여성_매출_건수', 'sum'),
).reset_index()

edabtm_상권별_추정매출 = edabtm_상권별_상주인구.groupby(['기준_년_코드','기준_분기_코드','분기_코드','서비스_업종_코드_명']).agg(
    분기당_매출_금액=('분기당_매출_금액', 'sum'),
    분기당_매출_건수=('분기당_매출_건수', 'sum'),
    점포수=('점포수', 'sum'),
    남성_매출_건수=('남성_매출_건수', 'sum'),
    여성_매출_건수=('여성_매출_건수', 'sum'),
).reset_index()

edatop_상권별_추정매출['분기당_매출_금액'] = edatop_상권별_추정매출['분기당_매출_금액']/1000000000
edabtm_상권별_추정매출['분기당_매출_금액'] = edabtm_상권별_추정매출['분기당_매출_금액']/1000000000

fig, (ax1, ax2) = plt.subplots(2,1)
ax1.set_title("2020-2019년 매출차액 상위 10개 서비스업종별 매출금액(10억)", fontsize=15)
ax1.set_xlabel('분기')
for label, grp in edatop_상권별_추정매출.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '분기당_매출_금액', ax = ax1, label = label, linestyle='-', marker='o')
ax2.set_title("2020-2019년 매출차액 하위 10개 서비스업종별 매출금액(10억)", fontsize=15)
ax2.set_xlabel('분기')
for label, grp in edabtm_상권별_추정매출.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '분기당_매출_금액', ax = ax2, label = label, linestyle='-', marker='o')
ax1.legend(fontsize=7, loc="upper right")
ax2.legend(fontsize=7, loc="upper right")
fig.subplots_adjust(wspace=0.1, hspace=0.4)
fig.suptitle('2020-2019년 매출차액 상,하위 10개 서비스업종별 매출금액(10억)', fontsize=20)

# EDA PART 8 : 생활인구
'''
질문1 : 분기별 총생활인구
그래프 1 : 2018Q4이후 급격한 생활인구 상승. 코로나 이후 하향.

질문2 & 질문3 : 각 지역 분기별/연령대별/요일별 생활인구수
설명 : 상권코드의 숫자를 없앤후, '로' 앞에 위치한 지역이름을 동일지역으로 구분하고 그룹화.
그래프2 & 그래프3 : 분기별 총생활인구와 동일하게 2018Q4이후 상,하 모든지역 동일하게 상승.
코로나 이후 특정지역은 생활인구가 증가함. 
 
'''
생활인구['분기_코드'] = 생활인구['기준_년_코드'].astype(str) + 'Q' + 생활인구['기준_분기_코드'].astype(str)
생활인구['상권_병합'] = 생활인구['상권_코드_명'].str.replace('\d+', '')
생활인구['상권_병합'] = 생활인구['상권_병합'].str.rsplit('로', 1).str[0]

eda_분기별_생활인구 = 생활인구.groupby(['기준_년_코드','기준_분기_코드','분기_코드']).agg(
    총_생활인구_수=('총_생활인구_수', 'sum')
).reset_index()

eda_분기별_평균생활인구 = 생활인구.groupby(['기준_년_코드','기준_분기_코드','분기_코드']).agg(
    평균_생활인구=('총_생활인구_수', 'mean')
).reset_index()

eda_상권병합_생활인구 = 생활인구.groupby(['기준_년_코드','기준_분기_코드','분기_코드', '상권_병합']).agg(
    총_생활인구_수=('총_생활인구_수', 'sum'), 연령대_10_생활인구_수=('연령대_10_생활인구_수', 'sum'),
    연령대_20_생활인구_수=('연령대_20_생활인구_수', 'sum'), 연령대_30_생활인구_수=('연령대_30_생활인구_수', 'sum'),
    연령대_40_생활인구_수=('연령대_40_생활인구_수', 'sum'), 연령대_50_생활인구_수=('연령대_50_생활인구_수', 'sum'),
    연령대_60_이상_생활인구_수=('연령대_60_이상_생활인구_수', 'sum'), 월요일_생활인구_수=('월요일_생활인구_수', 'sum'),
    화요일_생활인구_수=('화요일_생활인구_수', 'sum'), 수요일_생활인구_수=('수요일_생활인구_수', 'sum'),
    목요일_생활인구_수=('목요일_생활인구_수', 'sum'), 금요일_생활인구_수=('금요일_생활인구_수', 'sum'),
    토요일_생활인구_수=('토요일_생활인구_수', 'sum'), 일요일_생활인구_수=('일요일_생활인구_수', 'sum'),
).reset_index()

eda_생활인구 = eda_상권병합_생활인구.groupby(['상권_병합']).agg(총_생활인구_수=('총_생활인구_수', 'sum')).reset_index()
edatop_상권병합_생활인구 = eda_생활인구.sort_values(by='총_생활인구_수', ascending=False).head(10)
edabtm_상권병합_생활인구 = eda_생활인구.sort_values(by='총_생활인구_수', ascending=False).tail(10)
edatop_상권병합_생활인구 = eda_상권병합_생활인구[eda_상권병합_생활인구['상권_병합'].isin(edatop_상권병합_생활인구['상권_병합'])]
edabtm_상권병합_생활인구 = eda_상권병합_생활인구[eda_상권병합_생활인구['상권_병합'].isin(edabtm_상권병합_생활인구['상권_병합'])]
edatop_상권병합_생활인구['총_생활인구_수'] = edatop_상권병합_생활인구['총_생활인구_수']/10000000
edabtm_상권병합_생활인구['총_생활인구_수'] = edabtm_상권병합_생활인구['총_생활인구_수']/10000000

# 그래프 1 : 분기당 총 생활인구(억)와 평균생활인구
fig, (ax1,ax2) = plt.subplots(2,1)
ax1.plot(eda_분기별_생활인구['분기_코드'], eda_분기별_생활인구['총_생활인구_수']/10000000, label='총_생활인구_수(10억)')
ax1.set_title("분기당 총 생활인구(억)", fontsize=20)
ax1.set_ylabel('생활인구(억)')
ax1.grid(linewidth=0.3)
ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(eda_분기별_평균생활인구['분기_코드'], eda_분기별_평균생활인구['평균_생활인구']/10000000, label='평균_생활인구', color='orange')
ax2.set_title("분기당 총 평균생활인구(억)", fontsize=20)
ax2.set_ylabel('생활인구(억)')
ax2.grid(linewidth=0.3)
ax2.axvline(x='2020Q1', color='darkred', linestyle='--')
plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
fig.subplots_adjust(wspace=0.2, hspace=0.5)
fig.suptitle('분기당 총 생활인구(억)와 평균생활인구', fontsize=20)
plt.show()

# 그래프 2 : 지역별 총 생활인구기준 상위 15지역의 총 생활인구 수(억)
fig, (ax1,ax2) = plt.subplots(2,1)
ax1.set_title("지역별 총 생활인구기준 상위 15지역의 총 생활인구 수(억)", fontsize=15)
ax1.set_xlabel('인구수(억)')
for label, grp in edatop_상권병합_생활인구.groupby('상권_병합'):
    grp.plot(x = '분기_코드', y = '총_생활인구_수',ax = ax1, label = label, linestyle='-', marker='o')
ax1.grid(linewidth=0.3)
ax1.legend(loc="upper right", fontsize=10)
ax2.plot(eda_분기별_생활인구['분기_코드'], eda_분기별_생활인구['총_생활인구_수']/10000000, label='총_생활인구_수(억)')
ax2.set_title("분기별 총 생활인구(억)", fontsize=15)
ax2.set_xlabel('분기')
ax2.set_ylabel('생활인구(억')
ax2.grid(linewidth=0.3)
ax2.axvline(x='2020Q1', color='darkred', linestyle='--')
fig.subplots_adjust(wspace=0.2, hspace=0.5)
fig.suptitle('지역별 총 생활인구기준 상위 15지역과 분기별 총 생활인구(억)', fontsize=20)
plt.legend(loc="upper right")
plt.show()

# 그래프 3 : 지역별 총 생활인구기준 하위 15지역의 총 생활인구 수(억)
fig, (ax1,ax2) = plt.subplots(2,1)
ax1.set_title("지역별 총 생활인구기준 하위 15지역의 총 생활인구 수(억)", fontsize=15)
ax1.set_xlabel('인구수(억)')
for label, grp in edabtm_상권병합_생활인구.groupby('상권_병합'):
    grp.plot(x = '분기_코드', y = '총_생활인구_수',ax = ax1, label = label, linestyle='-', marker='o')
ax1.grid(linewidth=0.3)
ax1.legend(loc="upper right", fontsize=10)
ax2.plot(eda_분기별_생활인구['분기_코드'], eda_분기별_생활인구['총_생활인구_수']/10000000, label='총_생활인구_수(억)')
ax2.set_title("분기별 총 생활인구(억)", fontsize=15)
ax2.set_xlabel('분기')
ax2.set_ylabel('생활인구(억')
ax2.grid(linewidth=0.3)
ax2.axvline(x='2020Q1', color='darkred', linestyle='--')
fig.subplots_adjust(wspace=0.2, hspace=0.5)
fig.suptitle('지역별 총 생활인구기준 하위 15지역과 분기별 총 생활인구(억)', fontsize=20)
plt.legend(loc="upper right")
plt.show()

##################### HYPOTHESIS TEST #####################

# PART 1 : 유동인구
#생활인구1920, 생활인구19, 생활인구20 데이터프레임 생성
생활인구1920 = 생활인구[(생활인구['기준_년_코드'] == 2019) | (생활인구['기준_년_코드'] == 2020)]
생활인구19=생활인구[생활인구['기준_년_코드']==2019]
생활인구20=생활인구[생활인구['기준_년_코드']==2020]

'''
'코로나 이전(2019년)과 이후(2020년) 골목상권의 유동인구가 감소하였다' 가설 검정
H0(귀무가설): 코로나 이전 골목상권의 유동인구 = 코로나 이후 골목상권의 유동인구
H1(대립가설): 코로나 이전 골목상권의 유동인구 > 코로나 이후 골목상권의 유동인구
'''

# STEP 1 : 정규성 검정
stats.ranksums(생활인구19['총_생활인구_수'], 생활인구20['총_생활인구_수'])

# STEP 2 : 등분산성 검정
print(stats.levene(생활인구19['총_생활인구_수'], 생활인구20['총_생활인구_수']))
print(stats.fligner(생활인구19['총_생활인구_수'], 생활인구20['총_생활인구_수']))
print(stats.bartlett(생활인구19['총_생활인구_수'], 생활인구20['총_생활인구_수']))

# STEP 3 : t 검정
t, p = stats.ttest_ind(생활인구19['총_생활인구_수'], 생활인구20['총_생활인구_수'], alternative='greater')
print("t = " + str(t))
print("p = " + str(p))

# STEP 4 : ttest(상권별)
가설검정_상권병합= ['풍성', '천호옛길', '천호대', '천중', '진황도', '올림픽', '양재대', '암사길', '성안', '성내',
       '상일', '상암', '명일', '동남', '구천면', '고덕', '강동대', '오금', '송파대', '송이',
       '삼전', '백제고분', '마천', '거마', '학동', '테헤란', '일원', '영동대', '언주', '압구정',
       '선릉', '삼성', '봉은사', '도산대', '도곡', '논현', '남부순환', '개포', '강남대', '서초중앙',
       '방배중앙', '효령', '청두곶길', '주흥길', '언남길', '신반포', '서초대', '사평대', '사임당',
       '방배', '반포대', '바우뫼', '마방', '방배천', '동산', '동광', '고무래', '소담길', '원신길',
       '양지길', '양산길', '호암', '행운길', '청림길', '청룡길', '중앙길', '조원중앙', '조원',
       '장군봉길', '인헌길', '은천', '양녕', '신원', '신사', '신림', '신림동길', '승방길', '서림길',
       '봉천', '복은길', '법원단지길', '미성길', '대학길', '당곡길', '남현길', '난향길', '난우길',
       '난곡', '낙성대역길', '국회단지길', '구암길', '관천', '관악', '흑석', '장승배기', '여의대방',
       '신대방길', '성대', '서달', '상도', '사당', '만양', '등용', '동작대', '대방동길', '노량진',
       '국사봉길', '영신', '영등포', '양평', '신길', '선유서', '선유', '디지털', '도신', '도림천',
       '도림', '대림', '당산', '국회대', '경인', '가마산', '시흥대', '벚꽃', '범안', '문성',
       '독산', '금하', '가산', '중앙', '우마길', '오류', '신도림', '새말', '부일', '구로중앙',
       '구로동', '공원', '고척', '개봉', '화곡', '초원', '초록마을', '월정', '우장산', '양천',
       '방화대', '등촌', '까치산', '공항대', '곰달래', '개화동', '강서', '가로공원', '지양', '은행정',
       '오목', '신월', '신목', '목동중앙서', '목동중앙북', '목동중앙본', '목동중앙', '목동중앙남', '목동',
       '목동동', '목동남', '효창원', '토정', '월드컵', '와우산', '양화진길', '양화', '신촌', '숭문길',
       '성지길', '성산', '성미산', '백범', '방울내', '모래내', '매봉산', '망원', '만리재옛길',
       '마포대', '동교', '독막', '도화길', '대흥', '광성', '홍제내길', '홍연길', '통일', '충정',
       '증가', '응암', '연희', '수색', '세무서길', '세검정', '북아현', '명지대길', '독립문', '가재울',
       '진흥', '증산서길', '증산', '은평', '연서', '역말', '서오릉', '불광천길', '갈현', '가좌',
       '한글비석', '석계', '상계', '동일', '공릉', '해등', '우이천', '시루봉', '삼양', '방학',
       '도봉산길', '도봉', '도당', '덕릉', '노해', '한천', '인수봉', '오패산', '수유', '솔샘',
       '솔매', '삼각산', '화랑', '창경궁', '지봉', '종암', '정릉', '장위', '장월', '인촌',
       '개운사길', '안암', '아리랑', '성북', '삼선교', '보문', '보국문', '동소문', '돌곶이', '길음',
       '중랑천', '용마산', '신내', '사가정', '봉화산', '봉우재', '면목', '망우', '답십리', '겸재',
       '휘경', '천장산', '제기', '전농', '장한', '이문', '왕산', '약령시', '서울시립대', '무학',
       '난계', '경희대', '자양번영', '자양', '아차산', '뚝섬', '능동', '긴고랑', '광나루', '한림말길',
       '청계천', '장터길', '용답중앙길', '용답길', '왕십리', '송정가길', '송정라길', '성수일', '성수이',
       '성덕정길', '서울숲길', '상원길', '사근동길', '무학봉길', '무수막길', '매봉길', '마조', '마장',
       '둘레길', '금호산길', '고산자', '후암', '회나무', '한남대', '한강대', '청파', '장문', '이태원',
       '이촌', '원효', '우사단', '신흥', '소월', '서빙고', '두텁바위', '대사관', '녹사평대', '퇴계',
       '청구', '장충단', '삼일대', '명동길', '동호', '다산', '필운대', '평창길', '창신길', '종',
       '자하문', '이화장길', '율곡', '옥인길', '숭인동길', '성균관', '삼청', '북촌', '백석동길',
       '명륜길', '돈화문', '계동길']

test1=[]
test2=[]
test3=[]

for i in 가설검정_상권병합:
    t, p = stats.ttest_ind(생활인구19[생활인구19['상권_병합']==i]['총_생활인구_수'], 생활인구20[생활인구20['상권_병합']==i]['총_생활인구_수'], alternative='greater')
    test1.append(i)
    test2.append(t)
    test3.append(p)
    print(i, "t = " + str(t), "p = " + str(p))

ttest = pd.DataFrame(
    {'i': test1,
     't': test2,
     'p': test3
    })

ttest.rename(columns={'i':'상권'}, inplace=True)
ttest['p<0.05'] = ttest['p']<0.05
ttest[ttest['p<0.05']==True]

# PART 2 : 매출액

# 추정매출20
추정매출20=추정매출[추정매출['기준_년_코드']==2020]
추정매출20=추정매출20.reset_index(drop=True)
#추정매출19
추정매출19=추정매출[추정매출['기준_년_코드']==2019]
추정매출19=추정매출19.reset_index(drop=True)
추정매출19['분기_코드'] = 추정매출19['기준_년_코드'].astype(str) + 'Q' + 추정매출19['기준_분기_코드'].astype(str)
추정매출20['분기_코드'] = 추정매출20['기준_년_코드'].astype(str) + 'Q' + 추정매출20['기준_분기_코드'].astype(str)

'''
'코로나 이전(2019년)과 이후(2020년) 골목상권의 매출액이 감소하였다' 가설 검정
H0(귀무가설): 코로나 이전 골목상권의 매출액 = 코로나 이후 골목상권의 매출액
H1(대립가설): 코로나 이전 골목상권의 매출액 > 코로나 이후 골목상권의 매출액
단측 검정
'''

# STEP 1 : 정규성 검정
stats.ranksums(추정매출19['분기당_매출_금액'], 추정매출20['분기당_매출_금액'])

# STEP 2 : 등분산성 검정
print(stats.levene(추정매출19['분기당_매출_금액'], 추정매출20['분기당_매출_금액']))

# STEP 3 : t 검정
from scipy import stats
t, p = stats.ttest_ind(추정매출19['분기당_매출_금액'], 추정매출20['분기당_매출_금액'], equal_var=False, alternative='greater') #등분산 검정결과 등분산이 아니였기 때문에 false를 입력
print("t = " + str(t))
print("p = " + str(p))

# STEP 4 : ttest (서비스업종별)
가설검정_서비스업종 = ['중식음식점', '패스트푸드점', '의약품', '일반의류', '일식음식점', '애완동물', '운동/경기용품', '화초',
       '컴퓨터및주변장치판매', '여관', '치과의원', '한식음식점', '한의원', '예술학원', '편의점',
       '호프-간이주점', '양식음식점', '분식전문점', '스포츠 강습', '육류판매', '일반의원', '노래방',
       '청과상', '고시원', '가구', '섬유제품', '슈퍼마켓', '전자상거래업', '당구장', '피부관리실',
       '화장품', '골프연습장', '핸드폰', 'PC방', '제과점', '커피-음료', '인테리어', '치킨전문점',
       '시계및귀금속', '의료기기', '세탁소', '신발', '철물점', '자동차수리', '조명용품', '미곡판매',
       '네일숍', '자동차미용', '문구', '일반교습학원', '스포츠클럽', '서적', '외국어학원', '미용실',
       '가방', '가전제품', '안경', '가전제품수리', '반찬가게', '수산물판매', '자전거 및 기타운송장비',
       '완구', '부동산중개업']

test1=[]
test2=[]
test3=[]

for i in 가설검정_서비스업종:
    t, p = stats.ttest_ind(추정매출19[추정매출19['서비스_업종_코드_명']==i]['분기당_매출_금액'], 추정매출20[추정매출20['서비스_업종_코드_명']==i]['분기당_매출_금액'], alternative='greater')
    test1.append(i)
    test2.append(t)
    test3.append(p)
    print(i, "t = " + str(t), "p = " + str(p))

ttest = pd.DataFrame(
    {'i': test1,
     't': test2,
     'p': test3
    })

ttest.rename(columns={'i':'서비스업종'}, inplace=True)
ttest['p<0.05'] = ttest['p'] < 0.05
ttest[ttest['p<0.05']==True]

##################### DATA MERGE #####################

# F01 : 추정매출
df = 추정매출[[
    '기준_년_코드','기준_분기_코드','상권_코드','상권_코드_명','서비스_업종_코드_명', '분기_코드', '분기당_매출_금액', '점포수',
    '남성_매출_비율','여성_매출_비율',
    '월요일_매출_비율','화요일_매출_비율','수요일_매출_비율','목요일_매출_비율','금요일_매출_비율','토요일_매출_비율','일요일_매출_비율',
    '연령대_10_매출_비율','연령대_20_매출_비율','연령대_30_매출_비율','연령대_40_매출_비율','연령대_50_매출_비율','연령대_60_이상_매출_비율',
    '시간대_00~06_매출_비율','시간대_06~11_매출_비율','시간대_11~14_매출_비율','시간대_14~17_매출_비율','시간대_17~21_매출_비율','시간대_21~24_매출_비율',
    '남성_매출_금액', '여성_매출_금액',
    '월요일_매출_금액', '화요일_매출_금액', '수요일_매출_금액', '목요일_매출_금액', '금요일_매출_금액', '토요일_매출_금액', '일요일_매출_금액',
    '연령대_10_매출_금액', '연령대_20_매출_금액', '연령대_30_매출_금액', '연령대_40_매출_금액', '연령대_50_매출_금액', '연령대_60_이상_매출_금액',
    '시간대_00~06_매출_금액', '시간대_06~11_매출_금액', '시간대_11~14_매출_금액', '시간대_14~17_매출_금액', '시간대_17~21_매출_금액', '시간대_21~24_매출_금액'
]]

# F02 : 점포
f_02 = 점포[[
    '기준_년_코드', '기준_분기_코드', '상권_코드', '상권_코드_명', '서비스_업종_코드_명', '분기_코드',
    '유사_업종_점포_수', '개업_점포_수', '폐업_점포_수', '프랜차이즈_점포_수'
]]
df = pd.merge(df, f_02, how='left', on=['기준_년_코드','기준_분기_코드','상권_코드','상권_코드_명','서비스_업종_코드_명','분기_코드'])

# F03 : 직장인구
f_03 = 직장인구[[
    '기준_년_코드', '기준_분기_코드', '상권_코드', '상권_코드_명', '분기_코드', '총_직장_인구_수',
    '남성_직장_인구_수','여성_직장_인구_수',
    '연령대_10_직장_인구_수','연령대_20_직장_인구_수','연령대_30_직장_인구_수','연령대_40_직장_인구_수','연령대_50_직장_인구_수','연령대_60_이상_직장_인구_수'
]]
f_03 = f_03.loc[f_03['기준_년_코드'].isin([2019,2020,2021])]
df = pd.merge(df, f_03, how='left', on=['기준_년_코드','기준_분기_코드','상권_코드','상권_코드_명','분기_코드'])

# F04 : 소득소비
f_04 = 소득소비[[
    '기준_년_코드', '기준_분기_코드', '상권_코드', '상권_코드_명', '분기_코드', '월_평균_소득_금액', '지출_총금액',
    '식료품_지출_총금액','의류_신발_지출_총금액','생활용품_지출_총금액','의료비_지출_총금액','교통_지출_총금액','여가_지출_총금액','문화_지출_총금액','교육_지출_총금액','유흥_지출_총금액'
]]
f_04 = f_04.loc[f_04['기준_년_코드'].isin([2019,2020,2021])]
df = pd.merge(df, f_04, how='left', on=['기준_년_코드','기준_분기_코드','상권_코드','상권_코드_명','분기_코드'])

# F05 : 상주인구
f_05 = 상주인구[[
    '기준_년_코드', '기준_분기_코드', '상권_코드', '상권_코드_명', '분기_코드', '총_상주인구_수',
    '남성_상주인구_수','여성_상주인구_수',
    '연령대_10_상주인구_수','연령대_20_상주인구_수','연령대_30_상주인구_수','연령대_40_상주인구_수','연령대_50_상주인구_수','연령대_60_이상_상주인구_수'
]]
f_05 = f_05.loc[f_05['기준_년_코드'].isin([2019,2020,2021])]
df = pd.merge(df, f_05, how='left', on=['기준_년_코드','기준_분기_코드','상권_코드','상권_코드_명','분기_코드'])

# F06 : 생활인구
f_06 = 생활인구[[
    '기준_년_코드', '기준_분기_코드', '상권_코드', '상권_코드_명', '분기_코드', '총_생활인구_수',
    '남성_생활인구_수','여성_생활인구_수',
    '연령대_10_생활인구_수','연령대_20_생활인구_수','연령대_30_생활인구_수','연령대_40_생활인구_수','연령대_50_생활인구_수','연령대_60_이상_생활인구_수',
    '시간대_1_생활인구_수', '시간대_2_생활인구_수', '시간대_3_생활인구_수', '시간대_4_생활인구_수', '시간대_5_생활인구_수', '시간대_6_생활인구_수'
]]
f_06 = f_06.loc[f_06['기준_년_코드'].isin([2019,2020,2021])]
df = pd.merge(df, f_06, how='left', on=['기준_년_코드','기준_분기_코드','상권_코드','상권_코드_명','분기_코드'])

##################### Simple model before data engineering #####################

# Step 1 : DROP 2019 Q1,Q2 (2019Q2 기간전의 소득소비와 직장인구의 데이터의 OUTLIER)
df_pre_eng = df.loc[(df['분기_코드'] != '2019Q1') & (df['분기_코드'] != '2019Q2')].reset_index(drop=True)
df_pre_eng = df_pre_eng[[
    '분기당_매출_금액', '서비스_업종_코드_명', '기준_분기_코드', '점포수',
    '남성_매출_비율', '여성_매출_비율',
    '월요일_매출_비율', '화요일_매출_비율', '수요일_매출_비율', '목요일_매출_비율', '금요일_매출_비율', '토요일_매출_비율', '일요일_매출_비율',
    '연령대_10_매출_비율', '연령대_20_매출_비율', '연령대_30_매출_비율', '연령대_40_매출_비율', '연령대_50_매출_비율', '연령대_60_이상_매출_비율',
    '시간대_00~06_매출_비율', '시간대_06~11_매출_비율', '시간대_11~14_매출_비율', '시간대_14~17_매출_비율', '시간대_17~21_매출_비율', '시간대_21~24_매출_비율',
    '유사_업종_점포_수', '개업_점포_수', '폐업_점포_수', '프랜차이즈_점포_수',
    '총_직장_인구_수',
    '월_평균_소득_금액', '지출_총금액',
    '총_상주인구_수',
    '총_생활인구_수'
]]
# Step 2 : Scaling
scale_feature = ['총_직장_인구_수','총_상주인구_수', '총_생활인구_수',
                 '점포수', '유사_업종_점포_수', '개업_점포_수', '폐업_점포_수', '프랜차이즈_점포_수',
                 '월_평균_소득_금액', '지출_총금액'
                 ]
scale_비율 = ['남성_매출_비율', '여성_매출_비율',
    '월요일_매출_비율', '화요일_매출_비율', '수요일_매출_비율', '목요일_매출_비율', '금요일_매출_비율', '토요일_매출_비율', '일요일_매출_비율',
    '연령대_10_매출_비율', '연령대_20_매출_비율', '연령대_30_매출_비율', '연령대_40_매출_비율', '연령대_50_매출_비율', '연령대_60_이상_매출_비율',
    '시간대_00~06_매출_비율', '시간대_06~11_매출_비율', '시간대_11~14_매출_비율', '시간대_14~17_매출_비율', '시간대_17~21_매출_비율', '시간대_21~24_매출_비율'
]

# Step 3 : Dummy Variables
enc = OneHotEncoder()
enc_df = pd.DataFrame(enc.fit_transform(df_pre_eng[['서비스_업종_코드_명']]).toarray()).astype(int)
df_pre_eng = pd.merge(df_pre_eng,enc_df,left_index=True,right_index=True)
del df_pre_eng['서비스_업종_코드_명']

# Step 4 : Scaling
scaler = StandardScaler()
#df_pre_eng[['분기당_매출_금액']] = scaler.fit_transform(df_pre_eng[['분기당_매출_금액']])
df_pre_eng['분기당_매출_금액'] = np.log(1+df_pre_eng['분기당_매출_금액']) #Log transformations reduce right hand skewness and hopefully make the variable more normal
df_pre_eng[scale_feature] = pd.DataFrame(scaler.fit_transform(df_pre_eng[scale_feature].T).T, columns=df_pre_eng[scale_feature].columns).values
df_pre_eng[scale_비율] = df_pre_eng[scale_비율]/100

# Step 5 : Distribution
fig, (ax1,ax2) = plt.subplots(2,1)
ax1.set_title("분기당 매출금액 분포(10억)")
ax1.hist(df['분기당_매출_금액']/1000000000, color = 'skyblue', edgecolor = 'blue',
         bins = int(180/5))
ax2.set_title("분기당 매출로그금액")
ax2.hist(df_pre_eng['분기당_매출_금액'], color = 'skyblue', edgecolor = 'blue',
         bins = int(180/5))
fig.suptitle('분기별 매출금액 분포비교', fontsize=20)
fig.subplots_adjust(wspace=0.2, hspace=0.5)
plt.show()

# Step 6 : Split
X, Y = df_pre_eng.iloc[:, 1:], df_pre_eng.iloc[:, 0]
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=0)
print(X_train.shape, y_train.shape, X_test.shape, y_test.shape, X_val.shape, y_val.shape)

# Step 7 : XGB_Regression Random
model = XGBRegressor(
    max_depth=8,
    n_estimators=300,
    min_child_weight=300,
    colsample_bytree=0.8,
    subsample=0.8,
    eta=0.3,
    seed=42)

model.fit(
    X_train,
    y_train,
    eval_metric="rmse",
    eval_set=[(X_train, y_train), (X_val, y_val)],
    verbose=True,
    early_stopping_rounds = 10)

xgb_train_pred = model.predict(X_train)
xgb_val_pred = model.predict(X_val)
xgb_test_pred = model.predict(X_test)
print('Train rmse : ', np.sqrt(mean_squared_error(y_train, xgb_train_pred))) #Train rmse: 0.9206997251428196
print('test mape : ',np.mean(np.abs((y_train - xgb_train_pred) / y_train)) * 100) #test mape : 3.7201277170412714
print('Validation rmse : ', np.sqrt(mean_squared_error(y_val, xgb_val_pred))) #Validation rmse: 1.0282463657056082
print('test mape : ',np.mean(np.abs((y_val - xgb_val_pred) / y_val)) * 100) #test mape : 4.121176078539861
print('Test rmse: : ', np.sqrt(mean_squared_error(y_test, xgb_test_pred))) #Test rmse: 1.0138469206304064
print('test mape : ',np.mean(np.abs((y_test - xgb_test_pred) / y_test)) * 100) #test mape : 4.055939611795765

# Step 8 : XGB_Regression Hyperparameter_Tune
xgb1 = XGBRegressor()
parameters = {'nthread':[3],
              'objective':['reg:linear'],
              'learning_rate': [.03, 0.05, .07],
              'max_depth': [5, 6, 7],
              'min_child_weight': [4],
              'silent': [1],
              'subsample': [0.7],
              'colsample_bytree': [0.7],
              'n_estimators': [300]}

xgb_grid = GridSearchCV(xgb1,
                        parameters,
                        cv = 2,
                        n_jobs = 5,
                        verbose=True)
xgb_grid.fit(X, Y)
print(xgb_grid.best_score_) #0.6934677293491974
print(xgb_grid.best_params_)
#{'colsample_bytree': 0.7, 'learning_rate': 0.07, 'max_depth': 7, 'min_child_weight': 4, 'n_estimators': 300, 'nthread': 3, 'objective': 'reg:linear', 'silent': 1, 'subsample': 0.7}

xgbgs_train_predict = xgb_grid.best_estimator_.predict(X_train)
xgbgs_test_predict = xgb_grid.best_estimator_.predict(X_test)
print('Train rmse:', np.sqrt(mean_squared_error(y_train, xgbgs_train_predict))) # Train rmse: 0.99123679942298
print('Traim mape : ',np.mean(np.abs((y_train - xgbgs_train_predict) / y_train)) * 100) # Train mape :  4.043447782253021
print('Test rmse:', np.sqrt(mean_squared_error(y_test, xgbgs_test_predict))) #Test rmse: 0.9858068042053384
print('Test mape : ',np.mean(np.abs((y_test - xgbgs_test_predict) / y_test)) * 100) #Test mape :  4.00961970732005

# Step 9 : Importance
plt.rcParams["figure.figsize"] = (20, 8)
plot_importance(xgb_grid.best_estimator_)
plt.yticks(fontsize=6)
plt.title('Simple model before data engineering using XGBregression')
plt.show()

##################### data engineering and modelling #####################

# Step 1 : adding features (비율)
#직장인구비율
df['연령대_10_직장_인구_비율'] = (df['연령대_10_직장_인구_수']/df['총_직장_인구_수'])*100
df['연령대_20_직장_인구_비율'] = (df['연령대_20_직장_인구_수']/df['총_직장_인구_수'])*100
df['연령대_30_직장_인구_비율'] = (df['연령대_30_직장_인구_수']/df['총_직장_인구_수'])*100
df['연령대_40_직장_인구_비율'] = (df['연령대_40_직장_인구_수']/df['총_직장_인구_수'])*100
df['연령대_50_직장_인구_비율'] = (df['연령대_50_직장_인구_수']/df['총_직장_인구_수'])*100
df['연령대_60_이상_직장_인구_비율'] = (df['연령대_60_이상_직장_인구_수']/df['총_직장_인구_수'])*100
df['남성_직장_인구_비율'] = (df['남성_직장_인구_수']/df['총_직장_인구_수'])*100
df['여성_직장_인구_비율'] = (df['여성_직장_인구_수']/df['총_직장_인구_수'])*100
#지출종류비율
df['식료품_지출_비율'] = (df['식료품_지출_총금액']/df['지출_총금액'])*100
df['의류_신발_지출_비율'] = (df['의류_신발_지출_총금액']/df['지출_총금액'])*100
df['생활용품_지출_비율'] = (df['생활용품_지출_총금액']/df['지출_총금액'])*100
df['의료비_지출_비율'] = (df['의료비_지출_총금액']/df['지출_총금액'])*100
df['교통_지출_비율'] = (df['교통_지출_총금액']/df['지출_총금액'])*100
df['여가_지출_비율'] = (df['여가_지출_총금액']/df['지출_총금액'])*100
df['문화_지출_비율'] = (df['문화_지출_총금액']/df['지출_총금액'])*100
df['교육_지출_비율'] = (df['교육_지출_총금액']/df['지출_총금액'])*100
df['유흥_지출_비율'] = (df['유흥_지출_총금액']/df['지출_총금액'])*100
#상주인구비율
df['연령대_10_상주인구_비율'] = (df['연령대_10_상주인구_수']/df['총_상주인구_수'])*100
df['연령대_20_상주인구_비율'] = (df['연령대_20_상주인구_수']/df['총_상주인구_수'])*100
df['연령대_30_상주인구_비율'] = (df['연령대_30_상주인구_수']/df['총_상주인구_수'])*100
df['연령대_40_상주인구_비율'] = (df['연령대_40_상주인구_수']/df['총_상주인구_수'])*100
df['연령대_50_상주인구_비율'] = (df['연령대_50_상주인구_수']/df['총_상주인구_수'])*100
df['연령대_60_이상_상주인구_비율'] = (df['연령대_60_이상_상주인구_수']/df['총_상주인구_수'])*100
df['남성_상주인구_비율'] = (df['남성_상주인구_수']/df['총_상주인구_수'])*100
df['여성_상주인구_비율'] = (df['여성_상주인구_수']/df['총_상주인구_수'])*100
#생활인구비율
df['연령대_10_생활인구_비율'] = (df['연령대_10_생활인구_수']/df['총_생활인구_수'])*100
df['연령대_20_생활인구_비율'] = (df['연령대_20_생활인구_수']/df['총_생활인구_수'])*100
df['연령대_30_생활인구_비율'] = (df['연령대_30_생활인구_수']/df['총_생활인구_수'])*100
df['연령대_40_생활인구_비율'] = (df['연령대_40_생활인구_수']/df['총_생활인구_수'])*100
df['연령대_50_생활인구_비율'] = (df['연령대_50_생활인구_수']/df['총_생활인구_수'])*100
df['연령대_60_이상_생활인구_비율'] = (df['연령대_60_이상_생활인구_수']/df['총_생활인구_수'])*100
df['남성_생활인구_비율'] = (df['남성_생활인구_수']/df['총_생활인구_수'])*100
df['여성_생활인구_비율'] = (df['여성_생활인구_수']/df['총_생활인구_수'])*100

df['시간대_1_생활인구_비율'] = (df['시간대_1_생활인구_수']/df['총_생활인구_수'])*100
df['시간대_2_생활인구_비율'] = (df['시간대_2_생활인구_수']/df['총_생활인구_수'])*100
df['시간대_3_생활인구_비율'] = (df['시간대_3_생활인구_수']/df['총_생활인구_수'])*100
df['시간대_4_생활인구_비율'] = (df['시간대_4_생활인구_수']/df['총_생활인구_수'])*100
df['시간대_5_생활인구_비율'] = (df['시간대_5_생활인구_수']/df['총_생활인구_수'])*100
df['시간대_6_생활인구_비율'] = (df['시간대_6_생활인구_수']/df['총_생활인구_수'])*100

# Step 2 : Feature selection after (2019Q1 & 2019Q2)
df_eng = df.loc[(df['분기_코드'] != '2019Q1') & (df['분기_코드'] != '2019Q2')].reset_index(drop=True)
df_eng = df_eng[[
    '분기당_매출_금액', '기준_분기_코드',
    '식료품_지출_비율', '의류_신발_지출_비율', '생활용품_지출_비율','의료비_지출_비율','교통_지출_비율','여가_지출_비율','문화_지출_비율','교육_지출_비율','유흥_지출_비율',
    '남성_매출_비율', '여성_매출_비율', '남성_직장_인구_비율', '여성_직장_인구_비율', '남성_상주인구_비율', '여성_상주인구_비율', '남성_생활인구_비율', '여성_생활인구_비율',
    '연령대_10_직장_인구_비율', '연령대_20_직장_인구_비율', '연령대_30_직장_인구_비율', '연령대_40_직장_인구_비율', '연령대_50_직장_인구_비율', '연령대_60_이상_직장_인구_비율',
    '연령대_10_상주인구_비율', '연령대_20_상주인구_비율', '연령대_30_상주인구_비율', '연령대_40_상주인구_비율', '연령대_50_상주인구_비율', '연령대_60_이상_상주인구_비율',
    '연령대_10_생활인구_비율', '연령대_20_생활인구_비율', '연령대_30_생활인구_비율', '연령대_40_생활인구_비율', '연령대_50_생활인구_비율', '연령대_60_이상_생활인구_비율',
    '시간대_1_생활인구_비율', '시간대_2_생활인구_비율', '시간대_3_생활인구_비율', '시간대_4_생활인구_비율', '시간대_5_생활인구_비율', '시간대_6_생활인구_비율'
]]
# Step 3 : Scaling
scale_비율 = ['남성_매출_비율', '여성_매출_비율']

# Step 4 : No dummy variables in 서비스_업종_코드_명
# Step 5 : Scaling
scaler = StandardScaler()
df_eng['분기당_매출_금액'] = np.log(1+df_eng['분기당_매출_금액']) #Log transformations reduce right hand skewness and hopefully make the variable more normal
df_eng[scale_비율] = df_eng[scale_비율]/100

# Step 5 : Split
X, Y = df_eng.iloc[:, 1:], df_eng.iloc[:, 0]
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=0)

# Step 6 : XGB_Regression Hyperparameter_Tune
xgb2 = XGBRegressor()
parameters = {'nthread':[3],
              'objective':['reg:linear'],
              'learning_rate': [.03, 0.05, .07],
              'max_depth': [5, 6, 7],
              'min_child_weight': [4],
              'silent': [1],
              'subsample': [0.7],
              'colsample_bytree': [0.7],
              'n_estimators': [300]}

xgb_grid2 = GridSearchCV(xgb2,
                        parameters,
                        cv = 2,
                        n_jobs = 5,
                        verbose=True)
xgb_grid2.fit(X, Y)
print(xgb_grid2.best_score_)
#0.25398606342292424
print(xgb_grid2.best_params_)
#{'colsample_bytree': 0.7, 'learning_rate': 0.07, 'max_depth': 7, 'min_child_weight': 4, 'n_estimators': 300, 'nthread': 3, 'objective': 'reg:linear', 'silent': 1, 'subsample': 0.7}

xgbgs2_train_predict = xgb_grid2.best_estimator_.predict(X_train)
xgbgs2_test_predict = xgb_grid2.best_estimator_.predict(X_test)
print('Train rmse:', np.sqrt(mean_squared_error(y_train, xgbgs2_train_predict))) #Train rmse: 1.6541276461866792
print('Traim mape : ',np.mean(np.abs((y_train - xgbgs2_train_predict) / y_train)) * 100) #Train mape :  7.082597456269241
print('Test rmse:', np.sqrt(mean_squared_error(y_test, xgbgs2_test_predict))) # Test rmse: 1.6458114260121803
print('Test mape : ',np.mean(np.abs((y_test - xgbgs2_test_predict) / y_test)) * 100) #Test mape :  7.029744998432188

# Step 7 : XGB_Regression Hyperparameter_Tune
plt.rcParams["figure.figsize"] = (20, 8)
plot_importance(xgb_grid2.best_estimator_)
plt.yticks(fontsize=8)
plt.title('Feature importance after data engineering using XGBregression')
plt.show()
