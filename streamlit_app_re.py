import streamlit as st  # Streamlit 라이브러리 import (웹 앱 개발)
import pandas as pd  # Pandas 라이브러리 import (데이터 조작 및 분석)
import matplotlib.pyplot as plt  # Matplotlib 라이브러리 import (그래프 그리기)
import platform  # 플랫폼 정보 접근 라이브러리 import
import bar_graph as bg  # bar_graph.py 파일에서 정의된 객체(bg)를 import

# streamlit run streamlit_app_re.py

class CertificationVisualizer:
    """자격증 연도별 통계 시각화를 위한 클래스"""
    def __init__(self, people_df, per_df):
        """
        초기화 메서드

        Args:
            people_df (pd.DataFrame): 합격 인원 데이터프레임
            per_df (pd.DataFrame): 합격률 데이터프레임
        """
        self.people_df = people_df  # 인수로 받은 합격 인원 데이터프레임을 클래스 속성에 저장
        self.per_df = per_df        # 인수로 받은 합격률 데이터프레임을 클래스 속성에 저장
        self._set_korean_font()   # 한글 폰트 설정 메서드 호출
        st.title("📊 자격증 연도별 통계 시각화")  # Streamlit 앱 제목 표시
        self.all_years = ['2019 년', '2020 년', '2021 년', '2022 년', '2023 년']  # 선택 가능한 모든 연도 리스트 정의
        self.selected_years = st.multiselect("📆 확인할 연도를 선택하세요", self.all_years, default=self.all_years)  # 연도 선택 멀티 셀렉트 위젯 생성 (기본값으로 모든 연도 선택)
        self.view_type = st.selectbox("📈 보고 싶은 항목을 선택하세요", ["합격률 (%)", "합격 인원 수"])  # 보고 싶은 항목 선택 셀렉트 박스 생성
        self.current_df = self._set_current_dataframe()  # 선택된 보기에 따라 사용할 데이터프레임 설정 메서드 호출
        self.y_label = self._set_y_label()        # y축 레이블 설정 메서드 호출
        self.y_max = self._set_y_max()          # y축 최대값 설정 메서드 호출

    def _set_korean_font(self):
        """플랫폼에 따라 한글 폰트를 설정하는 내부 메서드"""
        if platform.system() == 'Windows':  # 운영체제가 Windows인 경우
            plt.rcParams['font.family'] = 'Malgun Gothic'  # 맑은 고딕 폰트 설정
        elif platform.system() == 'Darwin':  # macOS인 경우
            plt.rcParams['font.family'] = 'AppleGothic'  # AppleGothic 폰트 설정
        else:  # Linux 등 다른 운영체제인 경우
            plt.rcParams['font.family'] = 'NanumGothic'  # 나눔고딕 폰트 설정
        plt.rcParams['axes.unicode_minus'] = False  # 그래프에서 음수 기호 깨짐 방지

    def _set_current_dataframe(self):
        """선택된 보기에 따라 사용할 데이터프레임을 반환하는 내부 메서드"""
        if self.view_type == "합격률 (%)":  # 보고 싶은 항목으로 '합격률 (%)'이 선택된 경우
            return self.per_df  # 합격률 데이터프레임 반환
        else:  # 그 외 (여기서는 '합격 인원 수'가 선택된 경우)
            return self.people_df  # 합격 인원 데이터프레임 반환

    def _set_y_label(self):
        """선택된 보기에 따라 y축 레이블을 반환하는 내부 메서드"""
        if self.view_type == "합격률 (%)":  # 보고 싶은 항목으로 '합격률 (%)'이 선택된 경우
            return "합격률 (%)"  # y축 레이블을 "합격률 (%)"으로 설정
        else:  # 그 외 (여기서는 '합격 인원 수'가 선택된 경우)
            return "합격 인원 수"  # y축 레이블을 "합격 인원 수"로 설정

    def _set_y_max(self):
        """선택된 보기에 따라 y축 최대값을 반환하는 내부 메서드"""
        if self.view_type == "합격률 (%)":  # 보고 싶은 항목으로 '합격률 (%)'이 선택된 경우
            return 100  # y축 최대값을 100으로 설정 (합격률은 0~100%)
        else:  # 그 외 (여기서는 '합격 인원 수'가 선택된 경우)
            return None  # y축 최대값을 자동으로 설정

    def _filter_dataframe(self):
        """검색어에 따라 데이터프레임을 필터링하는 내부 메서드"""
        if self.search_term:  # 검색어가 입력된 경우
            filtered_df = self.current_df[self.current_df['종목별'].str.contains(self.search_term, case=False)]  # '종목별' 컬럼에 검색어를 포함하는 행을 찾아 필터링 (대소문자 구분 없이)
            return filtered_df  # 필터링된 데이터프레임 반환
        return None  # 검색어가 없으면 None 반환

    def _plot_bar_chart(self, data, title):
        """막대 그래프를 그리고 Streamlit에 표시하는 내부 메서드"""
        plt.figure(figsize=(8, 4))  # 그래프의 가로, 세로 크기 설정
        plt.bar(self.selected_years, data[self.selected_years].values)  # 선택된 연도를 x축, 해당 연도의 값을 y축으로 하는 막대 그래프 생성
        plt.ylabel(self.y_label)  # y축 레이블 설정
        if self.y_max:  # y축 최대값이 설정된 경우
            plt.ylim(0, self.y_max)  # y축의 범위를 0부터 y축 최대값까지로 설정
        plt.grid(axis='y', linestyle='--', alpha=0.5)  # y축 방향으로 점선 형태의 격자선 표시 (투명도 0.5)
        st.pyplot(plt)  # Matplotlib으로 그린 그래프를 Streamlit 앱에 표시

    def display_results(self):
        """검색 결과를 표시하고 해당하는 그래프를 출력하는 메서드"""
        filtered_df = self._filter_dataframe()  # 검색어에 따라 데이터프레임 필터링
        if self.search_term:  # 검색어가 있는 경우
            if filtered_df is None or filtered_df.empty:  # 필터링된 데이터프레임이 없거나 비어있는 경우
                st.warning("검색 결과가 없습니다.")  # 경고 메시지 표시
            else:  # 필터링된 데이터프레임이 있는 경우
                st.dataframe(filtered_df)  # 필터링된 데이터프레임 표시
                for idx, row in filtered_df.iterrows():  # 필터링된 데이터프레임의 각 행에 대해 반복 처리
                    st.subheader(f"{row['종목별']} - {row['항목']}")  # 종목명과 항목을 조합하여 하위 제목 표시
                    self._plot_bar_chart(row, f"{row['종목별']} - {row['항목']}")  # 해당 종목의 연도별 데이터를 사용하여 막대 그래프 그림
        else:  # 검색어가 없는 경우
            st.info("종목명을 입력하여 검색하세요.")  # 안내 메시지 표시

# 사용 예시 (bg 객체가 이미 정의되어 있다고 가정)
if __name__ == '__main__':
    # 📌 전처리된 데이터프레임 (bar_graph.py에서 로드 및 전처리됨)
    people_df = bg.people_pr_df  # bar_graph.py에서 합격 인원 데이터프레임 로드
    per_df = bg.per_pr_df        # bar_graph.py에서 합격률 데이터프레임 로드

    visualizer = CertificationVisualizer(people_df, per_df)  # CertificationVisualizer 클래스의 인스턴스 생성
    visualizer.display_results()  # 결과 표시 메서드 호출