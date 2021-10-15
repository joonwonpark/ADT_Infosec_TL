import pandas as pd
import matplotlib.pyplot as plt
from Contact10 import eda
import warnings
warnings.filterwarnings(action = 'ignore')

region_path = '/home/ubuntu/ai/cloud/workspace/flask_project/hello_flask/data/Region.csv'
high_shcool_path = '/home/ubuntu/ai/cloud/workspace/flask_project/hello_flask/data/전국초중등학교위치표준데이터.csv'
region = pd.read_csv(region_path, encoding = "UTF8")
shcool = pd.read_csv(high_shcool_path, encoding = "cp949")


def academy_region_num(html_name):
    patient_info, patient_route, region = eda()
    # 새로운 데이터표를 만들어 region [지역] 에서 중복제거된 리스트에 [city]와 동일한 행 추가
    region_set = pd.DataFrame(columns=region.columns)
    for i in region["지역"].unique():
      region_set = region_set.append(region[region["city"] == i])

    #지역, 대학수 컬럼 추출
    region_uni_count = region_set[["지역","대학수"]]
    region_uni_count = region_uni_count.drop(243, axis=0) # 쓸데없는 korea행 삭제

    # shcool 데이터 전처리
    shcool_set = shcool[["학교급구분",'시도교육청명', '위도','경도']] # 필요한 컬럼 추출
    shcool_set['지역']=shcool["시도교육청명"].str.replace("교육청",'') # 교육청 단어 공백처리
    shcool_set=shcool_set.drop("시도교육청명", axis=1) # 시도교육청명 행 삭제
    shcool_set=shcool_set[shcool_set["학교급구분"] == "고등학교"] # shcool_set에 저장


    # 대학 데이터와 고등학교 열이름이 달라 맞춰 줌
    shcool_set["지역"] = shcool_set["지역"].str.replace("서울특별시",'Seoul').replace('부산광역시', 'Busan').replace('대구광역시', 'Deagu').replace('광주광역시', 'Gwangju')\
    .replace('인천광역시', 'Incheon').replace('대전광역시', 'Deajeon').replace('울산광역시', 'Ulsan').replace('세종특별자치시', 'Sejong')\
    .replace('경기도', 'Gyeonggi-do').replace('강원도', 'Gangwon-do').replace('충청북도', 'Chungcheongbuk-do').replace('충청남도', 'Chungcheongnam-do')\
    .replace('전라남도', 'Jeollanam-do').replace('경상북도', 'Gyeongsangbuk-do').replace('경상남도', 'Gyeongsangnam-do').replace('제주도', 'Jeju-do')


    # 필요한 컬럼 추출
    shcool_set = shcool_set[["지역","학교급구분"]]

    # 고딩학교 수 파악
    shcool_count =  pd.DataFrame(shcool_set.groupby(["지역"])["학교급구분"].count())
    shcool_count = shcool_count.rename(columns={'학교급구분':'고등학교수'}).reset_index()

    # 데이터 병합
    academy = pd.merge(
        shcool_count.sort_values("고등학교수", ascending=False),
        region_uni_count.sort_values("대학수", ascending=False),
        on = ['지역']
    )

    # 새로운 데이터 프레임에 지역을 기준으로 index
    df = pd.DataFrame(academy)
    df.set_index("지역", inplace=True)

    # 가로 막대 그래프 출력
    plt.figure(figsize=(10, 10))
    df.plot(kind="barh", title="지역별 학교수")
    plt.legend(bbox_to_anchor=(1.04, 0.5), borderaxespad=1) # 범례 위치조정, borderaxespad : 세세 조정
    plt.savefig(f"/home/ubuntu/ai/cloud/workspace/flask_project/hello_flask/static/image/{html_name}.png",bbox_inches = "tight")


