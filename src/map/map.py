#------------------------------- LIBRARY -------------------------------#
import pandas as pd
import requests
import json
# Converting X,Y axes into Latitude, Longitude
from pyproj import Transformer, CRS
# Trade hub data load and setup
from src.setup.setup import select_columns, setup_tradehub
# Directory path and pickle setup
import os
from datetime import datetime
import pickle

# Load cleaned data
from src.rpt.carpark import carpark_data_load

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

def data_load(data_name):
    """
    DESCRIPTION 1 : Load cleaned data for mapping
    AVAILABILITY : '공연주차장', '상권_아파트'
    """
    상권_아파트 = setup_tradehub('상권_아파트.csv')
    상권_아파트 = select_columns(data=상권_아파트, names=['기준_년_코드', '기준_분기_코드', '분기_코드', '상권_구분_코드_명', '상권_코드_명',
                                                '아파트_평균_면적', '아파트_평균_시가', '시도', '시군구', '법정동', '엑스좌표_값', '와이좌표_값'])

    return 상권_아파트

#key = '65265d19337c32168628d36054955392'
def map_address(key, x_axis, y_axis):
    """
    DESCRIPTION 1 : Search map address using 'x_좌표' and 'y_좌표'.
    DESCRIPTION 2 : Please note that it is not latitude and longitude
    REFERENCE : https://mentha2.tistory.com/176
    """
    key = 'KakaoAK ' + key
    url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={}&y={}'.format(x_axis, y_axis)
    headers = {"Authorization": key}
    api_test = requests.get(url, headers=headers)
    url_text = json.loads(api_test.text)
    output = url_text['documents'][0]['address_name']

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

def run_xy_convert(api, transformer, data):
    """
    DESCRIPTION : Running

    """
    # Load pre-processed trade hub data
    상권_아파트 = data_load()

    # Converting X,Y axes into Latitude and Longitude
    df = pd.DataFrame(columns=['x', 'y'])
    transformer = axes_setup()

    # Loop converting X,Y axes columns
    for x, y in zip(상권_아파트['엑스좌표_값'], 상권_아파트['와이좌표_값']):
        # 001 : Transform X,Y into Latitude and Longitude
        x_y_output = transformer.transform(x, y)
        df_output = pd.DataFrame(x_y_output).transpose().rename(columns={0: 'x', 1: 'y'})
        df = df.append(df_output, ignore_index=True)

    # Merge new x,y coordinate
    상권_아파트 = pd.merge(상권_아파트, df, left_index=True, right_index=True)

    # Mapping the address using Latitude and Longitude
    df_address = pd.DataFrame()
    print('카카오 API epsg5181에서 wgs84변환중 : ' + str(datetime.now()))
    for x, y in zip(상권_아파트['x'], 상권_아파트['y']):
        df_address = df_address.append([map_address(key=api, x_axis=x, y_axis=y)],
                                       ignore_index=True)
    print('카카오 API wgs84 변환완료 : ' + str(datetime.now()))

    # Merge the address field
    df_address = df_address.rename(columns={0: '도로명_주소'})
    상권_아파트 = pd.merge(상권_아파트, df_address, left_index=True, right_index=True)
    상권_아파트 = 상권_아파트.drop(['엑스좌표_값', '와이좌표_값'], axis=1)

    # EXPORT & READ PICKLE ---------------------------------------------------------#
    pickle_replace(name='상권_아파트', file=df_address)
    pickle_output = read_pickle('youtube_popular.pkl')

    return pickle_output



#----------------------------- DATA LOAD -----------------------------#

