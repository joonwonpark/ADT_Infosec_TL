from flask import Flask
from waitress import serve
import boto3
from flask import render_template
from flask import redirect, url_for
from flask import request
from decimal import Decimal
app = Flask(__name__)

@app.route('/')
def hello_student_manager():
    # boto3.resource('dynamodb') : dynamodb에 접속해서 데이터를 추가,수정,삭제, 조회를 수행할 객체를 생성
    dynamodb = boto3.resource('dynamodb')
    # table = dynamodb.Table('UnivStudent') UnivStudent 테이블에 데이터를 추가,수정,삭제, 조회를 수행할 객체를 생성
    table = dynamodb.Table('UnivStudent')
    # table.scan() : UnivStudent 테이블의 모든 데이터를 조회해서 리턴
    response = table.scan()
    print("response = ", response)
    # 테이블의 레코드 정보를 출력
    print("response['Items'] = ", response["Items"])

    return render_template("ViewStudentList.html", student_list=response['Items'])

# 학생 추가 화면으로 이동
@app.route('/AddStudentForm')
def add_student_form():
    # 학생 추가 페이지 AddStudentForm.html 으로 페이지 이동
    return render_template('AddStudentForm.html')

# 학생 추가 처리
# url 이 AddStudent 일때 아래의 함수를 실행
@app.route('/AddStudent', methods=['POST'])
def add_student():
    # AddStudentForm.html 에서 name 속성의 값이 univ_id 에 입력값 (학번) 리턴
    univ_id = request.form["univ_id"]
    # AddStudentForm.html 에서 name 속성의 값이 univ_name 에 입력값 (이름) 리턴
    univ_name = request.form["univ_name"]
    # AddStudentForm.html 에서 name 속성의 값이 major 에 입력값 (학과) 리턴
    major = request.form["major"]
    # AddStudentForm.html 에서 name 속성의 값이 avg_credit 에 입력값 (학점) 리턴
    avg_credit = request.form["avg_credit"]
    # AddStudentForm.html 에서 name 속성의 값이 circle 에 입력값 (동아리) 리턴
    circle = request.form["circle"]

    # boto3.resource('dynamodb') : dynamodb에 접속해서 데이터를 추가,수정,삭제 조회를 수행할 객체를 생성
    dynamodb = boto3.resource('dynamodb')
    # dynamodb.Table('UnivStudent') : UnivStudent 테이블에 데이터를 추가,수정,삭제 조회를 수행할 객체를 생성
    table = dynamodb.Table('UnivStudent')
    # 학번이 입력된 univ_id 와 이름이 입력된 univ_name 에 값이 입력 되었을 때
    if univ_id != "" and univ_name != "":
        # dictionary new student 생성
        new_student = {
            'univ_id' : Decimal(univ_id),
            'univ_name' : univ_name
        }
        # major 에 값이 존재하면
        if major != "":
            # new_student 에 major추가
            new_student["major"] = major

        # circle 에 값이 존재하면
        if circle != "":
            # new_student 에 circle 추가
            new_student['circle'] = circle

        # avg_credit 에 값이 존재하면
        if avg_credit != "":
            # new_student 에 avg_credit 추가
            new_student['avg_credit'] = Decimal(avg_credit)

        print("new_student = ", new_student)

        # 테이블 UnivStudent 에 new_student 추가
        table.put_item(Item=new_student)

    # Flask 의 hello_student_manager 함수 호출
    return redirect(url_for('hello_student_manager'))

# url이 RemoveStudent 일때 아래의 함수를 실행
@app.route("/RemoveStudent", methods = ["POST"])
def remove_student():
    print(request.form)
    # AddStudentForm.html 에서 name 속성의 값이 univ_name 에 입력값 (이름) 리턴
    univ_name = request.form["univ_name"]
    print(f"univ_name = {univ_name}")
    # AddStudentForm.html 에서 name 속성의 값이 univ_id 에 입력값 (학번) 리턴
    univ_id = request.form["univ_id"]
    print(f"univ_id = {univ_id}")

    # boto3.resource('dynamodb') : dynamodb에 접속해서 데이터를 추가,수정,삭제 조회를 수행할 객체를 생성
    dynamodb = boto3.resource('dynamodb')
    #     # dynamodb.Table('UnivStudent') : UnivStudent 테이블에 데이터를 추가,수정,삭제 조회를 수행할 객체를 생성
    table = dynamodb.Table('UnivStudent')
    # 삭제하고자 하는 학생의 이름, 학번을 저장하고 있는 Dictionary 객체 생성
    will_remove_student = {
            'univ_name' : univ_name,
            'univ_id' : Decimal(univ_id)
        }
    print(f"will_remove_student = {will_remove_student}")

    # univ_id와 univ_name 이 일치하는 레코드를 UnivStudent 테이블에서 삭제
    table.delete_item(
        Key = will_remove_student
    )

    return redirect(url_for('hello_student_manager'))

# 학생 수정 화면으로 이동
@app.route('/EditStudentForm', methods=['GET','POST'])
def EditStudentForm():
    print("EditStudentForm call")

    univ_id = request.form["univ_id"]
    print(f"univ_id = {univ_id}")
    univ_name = request.form["univ_name"]
    print(f"univ_name = {univ_name}")

    # boto3.resource('dynamodb') : dynamodb에 접속해서 데이터를 추가,수정,삭제 조회를 수행할 객체를 생성
    dynamodb = boto3.resource('dynamodb')
    # dynamodb.Table('UnivStudent') : UnivStudent 테이블에 데이터를 추가,수정,삭제 조회를 수행할 객체를 생성
    table = dynamodb.Table('UnivStudent')
    # 삭제하고자 하는 학생의 이름, 학번을 저장하고 있는 Dictionary 객체 생성
    will_edit_student = {
            'univ_name' : univ_name,
            'univ_id' : Decimal(univ_id)
        }
    # 수정할 학생 정보 조회
    response = table.get_item(Key=will_edit_student)
    print(f"response = {response}")
    # 테이블의 레코드 정보를 출력 수정할 학생 1명의 정보는 response['Item']에 저장되 있음
    print(f"response['Item'] = {response['Item']}")
    # 수정할 학생정보를 출력할 EditStudentForm.html 페이지로 이동
    # student 변수에 response['Item'] (UnivStudent 테이블의 모든 레코드) 를 대입
    return render_template('EditStudentForm.html', student = response['Item'])

# 학생 수정 처리
# url이 EditStudent 일때 아래의 함수를 실행
@app.route('/EditStudent', methods=['GET','POST'])
def edit_student():
    univ_id = request.form["univ_id"]
    univ_name = request.form["univ_name"]
    major = request.form["major"]
    avg_credit = request.form["avg_credit"]
    circle = request.form["circle"]

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('UnivStudent')

    if univ_id != "" and univ_name != "":
        # dictionary edit_student 생성
        edit_student = {
            'univ_id' : Decimal(univ_id),
            'univ_name' : univ_name
        }
        # major 에 값이 존재하면
        if major != "":
            # edit_student 에 major추가
            edit_student["major"] = major

        # circle 에 값이 존재하면
        if circle != "":
            # edit_student 에 cricle 추가
            edit_student['circle'] = circle

        # avg_credit 에 값이 존재하면
        if avg_credit != "":
            # edit_student 에 avg_credit 추가
            edit_student['avg_credit'] = Decimal(avg_credit)

        print("edit_student = ", edit_student)

        # 테이블 UnivStudent 에 new_student 추가
        table.put_item(Item=edit_student)

    return redirect(url_for('hello_student_manager'))
serve(app, host='0.0.0.0', port=8082)