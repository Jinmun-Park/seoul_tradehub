#------------------------------- LIBRARY -------------------------------#
import pandas as pd
import requests
import json
# Converting X,Y axes into Latitude, Longitude
from pyproj import Transformer, CRS
# Tradehub data load and setup
from src.setup.setup import select_columns, setup_tradehub

#------------------------------- SET UP -------------------------------#
def tradehub_data_load():
    """
    DESCRIPTION 1 : Load trade hub data and filtering the fields before modelling

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

def conversion_axes(transformer, data):
    """
    DESCRIPTION :

    """

    # Load pre-processed trade hub data
    상권_아파트 = tradehub_data_load()

    # Converting X,Y axes into Latitude and Longitude
    df = pd.DataFrame(columns=['x', 'y'])
    transformer = axes_setup()

    # Loop converting X,Y axes columns
    for x, y in zip(상권_아파트['엑스좌표_값'], 상권_아파트['와이좌표_값']):
        # 001 : Transform X,Y into Latitude and Longitude
        x_y_output = transformer.transform(x, y)
        df_output = pd.DataFrame(x_y_output).transpose().rename(columns={0: 'x', 1: 'y'})
        df = df.append(df_output, ignore_index=True)

    # Data merge
    상권_아파트 = pd.merge(상권_아파트, df, left_index=True, right_index=True)

    # Mapping the address using Latitude and Longitude
    df_address = pd.DataFrame()
    for x, y in zip(상권_아파트['x'], 상권_아파트['y']):
        df_address = df_address.append([map_address(key='65265d19337c32168628d36054955392', x_axis=x, y_axis=y)], ignore_index=True)
    print('End')

    df_address = df_address.rename(columns={0: '도로명_주소'})

    return df_address

#----------------------------- DATA LOAD -----------------------------#

'''
map_address(key='65265d19337c32168628d36054955392', x_axis='127.1086228', y_axis='37.4012191')

a = [map_address(key='65265d19337c32168628d36054955392', x_axis=상권_아파트['x'][500], y_axis=상권_아파트['y'][500])]
a = [map_address(key='65265d19337c32168628d36054955392', x_axis='127.04318987696023', y_axis='37.58011691623963')]
df_address = df_address.append(a, ignore_index=True)
df_address = df_address.rename(columns={0: '도로명_주소'})
'''