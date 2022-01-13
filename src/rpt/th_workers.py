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
빅데이터_상권_분석 : 상권_직장인구
분석 결과 1 : 2019 2분기에 급격하게 직장인구가 줄어들었으며, 2019 4분기 이후의 데이터는 업데이트 되어 있지 않음 (2019Q4 이후의 데이터가 모두 똑같음)
2019년 1분기 대비 2019년 2분기에 어디가 가장 많이 줄었는지 파악 
-> 시군구: 중구, 영등포구, 종로구, 마포구, 용산구 등이 가장 많이 감소
-> 상권: 명동 남대문 북창동 다동 무교동 관광특구, 종로구청, 여의도역, 구로디지털1단지, 을지로3가역 등이 가장 많이 감소
분석 결과 2 : 구별로 확인한 결과,
구별 총 직장 인구 수 & 구별 남성/여성 직장인구 수는 강남구, 중구, 서초구, 종로구, 영등포구 순으로 많음(다른 구에 비해 강남구가 압도적으로 많음), 직장 인구가 적은 구는 강북구, 노원구, 도봉구, 중랑구, 은평구 등
분석 결과 3 : 상권별로 확인한 결과,
총 직장 인구 수는 남대문 북창동 다동 무교동 관광특구, 강남역_1, 구로디지털1단지, 가산디지털단지역_2, 시청역_1 순으로 많고,
푸른터시장, 용두시장, 이태원제일시장, 신신림시장, 새석관시장이 적음
남성 직장 인구 수는 남대문 북창동 다동 무교동 관광특구, 강남역_1, 구로디지털1단지, 가산디지털단지역_2, 시청역_1 순으로 많고,
푸른터시장, 용두시장, 상계시장, 이태원제일시장, 새석관시장이 적음
여성 직장 인구 수는 남대문 북창동 다동 무교동 관광특구, 강남역_1, 구로디지털1단지, 롯데백화점, 선릉역_1 순으로 많고,
푸른터시장, 신신림시장, 용두시장, 이태원제일시장, 동서시장이 적음
분석 결과 4 : + 추가적으로 상주인구 혹은 생활인구과 연관성 확인해보기(correlation plot)
"""

# 001 : Data Load
상권_직장인구 = setup_tradehub('상권_직장인구.csv')

# 002 : [EDA : LINE] Total Quarter View Plot
분기별_직장인구 = 상권_직장인구.groupby(['기준_년_코드','기준_분기_코드','분기_코드']).agg(
    총_직장_인구_수=('총_직장_인구_수', 'sum'),
    남성_직장_인구_수=('남성_직장_인구_수', 'sum'),
    여성_직장_인구_수=('여성_직장_인구_수', 'sum')).reset_index()
분기별_직장인구['총_직장_인구_수'] = 분기별_직장인구['총_직장_인구_수']/10000
분기별_직장인구['남성_직장_인구_수'] = 분기별_직장인구['남성_직장_인구_수']/10000
분기별_직장인구['여성_직장_인구_수'] = 분기별_직장인구['여성_직장_인구_수']/10000

fig, (ax1,ax2) = plt.subplots(2,1)
ax1.plot(분기별_직장인구['분기_코드'], 분기별_직장인구['총_직장_인구_수'])
ax1.set_title("분기별 직장인구(만)", fontsize=13)
ax1.set_ylabel('직장인구(만)')
ax1.grid(linewidth=0.3)
#ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(분기별_직장인구['분기_코드'], 분기별_직장인구['남성_직장_인구_수'], label='남성 직장인구')
ax2.plot(분기별_직장인구['분기_코드'], 분기별_직장인구['여성_직장_인구_수'], label='여성 직장인구')
ax2.set_title("분기별 남성 & 여성 직장인구(만)", fontsize=13)
ax2.set_ylabel('직장인구(만)')
ax2.grid(linewidth=0.3)
#ax2.axvline(x='2020Q1', color='darkred', linestyle='--')

plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
fig.subplots_adjust(wspace=0.2, hspace=0.5)
fig.suptitle('분기별 직장인구(만)', fontsize=20)
plt.legend(loc="upper right")
plt.show()

# 분기별 직장인구 왜 줄었는지? 2019년 1분기 대비 2019년 2분기 감소율
상권_직장인구_2019_1 = 상권_직장인구[상권_직장인구['분기_코드'].str.contains("2019Q1")]
상권_직장인구_2019_2 = 상권_직장인구[상권_직장인구['분기_코드'].str.contains("2019Q2")]

# 상권_직장인구_2019_1 = 상권_직장인구_2019_1.groupby(['상권_코드_명']).agg(직장인구_2019Q1=('총_직장_인구_수', 'sum'))
# 상권_직장인구_2019_2 = 상권_직장인구_2019_2.groupby(['상권_코드_명']).agg(직장인구_2019Q2=('총_직장_인구_수', 'sum'))

상권_직장인구_2019_1 = 상권_직장인구_2019_1.groupby(['시군구']).agg(직장인구_2019Q1=('총_직장_인구_수', 'sum'))
상권_직장인구_2019_2 = 상권_직장인구_2019_2.groupby(['시군구']).agg(직장인구_2019Q2=('총_직장_인구_수', 'sum'))

# 상권_직장인구_1920 = pd.merge(상권_직장인구_2019_1, 상권_직장인구_2019_2, on='상권_코드_명')
상권_직장인구_1920 = pd.merge(상권_직장인구_2019_1, 상권_직장인구_2019_2, on='시군구')
상권_직장인구_1920['직장 인구 차이'] = 상권_직장인구_1920['직장인구_2019Q2']-상권_직장인구_1920['직장인구_2019Q1']
상권_직장인구_1920['직장 인구 차이(%)'] = ((상권_직장인구_1920['직장인구_2019Q2']-상권_직장인구_1920['직장인구_2019Q1'])/상권_직장인구_1920['직장인구_2019Q1'])*100
상권_직장인구_1920 = 상권_직장인구_1920.sort_values(by='직장 인구 차이', ascending=True)

# 003 : [EDA : LINE] Quarter View Plot, Category by Region
시군구_직장인구 = 상권_직장인구.groupby(['시군구','분기_코드']).agg(총_직장_인구_수=('총_직장_인구_수','sum'), 남성_직장_인구_수=('남성_직장_인구_수','sum'), 여성_직장_인구_수=('여성_직장_인구_수','sum')).reset_index()

# 총 직장 인구 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='총_직장_인구_수',
             hue='시군구',
             data=시군구_직장인구)

plt.title('구별 총 직장 인구 수', fontsize=20)
plt.ylabel('총 직장 인구 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 남성 직장 인구 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='남성_직장_인구_수',
             hue='시군구',
             data=시군구_직장인구)

plt.title('구별 남성 직장 인구 수', fontsize=20)
plt.ylabel('남성 직장 인구 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 여성 직장 인구 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='여성_직장_인구_수',
             hue='시군구',
             data=시군구_직장인구)

plt.title('구별 여성 직장 인구 수', fontsize=20)
plt.ylabel('여성 직장 인구 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 004 : [EDA : BAR] Category by Region
시군구_직장인구2 = 시군구_직장인구.groupby(['시군구']).총_직장_인구_수.mean().reset_index()
시군구_직장인구2 = 시군구_직장인구2.sort_values(by=['총_직장_인구_수'], ascending=True)
시군구_직장인구2 = 시군구_직장인구2.set_index('시군구')

# 총 직장 인구 수 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_직장인구2.index, 시군구_직장인구2['총_직장_인구_수'], color=my_colors)
plt.title('구별 총 직장 인구 수', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('총 직장 인구 수', fontsize=15)
plt.show();

시군구_직장인구2 = 시군구_직장인구.groupby(['시군구']).남성_직장_인구_수.mean().reset_index()
시군구_직장인구2 = 시군구_직장인구2.sort_values(by=['남성_직장_인구_수'], ascending=True)
시군구_직장인구2 = 시군구_직장인구2.set_index('시군구')

# 남성 직장 인구 수 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_직장인구2.index, 시군구_직장인구2['남성_직장_인구_수'], color=my_colors)
plt.title('구별 남성 직장 인구 수', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('남성 직장 인구 수', fontsize=15)
plt.show();

시군구_직장인구2 = 시군구_직장인구.groupby(['시군구']).여성_직장_인구_수.mean().reset_index()
시군구_직장인구2 = 시군구_직장인구2.sort_values(by=['여성_직장_인구_수'], ascending=True)
시군구_직장인구2 = 시군구_직장인구2.set_index('시군구')

# 여성 직장 인구 수 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_직장인구2.index, 시군구_직장인구2['여성_직장_인구_수'], color=my_colors)
plt.title('구별 여성 직장 인구 수', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('여성 직장 인구 수', fontsize=15)
plt.show();

# 005 : [EDA : BAR] Category by 상권_코드_명
상권코드_직장인구 = 상권_직장인구.groupby(['상권_코드_명']).agg(총_직장_인구_수=('총_직장_인구_수','mean'), 남성_직장_인구_수=('남성_직장_인구_수','mean'), 여성_직장_인구_수=('여성_직장_인구_수','mean')).reset_index()

# 상위 10 / 하위 10 직장인구
top_상권코드_직장인구 = 상권코드_직장인구.sort_values(by=['총_직장_인구_수'], ascending=False).head(10)
btm_상권코드_직장인구 = 상권코드_직장인구.sort_values(by=['총_직장_인구_수'], ascending=False).tail(10)

# 상위 10 / 하위 10 남성 직장인구
top_상권코드_남성_직장인구 = 상권코드_직장인구.sort_values(by=['남성_직장_인구_수'], ascending=False).head(10)
btm_상권코드_남성_직장인구 = 상권코드_직장인구.sort_values(by=['남성_직장_인구_수'], ascending=False).tail(10)

# 상위 10 / 하위 10 여성 직장인구
top_상권코드_여성_직장인구 = 상권코드_직장인구.sort_values(by=['여성_직장_인구_수'], ascending=False).head(10)
btm_상권코드_여성_직장인구 = 상권코드_직장인구.sort_values(by=['여성_직장_인구_수'], ascending=False).tail(10)

# 총 직장 인구 수 시각화
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(top_상권코드_직장인구['상권_코드_명'].astype(str), top_상권코드_직장인구['총_직장_인구_수'], color='blue')
ax1.grid(True)
ax1.set_title("상권코드별 상위10 직장 인구 수", fontsize=15)
ax1.set_ylabel('직장 인구 수')
ax2.barh(btm_상권코드_직장인구['상권_코드_명'].astype(str), btm_상권코드_직장인구['총_직장_인구_수'], color='skyblue')
ax2.grid(True)
ax2.set_title("상권코드별 하위10 직장 인구 수", fontsize=15)
ax2.set_ylabel('직장 인구 수')
fig.suptitle('상권코드별 상위 10 / 하위 10 직장 인구 수', fontsize=20)
plt.show(block=True)

# 남성 직장 인구 수 시각화
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(top_상권코드_남성_직장인구['상권_코드_명'].astype(str), top_상권코드_남성_직장인구['남성_직장_인구_수'], color='blue')
ax1.grid(True)
ax1.set_title("상권코드별 상위10 남성 직장 인구 수", fontsize=15)
ax1.set_ylabel('남성 직장 인구 수')
ax2.barh(btm_상권코드_남성_직장인구['상권_코드_명'].astype(str), btm_상권코드_남성_직장인구['남성_직장_인구_수'], color='skyblue')
ax2.grid(True)
ax2.set_title("상권코드별 하위10 남성 직장 인구 수", fontsize=15)
ax2.set_ylabel('남성 직장 인구 수')
fig.suptitle('상권코드별 상위 10 / 하위 10 남성 직장 인구 수', fontsize=20)
plt.show(block=True)

# 여성 직장 인구 수 시각화
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(top_상권코드_여성_직장인구['상권_코드_명'].astype(str), top_상권코드_여성_직장인구['여성_직장_인구_수'], color='blue')
ax1.grid(True)
ax1.set_title("상권코드별 상위10 여성 직장 인구 수", fontsize=15)
ax1.set_ylabel('여성 직장 인구 수')
ax2.barh(btm_상권코드_여성_직장인구['상권_코드_명'].astype(str), btm_상권코드_여성_직장인구['여성_직장_인구_수'], color='skyblue')
ax2.grid(True)
ax2.set_title("상권코드별 하위10 여성 직장 인구 수", fontsize=15)
ax2.set_ylabel('여성 직장 인구 수')
fig.suptitle('상권코드별 상위 10 / 하위 10 여성 직장 인구 수', fontsize=20)
plt.show(block=True)

# 006 : [EDA] 2021Q3 Data
상권_직장인구_2021_3 = 상권_직장인구[상권_직장인구['분기_코드'].str.contains("2021Q3")]
상권_직장인구_2021_3 = 상권_직장인구_2021_3.groupby(['시군구']).agg(총_직장_인구_수=('총_직장_인구_수', 'sum')).sort_values(by="총_직장_인구_수", ascending=False)
상권_직장인구_2021_3 = 상권_직장인구_2021_3.groupby(['상권_코드_명']).agg(총_직장_인구_수=('총_직장_인구_수', 'sum'))