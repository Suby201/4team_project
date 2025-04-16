import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os

class QnetScheduleApp:
    def __init__(self, data_folder='data'):
        self.data_folder = data_folder
        os.makedirs(self.data_folder, exist_ok=True)
        self.year = 2025 #url에 사용될 연도 변수화

    def search_text(self, text, text_list):
        return [s for s in text_list if text in s]

    def fetch_schedule(self, month):
        month_str = f'0{month}' if month < 10 else str(month)
        url = f'https://www.q-net.or.kr/crf021.do?id=crf02103&gSite=Q&gId=&schGb=list&schMonth={self.year}{month_str}01'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except requests.exceptions.RequestException as e:
            st.error(f"URL 요청 실패: {e}")
            return None

    def parse_schedule(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        dates = [p.text.strip() for p in soup.select('th p.month')]
        tests = []
        for a in soup.select('div[class*=type] a'):
            parts = a['onclick'].split(',')[1:-2]
            tests.append(', '.join(parts).strip())
        return dict(zip(dates, tests))

    def save_schedule(self, schedule, month):
        filename = os.path.join(self.data_folder, f'test_schedule_{month}.json')
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(schedule, f, ensure_ascii=False, indent=4)
        except IOError as e:
            st.error(f"파일 저장 실패: {e}")

    def load_schedule(self, month):
        filename = os.path.join(self.data_folder, f'test_schedule_{month}.json')
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except IOError as e:
            st.error(f"파일 로딩 실패: {e}")
            return None

    def filter_and_display(self, tag, df):
        filtered_tests = self.search_text(tag, df['시험명'].tolist())
        st.dataframe(df[df['시험명'].isin(filtered_tests)].reset_index(drop=True))

    def run(self):
        st.title("큐넷 시험 일정 검색")
        month = st.number_input("월을 입력하세요 (예: 1):", min_value=1, max_value=12, value=1)

        if 'schedule_df' not in st.session_state:
            st.session_state.schedule_df = None

        if st.button("일정 불러오기"):
            with st.spinner("일정을 불러오는 중..."):
                html = self.fetch_schedule(month)
                if html:
                    schedule = self.parse_schedule(html)
                    self.save_schedule(schedule, month)
                    st.session_state.schedule_df = pd.DataFrame(list(schedule.items()), columns=['일정', '시험명'])
                else:
                    st.error("일정 불러오기 실패")

        if st.session_state.schedule_df is not None:
            tag = st.text_input("검색할 태그를 입력하세요:")
            if tag:
                self.filter_and_display(tag, st.session_state.schedule_df)
            else:
                st.dataframe(st.session_state.schedule_df)

if __name__ == "__main__":
    app = QnetScheduleApp()
    app.run()