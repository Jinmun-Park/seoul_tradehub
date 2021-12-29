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
빅데이터_상권_분석 : 상권_생활인구
분석 결과 1 : 
"""

# 001 : Data Load
상권_생활인구 = setup_tradehub('상권_생활인구.csv')

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

eda_분기별_생활인구 = 생활인구.groupby(['기준_년_코드', '기준_분기_코드', '분기_코드']).agg(
    총_생활인구_수=('총_생활인구_수', 'sum')
).reset_index()

eda_분기별_평균생활인구 = 생활인구.groupby(['기준_년_코드', '기준_분기_코드', '분기_코드']).agg(
    평균_생활인구=('총_생활인구_수', 'mean')
).reset_index()

eda_상권병합_생활인구 = 생활인구.groupby(['기준_년_코드', '기준_분기_코드', '분기_코드', '상권_병합']).agg(
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
edatop_상권병합_생활인구['총_생활인구_수'] = edatop_상권병합_생활인구['총_생활인구_수'] / 10000000
edabtm_상권병합_생활인구['총_생활인구_수'] = edabtm_상권병합_생활인구['총_생활인구_수'] / 10000000

# 그래프 1 : 분기당 총 생활인구(억)와 평균생활인구
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(eda_분기별_생활인구['분기_코드'], eda_분기별_생활인구['총_생활인구_수'] / 10000000, label='총_생활인구_수(10억)')
ax1.set_title("분기당 총 생활인구(억)", fontsize=20)
ax1.set_ylabel('생활인구(억)')
ax1.grid(linewidth=0.3)
ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(eda_분기별_평균생활인구['분기_코드'], eda_분기별_평균생활인구['평균_생활인구'] / 10000000, label='평균_생활인구', color='orange')
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
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.set_title("지역별 총 생활인구기준 상위 15지역의 총 생활인구 수(억)", fontsize=15)
ax1.set_xlabel('인구수(억)')
for label, grp in edatop_상권병합_생활인구.groupby('상권_병합'):
    grp.plot(x='분기_코드', y='총_생활인구_수', ax=ax1, label=label, linestyle='-', marker='o')
ax1.grid(linewidth=0.3)
ax1.legend(loc="upper right", fontsize=10)
ax2.plot(eda_분기별_생활인구['분기_코드'], eda_분기별_생활인구['총_생활인구_수'] / 10000000, label='총_생활인구_수(억)')
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
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.set_title("지역별 총 생활인구기준 하위 15지역의 총 생활인구 수(억)", fontsize=15)
ax1.set_xlabel('인구수(억)')
for label, grp in edabtm_상권병합_생활인구.groupby('상권_병합'):
    grp.plot(x='분기_코드', y='총_생활인구_수', ax=ax1, label=label, linestyle='-', marker='o')
ax1.grid(linewidth=0.3)
ax1.legend(loc="upper right", fontsize=10)
ax2.plot(eda_분기별_생활인구['분기_코드'], eda_분기별_생활인구['총_생활인구_수'] / 10000000, label='총_생활인구_수(억)')
ax2.set_title("분기별 총 생활인구(억)", fontsize=15)
ax2.set_xlabel('분기')
ax2.set_ylabel('생활인구(억')
ax2.grid(linewidth=0.3)
ax2.axvline(x='2020Q1', color='darkred', linestyle='--')
fig.subplots_adjust(wspace=0.2, hspace=0.5)
fig.suptitle('지역별 총 생활인구기준 하위 15지역과 분기별 총 생활인구(억)', fontsize=20)
plt.legend(loc="upper right")
plt.show()