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
빅데이터_상권_분석 : 상권_상주인구
분석 결과 1 : 상주 인구와 가구 수의 <분기별 지표>를 분석한 결과, 2015Q2부터 데이터 사용이 가능하다는 것을 확인
"""

# 001 : Data Load
상권_상주인구 = setup_tradehub('상권_상주인구.csv')
상권_상주인구['총_상주인구_수'] = 상권_상주인구['총_상주인구_수']/1000000 #백만
상권_상주인구['총_가구_수'] = 상권_상주인구['총_가구_수']/1000000 #백만

# 002 : [EDA : LINE] Total Quarter View Plot
분기별_상주인구 = 상권_상주인구.groupby(['기준_년_코드','기준_분기_코드','분기_코드']).agg(총_상주인구_수=('총_상주인구_수','sum'), 총_가구_수=('총_가구_수','sum')).reset_index()

fig, (ax1,ax2) = plt.subplots(2,1)
ax1.plot(분기별_상주인구['분기_코드'], 분기별_상주인구['총_상주인구_수'], color='skyblue')
ax1.set_title("분기별 상주인구(백만)", fontsize=10)
ax1.set_ylabel('상주인구(백만)')
ax1.grid(True, linewidth=0.2, color='gray', linestyle='--')
ax1.xaxis.set_tick_params(labelsize=8)
ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(분기별_상주인구['분기_코드'], 분기별_상주인구['총_가구_수'], color='pink')
ax2.set_title("분기별 가구수(백만)", fontsize=10)
ax2.set_ylabel('가구수 (백만)')
ax2.grid(True, linewidth=0.2, color='gray', linestyle='--')
ax2.xaxis.set_tick_params(labelsize=8)
ax2.axvline(x='2020Q1', color='darkred', linestyle='--')

plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
fig.subplots_adjust(wspace=0.2, hspace=0.5)
fig.suptitle('분기별 상주인구 & 가구수 (백만)', fontsize=12)
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

plt.title('구별 상주인구', fontsize=20)
plt.ylabel('상주인구', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.show();

# 가구수 시각화
ax = sns.lineplot(x='분기_코드',
             y='총_가구_수',
             hue='시군구',
             data=시군구_상주인구)

plt.title('구별 가구 수', fontsize=20)
plt.ylabel('가구 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.show();

# 004 : [EDA : BAR] Category by Region
시군구_상주인구2 = 시군구_상주인구.groupby(['시군구']).총_상주인구_수.mean().reset_index()
시군구_상주인구2 = 시군구_상주인구2.sort_values(by=['총_상주인구_수'], ascending=True)
시군구_상주인구2 = 시군구_상주인구2.set_index('시군구')

# 상주인구 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_상주인구2.index, 시군구_상주인구2['총_상주인구_수'], color=my_colors)
plt.title('구별 상주인구', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('상주인구', fontsize=15)
plt.show();

시군구_가구수 = 시군구_상주인구.groupby(['시군구']).총_가구_수.mean().reset_index()
시군구_가구수 = 시군구_가구수.sort_values(by=['총_가구_수'], ascending=True)
시군구_가구수 = 시군구_가구수.set_index('시군구')

# 가구수 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_가구수.index, 시군구_가구수['총_가구_수'], color=my_colors)
plt.title('구별 가구수', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('가구수', fontsize=15)
plt.show();

