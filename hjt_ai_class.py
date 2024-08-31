import streamlit as st
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Streamlit 페이지 설정
st.set_page_config(page_title="우리 학교 통합 학습 플랫폼", layout="wide")

# Google Sheets API 설정
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'path/to/your/service_account.json'
SPREADSHEET_ID = '여기에_당신의_스프레드시트_ID를_입력하세요'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# 헤더
st.title("우리 학교 통합 학습 플랫폼")

# 네비게이션
nav = st.sidebar.radio("메뉴", ["수업 전달사항", "수업 자료", "사진 갤러리", "질문 게시판", "출석 인증", "조별 활동", "학생 데이터"])

# 데이터 로드 함수
def load_data(range_name):
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
    data = result.get('values', [])
    return pd.DataFrame(data[1:], columns=data[0])

# 각 섹션 함수
def notices_section():
    st.header("수업 전달사항")
    notices = load_data("Notices!A2:C")
    for _, notice in notices.iterrows():
        st.subheader(notice['제목'])
        st.write(notice['내용'])
        st.caption(f"작성일: {notice['날짜']}")
    
    with st.form("새 공지사항"):
        title = st.text_input("제목")
        content = st.text_area("내용")
        submit = st.form_submit_button("공지사항 추가")
        if submit:
            # 여기에 새 공지사항을 Google Sheets에 추가하는 코드 작성

def materials_section():
    st.header("수업 자료")
    materials = load_data("Materials!A2:C")
    for _, material in materials.iterrows():
        st.subheader(material['제목'])
        st.write(material['설명'])
        st.download_button("다운로드", material['링크'], file_name=material['제목'])
    
    uploaded_file = st.file_uploader("자료 업로드", type=['pdf', 'doc', 'docx', 'ppt', 'pptx'])
    if uploaded_file is not None:
        # 여기에 파일 업로드 처리 코드 작성

def gallery_section():
    st.header("사진 갤러리")
    gallery = load_data("Gallery!A2:C")
    cols = st.columns(3)
    for idx, (_, photo) in enumerate(gallery.iterrows()):
        with cols[idx % 3]:
            st.image(photo['이미지_URL'], caption=photo['설명'])
    
    uploaded_image = st.file_uploader("사진 업로드", type=['png', 'jpg', 'jpeg'])
    if uploaded_image is not None:
        # 여기에 이미지 업로드 처리 코드 작성

def questions_section():
    st.header("질문 게시판")
    questions = load_data("Questions!A2:C")
    for _, question in questions.iterrows():
        st.subheader(question['제목'])
        st.write(question['내용'])
        st.caption(f"작성일: {question['날짜']}")
    
    with st.form("새 질문"):
        title = st.text_input("제목")
        content = st.text_area("내용")
        submit = st.form_submit_button("질문 제출")
        if submit:
            # 여기에 새 질문을 Google Sheets에 추가하는 코드 작성

def attendance_section():
    st.header("출석 인증")
    attendance_code = "ABC123"  # 이 코드는 동적으로 생성되어야 합니다
    st.write(f"오늘의 출석 코드: {attendance_code}")
    user_code = st.text_input("출석 코드 입력")
    if st.button("출석 확인"):
        if user_code == attendance_code:
            st.success("출석이 확인되었습니다.")
        else:
            st.error("잘못된 출석 코드입니다.")

def group_section():
    st.header("조별 활동")
    groups = load_data("Groups!A2:C")
    st.dataframe(groups)
    
    if st.button("조별 활동 업데이트"):
        # 여기에 조별 활동 업데이트 코드 작성
        pass

def student_data_section():
    st.header("학생 데이터 관리")
    students = load_data("Students!A2:F")
    edited_df = st.data_editor(students)
    if st.button("학생 데이터 저장"):
        # 여기에 수정된 데이터를 Google Sheets에 저장하는 코드 작성
        pass

# 메인 앱 로직
if nav == "수업 전달사항":
    notices_section()
elif nav == "수업 자료":
    materials_section()
elif nav == "사진 갤러리":
    gallery_section()
elif nav == "질문 게시판":
    questions_section()
elif nav == "출석 인증":
    attendance_section()
elif nav == "조별 활동":
    group_section()
elif nav == "학생 데이터":
    student_data_section()
