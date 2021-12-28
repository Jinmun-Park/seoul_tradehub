# 서울시 상권별 매출분석과 어플리케이션 프로젝트

### [프로젝트 목적]
'서울 열린데이터 광장' 에서 추출한 상권데이터와 주변지역 시설데이터를 활용하여, 
매출분석 리포트를 작성하고 이에 기반하여 창업 매출예상 어플리케이션을 만든다. 

### [프로젝트 참여원]
- 박진문 : pjm9827@gmail.com
- 박은정 : pej111797@gmail.com
- 전민수 : - 

### [계획]
#### 1. 분석 리포트 작성 
| PLAN &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| DATE &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| STATUS &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;|
| --- | --- | --- |
| 데이터 매핑 | 31'DEC'2021 | IN PROGRESS |
| EDA 리포트 | 7'JAN'2022 | IN PROGRESS |
| 모델링 | 14'JAN'2022 | IN PROGRESS |
| 최종리포트 | 18'JAN'2022 | IN PROGRESS |

#### 2. 모바일 어플리케이션
| PLAN &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| DATE &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| STATUS &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;|
| --- | --- | --- |
| FLASK 앱 | 31'JAN'2021 | IN PROGRESS |
| AWS | 10'FEB'2022 | IN PROGRESS |

### [출저]
#### 1. API
| 주소 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| 설명 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;|
| --- | --- |
| 서울특별시 빅데이터 플랫폼 | [서울 열린데이터] |
| 한국행정구역코드 | [한국빅데이터] |

#### 2. 데이터
| 이름 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| 출저 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| 파일이름 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;|
| --- | --- | --- |
| 상권데이터 | [서울 열린데이터] | 상권_데이터이름 |
| 공연주차장 | [서울 열린데이터] | 상권_데이터이름 |
| 병원인허가 | [서울 열린데이터] | 상권_데이터이름 |
| 어린이보호구역 | [서울 열린데이터] | 상권_데이터이름 |
| 건축물대장 법정동 코드정보 | [공공데이터포탈] | 병합<행정구역_종합코드> |
| 상권분석서비스(상권영역) | [서울 열린데이터] | 병합<행정구역_종합코드> |
| 한국행정구역코드 | [한국빅데이터] | 병합<행정구역_종합코드> |

#### 데이터 정의 
- 상주인구 : "서울시 주민등록주소 기반으로 작성한 인구수" 
- 생활인구 : "서울시와 KT가 공공빅데이터와 통신데이터를 이용하여 작성한 서울의 특정지역, 특정시점에 존재하는 인구수" 
- 직장인구 : "국민건강보험공단 직장건강보험 가입자의 직장주소 기반으로 작성한 인구수"

[서울 열린데이터]:http://data.seoul.go.kr/dataList/datasetList.do
[한국빅데이터]:https://www.bigdata-environment.kr/
[공공데이터포탈]:https://www.data.go.kr/data/15049340/fileData.do
