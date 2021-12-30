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
빅데이터_상권_분석 : 상권_추정매출
분석 결과 1 : 
"""

# 001 : Data Load
상권_추정매출 = setup_tradehub('상권_추정매출.csv')

# EDA PART 7 : 추정매출
'''
질문 1 : 분기별 매출은 줄어들었을까 ? 남성매출건수, 여성매출건수로 보면은 차이가 있을까?
그래프 1 [분기당 매출금액(10억)과 남성&여성 매출건수(1만)] : 분기별 매출은 코로나시기에 줄어들었으나, 2019년과 비교하여서
상대적으로 높은 매출의 그래프. 남성 & 여성 매출건수는 분기별 매출과 매우 비슷한 그래프 형태를 띄고 있음.

질문 2 : 분기별 매출금액과 점포수는 동일하게 움직일까 ?
그래프 2 [분기별 매출금액(10억)과 점포수] : 코로나시기에 줄어든 매출금액과 반대로 점포수는 반대로 증가하였음을 보여준다.

질문 3 : 상하위 서비스업종별 매출의 분기별 차이는 ? 2019년 매출이 2020년 매출보다 높은이유를 설명하기 위한 차트로 충분한가?
그래프 3 [2020-2019년 매출차액 상,하위 10개 서비스업종별 매출금액] : 의료품의 상승세와 가장많은 점포수를 가지고 있는 한식점의 하락은
코로나시기에도 불구하고 2020년의 매출이 2019년보다 높은 이유를 설명해준다.
'''
추정매출['분기_코드'] = 추정매출['기준_년_코드'].astype(str) + 'Q' + 추정매출['기준_분기_코드'].astype(str)
eda_분기별_추정매출 = 추정매출.groupby(['기준_년_코드', '기준_분기_코드', '분기_코드']).agg(
    분기당_매출_금액=('분기당_매출_금액', 'sum'),
    분기당_매출_건수=('분기당_매출_건수', 'sum'),
    점포수=('점포수', 'sum'),
    남성_매출_건수=('남성_매출_건수', 'sum'),
    여성_매출_건수=('여성_매출_건수', 'sum'),
).reset_index()

# 그래프 1 : 분기당 매출금액(10억)과 남성&여성 매출건수(1만)
fig, ax = plt.subplots()
ax.plot(eda_분기별_추정매출['분기_코드'], eda_분기별_추정매출['분기당_매출_금액'] / 1000000000, label='분기당_매출_금액(10억)')
ax.plot(eda_분기별_추정매출['분기_코드'], eda_분기별_추정매출['남성_매출_건수'] / 10000, label='남성_매출_건수(1만)')
ax.plot(eda_분기별_추정매출['분기_코드'], eda_분기별_추정매출['여성_매출_건수'] / 10000, label='여성_매출_건수(1만)')
ax.set_title("분기당 매출금액(10억)과 남성&여성 매출건수(1만)", fontsize=20)
ax.set_xlabel('분기')
ax.set_ylabel('매출금액(10억),매출건수(1만)')
ax.grid(linewidth=0.3)
plt.axvline(x='2020Q1', color='darkred', linestyle='--')
plt.text('2019Q4', 1, 'COVID19', rotation=90, color='darkred')
plt.xticks(rotation=45)
plt.legend(loc="upper right")
plt.show()

# 그래프 2 : 분기당 매출금액(10억)과 점포수
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(eda_분기별_추정매출['분기_코드'], eda_분기별_추정매출['분기당_매출_금액'] / 1000000000, label='분기당_매출_금액(10억)')
ax1.set_title("분기별 매출금액(10억)", fontsize=15)
ax1.set_ylabel('매출금액(10억)')
ax1.grid(linewidth=0.3)
ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(eda_분기별_추정매출['분기_코드'], eda_분기별_추정매출['점포수'], label='점포수', color='orange')
ax2.set_title("분기별 점포수", fontsize=18)
ax2.set_ylabel('점포수')
ax2.grid(linewidth=0.3)
ax2.axvline(x='2020Q1', color='darkred', linestyle='--')
plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
fig.subplots_adjust(wspace=0.2, hspace=0.5)
fig.suptitle('분기별 매출금액(10억)과 점포수', fontsize=20)
plt.show()

# 그래프 3 : 2020-2019년 매출차액 상,하위 10개 서비스업종별 매출금액
eda_추정매출 = pd.pivot_table(추정매출, values=['분기당_매출_금액'], index=['서비스_업종_코드_명'], columns=['기준_년_코드'],
                          aggfunc=sum).reset_index()
eda_추정매출 = eda_추정매출.droplevel(0, axis=1).reset_index().rename_axis(columns=None)
eda_추정매출 = eda_추정매출.rename(columns={'': '서비스_업종_코드_명'})
eda_추정매출['차액'] = eda_추정매출[2020] - eda_추정매출[2019]
edatop_추정매출 = eda_추정매출.sort_values(by='차액', ascending=False).head(10)
edabtm_추정매출 = eda_추정매출.sort_values(by='차액', ascending=False).tail(10)

edatop_상권별_추정매출 = 추정매출[추정매출['서비스_업종_코드_명'].isin(edatop_추정매출['서비스_업종_코드_명'])]
edabtm_상권별_상주인구 = 추정매출[추정매출['서비스_업종_코드_명'].isin(edabtm_추정매출['서비스_업종_코드_명'])]

edatop_상권별_추정매출 = edatop_상권별_추정매출.groupby(['기준_년_코드', '기준_분기_코드', '분기_코드', '서비스_업종_코드_명']).agg(
    분기당_매출_금액=('분기당_매출_금액', 'sum'),
    분기당_매출_건수=('분기당_매출_건수', 'sum'),
    점포수=('점포수', 'sum'),
    남성_매출_건수=('남성_매출_건수', 'sum'),
    여성_매출_건수=('여성_매출_건수', 'sum'),
).reset_index()

edabtm_상권별_추정매출 = edabtm_상권별_상주인구.groupby(['기준_년_코드', '기준_분기_코드', '분기_코드', '서비스_업종_코드_명']).agg(
    분기당_매출_금액=('분기당_매출_금액', 'sum'),
    분기당_매출_건수=('분기당_매출_건수', 'sum'),
    점포수=('점포수', 'sum'),
    남성_매출_건수=('남성_매출_건수', 'sum'),
    여성_매출_건수=('여성_매출_건수', 'sum'),
).reset_index()

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
