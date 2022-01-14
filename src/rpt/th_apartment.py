from src.setup.setup import setup_tradehub

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import font_manager, rc
import matplotlib
import seaborn as sns
import pandas as pd

# Setup
font_name = font_manager.FontProperties(fname="src/BMDOHYEON_ttf.ttf").get_name()
plt.rc('font', family=font_name)
matplotlib.rcParams['axes.unicode_minus'] = False

"""
빅데이터_상권_분석 : 상권_아파트
분석 결과1: 분기별 아파트 평균 시가와 아파트 단지 수를 확인한 결과, 2020년 1분기에 급격히 상승하고 2021 2분기에 또 한번 상승한 것으로 파악됨.
2019년 4분기 대비 2020년 1분기에 어디가 가장 많이 증가했는지 파악 
-> 아파트 단지 수(상권): 오패산로52길, 백제고분로50길, 백제고분로34길, 암사길, 개봉로11길, 백제고분로32길, 초록마을로8길 등 가장 많이 증가
-> 아파트 평균 시가 차이(시군구): 선릉역1, 한강대로43길, 강남역1, 대치역2, 압구정 로데오거리1, 중구 명동역, 사평대로26길, 모래내로15길 등 가장 많이 증가
분석 결과2: 구별로 확인한 결과, 
평균 시가: 강남구의 아파트 평균 시가가 꾸준히 높고 최근에 급격하게 상승하는 추세이며, 다음은 용산구>서초구>송파구>마포구 순으로 높음. 도봉구<은평구<노원구<성북구<금천구의 평균 시가가 낮음
단지 수: 은평구>강서구>송파구>강남구>양천구 순으로 많고, 최근에는 강서구>송파구>은평구 순으로 많음. 노원구<중구<종로구는 적음
평균 면적: 서초구>강남구>용산구 순으로 크고, 최근에는 강남구>서초구>용산구 순으로 큼. 도봉구<노원구<성북구는 작음
분석 결과3: 상권별로 확인한 결과,
시가가 높은 상권은 청담역_1>대치역_1>청담삼익시장>압구정 로데오거리_1>청담역2 등, 낮은 상권은 아차산로15길<새석관시장<장한평역<연신내역_3<구로디지털1단지 등
단지 수가 많은 상권은 구로동로8길>백제고분로 50길>백제고분로34길>남부순환로70길>백제고분로22길 등, 적은 상권은 강변역, 율곡로16길, 청담삼익시장, 청담역1, 금남시장 등
면적이 넓은 상권은 가리봉시장>청담역_1>공덕역>압구정 로데오거리_1>강변역 등, 좁은 상권은 아차산로15길<영등포역_1<신림역_1<신설동역<가산디지털단지역_3 등
"""

# 001 : Data Load
상권_아파트 = setup_tradehub('상권_아파트.csv')

# 002 : [EDA : LINE] Total Quarter View Plot
분기별_아파트 = 상권_아파트.groupby(['기준_년_코드','기준_분기_코드','분기_코드']).agg(아파트_단지_수=('아파트_단지_수','sum'),아파트_평균_시가=('아파트_평균_시가', 'mean')).reset_index()
분기별_아파트['아파트_평균_시가'] = 분기별_아파트['아파트_평균_시가']/100000000

fig, (ax1,ax2) = plt.subplots(2,1)
ax1.plot(분기별_아파트['분기_코드'], 분기별_아파트['아파트_평균_시가'])
ax1.set_title("분기별 아파트 평균 시가(억)", fontsize=15)
ax1.set_ylabel('아파트 시가(억)')
ax1.grid(linewidth=0.3)
# ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(분기별_아파트['분기_코드'], 분기별_아파트['아파트_단지_수'])
ax2.set_title("아파트 단지 수", fontsize=15)
ax2.set_ylabel('단지 수')
ax2.grid(linewidth=0.3)
# ax2.axvline(x='2020Q1', color='darkred', linestyle='--')

plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
fig.subplots_adjust(wspace=0.2, hspace=0.5)
fig.suptitle('분기별 아파트 평균시가(억)와 단지 수', fontsize=20)
plt.show();

# 분기별 아파트 단지 수 왜 늘었는지? 평균 시가 왜 올랐는지? 2019년 4분기 대비 2020년 1분기 증가율
상권_아파트_2019_4 = 상권_아파트[상권_아파트['분기_코드'].str.contains("2019Q4")]
상권_아파트_2020_1 = 상권_아파트[상권_아파트['분기_코드'].str.contains("2020Q1")]

