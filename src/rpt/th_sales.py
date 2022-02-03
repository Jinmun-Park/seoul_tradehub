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
분석 결과 1 : 분기별로 확인한 결과, 
분기별 매출 금액(10억) 및 남성 & 여성 매출 건수(만): 
남성 매출 건수가 항상 여성 매출 건수에 비해 많고 매출 금액과 매출 건수는 같은 양상으로 움직이는 경우가 많음
매출 금액과 매출 건수는 2019년 1분기에 모두 급격히 하락, 2019년 4분기까지 지속적으로 상승한 후 2020년 1분기에 하락, 이후 2020년 2분기부터 2021년 1분기까지 하락하는 모습 보임
분기별 매출 금액(10억) 및 점포 수: 
2019년 1분기에 둘다 급격하게 하락하는 형태를 보임, 2020년 1분기에는 매출 금액이 많이 하락하지만, 점포 수는 하락하는 변화가 없음을 알 수 있음

분석 결과 2 : 구별로 확인한 결과, 모두 다른 구에 비해 강남구가 압도적으로 많은 것을 확인할 수 있음
매출 금액: 강남구>중구>서초구>용산구>송파구 순으로 많고, 강북구<도봉구<노원구<중랑구<성북구 등이 적음
매출 건수: 강남구>중구>서초구>마포구>종로구 순으로 많고, 강북구<도봉구<노원구<중랑구<양천구 등이 적음
점포 수: 중구>강남구>종로구>서초구>송파구 순으로 많고, 강북구<노원구<도봉구<서대문구<중랑구 등이 적음

분석 결과 3 : 상권별로 확인한 결과,
매출 금액: 남대문 북창동 다동 무교동 관광특구>가락시장>용산 전자상가_1>용산 전자상가_2>홍익대학교 주변 순으로 많고, 자양종합시장<번동시장<동부청과시장<유영시장<구의시장 순으로 적음
매출 건수: 남대문 북창동 다동 무교통 관광특구>홍익대학교 주변>강남역>동대문패션타운 관광특구>잠실 관광특구 순으로 많고, 자양종합시장<번동시장<푸른터시장<용두시장<도림시장 순으로 적음

분석 결과 4 : 서비스 업종 별로 확인한 결과,
매출 금액/매출 건수가 많은 서비스 업종 상위 15:
어떠한 서비스 업종의 매출 금액이 가장 많았는지 확인한 결과, 한식음식점>일반의류>편의점>컴퓨터 및 주변 장치 판매>슈퍼마켓>일반의원>의약품>화장품>육류판매>호프간이주점>커피음료>청과상>치과의원>반찬가게>분식전문점 순으로 많았음
어떠한 서비스 업종의 매출 건수가 가장 많았는지 확인한 결과, 편의점>한식음식점>커피음료>슈퍼마켓>의약품>분식전문점>일반의원>일반의류>화장품>호프간이주점>반찬가게>육류판매>청과상>컴퓨터 및 주변 장치 판매>치과의원 순으로 많았음
상위 15 서비스 업종별 매출 금액 & 매출 건수: 
상위 15 서비스 업종별로 매출 금액을 확인한 결과, 한식음식점이 꾸준히 많고 그 다음은 일반의류의 매출 금액이 꾸준히 많았으며, 2019년 4분기에 반찬가게의 상승세가 있음. 
매출 건수의 경우, 편의점이 다른 업종에 비해 훨씬 많고, 다음으로 한식음식점, 커피음료 등이 많음
상위 15 서비스 업종별 매출 금액 (전분기 대비 % Change):
상위 15 서비스 업종별로 매출 금액을 전분기 대비 퍼센트 변화로 확인해본 결과, 2019년 4분기에 반찬가게>컴퓨터 및 주변 장치 판매>청과상>일반의류>육류판매>의약품>일반의원이 크게 상승
또한, 2020년 1분기에 육류판매>의약품>슈퍼마켓이 상승하였고, 일반의류, 한식음식점, 분식전문점, 커피음료, 호프간이주점**이 크게 하락함. 이는 코로나로 인한 영향으로 파악됨
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
ax.set_title("분기별 매출 금액(10억)과 남성&여성 매출 건수(1만)", fontsize=20)
ax.set_xlabel('분기')
ax.set_ylabel('매출금액(10억),매출건수(1만)')
ax.grid(linewidth=0.3)
#plt.axvline(x='2020Q1', color='darkred', linestyle='--')
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
#ax1.axvline(x='2020Q1', color='darkred', linestyle='--')
ax2.plot(분기별_추정매출['분기_코드'], 분기별_추정매출['점포수'], label='점포수', color='orange')
ax2.set_title("분기별 점포수", fontsize=18)
ax2.set_ylabel('점포수')
ax2.grid(linewidth=0.3)
#ax2.axvline(x='2020Q1', color='darkred', linestyle='--')

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

