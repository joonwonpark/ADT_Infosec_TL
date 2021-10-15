# nginx 를 기본 이미지로 함
FROM nginx
# 작성자 정보
LABEL maintainer="cloud.ai.education@gmail.com"

# GUI 화면이 없어서 pandas 설치시 경고창이출력됨
# GIU 화면이 없는것을 다른 프로그램에 알려주는 설정
ENV DEBIAN_FRONTEND noninteractive

# 리눅스 업데이트
RUN apt-get update

#개발과 관련한 프로그램 (파이썬등) 업데이트 -y는 설치할때 y를 자동 입력
#파이썬 3.7.3 버젼이 설치됨
RUN apt install -y software-properties-common

#파이썬 개발 관련 패키지 설치
RUN apt-get install -y python3-dev

# 파이썬 라이브러리를 설치할 pip3 설치
RUN apt-get install -y python3-pip

# wheel pandas Flask matplotlib  pyecharts  waitress 라이브러리 설치
RUN pip3 install wheel 
RUN pip3 install pandas
RUN pip3 install Flask
RUN pip3 install matplotlib
RUN pip3 install pyecharts
RUN pip3 install waitress

# 한글 폰트 설치
RUN apt -qq -y install fonts-nanum

# 한글폰트를 matplotlib로 복사
RUN cp /usr/share/fonts/truetype/nanum/Nanum* /usr/local/lib/python3.7/dist-packages/matplotlib/mpl-data/fonts/ttf/

# 파이참과 파일을 주고 받을 ssh 설치 (-y 옵션은 프롬프트에 자동으로 yes라고 응답해줌)
RUN apt-get install -y openssh-server 

# /var/run/sshd 디렉토리 생성
RUN mkdir /var/run/sshd 

# 파이프라인(|) 왼쪽의 표준 출력이 오른쪽의 표준 입력으로 처리됨 
# root의 password를 password1234로 변경
RUN echo 'root:password1234' | chpasswd 

# 설정파일의 편집을위해 nano에디터 설치
RUN apt-get install nano

# openssh 7.0버전 부터 PermitRootLogin 옵션이 'prohibit-password'를 인자로 받아들인다. (without-password 와 살짝 비슷) 
#  PermitRootLogin yes 추가 
# pw 없이 접속 가능하던 것을 root 계정으로 로그인 하도록 변경 
# https://www.openssh.com/txt/release-7.0 
# permitrootlogin : http://manpages.ubuntu.com/manpages/trusty/en/man5/sshd_config.5.html
# ssh에 비밀 번호로 로그인 가능하도록 설정
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

# sed -i 옵션은 타겟 파일에서 문자열을 검색한 후 변경한다. 
# s/대신 s@로 표현되었다(s 는 substitue를 뜻함) 
# / 대신 백슬래쉬와 개행문자를 제외한 어느 것도 delimiter로 사용가능하다.
# 문자 같은 경우는 백슬래쉬 앞에 함게 써야 함 # delimiter 안쪽의 문자열들은 Regex 표현식이 사용됨 
# http://pubs.opengroup.org/onlinepubs/9699919799/utilities/sed.html 
# 'session required pam_loginuid.so' 문자열을 
# 'session optional pam_loginuid.so' 문자열로 교체 
# 표현식 내부의 \s는 공백을 의미 # *는 반복을 의미, \s*는 공백이 0번이상 반복 
# https://www.linux.co.kr/home2/board/subbs/board.php?bo_table=lecture&wr_id=1808

RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
# /etc/profile 파일은 user shell에 시스템 전역 환경변수를 설정하는데 사용된다. # >>, 파일 뒷부분에 내용 추가
RUN echo "export VISIBLE=now" >> /etc/profile

# 호스트와 연결할 포트번호
EXPOSE 22

# 폴더 생성
# docker는 기본 이미지에 bash 대신에 sh 가 설치되 있음
# flask 프로그램을 설치할 폴더 /root/project1 생성
RUN ["/bin/sh", "-c", "mkdir -p /root/project1"]


# 파일 생성
# 현재 폴더의(./) hello_flask 폴더를 Docker container의 /root/project1 폴더로 복사
COPY ./project1  /root/project1

# 폴더 생성
# docker는 기본 이미지에 bash 대신에 sh 가 설치되 있음
# flask 프로그램을 설치할 폴더 /root 의 권한을 모든 사용자에게 부여
RUN ["/bin/sh", "-c", "chmod 777 -R /root"]


# nginx 설정파일 project1.conf 를 /etc/nginx/conf.d 폴더로 복사
COPY ./project1.conf  /etc/nginx/conf.d/

# 기존 nginx 설정 파일 /etc/nginx/conf.d/default.conf 삭제
RUN ["/bin/sh", "-c", "rm  /etc/nginx/conf.d/default.conf"]

# nginx 실행 시 사용자를 root로 설정
RUN sed 's/user  nginx/user root/' -i /etc/nginx/nginx.conf;

# 해당 docker에서는 nginx 와 sshd 를 시작 프로그램에 등록 할 것임 (원래 1개만 등록하도록 되있음)
# Dockerfile 에서 2개 이상의 프로그램을 시작 명령에 등록 시킬 수 있는 supervisor 설치
RUN apt-get -y install supervisor

# 시작 프로그램이 설정된 supervisord.conf 을   /etc/supervisor/supervisord.conf 로 복사
ADD ./supervisord.conf /etc/supervisor/supervisord.conf

# supervisord에 등록된 시작 프로그램 nginx, sshd 실행
CMD ["/usr/bin/supervisord"]