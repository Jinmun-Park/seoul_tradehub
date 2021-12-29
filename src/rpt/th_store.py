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
빅데이터_상권_분석 : 상권_점포
분석 결과 1 : 
"""

# 001 : Data Load
상권_점포 = setup_tradehub('상권_점포.csv')

# EDA PART 4 : 점포
'''
***** 2019Q1부터 데이터 존재.
***** 중요한 데이터. 하지만 예)한식음식점이 증가하는것이 유동인구 혹은 골목상권에 어떠한 영향이 있을까?
질문 1 : 분기별 점포수는 코로나 이후 얼마 줄었을까? 폐업과 같이 확인
그래프 1 [2019-2021 분기별 점포수] : 코로나시기에 증가하는 점포수. 하지만 2020Q1이후로 줄어드는 트렌드.

질문 2 : 상위 15 점포의 변화는 어떨까 ?
그래프 2 & 3 [상위15 서비스업종별 점포 & 프랜차이즈 수] [서비스업종별 상위15 점포 & 프랜차이즈 수] :
첫벗째, 점포수 & 프랜차이즈 점포수는 크게 눈에띄게 하락하지 않았다.
두번째, 눈에 띄지않지만 줄어드는 개업점포수와 2020Q2 이후 증가하는 폐업수. 코로나의 영향이라 할수 있을만함 움직임.
세번째, 코로나 기간인 2020Q1 상위 15 서비스업종에서 보이는 폐업수

질문 3 : y-axis의 차이로 질문2에 대한 답변이 여러운관계로 %Change.
그래프 4 & 5 [점포수 기준 상위 15 서비스업종 폐업점포 수 (%Change)]:
-전자상거래업 12퍼센트 상승
-일반교습학원 10퍼센트상승
-호프간이주점 7퍼센트 상승
-분식전문저 5퍼센트 하락
'''
점포['분기_코드'] = 점포['기준_년_코드'].astype(str) + 'Q' + 점포['기준_분기_코드'].astype(str)

# 분기별 점포수
eda_분기별_점포 = 점포.groupby(['기준_년_코드','기준_분기_코드','분기_코드']).agg(
    점포_수=('점포_수', 'sum'),
    개업_점포_수=('개업_점포_수', 'sum'),
    폐업_점포_수=('폐업_점포_수', 'sum'),
    프랜차이즈_점포_수=('프랜차이즈_점포_수', 'sum')
).reset_index()

# 그래프 1
fig = plt.figure()
gs = gridspec.GridSpec(2, 2)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, :])

ax1.plot(eda_분기별_점포['분기_코드'], eda_분기별_점포['점포_수'], label='점포_수')
ax1.set_title("분기별 점포 수", fontsize=12)
ax1.set_xlabel('분기')
ax1.set_ylabel('점포수')
ax1.grid(which='major', linestyle='--', linewidth=0.5)
ax1.grid(which='minor', linestyle=':', linewidth=0.5)

ax2.plot(eda_분기별_점포['분기_코드'], eda_분기별_점포['프랜차이즈_점포_수'], label='프랜차이즈_점포_수')
ax2.set_title("분기별 프랜차이즈_점포 수", fontsize=12)
ax2.set_xlabel('분기')
ax2.set_ylabel('점포수')
ax2.grid(which='major', linestyle='--', linewidth=0.5)
ax2.grid(which='minor', linestyle=':', linewidth=0.5)

ax3.plot(eda_분기별_점포['분기_코드'], eda_분기별_점포['개업_점포_수'], label='개업_점포_수', color='teal')
ax3.plot(eda_분기별_점포['분기_코드'], eda_분기별_점포['폐업_점포_수'], label='폐업_점포_수', color='orange')
ax3.set_title("분기별 개업&폐업 수", fontsize=12)
ax3.set_xlabel('분기')
ax3.set_ylabel('점포수')
ax3.grid(which='major', linestyle='--', linewidth=0.5)
ax3.grid(which='minor', linestyle=':', linewidth=0.5)

plt.setp(ax1.get_xticklabels(), rotation=45)
plt.setp(ax2.get_xticklabels(), rotation=45)
fig.subplots_adjust(wspace=0.1, hspace=0.4)
fig.suptitle('2019-2021 분기별 점포수', fontsize=20)
ax3.legend()
plt.show()

# 업종별 점포수
eda_업종별_점포 = 점포.groupby(['기준_년_코드','기준_분기_코드','분기_코드','서비스_업종_코드_명']).agg(
    점포_수=('점포_수', 'sum'),
    개업_점포_수=('개업_점포_수', 'sum'),
    폐업_점포_수=('폐업_점포_수', 'sum'),
    프랜차이즈_점포_수=('프랜차이즈_점포_수', 'sum')
).reset_index()

eda_점포수 = pd.pivot_table(eda_업종별_점포, values = ['점포_수'], index=['서비스_업종_코드_명']).reset_index()
eda_점포수 = eda_점포수.sort_values(by='점포_수', ascending=False).head(15)
eda_점포수 = eda_점포수['서비스_업종_코드_명']

eda_업종별_점포 = pd.pivot_table(eda_업종별_점포, values = ['점포_수','개업_점포_수','폐업_점포_수','프랜차이즈_점포_수'], index=['서비스_업종_코드_명', '분기_코드']).reset_index()
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