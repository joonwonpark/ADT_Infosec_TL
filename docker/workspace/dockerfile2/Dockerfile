# nginx 를 기본 이미지로 함
FROM nginx
# 작성자 정보
LABEL maintainer="cloud.ai.education@gmail.com"

# 리눅스 업데이트
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

#개발과 관련한 프로그램 (파이썬등) 업데이트 -y는 설치할때 y를 자동 입력
#파이썬 3.7.3 버젼이 설치됨
RUN apt install -y software-properties-common

#파이썬 개발 관련 패키지 설치
RUN apt-get install -y python3-dev

# 폴더 생성
# docker는 기본 이미지에 bash 대신에 sh 가 설치되 있음
# flask 프로그램을 설치할 폴더 /home/ubuntu/ai/cloud/workspace/flask_project 생성
RUN ["/bin/sh", "-c", "mkdir -p /home/ubuntu/ai/cloud/workspace/flask_project/hello_flask"]

# 파일 생성
# 현재 폴더의(./) hello_flask 폴더를 Docker container의 /home/ubuntu/ai/cloud/workspace/flask_project/hello_flask 복사
COPY ./hello_flask  /home/ubuntu/ai/cloud/workspace/flask_project/hello_flask

# 파이썬 라이브러리를 설치할 pip3 설치
RUN apt-get install -y python3-pip

# wheel pandas Flask matplotlib  pyecharts  waitress 라이브러리 설치
RUN pip3 install wheel pandas Flask matplotlib  pyecharts  waitress

# nginx 설정파일 hello_flask.conf 를 /etc/nginx/conf.d 폴더로 복사
COPY ./hello_flask.conf  /etc/nginx/conf.d/

# 기존 nginx 설정 파일 /etc/nginx/conf.d/default.conf 삭제
RUN ["/bin/sh", "-c", "rm  /etc/nginx/conf.d/default.conf"]

# 한글 폰트 설치
RUN apt -qq -y install fonts-nanum

# 한글폰트를 matplotlib로 복사
RUN cp /usr/share/fonts/truetype/nanum/Nanum* /usr/local/lib/python3.7/dist-packages/matplotlib/mpl-data/fonts/ttf/
