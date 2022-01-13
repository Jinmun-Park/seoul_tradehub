from src.setup.setup import setup_tradehub

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import font_manager, rc
import matplotlib
import seaborn as sns

# Setup
font_name = font_manager.FontProperties(fname="src/BMDOHYEON_ttf.ttf").get_name()
plt.rc('font', family=font_name)
matplotlib.rcParams['axes.unicode_minus'] = False

"""
빅데이터_상권_분석 : 상권_상주인구
분석 결과 1 : 상주 인구와 가구 수의 <분기별 지표>를 분석한 결과, 2015Q2부터 데이터 사용이 가능하다는 것을 확인(상주 인구 &가구 수 모두 2015Q2에 급격하게 상승한 것으로 보아 그전 데이터 소실), 2015년을 제외하고 이후 크게 증가하거나 감소하지 않음
분석 결과 2 : (2015년 1분기까지의 데이터 제외하고)
분기별로 구별 상주인구를 확인한 결과, 관악구의 상주인구가 꾸준하게 가장 많고, 다음은 강서구, 강남구 순으로 많음, 또 종로구, 중구, 노원구의 상주인구가 적음
분기별로 구별 가구 수를 확인한 결과, 관악구의 가구 수가 가장 많고 분기마다 꾸준히 늘어나는 추세, 다음은 강남구, 강서구 순으로 많음, 또 노원구의 가구 수가 가장 적고, 강북구, 중구도 적음
분석 결과 3 : 상권별로 확인한 결과,
총 상주인구 수 & 남성 상주인구 수 & 여성상주 인구 모두 잠실 관광특구, 모래내로 15길, 백제고분로 50길, 백제고분로 34길, 진황도로 27길 순으로 많고,
총 상주인구 수는 청평화시장, 동부처과시장, 왕십리역_1, 동부시장, 고속터미널역이 적음
남성 상주인구 수는 동부시장, 고속터미널역, 청평화시장, 왕십리역_1, 동부청과시장이 적음
여성 상주인구 수는 동대문종합시장, 동서시장, 동부청과시장, 청평화시장, 왕십리역_1이 적음
"""

# 001 : Data Load
상권_상주인구 = setup_tradehub('상권_상주인구.csv')
상권_상주인구['총_상주인구_수'] = 상권_상주인구['총_상주인구_수']/1000000 #백만
상권_상주인구['총_가구_수'] = 상권_상주인구['총_가구_수']/1000000 #백만

# 002 : [EDA : LINE] Total Quarter View Plot
분기별_상주인구 = 상권_상주인구.groupby(['기준_년_코드','기준_분기_코드','분기_코드']).agg(총_상주인구_수=('총_상주인구_수','sum'), 총_가구_수=('총_가구_수','sum')).reset_index()

fig, (ax1,ax2) = plt.subplots(2,1)
ax1.plot(분기별_상주인구['분기_코드'], 분기별_상주인구['총_상주인구_수'], color='skyblue')
ax1.set_title("분기별 상주인구(백만)", fontsize=13)
ax1.set_ylabel('상주인구(백만)')
ax1.grid(True, linewidth=0.2, color='gray', linestyle='--')
ax1.xaxis.set_tick_params(labelsize=8)
#ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(분기별_상주인구['분기_코드'], 분기별_상주인구['총_가구_수'], color='pink')
ax2.set_title("분기별 가구수(백만)", fontsize=13)
ax2.set_ylabel('가구수 (백만)')
ax2.grid(True, linewidth=0.2, color='gray', linestyle='--')
ax2.xaxis.set_tick_params(labelsize=8)
#ax2.axvline(x='2020Q1', color='darkred', linestyle='--')

plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
fig.subplots_adjust(wspace=0.2, hspace=0.5)
fig.suptitle('분기별 상주인구 & 가구수 (백만)', fontsize=20)
plt.show();

# 003 : [EDA : LINE] Quarter View Plot, Category by Region
시군구_상주인구 = 상권_상주인구.groupby(['시군구','분기_코드']).agg(총_상주인구_수=('총_상주인구_수','sum'), 총_가구_수=('총_가구_수','sum')).reset_index()
시군구_상주인구 = 시군구_상주인구[~시군구_상주인구['분기_코드'].str.contains("2014")]
시군구_상주인구 = 시군구_상주인구[~시군구_상주인구['분기_코드'].str.contains("2015Q1")]

# 상주인구 시각화
ax = sns.lineplot(x='분기_코드',
             y='총_상주인구_수',
             hue='시군구',
             data=시군구_상주인구)

