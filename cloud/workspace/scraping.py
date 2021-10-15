# 필요한 라이브러리를 불러옵니다.

import pandas as pd
import numpy as np
import requests

# 서울시 코로나 데이터의 1페이지의 100개의 데이터를 수집하는 url을 변수에 저장
url = f"https://news.seoul.go.kr/api/27/getCorona19Status/get_status_ajax.php?draw=1&start=0&length=100"
print("url = ", url )
# requests.get(url) : url에 접속해서 서울시 코로나 데이터 1페이지의 데이터를 수집하고 성공 실패 여부를 리턴
# response : 수집의 성공여부가 저장 성공했으면 200이 저장되 있음
response = requests.get(url)
print("response = ", response)

# response.json() : 수집된 데이터를 JSON (Dictionary) 형태로 리턴
# data_json : 수집된 정보를 저장한 변수
data_json = response.json()
# 수집된 데이터를 출력
print("data_json = ", data_json)

# data_json 에 저장된 수집정보는 다음과 같다
# data_json =  {'draw': 1, 'recordsTotal': 14071, 'recordsFiltered': 14071 ...}
# data_json 의 타입은 dictionary 로 전체 데이터의 개수는 record_Total 키에 저장되 있음
# 전체 데이터수를 조회해서 변수 records_total에 대입
records_total = data_json['recordsTotal']
print("records_total=",records_total)

# 코로나 확진자 정보는 1페이지당 100명씩 저장되 있음
# 코로나 확진자 정보의 마지막 페이지를 계산해서 end_page 에 대입

