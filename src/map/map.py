#------------------------------- LIBRARY -------------------------------#
import pandas as pd
import requests
import json
import numpy as np
# Converting X,Y axes into Latitude, Longitude
from pyproj import Transformer, CRS
# Trade hub data load and setup
from src.setup.setup import select_columns, setup_tradehub
# Directory path and pickle setup
import os
from datetime import datetime
import pickle

# Load cleaned data
from src.rpt.carpark import 공영주차장_data_load
from src.rpt.cultural import 문화공간정보_data_load
#----------------------------- DATA LOAD -----------------------------#
def 아파트_data_load():
    """
    DESCRIPTION 1 : Load cleaned data for mapping
    AVAILABILITY : '공연주차장', '상권_아파트'
    """
    상권_아파트 = setup_tradehub('상권_아파트.csv')
    상권_아파트 = select_columns(data=상권_아파트, names=['기준_년_코드', '기준_분기_코드', '분기_코드', '상권_구분_코드_명', '상권_코드_명',
                                                '아파트_평균_면적', '아파트_평균_시가', '시도', '시군구', '법정동', '엑스좌표_값', '와이좌표_값'])
    return 상권_아파트

#------------------------------- SET UP -------------------------------#

def pickle_replace(name, file):
    """
    DESCRIPTION 1 : Creating Path and Pickle file if these are not existing.
    DESCROPTION 2 : If Pickle file is already existing in your directory, then it will be replaced with new pickle files.
    USAGE : Most API Calls in this project will use 'pickle_replace' function to store the dataframe in pickle format.
    """
    # Create pickle directory path if it does not exist
    try:
        if not os.path.exists('pickle/'):
            try:
                os.makedirs('pickle')
            except FileExistsError:
                pass
    except Exception as e:
        print('Failed to create directory (pickle/..) ' + name.upper() + e.__str__())
    else:
        print('Successfully created directory (pickle/..) ' + name.upper())
    # Create pickle file if the file is not existing (If the file exist, then write it again)
    try:
        if os.path.exists('pickle/' + name + '.pkl'):
            with open('pickle/' + name + '.pkl', 'wb') as f:
                pickle.dump(file, f)
        else:
            file.to_pickle('pickle/' + name + '.pkl')
    except Exception as e:
        print('Failed to export(.pkl) ' + name.upper() + e.__str__())
    else:
        print('Successfully export(.pkl) ' + name.upper())

def read_pickle(file_name: str) -> pd.DataFrame:
    return pd.read_pickle('pickle/' + file_name)

#key = '65265d19337c32168628d36054955392'
#address = '서울특별시 종로구 관훈동 196-10'
def map_axes(key, address):
    """
    DESCRIPTION 1 : Collecting 'x_좌표' and 'y_좌표' using map address(지번)
    DESCRIPTION 2 : Please note that the address is using '지번'.
    REFERENCE : https://blog.daum.net/geoscience/1436
    """
    url = 'https://dapi.kakao.com/v2/local/search/address.json?&query={}'.format(address)
    api_key = 'KakaoAK ' + key
    headers = {"Authorization": api_key}
    try:
        api_test = requests.get(url, headers=headers)
        url_text = json.loads(api_test.text)
        if url_text['documents'][0]['road_address'] is None:
            output_address = url_text['documents'][0]['address']['address_name']
            output_x = url_text['documents'][0]['address']['x']
            output_y = url_text['documents'][0]['address']['y']
        else:
            output_address = url_text['documents'][0]['road_address']['address_name']
            output_x = url_text['documents'][0]['road_address']['x']
            output_y = url_text['documents'][0]['road_address']['y']
    except:
        output_address = np.nan
        output_x = np.nan
        output_y = np.nan

    return output_address, output_x, output_y

def map_address(key, x_axis, y_axis):
    """
    DESCRIPTION 1 : Search map address using 'x_좌표' and 'y_좌표'.
    DESCRIPTION 2 : Please note that it is not latitude and longitude. (wgs84)
    REFERENCE : https://mentha2.tistory.com/176
    """
    api_key = 'KakaoAK ' + key
    url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={}&y={}'.format(x_axis, y_axis)
    headers = {"Authorization": api_key}
    try:
        api_test = requests.get(url, headers=headers)
        url_text = json.loads(api_test.text)
        output = url_text['documents'][0]['address_name']
    except ValueError as ve:
        print(str(x_axis) + ' and ' + str(y_axis) + ':' + ve)
        output = '좌표 미확인'
    except:
        output = '좌표 미확인'

    return output

