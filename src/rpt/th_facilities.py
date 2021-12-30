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
빅데이터_상권_분석 : 상권_집객시설
분석 결과 1 : 
"""

# 001 : Data Load
상권_집객시설 = setup_tradehub('상권_집객시설.csv')

# EDA PART 6 : 집객시설
'''
*** 모든 데이터를 이용할수 있을것 같다고 생각했지만 2018Q1 이후의 데이터는 전혀 변화가 없다.
*** 집객시설의 데이터는 이용할수 없다. 하지만 2017Q4 이후의 대학교의 급격한 상승은 데이터 신뢰성에 의심이 간다.

질문1 : 분기별 각 집객시설은 어떻게 변화 하였는가.
그래프 1 [분기별 집객시설 모음] : 2018Q1 이후의 변화가 없으므로 특별한 분석이 불가능

질문2 : 분기별 집객시설 수에는 어떻게 변화 하였는가.
그래프 2 [분기별 전체 집객시설 수] : 2018Q1 이후의 변화가 없는것은 동일하나 2017Q4이후로 가파른 상승을 한 집객시설수.
가파른 집객시설의 이유는 대학교의 수가 약 1300개 한분기 사이만에 증가한 이유. 데이터 신뢰에 의문.
'''
집객시설['분기_코드'] = 집객시설['기준_년_코드'].astype(str) + 'Q' + 집객시설['기준_분기_코드'].astype(str)
eda_분기별_집객시설 = 집객시설.groupby(['기준_년_코드','기준_분기_코드','분기_코드']).agg(
    집객시설_수=('집객시설_수', 'sum'), 관공서_수=('관공서_수', 'sum'), 은행_수=('은행_수', 'sum'),
    종합병원_수=('종합병원_수', 'sum'), 일반_병원_수=('일반_병원_수', 'sum'), 약국_수=('약국_수', 'sum'),
    유치원_수=('유치원_수', 'sum'), 초등학교_수=('초등학교_수', 'sum'), 중학교_수=('중학교_수', 'sum'),
    고등학교_수=('고등학교_수', 'sum'), 대학교_수=('대학교_수', 'sum'), 백화점_수=('백화점_수', 'sum'),
    슈퍼마켓_수=('슈퍼마켓_수', 'sum'), 극장_수=('극장_수', 'sum'), 숙박_시설_수=('숙박_시설_수', 'sum'),
    공항_수=('공항_수', 'sum'), 철도_역_수=('철도_역_수', 'sum'), 버스_터미널_수=('버스_터미널_수', 'sum'),
    지하철_역_수=('지하철_역_수', 'sum'), 버스_정거장_수=('버스_정거장_수', 'sum')
).reset_index()
eda_분기별_집객시설['집객시설_합계'] = eda_분기별_집객시설.iloc[:,4:].sum(axis=1)

# 그래프 1 : 분기별 집객시설 모음
fig, ax = plt.subplots()
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['관공서_수'], label='관공서_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['은행_수'], label='은행_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['종합병원_수'], label='종합병원_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['일반_병원_수'], label='일반_병원_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['약국_수'], label='약국_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['유치원_수'], label='유치원_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['초등학교_수'], label='초등학교_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['중학교_수'], label='중학교_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['고등학교_수'], label='고등학교_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['대학교_수'], label='대학교_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['백화점_수'], label='백화점_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['슈퍼마켓_수'], label='슈퍼마켓_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['극장_수'], label='극장_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['숙박_시설_수'], label='숙박_시설_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['공항_수'], label='공항_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['철도_역_수'], label='철도_역_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['버스_터미널_수'], label='버스_터미널_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['지하철_역_수'], label='지하철_역_수')
ax.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['버스_정거장_수'], label='버스_정거장_수')
ax.set_title("분기별 집객시설 모음", fontsize=20)
ax.set_xlabel('분기')
ax.set_ylabel('수')
ax.grid(linewidth=0.3)
plt.axvline(x='2020Q1', color='darkred', linestyle='--')
plt.text('2019Q4',1,'COVID19',rotation=90, color='darkred')
plt.xticks(rotation=45)
plt.legend(loc="upper right")
plt.show()

# 그래프 2 : 분기별 전체 집객시설 수(만)
fig, (ax1,ax2) = plt.subplots(2,1)
ax1.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['집객시설_수']/10000, label='집객시설_수')
ax1.set_title("분기별 집객시설 수(만)", fontsize=20)
ax1.set_xlabel('분기')
ax1.set_ylabel('수(만)')
ax1.grid(linewidth=0.3)
ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(eda_분기별_집객시설['분기_코드'], eda_분기별_집객시설['집객시설_합계']/10000, label='집객시설_합계')
ax2.set_title("분기별 모든 집객시설 합계(만)", fontsize=20)
ax2.set_xlabel('분기')
ax2.set_ylabel('수(만)')
ax2.grid(linewidth=0.3)
ax2.axvline(x='2020Q1', color='darkred', linestyle='--')
fig.subplots_adjust(wspace=0.2, hspace=0.5)
plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
plt.show()