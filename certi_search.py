import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os
import json
import matplotlib.pyplot as plt
import platform
import bar_graph as bg
import app_re as app
import my
import test_calender as tc
import streamlit_app_re as sa

def main():
    tabs = ["자격증 검색", "합격률 보기", "책 검색", "시험일정 확인"]
    selected_tab = st.radio("메뉴", tabs, horizontal=True, key="main_tab_selector")

    st.title(f"{selected_tab}")

    with st.sidebar:
        st.subheader("설정")
        if selected_tab == "자격증 검색":
            st.subheader("자격증 검색 설정")
            search_keyword = st.text_input("검색어 입력")
            search_button = st.button("검색")
            if search_button:
                st.write(f"'{search_keyword}'로 검색합니다...")
        elif selected_tab == "합격률 보기":
            st.subheader("합격률 보기 설정")
            qualification_type = st.selectbox("자격증 종류 선택", ["기사", "산업기사", "기능사"])
            year = st.slider("년도 선택", 2020, 2025, 2024)
            show_button = st.button("보기")
            if show_button:
                st.write(f"{qualification_type} {year}년 합격률을 표시합니다...")
        elif selected_tab == "책 검색":
            st.subheader("책 검색 설정")
            book_keyword = st.text_input("책 제목 또는 저자 입력")
            search_book_button = st.button("검색")
            if search_book_button:
                st.write(f"'{book_keyword}' 관련 책을 검색합니다...")
        elif selected_tab == "시험일정 확인":
            st.subheader("시험일정 확인 설정")
            exam_category = st.selectbox("시험 종류 선택", ["국가기술자격", "어학 시험", "기타"])
            view_schedule_button = st.button("확인")
            if view_schedule_button:
                st.write(f"{exam_category} 시험 일정을 확인합니다...")

    if selected_tab == "자격증 검색":
        st.write("자격증 검색 기능을 구현합니다.")
    elif selected_tab == "합격률 보기":
        st.write("자격증 합격률 보기 기능을 구현합니다.")
    elif selected_tab == "책 검색":
        st.write("자격증 관련 책 검색 기능을 구현합니다.")
    elif selected_tab == "시험일정 확인":
        st.write("시험 일정을 확인하는 기능을 구현합니다.")

if __name__ == "__main__":
    main()