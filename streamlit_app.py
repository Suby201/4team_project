import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import bar_graph as bg

# 🔠 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
else:  # Linux (Colab, Ubuntu 등)
    plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

# 📌 전처리된 데이터프레임
people_df = bg.people_pr_df  # 합격 인원
per_df = bg.per_pr_df        # 합격률

# 🏷️ 앱 제목
st.title("📊 자격증 연도별 통계 시각화")

# 📌 보기 종류 선택
view_type = st.selectbox("📈 보고 싶은 항목을 선택하세요", ["합격률 (%)", "합격 인원 수"])

# 📅 연도 선택 (멀티 선택)
all_years = ['2019 년', '2020 년', '2021 년', '2022 년', '2023 년']
selected_years = st.multiselect("📆 확인할 연도를 선택하세요", all_years, default=all_years)

# 🔍 검색어 입력
search_term = st.text_input("🔍 종목명을 입력하세요:").replace(' ', '')

# 📊 보기 선택에 따라 데이터프레임 설정
if view_type == "합격률 (%)":
    current_df = per_df
    y_label = "합격률 (%)"
    y_max = 100
else:
    current_df = people_df
    y_label = "합격 인원 수"
    y_max = None  # 자동 스케일

# 🔎 검색 및 시각화
if search_term:
    filtered_df = current_df[current_df['종목별'].str.contains(search_term, case=False)]

    if filtered_df.empty:
        st.warning("검색 결과가 없습니다.")
    else:
        st.dataframe(filtered_df)

        for idx, row in filtered_df.iterrows():
            st.subheader(f"{row['종목별']} - {row['항목']}")
            plt.figure(figsize=(8, 4))
            plt.bar(selected_years, row[selected_years].values)
            plt.ylabel(y_label)
            if y_max:
                plt.ylim(0, y_max)
            plt.grid(axis='y', linestyle='--', alpha=0.5)
            st.pyplot(plt)
