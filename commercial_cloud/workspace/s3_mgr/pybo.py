import urllib.parse

from flask import Flask
from flask import render_template
from flask import request
from flask import Response

import boto3

from waitress import serve
from os import path


app = Flask(__name__)

@app.route('/')
def hello_pybo():
    return "Hello S3"

@app.route("/SelectFile")
def select_file():
    return render_template('SelectFile.html')

@app.route('/UploadFile',methods=['POST'])
def upload_file():
    if request.method == "POST":
        file = request.files['select']
        print('선택한 파일 이름 =', file.filename)

        if file.filename != '':
            save_file_name = file.filename

            if len(path.splitext(save_file_name)) == 2:
                file_name, ext = path.splitext(save_file_name)
            else:
                file_name = save_file_name
                ext = ""

            count = 1
            # path.exits("./temporary/" + save_file_name) : temporary 폴더에 save_file_name과 같은 이름의
            # 파일이 이미 존재 한다면 True while 문 실행
            # 같은 이름의 파일이 존재 하지 않는 다면 False while 문 실행 안됨

            while path.exists("./temporary/" + save_file_name):
                # 이미 존재 하는 파일
                print(save_file_name + "은 이미 존재하는 파일")
                # path.splitext(save_file_name) : 파일 이름을 파일명과 확장자명으로 분리한 후 리스트에 담아서 리턴


                # 같은 이름의 파일이 존재하기 때문에
                # file_name + str(count) + ext를 save_file_name에 대입
                save_file_name = file_name + str(count) + ext
                print("save_file_name", save_file_name)
                count += 1

            # file (SelectFile.html 에서 선택한 파일) 을 temporary 폴더에 save_file_name 파일명으로 임시 저장
            file.save("./temporary/" + save_file_name)
            # AWS의 S3에 접속
            s3 = boto3.client('s3')
            s3.upload_file("./temporary/" + save_file_name, "pjwawsbucket", save_file_name)
            return save_file_name

    return "S3에 파일 업로드 실패!!"

@app.route('/ViewFileList')
def view_file_list():
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')

    response_iterator = paginator.paginate(
                            Bucket = 'pjwawsbucket'
                            )
    file_list = list(response_iterator)
    print("=" * 100)
    print('file_list =', file_list)
    print("=" * 100)

    print('file_list[0] =', file_list[0])
    print("=" * 100)
    print("file_list[0][Contents][0] =", file_list[0]["Contents"])
    print("=" * 100)

    return render_template('ViewFileList.html', file_list = file_list[0]["Contents"])

@app.route('/DownLoadFile', methods=['POST'])
def download_file():
    # request.form['file_name'] : input name = 'file_name' 의 value 속성의 값을 리턴
    file_name = request.form['file_name']
    print('file_name =', file_name)
    print("=" * 100)

    # boto3.client('s3') : AWS s3에 접속 하는 객체를 생성해서 리턴
    s3 = boto3.client('s3')

    file = s3.get_object(Bucket = 'pjwawsbucket', Key=file_name)
    print("file =", file)
    print("=" * 100)
    # urlib.parse.quote(file_name.encode('utf-8') : file_name (전송할 파일의 파일명) 을 UTF-8 로 변환
    filename_header = 'filename*=UTF-8\'\'%s' % urllib.parse.quote(file_name.encode('utf-8'))
    print("filename_header = ", filename_header)

    # file : AWS s3 버켓에서 파일명이 file_name 인 파일의 내용을 가져올 객첵
    # file['Body'].read() : AWS s3 버켓에서 파일명이 file_name 인 파일의 내용을 가져옴
    # headers = {"Contents-Disposition" : "attachment;filename=+file_name} : 다운로드할 파일의 이름
    # Response(웹브라우저로 전송할 내용) : 웹브라우저로 AWS s3 버켓에서 파일명이 file_name 인 파일의 내용을 전송 (파일 내용 다운로드 시작)
    return Response(
        file['Body'].read(),
        headers={"Content-Disposition": 'attachment;'+filename_header}
    )


serve(app, host='0.0.0.0', port=8081)