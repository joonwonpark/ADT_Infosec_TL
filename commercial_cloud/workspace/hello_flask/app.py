from flask import Flask
from waitress import serve
from flask import render_template

#그래프의 전체적인 설정을 하는 객체
import matplotlib as mpl
#그래프를 그리는 객체
import matplotlib.pyplot as plt
plt.style.use("seaborn")
#폰트 이름 설정
plt.rc('font', family='Malgun Gothic')

import pandas as pd

from pyecharts.charts import Bar
from pyecharts import options as opts


# Flask(__name__) : 플라스크 프로그램을 실행하는 Flask 객체 생성
# __name__ : 실행중인 파일명 app.py 에서 확장자 py를 제외한 app이 저장
app = Flask(__name__)

# 웹브라우저에서 http://localhost 입력했을때 실행
@app.route("/")
def hello():
 #return "Hello World!"

 #form1.html페이지를 실행 시킴
 return render_template('form.html')

# 주소표시줄에 http://localhost/view_image 입력시 실행할 함수
@app.route("/view_image")
def view_image():
 # image.html 을 실행시킴
 # title="안녕 플라스크" : title 변수에 안녕 플라스크 대입
 # image_name 변수에 flask.png 대입
 return render_template('image.html',title="안녕 플라스크", image_name="flask.png")

# 웹브라우저 주소 표시줄에 http://localhost/view_weather1 입력시 실행 할 함수
@app.route("/view_weather1")
def view_weather1():
 # weather.csv 를 읽어서 df에 대입, point 컬럼을 인덱스로 설정
 df = pd.read_csv("weather.csv", index_col="point")
 # df에 저장된 데이터 중에서 "서울", "인천", "대전", "대구", "광주", "부산", "울산" 리턴
 city_df = df.loc[["서울", "인천", "대전", "대구", "광주", "부산", "울산"]]
 # kind="bar" : 막대 그래프 생성
 # title="날씨" : 그래프 제목
 # figsize=(12, 4) : 가로 12, 세로 4
 # legend=True : 범례 있음
 # fontsize=12 : 글자 사이즈 12
 ax = city_df.plot(kind="bar", title="날씨", figsize=(12, 4), legend=True, fontsize=12)
 # X좌표 제목
 ax.set_xlabel("도시", fontsize=20)
 # y좌표 제목
 ax.set_ylabel("기온/습도", fontsize=30)
 #범례
 ax.legend(["기온", "습도"], fontsize=20)
 # 그래프를 weather1.png로 저장
 plt.savefig("C:/ai/cloud/workspace/flask_project/hello_flask/static/weather1.png")
 # weather1.html 실행
 return render_template('weather1.html', image_name="weather1.png", title="광역시 날씨 시각화")


@app.route("/view_weather2")
def view_weather2():
 # weather.csv 를 읽어서 df에 대입, point 컬럼을 인덱스로 설정
 df = pd.read_csv("weather.csv", index_col="point")
 # df에 저장된 데이터 중에서 "서울", "인천", "대전", "대구", "광주", "부산", "울산" 리턴
 city_df = df.loc[["서울", "인천", "대전", "대구", "광주", "부산", "울산"]]
 #PyeChart의 막대그래프 객체 생성
 bar = Bar()
 # 막대그래프 X 축 설정
 bar.add_xaxis(["서울", "인천", "대전", "대구", "광주", "부산", "울산"])
 # 막대그래프 범례와 해당 데이터 설정
 # city_df["temperature"] : city_df의 temperature 칸의 데이터
 # city_df["temperature"].tolist() : city_df의 temperature 칸의 데이터를 리스트로 변환
 bar.add_yaxis("온도", city_df["temperature"].tolist())
 # 막대그래프 범례와 해당 데이터 설정
 # city_df["humidity"] : city_df의 humidity 칸의 데이터
 # city_df["humidity"].tolist() : city_df의 humidity 칸의 데이터를 리스트로 변환
 bar.add_yaxis("습도", city_df["humidity"].tolist())
 #그래프 제목
 bar.set_global_opts(title_opts=opts.TitleOpts(title="광역시 온도 습도"))
 # Pyecharts로 만든 그래프를 static 폴더에 bar1.html로저장
 bar.render("C:/ai/cloud/workspace/flask_project/hello_flask/static/bar1.html")
 #weather2.html 실행
 return render_template('weather2.html', graph_file_name="bar1.html", title="광역시 날씨 시각화")


#host='0.0.0.0': 모든 아이피에서
# port=8080 : 8080 포트로 요청이 입력되면
# 함수 hello 실행
serve(app, host='0.0.0.0', port=8080)