# (records_total % 100) == 0 : 전체 데이터수 (전체 확진자수) 를 100 으로 나눈 나머지가 0 일때 (
#                               전체 확진자 수가 100 의 배수
if (records_total % 100) == 0:
    # (records_total // 100) : record_total (전체 확진자수) 를 100 으로 나눈 몫 이 페이지 수
    # 예를 들어서 record_total 이 100의 배수인 1400 이라고 하면 1400 을 100으로 나눈 몫 14가 페이지 수
    end_page = (records_total // 100)
else:
    # record_total (전체 확진자 수) 가 100 의 배수가 아닐때
    # 예를 들어서 record_total이 100 의 배수가 아닌 1401 이라고 하면 1401 을 100으로 나눈 몫 14 에 1을 더한 15가 페이지수
    end_page = (records_total // 100) + 1

print("end_page = ", end_page)


# 수집된 데이터가 저장된 변수 data_json 에서 키값 data에 코로나 환자 정보가 저장되 있음
# 코로나 환자 정보를 변수 data에 대입
data = data_json["data"]
print("data = ",data)


""" 전체 데이터 수집 함수"""

def get_seoul_covid19(page_no):
    """
    page_no : 입력값으로 페이지 번호를 입력하면 해당 번호의 데이터를 가져옴
    start_no : 입력받은 page_no로 시작 번호를 의미
    """
    # 1페이지 -> 시작 번호 0
    # 2페이지 -> 시작 번호 100
    # 3 페이지 -> 시작번호 200
    # 시작 번호 -> (페이지-1)*100
    start_no = (page_no - 1) * 100
    # f" ...  draw={page_no}&start={start_no}&length=100" : {page_no}에 변수 page_no 의 값 대입
    #                                                     : {start_no} 에 변수 start_no의 값 대입
    # 문자열 앞의 f 는 {변수명} 에 변수값을 대입하는 명령
    # page_no 페이지에 접속해서 start_no 번째 확진자 정보 부터 100명의 코로나 확진자 정보를 수집할 url
    url = f"https://news.seoul.go.kr/api/27/getCorona19Status/get_status_ajax.php?\
            draw={page_no}&start={start_no}&length=100"
    # url 에 접속해서 성공여부를 response에 대입 성공시 response에 200이 저장
    response = requests.get(url)
    #print("page_no = ",page_no , "response = ", response)
    # response.json() : 수집한 코로나 확진자 정보를 JSON 으로 변환해서 리턴
    data_json = response.json()
    #print("data_json = ", data_json)
    return data_json

# 2페이지의 코로나 확진자 정보를 수집
get_seoul_covid19(2)

""" ## 전체 데이터 가져오기 """

import time
from tqdm import trange
# 1 페이지 부터 마지막페이지 (마지막 페이지는 변수 end_page 에 저장되 있음)
# 까지 수집한 코로나 확진자 정보를 저장할 리스트
patient_list = []
# trange(1, end_page + 1) : 1부터 end_page+1 미만까지 반복문을 실행
#                          : 반복문의 실행을 progressbar 로 출력
for page_no in trange(1, end_page + 1):
    # get_seoul_covid19(page_no) : page_no 페이지의 전체 확진자 수, 확진자 정보를 수집해서 리턴
    one_page = get_seoul_covid19(page_no)
    print("one_page = ", one_page)
    # one_page["data"] : 확진자 정보가 저장된 one_page에서 key 가 data 인 확진자 정보만 리턴
    patient = pd.DataFrame(one_page["data"])
    print("patient = ", patient)
    print("=" *100)
    # 확진자 정보 patient 를 patient_list에 추가
    patient_list.append(patient)
    # 서버에 한번에 너무 많은요청을 보내면 서버에 부담이 됩니다.
    # 서버에 부담을 주지 않기 위애 0.5초씩 쉬었다 가져옵니다.
    time.sleep(0.5)



# concat을 통해 patient_list 를 하나의 데이터프레임으로 합쳐줍니다.
df_all = pd.concat(patient_list)
print("df_all =", df_all)

# df_all 의 컬럼명을 설정
df_all.columns = ["발생번호","환자번호","확진일","거주지","여행력","접촉력","퇴원현황" ]
print("df_all = ",df_all)



import re
# 발생 번호 컬럼의 데이터를 조회하면 <p class="corona19">3191</p> 으로 태그와 발생번호 3191 이 섞여 있음
# 발생번호 숫자 3191 만 추출하는 함수
# 매개변수 num_string : 수집한 발생번호가 저장
def extract_number(num_string):
    # num_string 의 타입이 문자(str) 이라면
    if type(num_string) == str:
        # num_string.replace("corona19", "") : num_string 에서 corona19 를 "" 로 수정(삭제)
        num_string = num_string.replace("corona19", "")
        # re.sub("[^0-9]", "", num_string) :  num_string 에서 [^0-9] (숫자가 아닌데이터) 를 검색해서 "" 로 수정 (삭제) 해서 리턴
        num = re.sub("[^0-9]", "", num_string)
        # int(num) : num을 정수로 변환
        num = int(num)
        # num 리턴
        return num
    else: # num_string 이 문자(str) 이 아니라면
        return num_string # 문자 리턴
# df_all["발생번호"].map(extract_number) : df_all의 발생번호 컬럼에서 데이터를 1줄씩 추출해서 extract_number 함수를 실행하고
# 함수 실행한 결과 ( conrona19 문자열 삭제, 숫자가 아닌 문자열 삭제) 를 리턴해서
#  df_all["발생번호"] (df_all의 발생번호 컬럼) 에 덮어 쓰기
df_all["발생번호"] = df_all["발생번호"].map(extract_number)

print('df_all["발생번호"] = ' , df_all["발생번호"])

# 퇴원 현황 <b class='status1'>퇴원</b> <b class='status1'>사망</b> 으로 저장되 있음
# 퇴원 현황에서 한글이 아닌 데이터 삭제
# origin_text : 퇴원 현황이 저장된 변수
def extract_hangeul(origin_text):
    # re.sub("[^가-힣]", "", origin_text) : orgin_text 에서 한글이 아닌 데이터 [^가-힣] 을 "" 로 수정(삭제) 해서 리턴
    subtract_text = re.sub("[^가-힣]", "", origin_text)
    return subtract_text

# df_all["퇴원현황"].map(extract_hangeul) : df_all의 퇴원현황 컬럼 (df_all["퇴원현황"]) 의 각줄을 extract_hangul 함수를 실행
#                                        : 해서 한글이 아닌 데이터를 삭제하고 결과를 df_all["퇴원현황"]에 대입
df_all["퇴원현황"] = df_all["퇴원현황"].map(extract_hangeul)

print("df_all['퇴원현황'] =",df_all ['퇴원현황'])



print("df_all = ", df_all)


# df_all 에 저장된 코로나 확진자 정보를 seoul_covid19.csv 로 저장
# index=False : index (줄이름) 은 저장하지 않음
df_all.to_csv("seoul_covid19.csv", index=False)
