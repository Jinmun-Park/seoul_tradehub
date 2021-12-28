from src.setup.setup import setup_tradehub

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import font_manager, rc
import matplotlib

# Setup
font_name = font_manager.FontProperties(fname="src/gulim.ttf").get_name()
plt.rc('font', family=font_name)
matplotlib.rcParams['axes.unicode_minus'] = False

"""
빅데이터_상권_분석 : 상권_상주인구
분석 결과 1 : 상주인구와 가구수의 <분기별 지표>를 통해 2015Q1부터 데이터 사용이 가능
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

# 003 : [EDA : BAR] Category by City
시군구_상주인구 = 상권_상주인구.groupby(['기준_년_코드','기준_분기_코드','분기_코드', '시군구']).agg(총_상주인구_수=('총_상주인구_수','sum'), 총_가구_수=('총_가구_수','sum')).reset_index()

fig, ax = plt.subplots(1,1)
ax.set_title("점포수 기준 상위 15 서비스업종 점포 수", fontsize=15)
ax.set_xlabel('분기')
for label, grp in 시군구_상주인구.groupby('시군구'):
    grp.plot(x='분기_코드', y='점포_수',ax=ax, label=label, linestyle='-', marker='o')
ax.legend(loc="upper right", fontsize=7)
ax.legend(fontsize=7, loc="upper right")
fig.subplots_adjust(wspace=0.1, hspace=0.4)
fig.suptitle('점포수 기준 상위15 서비스업종별 점포 & 프랜차이즈 수', fontsize=20)
plt.legend(loc="upper right")
plt.show()