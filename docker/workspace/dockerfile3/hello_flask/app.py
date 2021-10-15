from flask import Flask

from waitress import serve
from flask import render_template
#그래프의 전체적인 설정을 하는 객체
import matplotlib as mpl
#그래프를 그리는 객체
import matplotlib.pyplot as plt
plt.style.use("seaborn")
#폰트 이름 설정 
plt.rc('font', family='NanumGothic')

import pandas as pd

from pyecharts.charts import Bar
from pyecharts import options as opts

app = Flask(__name__)

@app.route("/")
def hello():
 #return "Hello World!"
 return render_template('form.html')

@app.route("/view_image")
def view_image():
 return render_template('image.html',title="안녕 플라스크", image_name="flask.png")

@app.route("/view_weather1")
def view_weather1():
 df = pd.read_csv("weather.csv", index_col="point")
 city_df = df.loc[["서울", "인천", "대전", "대구", "광주", "부산", "울산"]]
 ax = city_df.plot(kind="bar", title="날씨", figsize=(12, 4), legend=True, fontsize=12)
 ax.set_xlabel("도시", fontsize=20)
 ax.set_ylabel("기온/습도", fontsize=30)
 ax.legend(["기온", "습도"], fontsize=20)
 plt.savefig("/home/ubuntu/ai/cloud/workspace/flask_project/hello_flask/static/weather1.png")
 return render_template('weather1.html', image_name="weather1.png", title="광역시 날씨 시각화")

@app.route("/view_weather2")
def view_weather2():
 df = pd.read_csv("weather.csv", index_col="point")
 city_df = df.loc[["서울", "인천", "대전", "대구", "광주", "부산", "울산"]]

 bar = Bar()
 bar.add_xaxis(["서울", "인천", "대전", "대구", "광주", "부산", "울산"])
 bar.add_yaxis("온도", city_df["temperature"].tolist())
 bar.add_yaxis("습도", city_df["humidity"].tolist())
 bar.set_global_opts(title_opts=opts.TitleOpts(title="광역시 온도 습도"))
 bar.render("/home/ubuntu/ai/cloud/workspace/flask_project/hello_flask/static/bar1.html")
 return render_template('weather2.html', graph_file_name="bar1.html", title="광역시 날씨 시각화")



serve(app, host='0.0.0.0', port=8080)
