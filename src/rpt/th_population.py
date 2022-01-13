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
빅데이터_상권_분석 : 상권_생활인구
분석 결과 1 : 2018Q4에서 2019Q1으로 넘어가는 시기에 급격한 생활 인구 상승, 2020Q1부터 지속적으로 조금씩 하향.
2018년 4분기 대비 2019년 1분기에 어디가 가장 많이 늘었는지 파악 
-> 시군구: 관악구, 강남구, 강동구, 강서구, 광진구 등이 가장 많이 증가
-> 상권: 첫호옛길, 천중로39길, 방울내로9안길, 진황도로27길, 북아현로4길 등이 가장 많이 증가
분석 결과 2 : (2018년 4분기까지의 데이터 제외하고) 구별로 확인한 결과, 강남구가 압도적으로 많음 
구별 총 생활 인구 수 & 여성 생활 인구 수: 강남구>관악구>강동구>강서구>마포구 순으로 많고, 노원구<금천구<도봉구<강북구<용산구 순으로 적음
구별 남성 생활 인구 수: 강남구>관악구>강동구>강서구>서초구 순으로 많고, 노원구<도봉구<금천구<강북구<용산구 순으로 적음
(참고: 전체 데이터의 경우, 구별 총 생활 인구 수 & 구별 남성 생활 인구 수는 강남구, 관악구, 중구 순으로 많음, 노원구, 도봉구, 강북구가 가장 적음
구별 여성 생활 인구 수는 강남구, 관악구, 마포구 순으로 많음, 노원구, 금천구, 도봉구가 가장 적음)
분석 결과 3 : 상권별로 확인한 결과,
총 생활 인구 수: 홍익대학교 주변>북아현로4길>종로 청계 관광특구>명동 남대문 북창동 다동 무교동 관광특구>신촌역>선릉역2 순으로 많고, 
마포농수산물시장<동부청과시장<양재 화물트럭터미널앞1<번동시장<국회의사당역1<양재동꽃시장이 적음
남성 생활 인구 수: 홍익대학교 주변>북아현로4길>종로 청계 관광특구>명동 남대문 북창동 다동 무교동 관광특구>선릉역2>신촌역 순으로 많고, 
마포농수산물시장<동부청과시장<번동시장<양재 화물트럭터미널앞1<구의시장<양재동꽃시장이 적음
여성 생활 인구 수: 홍익대학교 주변>북아현로4길>신촌역>명동 남대문 북창동 다동 무교동 관광특구>신사동 가로수길>종로 청계 관광특구 순으로 많고, 
마포농수산물시장<국회의사당역1<동부청과시장<양재 화물트럭터미널앞1<양재동꽃시장<번동시장이 적음
"""

# 001 : Data Load
상권_생활인구 = setup_tradehub('상권_생활인구.csv')

# 002 : [EDA : LINE] Total Quarter View Plot
분기별_생활인구 = 상권_생활인구.groupby(['기준_년_코드', '기준_분기_코드', '분기_코드']).agg(총_생활인구_수=('총_생활인구_수', 'sum'), 남성_생활인구_수=('남성_생활인구_수', 'sum'), 여성_생활인구_수=('여성_생활인구_수', 'sum')).reset_index()
분기별_생활인구['총_생활인구_수'] = 분기별_생활인구['총_생활인구_수'] / 10000000 #천만
분기별_생활인구['남성_생활인구_수'] = 분기별_생활인구['남성_생활인구_수'] / 10000000
분기별_생활인구['여성_생활인구_수'] = 분기별_생활인구['여성_생활인구_수'] / 10000000

fig, (ax1,ax2) = plt.subplots(2,1)
ax1.plot(분기별_생활인구['분기_코드'], 분기별_생활인구['총_생활인구_수'])
ax1.set_title("분기별 생활인구(천만)", fontsize=15)
ax1.set_ylabel('생활인구(천만)')
ax1.grid(linewidth=0.3)
#ax1.axvline(x='2020Q1', color='darkred', linestyle='--')

ax2.plot(분기별_생활인구['분기_코드'], 분기별_생활인구['남성_생활인구_수'], label='남성 생활인구')
ax2.plot(분기별_생활인구['분기_코드'], 분기별_생활인구['여성_생활인구_수'], label='여성 생활인구')
ax2.set_title("분기별 남성 & 여성 생활인구(천만)", fontsize=15)
ax2.set_ylabel('생활인구(천만)')
ax2.grid(linewidth=0.3)
#ax2.axvline(x='2020Q1', color='darkred', linestyle='--')

plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
fig.subplots_adjust(wspace=0.2, hspace=0.5)
fig.suptitle('분기별 생활인구(천만)', fontsize=20)
plt.legend(loc="upper right")
plt.show()

# 분기별 생활인구 왜 늘었는지? 2018년 4분기 대비 2019년 1분기 증가율
상권_생활인구_2018_4 = 상권_생활인구[상권_생활인구['분기_코드'].str.contains("2018Q4")]
상권_생활인구_2019_1 = 상권_생활인구[상권_생활인구['분기_코드'].str.contains("2019Q1")]

# 상권_생활인구_2018_4 = 상권_생활인구_2018_4.groupby(['상권_코드_명']).agg(생활인구_2018Q4=('총_생활인구_수', 'sum'))
# 상권_생활인구_2019_1 = 상권_생활인구_2019_1.groupby(['상권_코드_명']).agg(생활인구_2019Q1=('총_생활인구_수', 'sum'))

상권_생활인구_2018_4 = 상권_생활인구_2018_4.groupby(['시군구']).agg(생활인구_2018Q4=('총_생활인구_수', 'sum'))
상권_생활인구_2019_1 = 상권_생활인구_2019_1.groupby(['시군구']).agg(생활인구_2019Q1=('총_생활인구_수', 'sum'))

# 상권_생활인구_1819 = pd.merge(상권_생활인구_2018_4, 상권_생활인구_2019_1, on='상권_코드_명')
상권_생활인구_1819 = pd.merge(상권_생활인구_2018_4, 상권_생활인구_2019_1, on='시군구')
상권_생활인구_1819['생활 인구 차이'] = 상권_생활인구_1819['생활인구_2019Q1']-상권_생활인구_1819['생활인구_2018Q4']
상권_생활인구_1819['생활 인구 차이(%)'] = ((상권_생활인구_1819['생활인구_2019Q1']-상권_생활인구_1819['생활인구_2018Q4'])/상권_생활인구_1819['생활인구_2018Q4'])*100
상권_생활인구_1819 = 상권_생활인구_1819.sort_values(by='생활 인구 차이', ascending=False)

# 003 : [EDA : LINE] Quarter View Plot, Category by Region
시군구_생활인구 = 상권_생활인구.groupby(['시군구','분기_코드']).agg(총_생활인구_수=('총_생활인구_수','sum'), 남성_생활인구_수=('남성_생활인구_수','sum'), 여성_생활인구_수=('여성_생활인구_수','sum')).reset_index()
시군구_생활인구 = 시군구_생활인구[시군구_생활인구['분기_코드'].str.contains("2019|2020|2021")]

# 총 생활 인구 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='총_생활인구_수',
             hue='시군구',
             data=시군구_생활인구)

plt.title('구별 총 생활 인구 수', fontsize=20)
plt.ylabel('총 생활 인구 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 남성 생활 인구 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='남성_생활인구_수',
             hue='시군구',
             data=시군구_생활인구)

plt.title('구별 남성 생활 인구 수', fontsize=20)
plt.ylabel('남성 생활 인구 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 여성 생활 인구 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='여성_생활인구_수',
             hue='시군구',
             data=시군구_생활인구)

plt.title('구별 여성 생활 인구 수', fontsize=20)
plt.ylabel('여성 생활 인구 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 004 : [EDA : BAR] Category by Region
시군구_생활인구2 = 시군구_생활인구.groupby(['시군구']).총_생활인구_수.mean().reset_index()
시군구_생활인구2 = 시군구_생활인구2.sort_values(by=['총_생활인구_수'], ascending=True)
시군구_생활인구2 = 시군구_생활인구2.set_index('시군구')

# 총 생활 인구 수 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_생활인구2.index, 시군구_생활인구2['총_생활인구_수'], color=my_colors)
plt.title('구별 총 생활 인구 수', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('총 생활 인구 수', fontsize=15)
plt.show();

시군구_생활인구2 = 시군구_생활인구.groupby(['시군구']).남성_생활인구_수.mean().reset_index()
시군구_생활인구2 = 시군구_생활인구2.sort_values(by=['남성_생활인구_수'], ascending=True)
시군구_생활인구2 = 시군구_생활인구2.set_index('시군구')

# 남성 생활 인구 수 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_생활인구2.index, 시군구_생활인구2['남성_생활인구_수'], color=my_colors)
plt.title('구별 남성 생활 인구 수', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('남성 생활 인구 수', fontsize=15)
plt.show();

시군구_생활인구2 = 시군구_생활인구.groupby(['시군구']).여성_생활인구_수.mean().reset_index()
시군구_생활인구2 = 시군구_생활인구2.sort_values(by=['여성_생활인구_수'], ascending=True)
시군구_생활인구2 = 시군구_생활인구2.set_index('시군구')

# 여성 생활 인구 수 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_생활인구2.index, 시군구_생활인구2['여성_생활인구_수'], color=my_colors)
plt.title('구별 여성 생활 인구 수', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('여성 생활 인구 수', fontsize=15)
plt.show();

# 005 : [EDA : BAR] Category by 상권_코드_명
상권_생활인구 = 상권_생활인구[상권_생활인구['분기_코드'].str.contains("2019|2020|2021")]
상권코드_생활인구 = 상권_생활인구.groupby(['상권_코드_명']).agg(총_생활인구_수=('총_생활인구_수', 'mean'), 남성_생활인구_수=('남성_생활인구_수', 'mean'), 여성_생활인구_수=('여성_생활인구_수', 'mean')).reset_index()

# 상위 10 / 하위 10 생활인구
top_상권코드_생활인구 = 상권코드_생활인구.sort_values(by=['총_생활인구_수'], ascending=False).head(10)
btm_상권코드_생활인구 = 상권코드_생활인구.sort_values(by=['총_생활인구_수'], ascending=False).tail(10)

# 상위 10 / 하위 10 남성 생활인구
top_상권코드_남성_생활인구 = 상권코드_생활인구.sort_values(by=['남성_생활인구_수'], ascending=False).head(10)
btm_상권코드_남성_생활인구 = 상권코드_생활인구.sort_values(by=['남성_생활인구_수'], ascending=False).tail(10)

# 상위 10 / 하위 10 여성 생활인구
top_상권코드_여성_생활인구 = 상권코드_생활인구.sort_values(by=['여성_생활인구_수'], ascending=False).head(10)
btm_상권코드_여성_생활인구 = 상권코드_생활인구.sort_values(by=['여성_생활인구_수'], ascending=False).tail(10)

# 총 생활 인구 수 시각화
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(top_상권코드_생활인구['상권_코드_명'].astype(str), top_상권코드_생활인구['총_생활인구_수'], color='blue')
ax1.grid(True)
ax1.set_title("상권코드별 상위10 생활 인구 수", fontsize=15)
ax1.set_ylabel('생활 인구 수')
ax2.barh(btm_상권코드_생활인구['상권_코드_명'].astype(str), btm_상권코드_생활인구['총_생활인구_수'], color='skyblue')
ax2.grid(True)
ax2.set_title("상권코드별 하위10 생활 인구 수", fontsize=15)
ax2.set_ylabel('생활 인구 수')
fig.suptitle('상권코드별 상위 10 / 하위 10 생활 인구 수', fontsize=20)
plt.show(block=True)

# 남성 생활 인구 수 시각화
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(top_상권코드_남성_생활인구['상권_코드_명'].astype(str), top_상권코드_남성_생활인구['남성_생활인구_수'], color='blue')
ax1.grid(True)
ax1.set_title("상권코드별 상위10 남성 생활 인구 수", fontsize=15)
ax1.set_ylabel('남성 생활 인구 수')
ax2.barh(btm_상권코드_남성_생활인구['상권_코드_명'].astype(str), btm_상권코드_남성_생활인구['남성_생활인구_수'], color='skyblue')
ax2.grid(True)
ax2.set_title("상권코드별 하위10 남성 생활 인구 수", fontsize=15)
ax2.set_ylabel('남성 생활 인구 수')
fig.suptitle('상권코드별 상위 10 / 하위 10 남성 생활 인구 수', fontsize=20)
plt.show(block=True)

# 여성 생활 인구 수 시각화
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(top_상권코드_여성_생활인구['상권_코드_명'].astype(str), top_상권코드_여성_생활인구['여성_생활인구_수'], color='blue')
ax1.grid(True)
ax1.set_title("상권코드별 상위10 여성 생활 인구 수", fontsize=15)
ax1.set_ylabel('여성 생활 인구 수')
ax2.barh(btm_상권코드_여성_생활인구['상권_코드_명'].astype(str), btm_상권코드_여성_생활인구['여성_생활인구_수'], color='skyblue')
ax2.grid(True)
ax2.set_title("상권코드별 하위10 여성 생활 인구 수", fontsize=15)
ax2.set_ylabel('여성 생활 인구 수')
fig.suptitle('상권코드별 상위 10 / 하위 10 여성 생활 인구 수', fontsize=20)
plt.show(block=True)