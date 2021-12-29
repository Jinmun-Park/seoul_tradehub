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
분석 결과1: 분기별 아파트 평균 시가와 아파트 단지 수를 확인한 결과, 2020년 1분기에 급격히 상승한 것으로 파악됨.
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

ax = sns.lineplot(x='분기_코드',
             y='아파트_단지_수',
             hue='시군구',
             data=시군구_아파트)

plt.title('구별 아파트 단지 수', fontsize=20)
plt.ylabel('아파트 단지 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.show();

# 아파트의 경우, 상권 코드 명 별로도 보는 게 좋을 것 같음('상권_코드_명')
