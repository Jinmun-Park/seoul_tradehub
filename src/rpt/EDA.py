from src.setup.setup import setup_tradehub

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import font_manager, rc
import matplotlib
import seaborn as sns
import pandas as pd
import numpy as np

# Setup
font_name = font_manager.FontProperties(fname="src/BMDOHYEON_ttf.ttf").get_name()
plt.rc('font', family=font_name)
matplotlib.rcParams['axes.unicode_minus'] = False

# 상주인구
상권_상주인구 = setup_tradehub('상권_상주인구.csv')
상주인구 = 상권_상주인구[[
    '기준_년_코드', '기준_분기_코드', '상권_코드', '상권_코드_명', '분기_코드', '총_상주인구_수','남성_상주인구_수','여성_상주인구_수','연령대_10_상주인구_수','연령대_20_상주인구_수','연령대_30_상주인구_수','연령대_40_상주인구_수','연령대_50_상주인구_수','연령대_60_이상_상주인구_수',
    '엑스좌표_값', '와이좌표_값','시군구_코드', '행정동_코드', '시도명', '시군구', '법정동명']]
상주인구 = 상주인구.loc[상주인구['기준_년_코드'].isin([2019,2020,2021])]

# 생활인구
상권_생활인구 = setup_tradehub('상권_생활인구.csv')
생활인구 = 상권_생활인구[[
    '기준_년_코드', '기준_분기_코드', '상권_코드', '상권_코드_명', '분기_코드', '총_생활인구_수','남성_생활인구_수','여성_생활인구_수','연령대_10_생활인구_수','연령대_20_생활인구_수','연령대_30_생활인구_수','연령대_40_생활인구_수','연령대_50_생활인구_수','연령대_60_이상_생활인구_수',
    '월요일_생활인구_수','화요일_생활인구_수','수요일_생활인구_수','목요일_생활인구_수','금요일_생활인구_수','토요일_생활인구_수','일요일_생활인구_수',
    '엑스좌표_값', '와이좌표_값', '시군구_코드', '행정동_코드', '시도명', '시군구', '법정동명']]
생활인구 = 생활인구.loc[생활인구['기준_년_코드'].isin([2019,2020,2021])]

# 아파트
상권_아파트 = setup_tradehub('상권_아파트.csv')
아파트 = 상권_아파트[[
     '기준_년_코드', '기준_분기_코드', '상권_코드', '상권_코드_명', '분기_코드', '아파트_평균_면적', '아파트_평균_시가',
      '엑스좌표_값', '와이좌표_값', '시군구_코드', '행정동_코드', '시도명', '시군구', '법정동명']]
아파트 = 아파트.loc[아파트['기준_년_코드'].isin([2019,2020,2021])]

# 점포
상권_점포_2019 = setup_tradehub('상권_점포_2019.csv')
상권_점포_2020_2021 = setup_tradehub('상권_점포_2020_2021.csv')
상권_점포 = pd.concat([상권_점포_2019, 상권_점포_2020_2021]).reset_index(drop=True)
점포 = 상권_점포[[
    '기준_년_코드', '기준_분기_코드', '상권_코드', '상권_코드_명', '서비스_업종_코드_명', '분기_코드', '점포_수', '유사_업종_점포_수', '개업_점포_수', '폐업_점포_수', '프랜차이즈_점포_수',
    '엑스좌표_값', '와이좌표_값', '시군구_코드', '행정동_코드', '시도명', '시군구', '법정동명']]

# 매출
상권_추정매출_2019 = setup_tradehub('상권_추정매출_2019.csv')
상권_추정매출_2020 = setup_tradehub('상권_추정매출_2020.csv')
상권_추정매출_2021 = setup_tradehub('상권_추정매출_2021.csv')
상권_추정매출 = pd.concat([상권_추정매출_2019, 상권_추정매출_2020, 상권_추정매출_2021]).reset_index(drop=True)

