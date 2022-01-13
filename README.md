# 서울시 상권별 매출 분석 및 예측, 어플리케이션 프로젝트

### [프로젝트 기획]
'서울 열린데이터 광장' 에서 추출한 상권 데이터와 주변 지역 시설 데이터를 활용하여, 
매출 분석 리포트를 작성하고 이에 기반하여 창업 매출 예상 어플리케이션을 제작할 예정입니다.

### [프로젝트 리포트]
모든 상권 데이터에 대한 데이터 분석 리포트는 [VELOG]에 작성하였습니다.

### [프로젝트 참여원]
- 박진문 : pjm9827@gmail.com
- 박은정 : pej111797@gmail.com
- 전민수 : mschun0621@gmail.com 

### [프로젝트 진행 계획]
#### 1. 분석 리포트 작성 
| PLAN &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| DATE &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| STATUS &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;|
| --- | --- | --- |
| 데이터 맵핑 | 31'DEC'2021 | COMPLETED |
| EDA 리포트 | 15'JAN'2022 | IN PROGRESS |
| 모델링 | 21'JAN'2022 | IN PROGRESS |
| 최종 리포트 | 31'JAN'2022 | IN PROGRESS |

#### 2. 모바일 어플리케이션
| PLAN &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| DATE &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| STATUS &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;|
| --- | --- | --- |
| FLASK 앱 | 15'FEB'2021 | IN PROGRESS |
| AWS | 25'FEB'2022 | IN PROGRESS |

### [프로젝트 데이터] 
#### 1. 데이터 출처
| 이름 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| 출처 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| 파일이름 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;|
| --- | --- | --- |
| 상권데이터 | [서울 열린데이터] | 상권_데이터이름 |
| 공영주차장 | [서울 열린데이터] | 도로명별_공영주차장 |
| 문화공간정보 | [서울 열린데이터] | 도로명별_문화공간정보 |
| 병원인허가 | [서울 열린데이터] | 도로명별_병원인허가 |
| 어린이보호구역 | [서울 열린데이터] | 도로명별_어린이보호구역 |
| 전월세가 | [서울 열린데이터] | 도로명별_전월세가 
| 등록외국인구별현황 | [서울 열린데이터] | 서울시 등록외국인 구별 현황 |
| 의료관광허가의료기관정보 | [서울 열린데이터] | 서울시 의료관광허가 의료기관 정보 |
| 행정동코드 | [한국빅데이터] | 행정동코드 |

[서울 열린데이터]:http://data.seoul.go.kr/dataList/datasetList.do
[한국빅데이터]:https://www.bigdata-environment.kr/
[공공데이터포탈]:https://www.data.go.kr/data/15049340/fileData.do
[VELOG]:https://velog.io/@data_park

#### 2. 데이터 정의 
- 상주인구 : "서울시 주민등록주소 기반으로 작성한 인구 수" 
- 생활인구 : "서울시와 KT가 공공빅데이터와 통신데이터 이용하여 작성한 서울의 특정지역, 특정시점에 존재하는 인구 수" 
- 직장인구 : "국민건강보험공단 직장건강보험 가입자의 직장주소 기반으로 작성한 인구 수"



