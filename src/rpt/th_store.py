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
빅데이터_상권_분석 : 상권_점포
분석 결과 1: 분기별 점포 수를 확인한 결과, 코로나 시기인 2020Q1에 급격히 하락하는 모습을 보임
분기별 프랜차이즈 점포 수를 확인한 결과, 2017Q3 ~ 2019Q3까지 지속적으로 하락하다가 2019Q4에 급격하게 상승한 이후 2020Q1에 조금 하락하는 형태를 보임
분기별 개업 수 & 폐업 수를 확인한 결과, 
개업 수: 2017Q4에 급격하게 하락하고, 코로나 시기인 2020Q1에 하락
폐업 수: 2017Q1에 폐업 점포 수가 가장 많고, 2018Q1과 2020Q1이 많음

분석 결과 2 : 구별로 확인한 결과, 
총 점포수 : 중구>강남구>종로구>서초구>송파구 순으로 많고, 강북구<노원구<도봉구<서대문구<중랑구가 적음
프랜차이즈 점포 수 : 강남구>중구>서초구>송파구>종로구 순으로 많고, 강북구<도봉구<노원구<중랑구<성동구가 적음, 강남구가 현저히 많음
개업 점포 수 : 강남구>중구>마포구>서초구>종로구 순으로 많고, 강북구<노원구<도봉구<서대문구<중랑구가 적음, 강남구, 중구는 2017년 4분기에 급격히 하락
폐업 점포 수 : 중구>강남구>서초구>종로구>마포구 순으로 많고, 강북구<노원구<도봉구<서대문구<성동구가 적음

분석 결과 3 : 상권별로 확인한 결과,
점포 수: 동대문패션타운 관광특구>남대문 북창동 다동 무교통 관광특구>종로청계 관광특구>홍익대학교 주변>남대문시장 순으로 많고, 푸른터시장<박미시장<양남시장<번동시장 등이 적음
프랜차이즈 점포 수: 남대문 북창동 다동 무교통 관광특구>홍익대학교 주변>강남역>명동거리>신촌역 순으로 많고, 양남시장, 번동시장, 천호대로12길, 신정2동골목시장, 천호대로45길 등이 없음
개업 점포 수: 동대문패션타운 관광특구>홍익대학교 주변>남대문 북창동 다동 무교통 관광특구>신사동 가로수길>강남역 순으로 많고, 양남시장, 상계시장, 동부청과시장, 번동시장, 푸른터시장 등이 없음
폐업 점포 수: 동대문패션타운 관광특구>남대문 북창동 다동 무교통 관광특구>홍익대학교 주변>종로청계 관광특구>신사동 가로수길 순으로 많고, 유영시장, 푸른터시장, 용두시장, 신곡종합시장, 양남시장 등이 적음

