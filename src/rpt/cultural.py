#------------------------------- LIBRARY -------------------------------#
# Library
import pandas as pd
from src.setup.setup import select_columns, column_space
#------------------------------- SET UP -------------------------------#

def 문화공간정보_data_load():
    """
    DESCRIPTION 1 : Data preprocessing and the dataframe will be used in data mapping process.
    """
    # Data load
    문화공간 = pd.read_csv('data/도로명별_문화공간정보.csv')

    # Text To Columns using address
    dic = {0: '시군구', 1: '법정동', 2: '주소_1', 3: '주소_2', 4: '주소_3', 5: '주소_4', 6: '주소_5', 7: '주소_6', 8: '주소_7', 9: '주소_8', 10: '주소_9'}
    문화공간 = pd.concat([문화공간, 문화공간['주소'].str.split(' ', expand=True)], axis=1).rename(columns=dic)

    # Select columns and rename
    문화공간 = select_columns(data=문화공간, names=['주제분류', '문화시설명', '주소', '법정동', 'X좌표', 'Y좌표'])
    문화공간 = 문화공간.rename(columns={'X좌표': 'y', 'Y좌표': 'x'})

    # Remove Column spaces
    output = column_space(문화공간)

    return output