#------------------------------- LIBRARY -------------------------------#
# Library
import pandas as pd
import numpy as np
from src.setup.setup import select_columns, column_space

from src.map.map import map_axes
#------------------------------- SET UP -------------------------------#

def run_adrapi(api_key, key_address):
    """
    DESCRIPTION 1 : Uses 'map_axes' function. It collects 'x_좌표' and 'y_좌표' using map address(지번)
    DESCRIPTION 2 : Cut the word in -n sequence till we can collect either '지번주소' or '도로명주소'
    """
    n = -1
    while True:
        n -= 1
        address = ' '.join(key_address.split()[:n])
        if pd.notnull(map_axes(key=api_key, address=address)[0]):
            a, b, c = map_axes(key=api_key, address=address)
            break
        elif len(address) == 0:
            a, b, c = np.nan
            break

    return a, b, c

def adjust_space(address):
    """
    DESCRIPTION 1 : Adjusting the addresses that they do not specify the state using white space.
    DESCRIPTION 2 : White space in the address will be adjusted using the function.
    """

    # Dictionary to identify the space
    num_dic = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    wd_dic = ['번', '-', '가', '호', '층', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    whitespace = 0
    space_whitespace = 0

    # Get the white space
    for i in range(len(address)):
        if address[i] == '동' and address[i+1].isdigit():
            whitespace = i

    # Get the text
    for i in range(len(address)-1):
        if (address[i] in num_dic) and (address[i-1] in num_dic) and (address[i+1] not in wd_dic):
            space_whitespace = i+1

    # Apply the spaces to adjust the address
    if whitespace == 0:
        output = address[:space_whitespace + 1] + ' ' + address[space_whitespace + 1:]
    elif space_whitespace == 0:
        output = address[:whitespace + 1] + ' ' + address[whitespace + 1:]
    else:
        output = address[:whitespace + 1] + ' ' + address[whitespace + 1:]
        output = output[:space_whitespace + 1] + ' ' + output[space_whitespace + 1:]

    return output

def 병원_data_load():
    """
    DESCRIPTION 1 : Data preprocessing and the dataframe will be used in data mapping process.
    """
    # Data load
    병원 = pd.read_csv('data/도로명별_병원인허가.csv')

    # Text To Columns using address
    dic = {0: '시군구', 1: '법정동', 2: '주소_1', 3: '주소_2', 4: '주소_3', 5: '주소_4', 6: '주소_5', 7: '주소_6', 8: '주소_7', 9: '주소_8', 10: '주소_9'}
    병원 = pd.concat([병원, 병원['지번주소'].str.split(' ', expand=True)], axis=1).rename(columns=dic)

    # Select columns and rename
    병원 = select_columns(data=병원, names=['상세영업상태명', '도로명주소', '지번주소', '법정동', '사업장명', '업태구분명', '좌표정보(X)', '좌표정보(Y)'])
    병원 = 병원.rename(columns={'지번주소': '상세주소', '좌표정보(X)': 'x', '좌표정보(Y)': 'y'})

    # Replace strings
    병원['도로명주소'] = 병원['도로명주소'].replace({' +': ' '}, regex=True)
    병원['상세주소'] = 병원['상세주소'].replace({' +': ' '}, regex=True)

    # Running loop to filter out either '지번' or '도로명' that does not contain 'x_좌표' and 'y_좌표'
    map_address = pd.DataFrame(columns=['입력주소', '추출_주소', 'x', 'y'])
    for i in range(len(병원)):
        if pd.isnull(병원['x'][i]) and pd.isnull(병원['도로명주소'][i]):
            map_address.loc[i, '입력주소'] = 병원['상세주소'][i]
        elif pd.isnull(병원['x'][i]) and pd.isnull(병원['상세주소'][i]):
            map_address.loc[i, '입력주소'] = 병원['도로명주소'][i]
        elif pd.isnull(병원['x'][i]):
            map_address.loc[i, '입력주소'] = 병원['도로명주소'][i]
        else:
            map_address.loc[i, '입력주소'] = np.nan

    # Adjusting the space in 'address' field
    for index, value in enumerate(map_address['입력주소']):
        if pd.isna(value):
            continue
        else:
            map_address.loc[index, '입력주소'] = adjust_space(address=value)

    # Merge
    #병원 = pd.merge(병원, map_address, left_index=True, right_index=True)

    #
    '''
    for index, value in enumerate(map_address['입력주소']):
        # Ignore the null values
        if pd.isnull(value):
            continue
        # Convert the pre-defined address to readable address that KAKAO API can read.
        else:
            #추출_주소, x, y = run_adrapi(api_key='65265d19337c32168628d36054955392', key_address=value)
            map_address.loc[index, '추출_주소'] = 추출_주소
            map_address.loc[index, 'x'] = x
            map_address.loc[index, 'y'] = y
    print('Completed filling in the address using x,y axes')

   return output
    '''