plt.title('구별 상주인구(백만)', fontsize=20)
plt.ylabel('상주인구(백만)', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 가구수 시각화
ax = sns.lineplot(x='분기_코드',
             y='총_가구_수',
             hue='시군구',
             data=시군구_상주인구)

plt.title('구별 가구 수 (백만)', fontsize=20)
plt.ylabel('가구 수(백만)', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 004 : [EDA : BAR] Category by Region
시군구_상주인구2 = 시군구_상주인구.groupby(['시군구']).총_상주인구_수.mean().reset_index()
시군구_상주인구2 = 시군구_상주인구2.sort_values(by=['총_상주인구_수'], ascending=True)
시군구_상주인구2 = 시군구_상주인구2.set_index('시군구')

# 상주인구 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_상주인구2.index, 시군구_상주인구2['총_상주인구_수'], color=my_colors)
plt.title('구별 상주인구(백만)', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('상주인구(백만)', fontsize=15)
plt.show();

시군구_가구수 = 시군구_상주인구.groupby(['시군구']).총_가구_수.mean().reset_index()
시군구_가구수 = 시군구_가구수.sort_values(by=['총_가구_수'], ascending=True)
시군구_가구수 = 시군구_가구수.set_index('시군구')

# 가구수 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_가구수.index, 시군구_가구수['총_가구_수'], color=my_colors)
plt.title('구별 가구 수(백만)', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('가구 수(백만)', fontsize=15)
plt.show();

# 005 : [EDA : BAR] Category by 상권_코드_명
상권_상주인구 = 상권_상주인구[~상권_상주인구['분기_코드'].str.contains("2014")]
상권_상주인구 = 상권_상주인구[~상권_상주인구['분기_코드'].str.contains("2015Q1")]
상권코드_상주인구 = 상권_상주인구.groupby(['상권_코드_명']).agg(총_상주인구_수=('총_상주인구_수','mean'), 남성_상주인구_수=('남성_상주인구_수','mean'), 여성_상주인구_수=('여성_상주인구_수','mean')).reset_index()

# 상위 10 / 하위 10 상주인구
top_상권코드_상주인구 = 상권코드_상주인구.sort_values(by=['총_상주인구_수'], ascending=False).head(10)
btm_상권코드_상주인구 = 상권코드_상주인구.sort_values(by=['총_상주인구_수'], ascending=False).tail(10)

# 상위 10 / 하위 10 남성 상주인구
top_상권코드_남성_상주인구 = 상권코드_상주인구.sort_values(by=['남성_상주인구_수'], ascending=False).head(10)
btm_상권코드_남성_상주인구 = 상권코드_상주인구.sort_values(by=['남성_상주인구_수'], ascending=False).tail(10)

# 상위 10 / 하위 10 여성 상주인구
top_상권코드_여성_상주인구 = 상권코드_상주인구.sort_values(by=['여성_상주인구_수'], ascending=False).head(10)
btm_상권코드_여성_상주인구 = 상권코드_상주인구.sort_values(by=['여성_상주인구_수'], ascending=False).tail(10)

# 총 상주인구 수 시각화
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(top_상권코드_상주인구['상권_코드_명'].astype(str), top_상권코드_상주인구['총_상주인구_수'], color='blue')
ax1.grid(True)
ax1.set_title("상권코드별 상위10 상주인구 수", fontsize=15)
ax1.set_ylabel('상주인구 수')
ax2.barh(btm_상권코드_상주인구['상권_코드_명'].astype(str), btm_상권코드_상주인구['총_상주인구_수'], color='skyblue')
ax2.grid(True)
ax2.set_title("상권코드별 하위10 상주인구 수", fontsize=15)
ax2.set_ylabel('상주인구 수')
fig.suptitle('상권코드별 상위 10 / 하위 10 상주인구 수', fontsize=20)
plt.show(block=True)

# 남성 상주인구 수 시각화
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(top_상권코드_남성_상주인구['상권_코드_명'].astype(str), top_상권코드_남성_상주인구['남성_상주인구_수'], color='blue')
ax1.grid(True)
ax1.set_title("상권코드별 상위10 남성 상주인구 수", fontsize=15)
ax1.set_ylabel('남성 상주인구 수')
ax2.barh(btm_상권코드_남성_상주인구['상권_코드_명'].astype(str), btm_상권코드_남성_상주인구['남성_상주인구_수'], color='skyblue')
ax2.grid(True)
ax2.set_title("상권코드별 하위10 남성 상주인구 수", fontsize=15)
ax2.set_ylabel('남성 상주인구 수')
fig.suptitle('상권코드별 상위 10 / 하위 10 남성 상주인구 수', fontsize=20)
plt.show(block=True)

# 여성 상주인구 수 시각화
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(top_상권코드_여성_상주인구['상권_코드_명'].astype(str), top_상권코드_여성_상주인구['여성_상주인구_수'], color='blue')
ax1.grid(True)
ax1.set_title("상권코드별 상위10 여성 상주인구 수", fontsize=15)
ax1.set_ylabel('여성 상주인구 수')
ax2.barh(btm_상권코드_여성_상주인구['상권_코드_명'].astype(str), btm_상권코드_여성_상주인구['여성_상주인구_수'], color='skyblue')
ax2.grid(True)
ax2.set_title("상권코드별 하위10 여성 상주인구 수", fontsize=15)
ax2.set_ylabel('여성 상주인구 수')
fig.suptitle('상권코드별 상위 10 / 하위 10 여성 상주인구 수', fontsize=20)
plt.show(block=True)
