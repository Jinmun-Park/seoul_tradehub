#------------------------------- LIBRARY -------------------------------#
# Library
import pandas as pd
from src.setup.setup import select_columns, convert_float_int, column_space
#------------------------------- SET UP -------------------------------#
공영주차장 = pd.read_csv('data/도로명별_공영주차장.csv')

# Text To Columns using address
dic = {0: '시군구', 1: '법정동', 2: '주소_1', 3: '주소_2', 4: '주소_3', 5: '주소_4', 6: '주소_5', 7: '주소_6', 8: '주소_7', 9: '주소_8', 10: '주소_9'}
공영주차장 = pd.concat([공영주차장, 공영주차장['주소'].str.split(' ', expand=True)], axis=1).rename(columns=dic)

# Converting float to int
공영주차장 = convert_float_int(data=공영주차장, columns=['주차장코드', '기본 주차 요금', '기본 주차 시간(분 단위)', '추가 단위 요금'])

# Select columns and rename
공영주차장 = select_columns(data=공영주차장, names=['주차장코드', '주소', '법정동', '총 주자면', '기본 주차 요금', '기본 주차 시간(분 단위)',
                                          '추가 단위 요금', '주차장 위치 좌표 위도', '주차장 위치 좌표 경도'])
공영주차장 = 공영주차장.rename(columns={'주차장 위치 좌표 위도': '주차장_x'})

# Remove Column spaces
공영주차장 = column_space(공영주차장)