def axes_setup():
    """
    DESCRIPTION 1 : Set up function to convert X,Y axes into Latitude, Longitude
    REFERENCE 1 : http://aispiration.com/spatial/geo-spatial-r.html
    REFERENCE 2 : https://pyproj4.github.io/pyproj/stable/gotchas.html#upgrading-to-pyproj-2-from-pyproj-1
    REFERENCE 3 : https://data.seoul.go.kr/dataList/OA-15560/S/1/datasetView.do
    """
    # (X,Y)
    epsg5181 = CRS.from_proj4('+proj=tmerc +lat_0=38 +lon_0=127 +k=1 +x_0=200000 +y_0=500000 +ellps=GRS80 +units=m +no_defs')
    # (Latitude,Longitude)
    wgs84 = CRS.from_proj4("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")
    transformer = Transformer.from_crs(epsg5181, wgs84, always_xy=True)

    return transformer

def run_xy_convert(api_key, data_load, pickle_name):
    """
    DESCRIPTION : Extracting address using wgs84 converter from 'axes_setup'
    """
    # Load pre-processed trade hub data
    if data_load == '아파트':
        data = 아파트_data_load()
    elif data_load == '문화공간':
        data = 문화공간정보_data_load()
    else:
        data = 공영주차장_data_load()

    # Converting X,Y axes into Latitude and Longitude
    df = pd.DataFrame(columns=['x', 'y'])
    transformer = axes_setup()

    # Loop converting X,Y axes columns
    print('카카오 API epsg5181에서 wgs84변환중 : ' + str(datetime.now()))
    for x, y in zip(data['엑스좌표_값'], data['와이좌표_값']):
        # 001 : Transform X,Y into Latitude and Longitude
        x_y_output = transformer.transform(x, y)
        df_output = pd.DataFrame(x_y_output).transpose().rename(columns={0: 'x', 1: 'y'})
        df = df.append(df_output, ignore_index=True)

    # Merge new x,y coordinate
    data = pd.merge(data, df, left_index=True, right_index=True)
    print('카카오 API wgs84 변환완료 : ' + str(datetime.now()))
    # Mapping the address using Latitude and Longitude
    df_address = pd.DataFrame()
    print('카카오 API wgs84에서 주소 추출중 : ' + str(datetime.now()))
    for x, y in zip(data['x'], data['y']):
        df_address = df_address.append([map_address(key=api_key, x_axis=x, y_axis=y)],
                                       ignore_index=True)
    print('카카오 API 주소 완료 : ' + str(datetime.now()))

    # Merge the address field
    df_address = df_address.rename(columns={0: '추출_주소'})
    data = pd.merge(data, df_address, left_index=True, right_index=True)
    data = data.drop(['엑스좌표_값', '와이좌표_값'], axis=1)

    # EXPORT & READ PICKLE ---------------------------------------------------------#
    pickle_replace(name=pickle_name, file=data)
    pickle_output = read_pickle(pickle_name + '.pkl')

    return pickle_output

def run_xy_wo_convert(api_key, data_load, pickle_name):
    """
    DESCRIPTION : Extracting address without converter
    """
    # Load pre-processed trade hub data
    if data_load == '아파트':
        data = 아파트_data_load()
    elif data_load == '문화공간':
        data = 문화공간정보_data_load()
    else:
        data = 공영주차장_data_load()

    # Mapping the address using Latitude and Longitude
    df_address = pd.DataFrame()
    print('카카오 API epsg5181에서 wgs84변환중 : ' + str(datetime.now()))
    for x, y in zip(data['x'], data['y']):
        df_address = df_address.append([map_address(key=api_key, x_axis=x, y_axis=y)],
                                       ignore_index=True)
    print('카카오 API wgs84 변환완료 : ' + str(datetime.now()))

    # Merge the address field
    df_address = df_address.rename(columns={0: '추출_주소'})
    data = pd.merge(data, df_address, left_index=True, right_index=True)

    # EXPORT & READ PICKLE ---------------------------------------------------------#
    pickle_replace(name=pickle_name, file=data)
    pickle_output = read_pickle(pickle_name + '.pkl')

    return pickle_output

#----------------------------- DATA LOAD -----------------------------#
#문화공간 = run_xy_wo_convert(api_key='65265d19337c32168628d36054955392', data_load='문화공간', pickle_name='문화공간')
공연주차장 = read_pickle('공연주차장' + '.pkl')
상권_아파트 = read_pickle('상권_아파트' + '.pkl')

#공연주차장 = 공연주차장.rename(columns={'지번_주소': '추출_주소'})
#pickle_replace(name='공연주차장', file=공연주차장)

