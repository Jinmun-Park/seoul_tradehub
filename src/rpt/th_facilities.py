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
빅데이터_상권_분석 : 상권_집객시설
분석 결과 1 : 
분기별로 집객시설 확인한 결과, 2017 Q4 급격한 상승 이후, 2018Q1 ~ 2021Q1 데이터는 전혀 변화가 없으며, 2021Q2에 급격히 감소한 형태 -> 과연 신뢰할 수 있는 데이터인가? 
집객시설별로 확인한 결과, 2016 3분기에 버스 정거장 수가 급격히 감소하고, 2017 1분기에 숙박시설 수가 급격히 증가하고 2021 2분기에 급격히 감소함
분석 결과 2 : 구별로 전체 확인한 결과, 
총 집객시설 수 : 강남구>중구>종로구 많음, 강북구<노원구<도봉구 적음
구별로 집객시설별로 확인한 결과, 
관공서_수 : 2016년 1분기에 급격하게 상승 후, 2018년 1분기에 또 급격하게 상승
은행_수 : 2017 1분기에 전체적으로 조금 하락하고, 2021 2분기에 조금 하락하는 형태
유치원_수, 초등학교_수, 중학교_수, 고등학교_수, 종합병원_수, 철도_역_수 등: 집계되지 않은 데이터가 많음
"""

# 001 : Data Load
상권_집객시설 = setup_tradehub('상권_집객시설.csv')

# 002 : [EDA : LINE] Total Quarter View Plot
분기별_집객시설 = 상권_집객시설.groupby(['기준_년_코드','기준_분기_코드','분기_코드']).agg(
    집객시설_수=('집객시설_수', 'sum'), 관공서_수=('관공서_수', 'sum'), 은행_수=('은행_수', 'sum'),
    종합병원_수=('종합병원_수', 'sum'), 일반_병원_수=('일반_병원_수', 'sum'), 약국_수=('약국_수', 'sum'),
    유치원_수=('유치원_수', 'sum'), 초등학교_수=('초등학교_수', 'sum'), 중학교_수=('중학교_수', 'sum'),
    고등학교_수=('고등학교_수', 'sum'), 대학교_수=('대학교_수', 'sum'), 백화점_수=('백화점_수', 'sum'),
    슈퍼마켓_수=('슈퍼마켓_수', 'sum'), 극장_수=('극장_수', 'sum'), 숙박_시설_수=('숙박_시설_수', 'sum'),
    공항_수=('공항_수', 'sum'), 철도_역_수=('철도_역_수', 'sum'), 버스_터미널_수=('버스_터미널_수', 'sum'),
    지하철_역_수=('지하철_역_수', 'sum'), 버스_정거장_수=('버스_정거장_수', 'sum')).reset_index()

# 모든 집객 시설을 합해 “집객시설 합계”라는 새로운 컬럼을 생성
분기별_집객시설['집객시설_합계'] = 분기별_집객시설.iloc[:, 4:].sum(axis=1)

fig, (ax1,ax2) = plt.subplots(2,1)
ax1.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['집객시설_수']/10000, label='집객시설_수')
ax1.set_title("분기별 집객시설 수(만)", fontsize=20)
ax1.set_xlabel('분기')
ax1.set_ylabel('집객시설 수(만)')
ax1.grid(linewidth=0.3)
#ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(분기별_집객시설['분기_코드'],  분기별_집객시설['집객시설_합계']/10000, label='집객시설_합계')
ax2.set_title("분기별 집객시설 합계(만)", fontsize=20)
ax2.set_xlabel('분기')
ax2.set_ylabel('집객시설 수(만)')
ax2.grid(linewidth=0.3)
#ax2.axvline(x='2020Q1', color='darkred', linestyle='--')

fig.subplots_adjust(wspace=0.2, hspace=0.5)
plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
plt.show();

# 집객시설별로 확인
fig, ax = plt.subplots()
ax.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['관공서_수'], label='관공서_수')
ax.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['은행_수'], label='은행_수')
ax.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['종합병원_수'], label='종합병원_수')
ax.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['일반_병원_수'], label='일반_병원_수')
ax.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['약국_수'], label='약국_수')
ax.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['유치원_수'], label='유치원_수')
ax.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['초등학교_수'], label='초등학교_수')
ax.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['중학교_수'], label='중학교_수')
ax.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['고등학교_수'], label='고등학교_수')
ax.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['대학교_수'], label='대학교_수')
ax.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['백화점_수'], label='백화점_수')
ax.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['슈퍼마켓_수'], label='슈퍼마켓_수')
ax.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['극장_수'], label='극장_수')
ax.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['숙박_시설_수'], label='숙박_시설_수')
ax.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['공항_수'], label='공항_수')
ax.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['철도_역_수'], label='철도_역_수')
ax.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['버스_터미널_수'], label='버스_터미널_수')
ax.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['지하철_역_수'], label='지하철_역_수')
ax.plot(분기별_집객시설['분기_코드'], 분기별_집객시설['버스_정거장_수'], label='버스_정거장_수')
ax.set_title("분기별 집객시설별 집객시설 수", fontsize=20)
ax.set_xlabel('분기')
ax.set_ylabel('각 집객시설 수')
ax.grid(linewidth=0.3)
#plt.axvline(x='2020Q1', color='darkred', linestyle='--')
#plt.text('2019Q4',1,'COVID19', rotation=90, color='darkred')
plt.xticks(rotation=45)
plt.legend(loc="upper right")
plt.show();

# 003 : [EDA : LINE] Quarter View Plot, Category by Region
시군구_집객시설 = 상권_집객시설.groupby(['시군구','분기_코드']).agg(
    집객시설_수=('집객시설_수', 'sum'), 관공서_수=('관공서_수', 'sum'), 은행_수=('은행_수', 'sum'),
    종합병원_수=('종합병원_수', 'sum'), 일반_병원_수=('일반_병원_수', 'sum'), 약국_수=('약국_수', 'sum'),
    유치원_수=('유치원_수', 'sum'), 초등학교_수=('초등학교_수', 'sum'), 중학교_수=('중학교_수', 'sum'),
    고등학교_수=('고등학교_수', 'sum'), 대학교_수=('대학교_수', 'sum'), 백화점_수=('백화점_수', 'sum'),
    슈퍼마켓_수=('슈퍼마켓_수', 'sum'), 극장_수=('극장_수', 'sum'), 숙박_시설_수=('숙박_시설_수', 'sum'),
    공항_수=('공항_수', 'sum'), 철도_역_수=('철도_역_수', 'sum'), 버스_터미널_수=('버스_터미널_수', 'sum'),
    지하철_역_수=('지하철_역_수', 'sum'), 버스_정거장_수=('버스_정거장_수', 'sum')).reset_index()

# 총 집객시설 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='집객시설_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 집객 시설 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 관공서 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='관공서_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 관공서 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 은행 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='은행_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 은행 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 종합병원 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='종합병원_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 종합병원 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 일반병원 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='일반_병원_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 일반병원 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 약국 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='약국_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 약국 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 유치원 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='유치원_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 유치원 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 초등학교 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='초등학교_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 초등학교 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 중학교 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='중학교_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 중학교 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 고등학교 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='고등학교_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 고등학교 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 대학교 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='대학교_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 대학교 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 백화점 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='백화점_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 백화점 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 슈퍼마켓 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='슈퍼마켓_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 슈퍼마켓 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 극장 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='극장_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 극장 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 숙박 시설 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='숙박_시설_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 숙박시설 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 공항 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='공항_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 공항 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 철도역 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='철도_역_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 철도역 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 버스터미널 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='버스_터미널_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 버스터미널 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 지하철역 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='지하철_역_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 지하철역 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 버스정거장 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='버스_정거장_수',
             hue='시군구',
             data=시군구_집객시설)

plt.title('구별 버스정거장 수', fontsize=20)
plt.ylabel('집객 시설 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 004 : [EDA : BAR] Category by Region
시군구_집객시설2 = 시군구_집객시설.groupby(['시군구']).집객시설_수.mean().reset_index()
시군구_집객시설2 = 시군구_집객시설2.sort_values(by=['집객시설_수'], ascending=True)
시군구_집객시설2 = 시군구_집객시설2.set_index('시군구')

# 집객시설 수 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_집객시설2.index, 시군구_집객시설2['집객시설_수'], color=my_colors)
plt.title('구별 집객시설 수', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('집객시설 수', fontsize=15)
plt.show();