상권_아파트_2019_4 = 상권_아파트_2019_4.groupby(['시군구']).agg(아파트단지수_2019Q4=('아파트_단지_수','sum'),아파트평균시가_2019Q4=('아파트_평균_시가', 'mean'))
상권_아파트_2020_1 = 상권_아파트_2020_1.groupby(['시군구']).agg(아파트단지수_2020Q1=('아파트_단지_수','sum'),아파트평균시가_2020Q1=('아파트_평균_시가', 'mean'))

# 상권_아파트_2019_4 = 상권_아파트_2019_4.groupby(['상권_코드_명']).agg(아파트단지수_2019Q4=('아파트_단지_수','sum'),아파트평균시가_2019Q4=('아파트_평균_시가', 'sum'))
# 상권_아파트_2020_1 = 상권_아파트_2020_1.groupby(['상권_코드_명']).agg(아파트단지수_2020Q1=('아파트_단지_수','sum'),아파트평균시가_2020Q1=('아파트_평균_시가', 'sum'))

상권_아파트_1920 = pd.merge(상권_아파트_2019_4, 상권_아파트_2020_1, on='시군구')
# 상권_아파트_1920 = pd.merge(상권_아파트_2019_4, 상권_아파트_2020_1, on='상권_코드_명')
상권_아파트_1920['아파트 단지 수 차이'] = 상권_아파트_1920['아파트단지수_2020Q1']-상권_아파트_1920['아파트단지수_2019Q4']
상권_아파트_1920['아파트 단지 수 차이(%)'] = ((상권_아파트_1920['아파트단지수_2020Q1']-상권_아파트_1920['아파트단지수_2019Q4'])/상권_아파트_1920['아파트단지수_2019Q4'])*100
상권_아파트_1920['아파트 평균 시가 차이'] = 상권_아파트_1920['아파트평균시가_2020Q1']-상권_아파트_1920['아파트평균시가_2019Q4']
상권_아파트_1920['아파트 평균 시가 차이(%)'] = ((상권_아파트_1920['아파트평균시가_2020Q1']-상권_아파트_1920['아파트평균시가_2019Q4'])/상권_아파트_1920['아파트평균시가_2019Q4'])*100
상권_아파트_1920 = 상권_아파트_1920.sort_values(by='아파트 단지 수 차이', ascending=False)
상권_아파트_1920 = 상권_아파트_1920.sort_values(by='아파트 평균 시가 차이', ascending=False)

# 003 : [EDA : LINE] Quarter View Plot, Category by Region
시군구_아파트 = 상권_아파트.groupby(['시군구','분기_코드']).agg(아파트_단지_수=('아파트_단지_수','sum'), 아파트_평균_면적=('아파트_평균_면적','mean'), 아파트_평균_시가=('아파트_평균_시가','mean')).reset_index()

# 아파트 평균 시가 시각화
ax = sns.lineplot(x='분기_코드',
             y='아파트_평균_시가',
             hue='시군구',
             data=시군구_아파트)

plt.title('구별 아파트 평균 시가', fontsize=20)
plt.ylabel('아파트 평균 시가', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 아파트 단지 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='아파트_단지_수',
             hue='시군구',
             data=시군구_아파트)

