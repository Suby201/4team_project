import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os

# streamlit run test_calender.py

class QnetScheduleApp:
    def __init__(self, data_folder='data'): #데이터 폴더 확인 및 연도 설정
        self.data_folder = data_folder
        os.makedirs(self.data_folder, exist_ok=True)  #data 폴더 생성 (이미 존재하는 경우 오류 발생 X)
        self.year = 2025 #url에 사용될 연도 변수화

    def search_text(self, text, text_list):
        return [s for s in text_list if text in s] #text_list에서 text를 포함하는 단어를 가진 단어들을 list로 반환

    def fetch_schedule(self, month):  #사이트 request 요청 확인 및 html 반환
        month_str = f'0{month}' if month < 10 else str(month)  #url에 쓰일 month string 화
        url = f'https://www.q-net.or.kr/crf021.do?id=crf02103&gSite=Q&gId=&schGb=list&schMonth={self.year}{month_str}01'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'}
        try:
            response = requests.get(url, headers=headers)  #request 요청
            response.raise_for_status()  #오류 발생 확인
            response.encoding = 'utf-8' #인코딩 설정
            return response.text
        except requests.exceptions.RequestException as e:
            st.error(f"URL 요청 실패: {e}") #에러 메세지 출력
            return None

    def parse_schedule(self, html):  #월별 시험일정 파싱
        soup = BeautifulSoup(html, 'html.parser')
        dates = [p.text.strip() for p in soup.select('th p.month')]  # 날짜는 p태그에 month 부분에 존재, 문자열 앞뒤 공백 제거
        tests = []
        for a in soup.select('div[class*=type] a'):
            parts = a['onclick'].split(',')[1:-2]  #앞에 쓸모 없는 부분과 뒤에 날짜 제외
            tests.append(', '.join(parts).strip()) #리스트 문자열 합치고 앞뒤 공백 제거
        return dict(zip(dates, tests)) # 날짜와 시험 명을 zip하여 dictnionary 화 

    def save_schedule(self, schedule, month):  # 저장하기
        filename = os.path.join(self.data_folder, f'test_schedule_{month}.json')  #파일 이름 설정
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(schedule, f, ensure_ascii=False, indent=4) #json 저장시 한글 깨짐 방지
        except IOError as e:
            st.error(f"파일 저장 실패: {e}")

    def load_schedule(self, month):  #json 파일 읽어오기
        filename = os.path.join(self.data_folder, f'test_schedule_{month}.json')
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except IOError as e:
            st.error(f"파일 로딩 실패: {e}")
            return None

    def filter_and_display(self, tag, df):  # 검색하기
        filtered_tests = self.search_text(tag, df['시험명'].tolist())  #tag가 포함된 시험명을 찾아 리스트로 저장
        st.dataframe(df[df['시험명'].isin(filtered_tests)].reset_index(drop=True))  # 해당하는 시험명을 데이터프레임으로 출력

    def run(self):
        st.title("큐넷 시험 일정 검색") #제목 출력
        month = st.number_input("월을 입력하세요 (예: 1):", min_value=1, max_value=12, value=1) # 월을 입력 받음

        if 'schedule_df' not in st.session_state: # 세션 상태에 schedule_df가 없으면 None 으로 초기화
            st.session_state.schedule_df = None

        if st.button("일정 불러오기"): #일정 불러오기 버튼 클릭시 실행
            with st.spinner("일정을 불러오는 중..."): # 로딩 중 스피너 표시
                html = self.fetch_schedule(month) # html 불러오기
                if html: #html 이 있다면
                    schedule = self.parse_schedule(html) #html 파싱
                    self.save_schedule(schedule, month) #파싱한 데이터 json으로 저장
                    st.session_state.schedule_df = pd.DataFrame(list(schedule.items()), columns=['일정', '시험명']) #세션 상태에 저장
                else: #html이 없다면
                    st.error("일정 불러오기 실패")

        if st.session_state.schedule_df is not None: #세션 상태에 schedule_df 가 존재 한다면
            tag = st.text_input("검색할 태그를 입력하세요:") #태그 입력 받기
            if tag: #태그가 있다면
                self.filter_and_display(tag, st.session_state.schedule_df) #태그 검색 및 출력
            else: #태그가 없다면
                st.dataframe(st.session_state.schedule_df) #전체 데이터프레임 출력

if __name__ == "__main__":
    app = QnetScheduleApp()
    app.run()