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
빅데이터_상권_분석 : 상권_추정매출
분석 결과 1 : 분기별 매출은 코로나시기에 줄어들었으나, 2019년과 비교하여서 상대적으로 높은 매출의 그래프. 남성 & 여성 매출건수는 분기별 매출과 매우 비슷한 그래프 형태를 띄고 있음.

그래프 2 [분기별 매출금액(10억)과 점포수] : 코로나시기에 줄어든 매출금액과 반대로 점포수는 반대로 증가하였음을 보여준다.
그래프 3 [2020-2019년 매출차액 상,하위 10개 서비스업종별 매출금액] : 
의료품의 상승세와 가장많은 점포수를 가지고 있는 한식점의 하락은 코로나 시기에도 불구하고 2020년의 매출이 2019년보다 높은 이유를 설명해준다.
"""

# 001 : Data Load
상권_추정매출_2016 = setup_tradehub('상권_추정매출_2016.csv')
상권_추정매출_2017 = setup_tradehub('상권_추정매출_2017.csv')
상권_추정매출_2018 = setup_tradehub('상권_추정매출_2018.csv')
상권_추정매출_2019 = setup_tradehub('상권_추정매출_2019.csv')
상권_추정매출_2020 = setup_tradehub('상권_추정매출_2020.csv')
상권_추정매출_2021 = setup_tradehub('상권_추정매출_2021.csv')

상권_추정매출 = pd.concat([상권_추정매출_2016, 상권_추정매출_2017, 상권_추정매출_2018, 상권_추정매출_2019, 상권_추정매출_2020, 상권_추정매출_2021]).reset_index(drop=True)

# 002 : [EDA : LINE] Total Quarter View Plot
분기별_추정매출 = 상권_추정매출.groupby(['기준_년_코드', '기준_분기_코드', '분기_코드']).agg(
    분기당_매출_금액=('분기당_매출_금액', 'sum'), 분기당_매출_건수=('분기당_매출_건수', 'sum'),
    주중_매출_비율=('주중_매출_비율','mean'), 주말_매출_비율=('주말_매출_비율','mean'),
    점포수=('점포수', 'sum'), 남성_매출_건수=('남성_매출_건수', 'sum'), 여성_매출_건수=('여성_매출_건수', 'sum')).reset_index()

fig, ax = plt.subplots()
ax.plot(분기별_추정매출['분기_코드'], 분기별_추정매출['분기당_매출_금액'] / 1000000000, label='분기당_매출_금액(10억)')
ax.plot(분기별_추정매출['분기_코드'], 분기별_추정매출['남성_매출_건수'] / 10000, label='남성_매출_건수(1만)')
ax.plot(분기별_추정매출['분기_코드'], 분기별_추정매출['여성_매출_건수'] / 10000, label='여성_매출_건수(1만)')
ax.set_title("분기당 매출 금액(10억)과 남성&여성 매출 건수(1만)", fontsize=20)
ax.set_xlabel('분기')
ax.set_ylabel('매출금액(10억),매출건수(1만)')
ax.grid(linewidth=0.3)
plt.axvline(x='2020Q1', color='darkred', linestyle='--')
plt.text('2019Q4', 1, 'COVID19', rotation=90, color='darkred')
plt.xticks(rotation=45)
plt.legend(loc="upper right")
plt.show()

# 분기당 매출금액(10억)과 점포수
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(분기별_추정매출['분기_코드'], 분기별_추정매출['분기당_매출_금액'] / 1000000000, label='분기당_매출_금액(10억)')
ax1.set_title("분기별 매출금액(10억)", fontsize=15)
ax1.set_ylabel('매출금액(10억)')
ax1.grid(linewidth=0.3)
ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(분기별_추정매출['분기_코드'], 분기별_추정매출['점포수'], label='점포수', color='orange')
ax2.set_title("분기별 점포수", fontsize=18)
ax2.set_ylabel('점포수')
ax2.grid(linewidth=0.3)
ax2.axvline(x='2020Q1', color='darkred', linestyle='--')

plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
fig.subplots_adjust(wspace=0.2, hspace=0.5)
fig.suptitle('분기별 매출금액(10억)과 점포수', fontsize=20)
plt.show()

# 003 : [EDA : LINE] Quarter View Plot, Category by Region
시군구_추정매출 = 상권_추정매출.groupby(['시군구','분기_코드']).agg(
    분기당_매출_금액=('분기당_매출_금액', 'sum'), 분기당_매출_건수=('분기당_매출_건수', 'sum'),
    점포수=('점포수', 'sum'), 남성_매출_건수=('남성_매출_건수', 'sum'), 여성_매출_건수=('여성_매출_건수', 'sum')).reset_index()

# 총 매출 금액 시각화
ax = sns.lineplot(x='분기_코드',
             y='분기당_매출_금액',
             hue='시군구',
             data=시군구_추정매출)

plt.title('구별 분기당 매출 금액', fontsize=20)
plt.ylabel('총 매출 금액', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.show();

# 총 매출 건수 시각화
ax = sns.lineplot(x='분기_코드',
             y='분기당_매출_건수',
             hue='시군구',
             data=시군구_추정매출)

plt.title('구별 분기당 매출 건수', fontsize=20)
plt.ylabel('총 매출 건수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.show();

# 총 점포수 시각화
ax = sns.lineplot(x='분기_코드',
             y='점포수',
             hue='시군구',
             data=시군구_추정매출)

plt.title('구별 점포수', fontsize=20)
plt.ylabel('총 점포수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.show();

# 004 : [EDA : BAR] Category by Region
시군구_추정매출2 = 시군구_추정매출.groupby(['시군구']).분기당_매출_금액.mean().reset_index()
시군구_추정매출2 = 시군구_추정매출2.sort_values(by=['분기당_매출_금액'], ascending=True)
시군구_추정매출2 = 시군구_추정매출2.set_index('시군구')

# 총 매출 금액 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_추정매출2.index, 시군구_추정매출2['분기당_매출_금액'], color=my_colors)
plt.title('구별 총 매출 금액', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('총 매출 금액', fontsize=15)
plt.show();

시군구_추정매출2 = 시군구_추정매출.groupby(['시군구']).분기당_매출_건수.mean().reset_index()
시군구_추정매출2 = 시군구_추정매출2.sort_values(by=['분기당_매출_건수'], ascending=True)
시군구_추정매출2 = 시군구_추정매출2.set_index('시군구')

# 총 매출 건수 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_추정매출2.index, 시군구_추정매출2['분기당_매출_건수'], color=my_colors)
plt.title('구별 총 매출 건수', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('총 매출 건수', fontsize=15)
plt.show();

시군구_추정매출2 = 시군구_추정매출.groupby(['시군구']).점포수.mean().reset_index()
시군구_추정매출2 = 시군구_추정매출2.sort_values(by=['점포수'], ascending=True)
시군구_추정매출2 = 시군구_추정매출2.set_index('시군구')

# 총 점포수 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_추정매출2.index, 시군구_추정매출2['점포수'], color=my_colors)
plt.title('구별 총 점포수', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('총 점포수', fontsize=15)
plt.show();

# 여기서부터는 추가 수정할 예정
# 005 : [EDA : BAR] Category by 상권_코드_명
상권코드_추정매출 = 상권_추정매출.groupby(['상권_코드_명']).agg(
    분기당_매출_금액=('분기당_매출_금액', 'mean'), 분기당_매출_건수=('분기당_매출_건수', 'mean'),
    점포수=('점포수', 'mean'), 남성_매출_건수=('남성_매출_건수', 'mean'), 여성_매출_건수=('여성_매출_건수', 'mean')).reset_index()

# 상위 10 / 하위 10 매출 금액
top_상권코드_추정매출 = 상권코드_추정매출.sort_values(by=['분기당_매출_금액'], ascending=False).head(10)
btm_상권코드_추정매출 = 상권코드_추정매출.sort_values(by=['분기당_매출_금액'], ascending=False).tail(10)

# 006 : [EDA : BAR] Category by 서비스_업종_코드_명
서비스업종코드_추정매출 = 상권_추정매출.groupby(['서비스_업종_코드_명']).agg(
    분기당_매출_금액=('분기당_매출_금액', 'mean'), 분기당_매출_건수=('분기당_매출_건수', 'mean'),
    점포수=('점포수', 'mean'), 남성_매출_건수=('남성_매출_건수', 'mean'), 여성_매출_건수=('여성_매출_건수', 'mean')).reset_index()

서비스업종코드_상권코드_추정매출 = 상권_추정매출.groupby(['상권_코드_명','서비스_업종_코드_명']).agg(
    분기당_매출_금액=('분기당_매출_금액', 'mean'), 분기당_매출_건수=('분기당_매출_건수', 'mean'),
    점포수=('점포수', 'mean'), 남성_매출_건수=('남성_매출_건수', 'mean'), 여성_매출_건수=('여성_매출_건수', 'mean')).reset_index()




# 2020-2019년 매출차액 상,하위 10개 서비스업종별 매출금액
eda_추정매출 = pd.pivot_table(상권_추정매출, values=['분기당_매출_금액'], index=['서비스_업종_코드_명'], columns=['기준_년_코드'],
                          aggfunc=sum).reset_index()
eda_추정매출 = eda_추정매출.droplevel(0, axis=1).reset_index().rename_axis(columns=None)
eda_추정매출 = eda_추정매출.rename(columns={'': '서비스_업종_코드_명'})
eda_추정매출['차액'] = eda_추정매출[2020] - eda_추정매출[2019]
edatop_추정매출 = eda_추정매출.sort_values(by='차액', ascending=False).head(10)
edabtm_추정매출 = eda_추정매출.sort_values(by='차액', ascending=False).tail(10)

edatop_상권별_추정매출 = 상권_추정매출[상권_추정매출['서비스_업종_코드_명'].isin(edatop_추정매출['서비스_업종_코드_명'])]
edabtm_상권별_상주인구 = 상권_추정매출[상권_추정매출['서비스_업종_코드_명'].isin(edabtm_추정매출['서비스_업종_코드_명'])]

edatop_상권별_추정매출 = edatop_상권별_추정매출.groupby(['기준_년_코드', '기준_분기_코드', '분기_코드', '서비스_업종_코드_명']).agg(
    분기당_매출_금액=('분기당_매출_금액', 'sum'),
    분기당_매출_건수=('분기당_매출_건수', 'sum'),
    점포수=('점포수', 'sum'),
    남성_매출_건수=('남성_매출_건수', 'sum'),
    여성_매출_건수=('여성_매출_건수', 'sum')).reset_index()

edabtm_상권별_추정매출 = edabtm_상권별_상주인구.groupby(['기준_년_코드', '기준_분기_코드', '분기_코드', '서비스_업종_코드_명']).agg(
    분기당_매출_금액=('분기당_매출_금액', 'sum'),
    분기당_매출_건수=('분기당_매출_건수', 'sum'),
    점포수=('점포수', 'sum'),
    남성_매출_건수=('남성_매출_건수', 'sum'),
    여성_매출_건수=('여성_매출_건수', 'sum')).reset_index()

edatop_상권별_추정매출['분기당_매출_금액'] = edatop_상권별_추정매출['분기당_매출_금액'] / 1000000000
edabtm_상권별_추정매출['분기당_매출_금액'] = edabtm_상권별_추정매출['분기당_매출_금액'] / 1000000000

fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.set_title("2020-2019년 매출차액 상위 10개 서비스업종별 매출금액(10억)", fontsize=15)
ax1.set_xlabel('분기')
for label, grp in edatop_상권별_추정매출.groupby('서비스_업종_코드_명'):
    grp.plot(x='분기_코드', y='분기당_매출_금액', ax=ax1, label=label, linestyle='-', marker='o')
ax2.set_title("2020-2019년 매출차액 하위 10개 서비스업종별 매출금액(10억)", fontsize=15)
ax2.set_xlabel('분기')
for label, grp in edabtm_상권별_추정매출.groupby('서비스_업종_코드_명'):
    grp.plot(x='분기_코드', y='분기당_매출_금액', ax=ax2, label=label, linestyle='-', marker='o')
ax1.legend(fontsize=7, loc="upper right")
ax2.legend(fontsize=7, loc="upper right")
fig.subplots_adjust(wspace=0.1, hspace=0.4)
fig.suptitle('2020-2019년 매출차액 상,하위 10개 서비스업종별 매출금액(10억)', fontsize=20)