plt.title('구별 아파트 단지 수', fontsize=20)
plt.ylabel('아파트 단지 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 아파트 평균 면적 시각화
ax = sns.lineplot(x='분기_코드',
             y='아파트_평균_면적',
             hue='시군구',
             data=시군구_아파트)

plt.title('구별 아파트 평균 면적', fontsize=20)
plt.ylabel('아파트 평균 면적', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 004 : [EDA : BAR] Category by Region
시군구_아파트2 = 시군구_아파트.groupby(['시군구']).아파트_평균_시가.mean().reset_index()
시군구_아파트2 = 시군구_아파트2.sort_values(by=['아파트_평균_시가'], ascending=True)
시군구_아파트2 = 시군구_아파트2.set_index('시군구')

#아파트 평균 시가 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_아파트2.index, 시군구_아파트2['아파트_평균_시가'], color=my_colors)
plt.title('구별 아파트 평균 시가', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('아파트 평균 시가', fontsize=15)
plt.show();

시군구_아파트2 = 시군구_아파트.groupby(['시군구']).아파트_단지_수.mean().reset_index()
시군구_아파트2 = 시군구_아파트2.sort_values(by=['아파트_단지_수'], ascending=True)
시군구_아파트2 = 시군구_아파트2.set_index('시군구')

# 아파트 단지 수 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_아파트2.index, 시군구_아파트2['아파트_단지_수'], color=my_colors)
plt.title('구별 아파트 단지 수', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('아파트 단지 수', fontsize=15)
plt.show();

시군구_아파트2 = 시군구_아파트.groupby(['시군구']).아파트_평균_면적.mean().reset_index()
시군구_아파트2 = 시군구_아파트2.sort_values(by=['아파트_평균_면적'], ascending=True)
시군구_아파트2 = 시군구_아파트2.set_index('시군구')

# 아파트 평균 면적 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_아파트2.index, 시군구_아파트2['아파트_평균_면적'], color=my_colors)
plt.title('구별 아파트 평균 면적', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('아파트 평균 면적', fontsize=15)
plt.show();

# 005 : [EDA : BAR] Category by 상권_코드_명
상권코드_아파트 = 상권_아파트.groupby(['상권_코드_명']).agg(아파트_단지_수=('아파트_단지_수','mean'), 아파트_평균_면적=('아파트_평균_면적','mean'), 아파트_평균_시가=('아파트_평균_시가','mean')).reset_index()

# 상위 10 / 하위 10 아파트 단지 수
top_상권코드_아파트_단지수 = 상권코드_아파트.sort_values(by=['아파트_단지_수'], ascending=False).head(10)
btm_상권코드_아파트_단지수 = 상권코드_아파트.sort_values(by=['아파트_단지_수'], ascending=False).tail(10)

# 상위 10 / 하위 10 아파트 면적
top_상권코드_아파트_면적 = 상권코드_아파트.sort_values(by=['아파트_평균_면적'], ascending=False).head(10)
btm_상권코드_아파트_면적 = 상권코드_아파트.sort_values(by=['아파트_평균_면적'], ascending=False).tail(10)

# 상위 10 / 하위 10 아파트 시가
top_상권코드_아파트_시가 = 상권코드_아파트.sort_values(by=['아파트_평균_시가'], ascending=False).head(10)
btm_상권코드_아파트_시가 = 상권코드_아파트.sort_values(by=['아파트_평균_시가'], ascending=False).tail(10)

# 아파트 평균 시가 시각화
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(top_상권코드_아파트_시가['상권_코드_명'].astype(str), top_상권코드_아파트_시가['아파트_평균_시가'], color='blue')
ax1.grid(True)
ax1.set_title("상권코드별 상위10 아파트 평균 시가", fontsize=15)
ax1.set_ylabel('아파트 평균 시가')
ax2.barh(btm_상권코드_아파트_시가['상권_코드_명'].astype(str), btm_상권코드_아파트_시가['아파트_평균_시가'], color='skyblue')
ax2.grid(True)
ax2.set_title("상권코드별 하위10 아파트 평균 시가", fontsize=15)
ax2.set_ylabel('아파트 평균 시가')
fig.suptitle('상권코드별 상위 10 / 하위 10 아파트 평균 시가', fontsize=20)
plt.show(block=True)

# 아파트 단지 수 시각화
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(top_상권코드_아파트_단지수['상권_코드_명'].astype(str), top_상권코드_아파트_단지수['아파트_단지_수'], color='blue')
ax1.grid(True)
ax1.set_title("상권코드별 상위10 아파트 단지 수", fontsize=15)
ax1.set_ylabel('아파트 단지 수')
ax2.barh(btm_상권코드_아파트_단지수['상권_코드_명'].astype(str), btm_상권코드_아파트_단지수['아파트_단지_수'], color='skyblue')
ax2.grid(True)
ax2.set_title("상권코드별 하위10 아파트 단지 수", fontsize=15)
ax2.set_ylabel('아파트 단지 수')
fig.suptitle('상권코드별 상위 10 / 하위 10 아파트 단지 수', fontsize=20)
plt.show(block=True)

# 아파트 평균 면적 시각화
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(top_상권코드_아파트_면적['상권_코드_명'].astype(str), top_상권코드_아파트_면적['아파트_평균_면적'], color='blue')
ax1.grid(True)
ax1.set_title("상권코드별 상위10 아파트 평균 면적", fontsize=15)
ax1.set_ylabel('아파트 평균 면적')
ax2.barh(btm_상권코드_아파트_면적['상권_코드_명'].astype(str), btm_상권코드_아파트_면적['아파트_평균_면적'], color='skyblue')
ax2.grid(True)
ax2.set_title("상권코드별 하위10 아파트 평균 면적", fontsize=15)
ax2.set_ylabel('아파트 평균 면적')
fig.suptitle('상권코드별 상위 10 / 하위 10 아파트 평균 면적', fontsize=20)
plt.show(block=True)