plt.title('구별 매출 금액', fontsize=20)
plt.ylabel('총 매출 금액', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 총 매출 건수 시각화
ax = sns.lineplot(x='분기_코드',
             y='분기당_매출_건수',
             hue='시군구',
             data=시군구_추정매출)

plt.title('구별 매출 건수', fontsize=20)
plt.ylabel('총 매출 건수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 총 점포수 시각화
ax = sns.lineplot(x='분기_코드',
             y='점포수',
             hue='시군구',
             data=시군구_추정매출)

plt.title('구별 점포 수', fontsize=20)
plt.ylabel('총 점포수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
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

# 005 : [EDA : BAR] Category by 상권_코드_명
상권코드_추정매출 = 상권_추정매출.groupby(['상권_코드_명']).agg(
    분기당_매출_금액=('분기당_매출_금액', 'sum'), 분기당_매출_건수=('분기당_매출_건수', 'sum')).reset_index()

# 상위 10 / 하위 10 매출 금액
top_상권코드_매출금액 = 상권코드_추정매출.sort_values(by=['분기당_매출_금액'], ascending=False).head(10)
btm_상권코드_매출금액 = 상권코드_추정매출.sort_values(by=['분기당_매출_금액'], ascending=False).tail(10)

# 상위 10 / 하위 10 매출 건수
top_상권코드_매출건수 = 상권코드_추정매출.sort_values(by=['분기당_매출_건수'], ascending=False).head(10)
btm_상권코드_매출건수 = 상권코드_추정매출.sort_values(by=['분기당_매출_건수'], ascending=False).tail(10)

# 총 매출 금액 시각화
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(top_상권코드_매출금액['상권_코드_명'].astype(str), top_상권코드_매출금액['분기당_매출_금액'], color='blue')
ax1.grid(True)
ax1.set_title("상권코드별 상위10 매출 금액", fontsize=15)
ax1.set_ylabel('매출 금액')
ax2.barh(btm_상권코드_매출금액['상권_코드_명'].astype(str), btm_상권코드_매출금액['분기당_매출_금액'], color='skyblue')
ax2.grid(True)
ax2.set_title("상권코드별 하위10 매출 금액", fontsize=15)
ax2.set_ylabel('매출 금액')
fig.suptitle('상권코드별 상위 10 / 하위 10 매출 금액', fontsize=20)
plt.show(block=True)

# 총 매출 건수 시각화
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(top_상권코드_매출건수['상권_코드_명'].astype(str), top_상권코드_매출건수['분기당_매출_건수'], color='blue')
ax1.grid(True)
ax1.set_title("상권코드별 상위10 매출 건수", fontsize=15)
ax1.set_ylabel('매출 건수')
ax2.barh(btm_상권코드_매출건수['상권_코드_명'].astype(str), btm_상권코드_매출건수['분기당_매출_건수'], color='skyblue')
ax2.grid(True)
ax2.set_title("상권코드별 하위10 매출 건수", fontsize=15)
ax2.set_ylabel('매출 건수')
fig.suptitle('상권코드별 상위 10 / 하위 10 매출 건수', fontsize=20)
plt.show(block=True)

# 006 : [EDA : LINE] Category by 서비스_업종_코드_명
업종별_추정매출 = 상권_추정매출.groupby(['기준_년_코드','기준_분기_코드','분기_코드','서비스_업종_코드_명']).agg(
    분기당_매출_금액=('분기당_매출_금액', 'sum'), 분기당_매출_건수=('분기당_매출_건수', 'sum'),점포수=('점포수', 'sum')).reset_index()

# 상위 15 매출 금액
매출금액 = pd.pivot_table(업종별_추정매출, values = ['분기당_매출_금액'], index=['서비스_업종_코드_명'], aggfunc = ['mean', 'sum']).reset_index()
매출금액.columns = ['서비스_업종_코드_명', '평균', '총합']
매출금액 = 매출금액.sort_values(by='총합', ascending=False).head(15)
매출금액 = 매출금액['서비스_업종_코드_명']

업종별_추정매출 = pd.pivot_table(업종별_추정매출, values = ['분기당_매출_금액','분기당_매출_건수'], index=['서비스_업종_코드_명', '분기_코드']).reset_index()
업종별_추정매출 = 업종별_추정매출[업종별_추정매출['서비스_업종_코드_명'].isin(매출금액)]

# 상위 15 매출 건수
매출건수 = pd.pivot_table(업종별_추정매출, values = ['분기당_매출_건수'], index=['서비스_업종_코드_명'], aggfunc = ['mean', 'sum']).reset_index()
매출건수.columns = ['서비스_업종_코드_명', '평균', '총합']
매출건수 = 매출건수.sort_values(by='총합', ascending=False).head(15)
매출건수 = 매출건수['서비스_업종_코드_명']

# 이전 분기 대비 변동률
업종별_추정매출['매출금액_pct_change'] = 업종별_추정매출.sort_values(['분기_코드']).groupby(['서비스_업종_코드_명']).분기당_매출_금액.pct_change()
업종별_추정매출['매출건수_pct_change'] = 업종별_추정매출.sort_values(['분기_코드']).groupby(['서비스_업종_코드_명']).분기당_매출_건수.pct_change()

# 상위 15 서비스 업종별 매출 금액 & 매출 건수
fig, (ax1, ax2) = plt.subplots(2,1)
ax1.set_title("상위 15 서비스 업종별 매출 금액", fontsize=15)
ax1.set_xlabel('분기')
for label, grp in 업종별_추정매출.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '분기당_매출_금액',ax = ax1, label = label, linestyle='-', marker='o')
ax2.set_title("상위 15 서비스 업종별 매출 건수", fontsize=15)
ax2.set_xlabel('분기')
for label, grp in 업종별_추정매출.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '분기당_매출_건수',ax = ax2, label = label, linestyle='-', marker='o')
ax1.legend(fontsize=7, loc="upper right")
ax2.legend(fontsize=7, loc="upper right")
fig.subplots_adjust(wspace=0.1, hspace=0.4)
fig.suptitle('상위 15 서비스 업종별 매출 금액 & 매출 건수', fontsize=20)

# 상위 15 서비스 업종별 매출 금액 (%Change)
# 확인1 = 업종별_추정매출[업종별_추정매출['분기_코드']=='2019Q4'].sort_values(by= '매출금액_pct_change', ascending=False)
# 확인2 = 업종별_추정매출[업종별_추정매출['분기_코드']=='2020Q1'].sort_values(by= '매출금액_pct_change', ascending=False)
fig, ax = plt.subplots()
ax.set_title("상위 15 서비스 업종별 매출 금액 (%Change)", fontsize=15)
ax.set_xlabel('% Change')
for label, grp in 업종별_추정매출.groupby('서비스_업종_코드_명'):
    grp.plot(x='분기_코드', y='매출금액_pct_change', ax = ax, label = label, linestyle='-', marker='o')
ax.legend(loc="upper right", fontsize=7)