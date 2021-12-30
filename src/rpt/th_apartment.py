from src.setup.setup import setup_tradehub

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import font_manager, rc
import matplotlib
import seaborn as sns

# Setup
font_name = font_manager.FontProperties(fname="src/gulim.ttc").get_name()
plt.rc('font', family=font_name)
matplotlib.rcParams['axes.unicode_minus'] = False

"""
빅데이터_상권_분석 : 상권_아파트
분석 결과1: 분기별 아파트 평균 시가와 아파트 단지 수를 확인한 결과, 2020년 1분기에 급격히 상승하고 2021 2분기에 또 한번 상승한 것으로 파악됨.
분석 결과2: 구별로 확인한 결과, 
단지 수는 (평균적으로) 은평구, 강서구, 송파구 순으로 많고 최근에는 강서구, 송파구, 은평구 순으로 많음. 또한, 종로구, 중구, 노원구는 적음
평균 면적은 강남구, 서초구, 관악구 순으로 큼. 도봉구, 강북구, 노원구는 작음
평균 시가는 강남구, 서초구, 용산구 순으로 많고 강남구는 지속적으로 급격하게 상승하는 추세임. 강북구, 도봉구, 노원구는 낮음
분석 결과3: 상권별로 확인한 결과,
단지 수가 가장 많은 상권은 구로동로8길, 백제고분로 50길, 가장 적은 상권은 청량리수산시장, 역삼역_2 등
면적이 가장 넓은 상권은 가리봉시장, 청담역_1, 공덕역, 압구정 로데오거리_1, 가장 좁은 상권은 영등포역_1, 신림역_1 등
시가가 가장 높은 상권은 청담역_1, 대치역_1, 청담삼익시장, 압구정 로데오거리_1 등, 가장 낮은 상권은 새석관시장, 장한평역, 연신내역_3 등

"""

# 001 : Data Load
상권_아파트 = setup_tradehub('상권_아파트.csv')

# 002 : [EDA : LINE] Total Quarter View Plot
분기별_아파트 = 상권_아파트.groupby(['기준_년_코드','기준_분기_코드','분기_코드']).agg(아파트_단지_수=('아파트_단지_수','sum'),아파트_평균_시가=('아파트_평균_시가', 'sum')).reset_index()
분기별_아파트['아파트_평균_시가'] = 분기별_아파트['아파트_평균_시가']/100000000

fig, (ax1,ax2) = plt.subplots(2,1)
ax1.plot(분기별_아파트['분기_코드'], 분기별_아파트['아파트_평균_시가'])
ax1.set_title("분기별 아파트 평균 시가(억)", fontsize=15)
ax1.set_ylabel('아파트 시가(억)')
ax1.grid(linewidth=0.3)
ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(분기별_아파트['분기_코드'], 분기별_아파트['아파트_단지_수'])
ax2.set_title("아파트 단지 수", fontsize=15)
ax2.set_ylabel('단지 수')
ax2.grid(linewidth=0.3)
ax2.axvline(x='2020Q1', color='darkred', linestyle='--')

plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
fig.subplots_adjust(wspace=0.2, hspace=0.5)
fig.suptitle('분기별 아파트 평균시가(억)와 단지 수', fontsize=20)
plt.show();

# 003 : [EDA : LINE] Quarter View Plot, Category by Region
시군구_아파트 = 상권_아파트.groupby(['시군구','분기_코드']).agg(아파트_단지_수=('아파트_단지_수','sum'), 아파트_평균_면적=('아파트_평균_면적','sum'), 아파트_평균_시가=('아파트_평균_시가','sum')).reset_index()

#아파트 단지 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='아파트_단지_수',
             hue='시군구',
             data=시군구_아파트)

plt.title('구별 아파트 단지 수', fontsize=20)
plt.ylabel('아파트 단지 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.show();

#아파트 평균 면적 시각화
ax = sns.lineplot(x='분기_코드',
             y='아파트_평균_면적',
             hue='시군구',
             data=시군구_아파트)

plt.title('구별 아파트 평균 면적', fontsize=20)
plt.ylabel('아파트 평균 면적', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.show();

#아파트 평균 시가 시각화
ax = sns.lineplot(x='분기_코드',
             y='아파트_평균_시가',
             hue='시군구',
             data=시군구_아파트)

plt.title('구별 아파트 평균 시가', fontsize=20)
plt.ylabel('아파트 평균 시가', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.show();

# 004 : [EDA : BAR] Category by Region
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