매출 = 상권_추정매출[[
    '기준_년_코드','기준_분기_코드','상권_코드','상권_코드_명','서비스_업종_코드_명', '분기_코드',
    '분기당_매출_금액', '분기당_매출_건수', '주중_매출_비율','주말_매출_비율','남성_매출_비율','여성_매출_비율',
    '월요일_매출_비율','화요일_매출_비율','수요일_매출_비율','목요일_매출_비율','금요일_매출_비율','토요일_매출_비율','일요일_매출_비율',
    '연령대_10_매출_비율','연령대_20_매출_비율','연령대_30_매출_비율','연령대_40_매출_비율','연령대_50_매출_비율','연령대_60_이상_매출_비율',
    '시간대_00~06_매출_비율','시간대_06~11_매출_비율','시간대_11~14_매출_비율','시간대_14~17_매출_비율','시간대_17~21_매출_비율','시간대_21~24_매출_비율',
    '엑스좌표_값', '와이좌표_값', '시군구_코드', '행정동_코드', '시도명', '시군구', '법정동명']]

# 상권_추정매출['서비스_업종_코드_명'].nunique()
# 상권_점포['서비스_업종_코드_명'].nunique()

# merge
df = 매출.copy()
df = pd.merge(df, 점포, how='left', on=['기준_년_코드','기준_분기_코드','상권_코드','상권_코드_명','서비스_업종_코드_명','분기_코드',
                                      '엑스좌표_값', '와이좌표_값', '시군구_코드', '행정동_코드', '시도명', '시군구', '법정동명'])
df = pd.merge(df, 상주인구, how='left', on=['기준_년_코드','기준_분기_코드','상권_코드','상권_코드_명','분기_코드',
                                        '엑스좌표_값', '와이좌표_값', '시군구_코드', '행정동_코드', '시도명', '시군구', '법정동명'])
df = pd.merge(df, 생활인구, how='left', on=['기준_년_코드','기준_분기_코드','상권_코드','상권_코드_명','분기_코드',
                                        '엑스좌표_값', '와이좌표_값', '시군구_코드', '행정동_코드', '시도명', '시군구', '법정동명'])
df = pd.merge(df, 아파트, how='left', on=['기준_년_코드','기준_분기_코드','상권_코드','상권_코드_명','분기_코드',
                                       '엑스좌표_값', '와이좌표_값', '시군구_코드', '행정동_코드', '시도명', '시군구', '법정동명'])

# null = df.isnull().sum()
# null_시도 = df[df['시도'].isnull()]
# null_상주인구 = 상권_상주인구.isnull().sum()
# null_생활인구 = 상권_생활인구.isnull().sum()
# null_아파트 = 상권_아파트.isnull().sum()
# null_점포 = 상권_점포.isnull().sum()
# null_매출 = 상권_추정매출.isnull().sum()


# df['서비스_업종_코드_명'].nunique() -> 63
# df['상권_코드_명'].nunique() -> 1490
# df['시군구'].nunique() -> 25
# df['시군구'].unique() -> '강동구', '성북구', '동작구', '관악구', '강남구', '구로구', '서초구', '강북구', '광진구', '종로구', '동대문구', '금천구', '성동구',
#                           '영등포구', '강서구', '용산구', '은평구', '중구', '도봉구', '노원구', '중랑구', '마포구', '양천구', '송파구', '서대문구'

시군구_서비스업종_매출 = 상권_추정매출.groupby(['시군구','분기_코드','서비스_업종_코드_명']).agg(분기당_매출_금액=('분기당_매출_금액', 'sum')).reset_index()
test = 시군구_서비스업종_매출[시군구_서비스업종_매출['시군구'] == '강남구'].groupby(['서비스_업종_코드_명']).head(10)


# correlation
df
df_corr = df.corr()
df_corr

# 그림 사이즈 지정
fig, ax = plt.subplots(figsize=(15,15))

# 삼각형 마스크 만들기
mask = np.zeros_like(df_corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# 히트맵을 그린다
sns.heatmap(df_corr,
            cmap = 'RdYlBu_r',
            annot = True,   # 실제 값을 표시한다
            mask=mask,      # 표시하지 않을 마스크 부분을 지정한다
            linewidths=.5,  # 경계면 실선으로 구분하기
            cbar_kws={"shrink": .5},# 컬러바 크기 절반으로 줄이기
            vmin = -1,vmax = 1   # 컬러바 범위 -1 ~ 1
           )
plt.show()


import seaborn as sns
sns.scatterplot(x="", y="", data=df);