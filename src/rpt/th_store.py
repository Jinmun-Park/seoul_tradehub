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
분석 결과 1 : 2019Q1부터 데이터 존재. 중요한 데이터. 하지만 예)한식음식점이 증가하는 것이 유동인구 혹은 골목상권에 어떠한 영향이 있을까?

질문 1 : 분기별 점포수는 코로나 이후 얼마 줄었을까? 폐업과 같이 확인
그래프 1 [2019-2021 분기별 점포수] : 코로나시기에 증가하는 점포수. 하지만 2020Q1이후로 줄어드는 트렌드.

질문 2 : 상위 15 점포의 변화는 어떨까 ?
[상위15 서비스업종별 점포 & 프랜차이즈 수] [서비스업종별 상위15 점포 & 프랜차이즈 수] :
첫벗째, 점포수 & 프랜차이즈 점포수는 크게 눈에띄게 하락하지 않았다.
두번째, 눈에 띄지않지만 줄어드는 개업점포수와 2020Q2 이후 증가하는 폐업수. 코로나의 영향이라 할수 있을만함 움직임.
세번째, 코로나 기간인 2020Q1 상위 15 서비스업종에서 보이는 폐업수

질문 3 : y-axis의 차이로 질문2에 대한 답변이 여러운관계로 %Change.
그래프 4 & 5 [점포수 기준 상위 15 서비스업종 폐업점포 수 (%Change)]:
-전자상거래업 12퍼센트 상승
-일반교습학원 10퍼센트상승
-호프간이주점 7퍼센트 상승
-분식전문점 5퍼센트 하락
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

# 006 : [EDA : BAR] Category by 업종

업종별_점포 = 상권_점포.groupby(['기준_년_코드','기준_분기_코드','분기_코드','서비스_업종_코드_명']).agg(
    점포_수=('점포_수', 'sum'),
    개업_점포_수=('개업_점포_수', 'sum'),
    폐업_점포_수=('폐업_점포_수', 'sum'),
    프랜차이즈_점포_수=('프랜차이즈_점포_수', 'sum')
).reset_index()

eda_점포수 = pd.pivot_table(업종별_점포, values = ['점포_수'], index=['서비스_업종_코드_명']).reset_index()
eda_점포수 = eda_점포수.sort_values(by='점포_수', ascending=False).head(15)
eda_점포수 = eda_점포수['서비스_업종_코드_명']

eda_업종별_점포 = pd.pivot_table(업종별_점포, values = ['점포_수','개업_점포_수','폐업_점포_수','프랜차이즈_점포_수'], index=['서비스_업종_코드_명', '분기_코드']).reset_index()
eda_업종별_점포 = eda_업종별_점포[eda_업종별_점포['서비스_업종_코드_명'].isin(eda_점포수)]
eda_업종별_점포['점포_수_pchange'] = eda_업종별_점포.groupby('서비스_업종_코드_명', sort=False)['점포_수'].apply(lambda x: x.pct_change()).to_numpy()
eda_업종별_점포['개업_점포_수_pchange'] = eda_업종별_점포.groupby('서비스_업종_코드_명', sort=False)['개업_점포_수'].apply(lambda x: x.pct_change()).to_numpy()
eda_업종별_점포['폐업_점포_수_pchange'] = eda_업종별_점포.groupby('서비스_업종_코드_명', sort=False)['폐업_점포_수'].apply(lambda x: x.pct_change()).to_numpy()
eda_업종별_점포['프랜차이즈_점포_수_pchange'] = eda_업종별_점포.groupby('서비스_업종_코드_명', sort=False)['프랜차이즈_점포_수'].apply(lambda x: x.pct_change()).to_numpy()

# 그래프 2 : 점포수 기준 상위15 서비스업종별 점포 & 프랜차이즈 수
fig, (ax1, ax2) = plt.subplots(2,1)
ax1.set_title("점포수 기준 상위 15 서비스업종 점포 수", fontsize=15)
ax1.set_xlabel('분기')
for label, grp in eda_업종별_점포.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '점포_수',ax = ax1, label = label, linestyle='-', marker='o')
ax.legend(loc="upper right", fontsize=7)
for label, grp in eda_업종별_점포.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '프랜차이즈_점포_수',ax = ax2, label = label, linestyle='-', marker='o')
ax1.legend(fontsize=7, loc="upper right")
ax2.legend(fontsize=7, loc="upper right")
fig.subplots_adjust(wspace=0.1, hspace=0.4)
fig.suptitle('점포수 기준 상위15 서비스업종별 점포 & 프랜차이즈 수', fontsize=20)

# 그래프 3 : 점포수 기준 서비스업종별 상위15 점포 & 프랜차이즈 수
fig, (ax1,ax2) = plt.subplots(2,1)
ax1.set_title("점포수 기준 상위15 점포 개업점포 수", fontsize=15)
ax1.set_xlabel('분기')
for label, grp in eda_업종별_점포.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '개업_점포_수',ax = ax1, label = label, linestyle='-', marker='o')
ax2.set_title("점포수 기준 상위15 점포 폐업 수", fontsize=15)
ax2.set_xlabel('분기')
for label, grp in eda_업종별_점포.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '폐업_점포_수',ax = ax2, label = label, linestyle='-', marker='o')
ax1.legend(fontsize=7, loc="upper right")
ax2.legend(fontsize=7, loc="upper right")
fig.subplots_adjust(wspace=0.1, hspace=0.4)
fig.suptitle('점포수 기준 서비스업종별 상위15 점포 & 프랜차이즈 수', fontsize=20)

# 그래프 4 : 점포수 기준 상위 15 서비스업종 점포수 (%Change)
fig, ax = plt.subplots()
ax.set_title("점포수 기준 상위 15 서비스업종 점포수 (%Change)", fontsize=15)
ax.set_xlabel('% Change')
for label, grp in eda_업종별_점포.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '점포_수_pchange',ax = ax, label = label, linestyle='-', marker='o')
ax.legend(loc="upper right", fontsize=7)

# 그래프 5 : 점포수 기준 상위 15 서비스업종 폐업점포 수 (%Change)
fig, ax = plt.subplots()
ax.set_title("점포수 기준 상위 15 서비스업종 폐업점포 수 (%Change)", fontsize=15)
ax.set_xlabel('% Change')
for label, grp in eda_업종별_점포.groupby('서비스_업종_코드_명'):
    grp.plot(x = '분기_코드', y = '폐업_점포_수_pchange',ax = ax, label = label, linestyle='-', marker='o')
ax.legend(loc="upper right", fontsize=7)