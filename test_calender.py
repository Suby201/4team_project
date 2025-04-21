import streamlit as st  # Streamlit 라이브러리 import (웹 앱 개발)
import requests  # HTTP 요청을 보내는 라이브러리
from bs4 import BeautifulSoup  # HTML 및 XML 파일 파싱 라이브러리
import pandas as pd  # 데이터 분석 및 조작 라이브러리
import json  # JSON 데이터 처리 라이브러리
import os  # 운영체제 관련 기능 라이브러리

# streamlit run test_calender.py

class QnetScheduleApp:
    def __init__(self, data_folder='data'): #데이터 폴더 확인 및 연도 설정
        self.data_folder = data_folder  # 데이터를 저장할 폴더 경로 설정 ('data' 폴더를 기본값으로 사용)
        os.makedirs(self.data_folder, exist_ok=True)  # data 폴더 생성 (이미 존재하는 경우 오류를 발생시키지 않음)
        self.year = 2025 #url에 사용될 연도 변수화 (기본적으로 2025년으로 설정)
        self.tag = None # 검색할 태그를 저장하는 변수 초기화 (run 메서드에서 사용자 입력을 받을 예정)

    def search_text(self, text, text_list):
        return [s for s in text_list if text in s] #text_list에서 text를 포함하는 단어를 가진 단어들을 list로 반환
        # 주어진 text가 text_list의 각 요소(문자열)에 포함되어 있는지 확인하고, 포함된 요소들로 이루어진 새로운 리스트를 반환합니다.

    def fetch_schedule(self, month):  #사이트 request 요청 확인 및 html 반환
        month_str = f'0{month}' if month < 10 else str(month)  #url에 쓰일 month string 화 (한 자리 수 월 앞에 '0'을 붙여 두 자리 문자열로 만듦)
        url = f'https://www.q-net.or.kr/crf021.do?id=crf02103&gSite=Q&gId=&schGb=list&schMonth={self.year}{month_str}01'
        # 큐넷 시험 일정 페이지 URL 생성 (year와 month_str 변수를 사용하여 동적으로 URL을 만듦)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'}
        # 웹사이트 요청 시 User-Agent 헤더를 설정하여 브라우저처럼 보이게 함 (일부 사이트에서 요청을 거부하는 것을 방지)
        try:
            response = requests.get(url, headers=headers)  #request 요청 (생성된 URL로 HTTP GET 요청을 보냄)
            response.raise_for_status()  #오류 발생 확인 (HTTP 응답 상태 코드가 200 OK가 아니면 예외 발생)
            response.encoding = 'utf-8' #인코딩 설정 (응답 텍스트의 인코딩을 UTF-8로 설정)
            return response.text # HTML 내용 반환
        except requests.exceptions.RequestException as e:
            st.error(f"URL 요청 실패: {e}") #에러 메세지 출력 (요청 중 발생한 오류 메시지를 Streamlit에 표시)
            return None # 오류 발생 시 None 반환

    def parse_schedule(self, html):  #월별 시험일정 파싱
        soup = BeautifulSoup(html, 'html.parser') # BeautifulSoup 객체 생성 (HTML 내용을 파싱하기 위해)
        dates = [p.text.strip() for p in soup.select('th p.month')]  # 날짜는 p태그에 month 부분에 존재, 문자열 앞뒤 공백 제거
        # HTML에서 'th' 태그 아래 'p' 태그 중 클래스 이름에 'month'를 포함하는 요소들을 찾아 텍스트를 추출하고, 앞뒤 공백을 제거하여 리스트에 저장
        tests = []
        for a in soup.select('div[class*=type] a'):
            parts = a['onclick'].split(',')[1:-2]  #앞에 쓸모 없는 부분과 뒤에 날짜 제외
            # HTML에서 'div' 태그 중 클래스 이름에 'type'을 포함하는 요소 아래의 'a' 태그에서 'onclick' 속성 값을 가져와 쉼표로 분리하고, 처음과 마지막 두 요소를 제외한 나머지 요소들을 추출
            tests.append(', '.join(parts).strip()) #리스트 문자열 합치고 앞뒤 공백 제거
            # 추출된 부분들을 쉼표와 공백으로 연결하여 하나의 문자열로 만들고, 앞뒤 공백을 제거하여 tests 리스트에 추가
        return dict(zip(dates, tests)) # 날짜와 시험 명을 zip하여 dictionary 화 (날짜 리스트와 시험명 리스트를 묶어 딕셔너리 형태로 반환)

    def save_schedule(self, schedule, month):  # 저장하기
        filename = os.path.join(self.data_folder, f'test_schedule_{month}.json')  #파일 이름 설정 (데이터 폴더 경로와 월 정보를 이용하여 JSON 파일 이름 생성)
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(schedule, f, ensure_ascii=False, indent=4) #json 저장시 한글 깨짐 방지
                # 생성한 딕셔너리 형태의 시험 일정을 JSON 파일로 저장 (ensure_ascii=False로 설정하여 한글 깨짐 방지, indent=4로 설정하여 들여쓰기 적용)
        except IOError as e:
            st.error(f"파일 저장 실패: {e}") # 파일 저장 중 오류 발생 시 오류 메시지 출력

    def load_schedule(self, month):  #json 파일 읽어오기
        filename = os.path.join(self.data_folder, f'test_schedule_{month}.json')
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f) # JSON 파일 내용을 읽어와 파이썬 딕셔너리 형태로 반환
        except FileNotFoundError:
            return None # 파일이 없을 경우 None 반환
        except IOError as e:
            st.error(f"파일 로딩 실패: {e}")
            return None # 파일 로딩 중 오류 발생 시 None 반환

    def filter_and_display(self, tag, df):  # 검색하기
        if tag.endswith('기사'):
            tag = '기사'
        elif tag.endswith('기술사'):
            tag = '기술사'
        elif tag.endswith('기능사'):
            tag = '기능사'
        elif tag.endswith('기능장'):
            tag = '기능장'
        # 입력된 태그가 특정 키워드로 끝나는 경우 해당 키워드로 일반화 (예: '정보처리기사' -> '기사')
        filtered_tests = self.search_text(tag, df['시험명'].tolist())  #tag가 포함된 시험명을 찾아 리스트로 저장
        # 데이터프레임의 '시험명' 컬럼의 모든 값을 리스트로 변환하여 search_text 함수를 사용하여 입력된 태그를 포함하는 시험명 검색
        if filtered_tests:
            st.dataframe(df[df['시험명'].isin(filtered_tests)].reset_index(drop=True))  # 해당하는 시험명을 데이터프레임으로 출력
            # 검색된 시험명들이 포함된 행들로 새로운 데이터프레임을 만들고, 인덱스를 재설정하여 Streamlit에 표시
        else:
            st.info(f"'{tag}' 관련 시험 일정이 없습니다.") # 검색 결과가 없을 경우 메시지 출력

    def run(self):
        st.title("📅큐넷 시험 일정 검색") #제목 출력
        month = st.number_input("월을 입력하세요 (예: 1):", min_value=1, max_value=12, value=1) # 월을 입력 받음
        # 사용자로부터 검색하고 싶은 월을 입력받는 숫자 입력 위젯 생성 (최소 1, 최대 12, 기본값 1)

        if 'schedule_df' not in st.session_state: # 세션 상태에 schedule_df가 없으면 None 으로 초기화
            st.session_state.schedule_df = None
            # Streamlit 세션 상태에 'schedule_df' 키가 존재하는지 확인하고, 없으면 None으로 초기화 (앱이 다시 실행될 때 이전 상태를 유지하기 위함)

        if st.button("일정 불러오기"): #일정 불러오기 버튼 클릭시 실행
            with st.spinner("일정을 불러오는 중..."): # 로딩 중 스피너 표시 (작업이 오래 걸릴 수 있음을 사용자에게 알림)
                html = self.fetch_schedule(month) # html 불러오기 (입력된 월에 해당하는 시험 일정 HTML 내용을 가져옴)
                if html: #html 이 있다면
                    schedule = self.parse_schedule(html) #html 파싱 (가져온 HTML 내용을 파싱하여 시험 일정 정보를 딕셔너리 형태로 변환)
                    self.save_schedule(schedule, month) #파싱한 데이터 json으로 저장 (파싱된 시험 일정 정보를 JSON 파일로 저장)
                    st.session_state.schedule_df = pd.DataFrame(list(schedule.items()), columns=['일정', '시험명']) #세션 상태에 저장
                    # 파싱된 딕셔너리를 Pandas DataFrame으로 변환하여 '일정'과 '시험명' 컬럼을 갖도록 하고, 세션 상태에 저장 (앱이 다시 실행되어도 데이터를 유지)
                else: #html이 없다면
                    st.error("일정 불러오기 실패") # HTML 내용을 가져오지 못한 경우 오류 메시지 출력

        if st.session_state.schedule_df is not None: #세션 상태에 schedule_df 가 존재 한다면
            tag = self.tag #태그 입력 받기 (사용자로부터 검색할 태그를 입력받는 텍스트 입력 위젯 생성)
            if tag: #태그가 있다면
                self.filter_and_display(tag, st.session_state.schedule_df) #태그 검색 및 출력 (입력된 태그와 세션 상태에 저장된 시험 일정 DataFrame을 이용하여 검색 및 결과 표시)
            else: #태그가 없다면
                st.dataframe(st.session_state.schedule_df) #전체 데이터프레임 출력 (태그가 입력되지 않았으면 전체 시험 일정 DataFrame을 화면에 표시)

if __name__ == "__main__":
    app = QnetScheduleApp() # QnetScheduleApp 클래스의 인스턴스 생성
    app.run() # 앱 실행 메서드 호출