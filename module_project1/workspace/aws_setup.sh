#!/bin/bash

# 리눅스 업데이트
apt-get update;

# 파이썬 패키지 설치 툴 pip 설치
apt install -y python3-pip;

# 파이썬 pip 명령을 실행 하도록 하는 wheel 설치
pip3 install wheel;

# Flask 설치
pip3 install Flask;

# pandas 설치
pip3 install pandas;

# matplotlib 설치
pip3 install matplotlib;

# pyecharts 설치
pip3 install pyecharts;

# waitress 설치
pip3 install waitress;

# root/project1 폴더의 권한을 모든 사용자가 읽고 쓰고 실행 가능하도록 설정
chmod -R 777 /root/project1;

# nginx 설치
apt install -y nginx;

# nginx 설치할 /etc/nginx/sites-available 폴더 생성
mkdir -p  /etc/nginx/sites-available;

# nginx 설정 파일을 /etc/nginx/sites-available/ 폴더에 복사
cp /root/project1.conf /etc/nginx/sites-available;

# AWS 아이피 확인
curl ipecho.net/plain; echo;

# AWS 아이피를 변수 my_ip에 저장
my_ip="$(curl ipecho.net/plain; echo)";

# 변수 my_ip 출력
echo $my_ip;
# sed는 파일에서 특정 문자를 찾아서 바꿔주는 함수 
# localhost를 찾아서 my_ip 값으로 변경

sed 's/localhost/'"$my_ip"'/' -i /etc/nginx/sites-available/project1.conf ;


# nginx 설정이 있는 /etc/nginx/sites-enabled 폴더로이동
cd /etc/nginx/sites-enabled; 
# nginx 기존 설정 삭제
rm default;

# nginx 설정
ln -s /etc/nginx/sites-available/project1.conf;

# nginx 의 권한을 777로 설정
chmod -R 777 /etc/nginx;

# nginx 실행하는 사용자를 기존 www-data 에서 root 로 변경
sed 's/www-data/root/' -i /etc/nginx/nginx.conf;
 


# nginx 재시작
systemctl restart nginx;

# 나눔폰트 설치
apt -qq -y install fonts-nanum;

# 나눔폰트 matplotlib에 복사
cp /usr/share/fonts/truetype/nanum/Nanum* /usr/local/lib/python3.6/dist-packages/matplotlib/mpl-data/fonts/ttf/;