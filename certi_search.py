import streamlit as st
from app_Re import BookSearchApp as bs
from my_re import CertificationSearchApp as cs
from test_calender import QnetScheduleApp as qs
from streamlit_app_re import CertificationVisualizer as cv
import bar_graph as bg

# 페이지 설정은 여기서 한 번만 합니다.
st.set_page_config(page_title="자격증 정보 통합 검색", page_icon=" 통합")

def main():
    tabs = ["자격증 검색", "합격률 보기", "책 검색", "시험일정 확인"]
    selected_tab = st.radio("메뉴", tabs, horizontal=True,
                             key="main_tab_selector") # 탭 선택 라디오 버튼

    st.title(f"{selected_tab}") # 선택된 탭 이름으로 제목 표시

    if selected_tab == "자격증 검색":
        app = cs()
        app.display_results()
    elif selected_tab == "합격률 보기":
        visualizer = cv(bg.people_pr_df, bg.per_pr_df)  # CertificationVisualizer 클래스의 인스턴스 생성
        visualizer.display_results()  # 결과 표시 메서드 호출
    elif selected_tab == "책 검색":
        app = bs()
        if st.session_state.get('search_button_clicked', False): # app_re.py의 버튼 클릭 상태를 확인
            app.display_book_results()
    elif selected_tab == "시험일정 확인":
        app = qs()
        app.run()

if __name__ == "__main__":
    main()