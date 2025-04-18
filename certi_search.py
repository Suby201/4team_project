import streamlit as st  # Streamlit 라이브러리 import (웹 앱 개발)
from app_re import BookSearchApp as bs  # app_re.py 파일에서 BookSearchApp 클래스를 bs라는 이름으로 import
from my_re import CertificationSearchApp as cs  # my_re.py 파일에서 CertificationSearchApp 클래스를 cs라는 이름으로 import
from test_calender import QnetScheduleApp as qs  # test_calender.py 파일에서 QnetScheduleApp 클래스를 qs라는 이름으로 import
from streamlit_app_re import CertificationVisualizer as cv  # streamlit_app_re.py 파일에서 CertificationVisualizer 클래스를 cv라는 이름으로 import
import bar_graph as bg  # bar_graph.py 파일을 bg라는 이름으로 import (데이터프레임 객체 포함)

# streamlit run certi_search.py


class PrepareCertification :
    # 페이지 설정은 여기서 한 번만 합니다.
    st.set_page_config(page_title="자격증 정보 통합 검색", page_icon=" 통합")  # 웹 페이지의 제목과 아이콘 설정

    def main(self):
        st.sidebar.header = '자격증명 검색'  # 사이드바에 헤더 텍스트 표시
        search_keyword = st.sidebar.text_input("검색할 자격증을 입력해주세요. ")  # 사이드바에 자격증 검색을 위한 텍스트 입력 위젯 생성

        # 탭 목록 정의
        tabs = ["자격증 검색", "합격 인원 및 합격률 보기", "책 검색", "시험일정 확인"]
        # 탭 선택 라디오 버튼 생성 (가로 방향 배치, 초기 선택 없음, key를 통해 상태 관리)
        selected_tab = st.radio("메뉴", tabs, horizontal=True,
                                    key="main_tab_selector")

        st.title(f"{selected_tab}")  # 선택된 탭의 이름을 앱의 제목으로 표시

        if selected_tab == "자격증 검색":
            app = cs()  # my_re.py의 CertificationSearchApp 인스턴스 생성
            app.keyword = search_keyword  # 검색 키워드를 CertificationSearchApp 객체의 keyword 속성에 할당
            app.display_results()  # 자격증 검색 결과 표시 메서드 호출
            if search_keyword:  # 검색어가 있는 경우
                st.session_state.search_keyword = app.certi_name  # 선택된 자격증 이름을 세션 상태에 저장 (다른 탭에서 사용)
        elif selected_tab == "합격 인원 및 합격률 보기":
            visualizer = cv(bg.people_pr_df, bg.per_pr_df)  # streamlit_app_re.py의 CertificationVisualizer 인스턴스 생성 (데이터프레임 전달)
            if st.session_state.search_keyword:  # 세션 상태에 검색 키워드가 있는 경우
                visualizer.search_term = st.session_state.search_keyword  # CertificationVisualizer 객체의 search_term 속성에 할당
            else:  # 세션 상태에 검색 키워드가 없는 경우 (초기 또는 검색어 삭제)
                visualizer.search_term = search_keyword  # 현재 사이드바의 검색어를 CertificationVisualizer 객체의 search_term 속성에 할당
            visualizer.display_results()  # 합격 인원 및 합격률 시각화 결과 표시 메서드 호출
        elif selected_tab == "책 검색":
            app = bs()  # app_re.py의 BookSearchApp 인스턴스 생성
            if st.session_state.search_keyword:  # 세션 상태에 검색 키워드가 있는 경우
                app.query = st.session_state.search_keyword  # BookSearchApp 객체의 query 속성에 할당
            else:  # 세션 상태에 검색 키워드가 없는 경우
                app.query = search_keyword  # 현재 사이드바의 검색어를 BookSearchApp 객체의 query 속성에 할당

            # app_re.py의 검색 버튼 클릭 상태를 확인하여 결과 표시 (세션 상태를 이용)
            if st.session_state.get('search_button_clicked', False):
                app.display_book_results()
        elif selected_tab == "시험일정 확인":
            app = qs()  # test_calender.py의 QnetScheduleApp 인스턴스 생성
            if st.session_state.search_keyword:  # 세션 상태에 검색 키워드가 있는 경우
                app.tag = st.session_state.search_keyword  # QnetScheduleApp 객체의 tag 속성에 할당
            else:  # 세션 상태에 검색 키워드가 없는 경우
                app.tag = search_keyword  # 현재 사이드바의 검색어를 QnetScheduleApp 객체의 tag 속성에 할당

            app.run()  # 큐넷 시험 일정 검색 앱 실행

if __name__ == "__main__":
    app = PrepareCertification()  # PrepareCertification 클래스의 인스턴스 생성
    app.main()  # 앱의 메인 함수 호출