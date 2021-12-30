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
빅데이터_상권_분석 : 상권_직장인구
분석 결과 1 : 
"""

# 001 : Data Load
상권_직장인구 = setup_tradehub('상권_직장인구.csv')

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