분석 결과 4 : 서비스 업종 별로 확인한 결과,
점포 수가 많은 서비스 업종 상위 15: 일반의류>한식음식점>부동산중개업>화장품>미용실>호프간이주점>슈퍼마켓>커피음료>분식전문점>전자상거래업>컴퓨터 및 주변 장치 판매>반찬가게>일반의원>노래방>일반교습학원
상위 15 서비스 업종별 점포 수 & 프랜차이즈 점포 수 : 
점포 수를 확인한 결과, 일반의류와 한식음식점의 점포 수는 꾸준히 많았으며, 한식 음식점의 경우 2020년 1분기에 감소하는 형태를 보임
프랜차이즈 점포 수의 경우, 한식 음식점과 커피음료의 점포 수가 꾸준히 많았으며, 최근에는 커피음료 업종의 점포 수가 더 많아짐
상위 15 서비스 업종별 개업 점포 수 & 폐업 점포 수:
개업 점포 수를 확인한 결과, 과거에 일반의류가 많았으나 2017년 이후 많이 감소하는 형태이며 지금까지 꾸준히 감소하고 있고, 한식음식점의 개업 점포 수는 꾸준히 많음
폐업 점포 수의 경우, 일반의류와 한식음식점이 꾸준히 많으며 최근에는 한식음식점이 더 많은 것을 알 수 있음
상위 15 서비스 업종별 점포 수 (전분기 대비 % Change): 
점포 수를 전분기 대비 퍼센트 변화로 확인해본 결과, 코로나 사태가 터진 2020년 1분기에 일반교습학원, 전자상거래업, 호프간이주점을 제외한 전 업종이 다 하락하는 형태 보임
특히 슈퍼마켓이 가장 많이 하락, 다음으로 분식전문점, 커피음료, 한식음식점, 미용실 등이 많이 하락, 다음 분기에는 커피음료, 분식전문점, 슈퍼마켓, 반찬가게, 한식음식점이 전분기 대비 많이 상승
"""

# 001 : Data Load
상권_점포_2016 = setup_tradehub('상권_점포_2016.csv')
상권_점포_2017 = setup_tradehub('상권_점포_2017.csv')
상권_점포_2018 = setup_tradehub('상권_점포_2018.csv')
상권_점포_2019 = setup_tradehub('상권_점포_2019.csv')
상권_점포_2020_2021 = setup_tradehub('상권_점포_2020_2021.csv')

상권_점포 = pd.concat([상권_점포_2016, 상권_점포_2017, 상권_점포_2018, 상권_점포_2019, 상권_점포_2020_2021]).reset_index(drop=True)

# 002 : [EDA : LINE] Total Quarter View Plot
분기별_점포 = 상권_점포.groupby(['기준_년_코드','기준_분기_코드','분기_코드']).agg(
    점포_수=('점포_수', 'sum'), 개업_점포_수=('개업_점포_수', 'sum'), 폐업_점포_수=('폐업_점포_수', 'sum'),프랜차이즈_점포_수=('프랜차이즈_점포_수', 'sum')).reset_index()

fig = plt.figure()
gs = gridspec.GridSpec(2, 2)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, :])

ax1.plot(분기별_점포['분기_코드'], 분기별_점포['점포_수'], label='점포_수')
ax1.set_title("분기별 점포 수", fontsize=12)
ax1.set_xlabel('분기')
ax1.set_ylabel('점포수')
ax1.grid(which='major', linestyle='--', linewidth=0.5)
ax1.grid(which='minor', linestyle=':', linewidth=0.5)

ax2.plot(분기별_점포['분기_코드'], 분기별_점포['프랜차이즈_점포_수'], label='프랜차이즈_점포_수')
ax2.set_title("분기별 프랜차이즈 점포 수", fontsize=12)
ax2.set_xlabel('분기')
ax2.set_ylabel('점포수')
ax2.grid(which='major', linestyle='--', linewidth=0.5)
ax2.grid(which='minor', linestyle=':', linewidth=0.5)

ax3.plot(분기별_점포['분기_코드'], 분기별_점포['개업_점포_수'], label='개업_점포_수', color='teal')
ax3.plot(분기별_점포['분기_코드'], 분기별_점포['폐업_점포_수'], label='폐업_점포_수', color='orange')
ax3.set_title("분기별 개업 수 & 폐업 수", fontsize=12)
ax3.set_xlabel('분기')
ax3.set_ylabel('점포수')
ax3.grid(which='major', linestyle='--', linewidth=0.5)
ax3.grid(which='minor', linestyle=':', linewidth=0.5)

plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
plt.setp(ax3.get_xticklabels(), rotation=45)
fig.subplots_adjust(wspace=0.1, hspace=0.4)
fig.suptitle('분기별 점포수', fontsize=20)
ax3.legend()
plt.show()

# 003 : [EDA : LINE] Quarter View Plot, Category by Region
시군구_점포 = 상권_점포.groupby(['시군구','분기_코드']).agg(
    점포_수=('점포_수', 'sum'), 개업_점포_수=('개업_점포_수', 'sum'), 폐업_점포_수=('폐업_점포_수', 'sum'),프랜차이즈_점포_수=('프랜차이즈_점포_수', 'sum')).reset_index()

# 총 점포 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='점포_수',
             hue='시군구',
             data=시군구_점포)

plt.title('구별 총 점포 수', fontsize=20)
plt.ylabel('총 점포 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 총 개업 점포 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='개업_점포_수',
             hue='시군구',
             data=시군구_점포)

plt.title('구별 총 개업 점포 수', fontsize=20)
plt.ylabel('총 개업 점포 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 총 폐업 점포 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='폐업_점포_수',
             hue='시군구',
             data=시군구_점포)

plt.title('구별 총 폐업 점포 수', fontsize=20)
plt.ylabel('총 폐업 점포 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 총 프랜차이즈 점포 수 시각화
ax = sns.lineplot(x='분기_코드',
             y='프랜차이즈_점포_수',
             hue='시군구',
             data=시군구_점포)

plt.title('구별 총 프랜차이즈 점포 수', fontsize=20)
plt.ylabel('총 프랜차이즈 점포 수', fontsize=14)
plt.xlabel('분기', fontsize=14)
plt.legend(fontsize=12, loc='best')
plt.xticks(rotation=45)
plt.show();

# 004 : [EDA : BAR] Category by Region
시군구_점포2 = 시군구_점포.groupby(['시군구']).점포_수.mean().reset_index()
시군구_점포2 = 시군구_점포2.sort_values(by=['점포_수'], ascending=True)
시군구_점포2 = 시군구_점포2.set_index('시군구')

# 총 점포 수 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_점포2.index, 시군구_점포2['점포_수'], color=my_colors)
plt.title('구별 총 점포 수', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('총 점포 수', fontsize=15)
plt.show();

시군구_점포2 = 시군구_점포.groupby(['시군구']).개업_점포_수.mean().reset_index()
시군구_점포2 = 시군구_점포2.sort_values(by=['개업_점포_수'], ascending=True)
시군구_점포2 = 시군구_점포2.set_index('시군구')

# 총 개업 점포 수 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_점포2.index, 시군구_점포2['개업_점포_수'], color=my_colors)
plt.title('구별 총 개업 점포 수', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('총 개업 점포 수', fontsize=15)
plt.show();

시군구_점포2 = 시군구_점포.groupby(['시군구']).폐업_점포_수.mean().reset_index()
시군구_점포2 = 시군구_점포2.sort_values(by=['폐업_점포_수'], ascending=True)
시군구_점포2 = 시군구_점포2.set_index('시군구')

# 총 폐업 점포 수 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_점포2.index, 시군구_점포2['폐업_점포_수'], color=my_colors)
plt.title('구별 총 폐업 점포 수', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('총 폐업 점포 수', fontsize=15)
plt.show();

시군구_점포2 = 시군구_점포.groupby(['시군구']).프랜차이즈_점포_수.mean().reset_index()
시군구_점포2 = 시군구_점포2.sort_values(by=['프랜차이즈_점포_수'], ascending=True)
시군구_점포2 = 시군구_점포2.set_index('시군구')

# 총 프랜차이즈 점포 수 시각화
my_colors = ['#fcd5ce', '#e8e8e4', '#ffd7ba']
plt.barh(시군구_점포2.index, 시군구_점포2['프랜차이즈_점포_수'], color=my_colors)
plt.title('구별 총 프랜차이즈 점포 수', fontsize=18)
plt.ylabel('시군구', fontsize=15)
plt.xlabel('총 프랜차이즈 점포 수', fontsize=15)
plt.show();

# 005 : [EDA : BAR] Category by 상권_코드_명
상권코드_점포 = 상권_점포.groupby(['상권_코드_명']).agg(
    점포_수=('점포_수', 'sum'),
    개업_점포_수=('개업_점포_수', 'sum'),
    폐업_점포_수=('폐업_점포_수', 'sum'),
    프랜차이즈_점포_수=('프랜차이즈_점포_수', 'sum')
).reset_index()

# 상위 10 / 하위 10 점포 수
top_상권코드_점포수 = 상권코드_점포.sort_values(by=['점포_수'], ascending=False).head(10)
btm_상권코드_점포수 = 상권코드_점포.sort_values(by=['점포_수'], ascending=False).tail(10)

# 상위 10 / 하위 10 프랜차이즈 점포 수
top_상권코드_프랜차이즈점포수 = 상권코드_점포.sort_values(by=['프랜차이즈_점포_수'], ascending=False).head(10)
btm_상권코드_프랜차이즈점포수 = 상권코드_점포.sort_values(by=['프랜차이즈_점포_수'], ascending=False).tail(10)

# 상위 10 / 하위 10 개업 점포 수
top_상권코드_개업점포수 = 상권코드_점포.sort_values(by=['개업_점포_수'], ascending=False).head(10)
btm_상권코드_개업점포수 = 상권코드_점포.sort_values(by=['개업_점포_수'], ascending=False).tail(10)

# 상위 10 / 하위 10 폐업 점포 수
top_상권코드_폐업점포수 = 상권코드_점포.sort_values(by=['폐업_점포_수'], ascending=False).head(10)
btm_상권코드_폐업점포수 = 상권코드_점포.sort_values(by=['폐업_점포_수'], ascending=False).tail(10)

# 총 점포 수 시각화
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(top_상권코드_점포수['상권_코드_명'].astype(str), top_상권코드_점포수['점포_수'], color='blue')
ax1.grid(True)
ax1.set_title("상권코드별 상위10 점포 수", fontsize=15)
ax1.set_ylabel('점포 수')
ax2.barh(btm_상권코드_점포수['상권_코드_명'].astype(str), btm_상권코드_점포수['점포_수'], color='skyblue')
ax2.grid(True)
ax2.set_title("상권코드별 하위10 점포 수", fontsize=15)
ax2.set_ylabel('점포 수')
fig.suptitle('상권코드별 상위 10 / 하위 10 점포 수', fontsize=20)
plt.show(block=True)

# 프랜차이즈 점포 수 시각화
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(top_상권코드_프랜차이즈점포수['상권_코드_명'].astype(str), top_상권코드_프랜차이즈점포수['프랜차이즈_점포_수'], color='blue')
ax1.grid(True)
ax1.set_title("상권코드별 상위10 프랜차이즈 점포 수", fontsize=15)
ax1.set_ylabel('프랜차이즈 점포 수')
ax2.barh(btm_상권코드_프랜차이즈점포수['상권_코드_명'].astype(str), btm_상권코드_프랜차이즈점포수['프랜차이즈_점포_수'], color='skyblue')
ax2.grid(True)
ax2.set_title("상권코드별 하위10 프랜차이즈 점포 수", fontsize=15)
ax2.set_ylabel('프랜차이즈 점포 수')
fig.suptitle('상권코드별 상위 10 / 하위 10 프랜차이즈 점포 수', fontsize=20)
plt.show(block=True)

# 개업 점포 수 시각화
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(top_상권코드_개업점포수['상권_코드_명'].astype(str), top_상권코드_개업점포수['개업_점포_수'], color='blue')
ax1.grid(True)
ax1.set_title("상권코드별 상위10 개업 점포 수", fontsize=15)
ax1.set_ylabel('개업 점포 수')
ax2.barh(btm_상권코드_개업점포수['상권_코드_명'].astype(str), btm_상권코드_개업점포수['개업_점포_수'], color='skyblue')
ax2.grid(True)
ax2.set_title("상권코드별 하위10 개업 점포 수", fontsize=15)
ax2.set_ylabel('개업 점포 수')
fig.suptitle('상권코드별 상위 10 / 하위 10 개업 점포 수', fontsize=20)
plt.show(block=True)

# 폐업 점포 수 시각화
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.barh(top_상권코드_폐업점포수['상권_코드_명'].astype(str), top_상권코드_폐업점포수['폐업_점포_수'], color='blue')
ax1.grid(True)
ax1.set_title("상권코드별 상위10 폐업 점포 수", fontsize=15)
ax1.set_ylabel('폐업 점포 수')
ax2.barh(btm_상권코드_폐업점포수['상권_코드_명'].astype(str), btm_상권코드_폐업점포수['폐업_점포_수'], color='skyblue')
ax2.grid(True)
ax2.set_title("상권코드별 하위10 폐업 점포 수", fontsize=15)
ax2.set_ylabel('폐업 점포 수')
fig.suptitle('상권코드별 상위 10 / 하위 10 폐업 점포 수', fontsize=20)
plt.show(block=True)

# 006 : [EDA : LINE] Category by 서비스_업종_코드_명
업종별_점포 = 상권_점포.groupby(['기준_년_코드','기준_분기_코드','분기_코드','서비스_업종_코드_명']).agg(
    점포_수=('점포_수', 'sum'),
    개업_점포_수=('개업_점포_수', 'sum'),
    폐업_점포_수=('폐업_점포_수', 'sum'),
    프랜차이즈_점포_수=('프랜차이즈_점포_수', 'sum')
).reset_index()

점포수 = pd.pivot_table(업종별_점포, values = ['점포_수'], index=['서비스_업종_코드_명'], aggfunc = ['mean', 'sum']).reset_index()
점포수.columns = ['서비스_업종_코드_명', '평균', '총합']
점포수 = 점포수.sort_values(by='총합', ascending=False).head(15)
점포수 = 점포수['서비스_업종_코드_명']

업종별_점포 = pd.pivot_table(업종별_점포, values = ['점포_수','개업_점포_수','폐업_점포_수','프랜차이즈_점포_수'], index=['서비스_업종_코드_명', '분기_코드']).reset_index()
업종별_점포 = 업종별_점포[업종별_점포['서비스_업종_코드_명'].isin(점포수)]

# 이전 분기 대비 변동률
# 업종별_점포['점포_수_pchange'] = 업종별_점포.groupby('서비스_업종_코드_명', sort=False)['점포_수'].apply(lambda x: x.pct_change()).to_numpy()
업종별_점포['점포수_pct_change'] = 업종별_점포.sort_values(['분기_코드']).groupby(['서비스_업종_코드_명']).점포_수.pct_change()
업종별_점포['개업점포수_pct_change'] = 업종별_점포.sort_values(['분기_코드']).groupby(['서비스_업종_코드_명']).개업_점포_수.pct_change()
업종별_점포['폐업점포수_pct_change'] = 업종별_점포.sort_values(['분기_코드']).groupby(['서비스_업종_코드_명']).폐업_점포_수.pct_change()
업종별_점포['프랜차이즈점포수_pct_change'] = 업종별_점포.sort_values(['분기_코드']).groupby(['서비스_업종_코드_명']).프랜차이즈_점포_수.pct_change()

# 상위 15 서비스 업종별 점포 수 & 프랜차이즈 점포 수
fig, (ax1, ax2) = plt.subplots(2,1)
ax1.set_title("상위 15 서비스 업종별 점포 수", fontsize=15)
ax1.set_xlabel('분기')
for label, grp in 업종별_점포.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '점포_수',ax = ax1, label = label, linestyle='-', marker='o')
ax2.set_title("상위 15 서비스 업종별 프랜차이즈 점포 수", fontsize=15)
ax2.set_xlabel('분기')
for label, grp in 업종별_점포.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '프랜차이즈_점포_수',ax = ax2, label = label, linestyle='-', marker='o')
ax1.legend(fontsize=7, loc="upper right")
ax2.legend(fontsize=7, loc="upper right")
fig.subplots_adjust(wspace=0.1, hspace=0.4)
fig.suptitle('상위 15 서비스 업종별 점포 수 & 프랜차이즈 점포 수', fontsize=20)

# 상위 15 서비스 업종별 개업 점포 수 & 폐업 점포 수
fig, (ax1,ax2) = plt.subplots(2,1)
ax1.set_title("상위 15 서비스 업종별 개업 점포 수", fontsize=15)
ax1.set_xlabel('분기')
for label, grp in 업종별_점포.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '개업_점포_수',ax = ax1, label = label, linestyle='-', marker='o')
ax2.set_title("상위 15 서비스 업종별 폐업 점포 수", fontsize=15)
ax2.set_xlabel('분기')
for label, grp in 업종별_점포.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '폐업_점포_수',ax = ax2, label = label, linestyle='-', marker='o')
ax1.legend(fontsize=7, loc="upper right")
ax2.legend(fontsize=7, loc="upper right")
fig.subplots_adjust(wspace=0.1, hspace=0.4)
fig.suptitle('상위 15 서비스 업종별 개업 점포 수 & 폐업 점포 수', fontsize=20)

# 상위 15 서비스 업종별 점포 수 (%Change)
# 확인1 = 업종별_점포[업종별_점포['분기_코드']=='2020Q1'].sort_values(by= '점포수_pct_change', ascending=False)
# 확인2 = 업종별_점포[업종별_점포['분기_코드']=='2020Q2'].sort_values(by= '점포수_pct_change', ascending=False)
fig, ax = plt.subplots()
ax.set_title("상위 15 서비스 업종별 점포 수 (%Change)", fontsize=15)
ax.set_xlabel('% Change')
for label, grp in 업종별_점포.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '점포수_pct_change',ax = ax, label = label, linestyle='-', marker='o')
ax.legend(loc="upper right", fontsize=7)


