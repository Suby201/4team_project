import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import platform
import bar_graph as bg

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
        self.people_df = people_df  # 합격 인원 데이터프레임 저장
        self.per_df = per_df      # 합격률 데이터프레임 저장
        self._set_korean_font()   # 한글 폰트 설정
        st.title("📊 자격증 연도별 통계 시각화")  # 앱 제목 표시
        self.all_years = ['2019 년', '2020 년', '2021 년', '2022 년', '2023 년']  # 선택 가능한 모든 연도
        self.selected_years = st.multiselect("📆 확인할 연도를 선택하세요", self.all_years, default=self.all_years)  # 연도 선택 멀티 셀렉트 위젯
        # self.search_term = st.text_input("🔍 종목명을 입력하세요:").replace(' ', '')  # 종목명 검색 텍스트 입력 위젯
        self.view_type = st.selectbox("📈 보고 싶은 항목을 선택하세요", ["합격률 (%)", "합격 인원 수"])  # 보고 싶은 항목 선택 셀렉트 박스
        self.current_df = self._set_current_dataframe()  # 선택된 보기에 따라 사용할 데이터프레임 설정
        self.y_label = self._set_y_label()          # y축 레이블 설정
        self.y_max = self._set_y_max()              # y축 최대값 설정

    def _set_korean_font(self):
        """플랫폼에 따라 한글 폰트를 설정하는 내부 메서드"""
        if platform.system() == 'Windows':
            plt.rcParams['font.family'] = 'Malgun Gothic'
        elif platform.system() == 'Darwin':  # macOS
            plt.rcParams['font.family'] = 'AppleGothic'
        else:  # Linux (Colab, Ubuntu 등)
            plt.rcParams['font.family'] = 'NanumGothic'
        plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

    def _set_current_dataframe(self):
        """선택된 보기에 따라 사용할 데이터프레임을 반환하는 내부 메서드"""
        if self.view_type == "합격률 (%)":
            return self.per_df
        else:
            return self.people_df

    def _set_y_label(self):
        """선택된 보기에 따라 y축 레이블을 반환하는 내부 메서드"""
        if self.view_type == "합격률 (%)":
            return "합격률 (%)"
        else:
            return "합격 인원 수"

    def _set_y_max(self):
        """선택된 보기에 따라 y축 최대값을 반환하는 내부 메서드"""
        if self.view_type == "합격률 (%)":
            return 100
        else:
            return None  # 자동 스케일

    def _filter_dataframe(self):
        """검색어에 따라 데이터프레임을 필터링하는 내부 메서드"""
        if self.search_term:
            filtered_df = self.current_df[self.current_df['종목별'].str.contains(self.search_term, case=False)]
            return filtered_df
        return None

    def _plot_bar_chart(self, data, title):
        """막대 그래프를 그리고 Streamlit에 표시하는 내부 메서드"""
        plt.figure(figsize=(8, 4))  # 그래프 크기 설정
        plt.bar(self.selected_years, data[self.selected_years].values)  # 막대 그래프 생성
        plt.ylabel(self.y_label)  # y축 레이블 설정
        if self.y_max:
            plt.ylim(0, self.y_max)  # y축 범위 설정 (합격률인 경우 0~100%)
        plt.grid(axis='y', linestyle='--', alpha=0.5)  # y축 격자선 표시
        st.pyplot(plt)  # Streamlit에 그래프 표시

    def display_results(self):
        """검색 결과를 표시하고 해당하는 그래프를 출력하는 메서드"""
        filtered_df = self._filter_dataframe()  # 검색어에 따라 데이터프레임 필터링
        if self.search_term:  # 검색어가 있는 경우
            if filtered_df is None or filtered_df.empty:
                st.warning("검색 결과가 없습니다.")  # 검색 결과가 없을 때 경고 메시지 표시
            else:
                st.dataframe(filtered_df)  # 필터링된 데이터프레임 표시
                for idx, row in filtered_df.iterrows():  # 각 행(종목별 데이터)에 대해
                    st.subheader(f"{row['종목별']} - {row['항목']}")  # 하위 제목 표시 (종목명 - 항목)
                    self._plot_bar_chart(row, f"{row['종목별']} - {row['항목']}")  # 막대 그래프 그리기
        else:
            st.info("종목명을 입력하여 검색하세요.")  # 검색어가 없을 때 안내 메시지 표시

# 사용 예시 (bg 객체가 이미 정의되어 있다고 가정)
if __name__ == '__main__':
    # 가상의 데이터프레임 생성 (실제로는 bg.people_pr_df, bg.per_pr_df 사용)
    
    # 📌 전처리된 데이터프레임
    people_df = bg.people_pr_df  # 합격 인원
    per_df = bg.per_pr_df        # 합격률

    visualizer = CertificationVisualizer(people_df, per_df)  # CertificationVisualizer 클래스의 인스턴스 생성
    visualizer.display_results()  # 결과 표시 메서드 호출