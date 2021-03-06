#------------------------------- LIBRARY -------------------------------#
# Library
import pandas as pd

#------------------------------- SET UP -------------------------------#

def read_csv_files(file_name):
    return pd.read_csv('data/' + file_name)

def select_columns(data, names):
    """
    Remove Columns from the dataframe after the load
    """
    output = data[names]

    return output

def convert_float_int(data, columns):
   """
   Converting float to int type
   """
   data[columns] = data[columns].fillna(0).astype(int)

   return data

def setup_code():
    """
    DESCRIPTION : Read tradehub.csv and map the code to elaborate address details. This dataframe will be used to map with other csv files.
    """
    # 1. TRADEHUB_ADDRESS
    상권_영역 = pd.read_csv('data/상권_영역.csv')
    #행정동코드 = pd.read_csv('data/행정동코드.csv')
    법정동코드 = pd.read_csv('data/법정동코드.csv')

    # 2. DROP COLUMN FIELDS
    상권_영역 = 상권_영역.drop(['기준_년월_코드', '상권_구분_코드', '상권_구분_코드_명', '상권_코드_명', '형태정보'], axis=1)
    #행정동코드 = select_columns(data=행정동코드, names=['시도', '시군구', '행정구역명', '행정동(행정기관명)', '법정동', '행정구역코드', '행정동_코드', '법정동코드'])
    #행정동코드 = 행정동코드.drop_duplicates(subset=['행정동_코드'])
    법정동코드 = select_columns(data=법정동코드, names=['시군구코드', '시도명', '시군구명', '법정동명'])
    법정동코드 = 법정동코드.drop_duplicates(subset=['시군구코드'])

    # 3. CHANGE TYPE 'FLOAT' TO 'INT"
    상권_영역 = convert_float_int(data=상권_영역, columns=['상권_코드', '엑스좌표_값', '와이좌표_값', '시군구_코드', '행정동_코드'])
    data_y = convert_float_int(data=법정동코드, columns=['시군구코드'])

    # 4. DATA MERGE BASED ON '행정동_코드'
    data_y = data_y.rename(columns={'시군구코드': '시군구_코드', '시군구명': '시군구'})
    output = 상권_영역.merge(data_y, how='left', on=['시군구_코드'])

    # output = '종합코드'
    return output

#------------------------ DATA PREPROCESSING FUNCTION ----------------------#

def column_space(data):
    """
    DESCRIPTION : Format the column names
    """
    data.columns = data.columns = data.columns.str.replace(' ', '_')
    return data


def run_cleaning(data):
    """
    DESCRIPTION : Run light data cleaning
    """
    # 1 : Changing text errors in column fields
    output = column_space(data)
    # 2 : Converting date
    data['분기_코드'] = data['기준_년_코드'].astype(str) + 'Q' + data['기준_분기_코드'].astype(str)

    return output

#------------------------ RUNNING ----------------------#
def setup_tradehub(file):
    """
    DESCRIPTION 1 : Run a basic data cleaning to merge the tradehub datasets
    DESCRIPTION 2 : Merge '상권영역' and '법정동코드' csv based on '시군구_코드'
    DESCRIPTION 3 : '법정동코드' adds the state, city information to the tradehub datasets
    """

    # 1. Read CSV Files
    csv = read_csv_files(file)
    # 2. Read tradehub address code dataframe
    종합코드 = setup_code()
    # 3. Run early data cleaning from the file loaded in step (1)
    data = run_cleaning(data=csv)
    # 4. Data Merge
    output = data.merge(종합코드, how='left', on=['상권_코드'])

    return output


