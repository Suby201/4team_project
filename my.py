import streamlit as st
import pandas as pd

# 데이터 로드 함수
@st.cache_data
def load_data():
    return pd.read_csv("자격증.csv", encoding='cp949')

df = load_data()

# 불필요한 열 제거
df = df.drop(columns=[col for col in df.columns if "Unnamed" in col])

# 앱 제목
st.title("📘 자격증 통계 검색")
st.write("자격증 종목명을 입력하면 관련된 통계 항목을 보여드립니다.")

# 사용자 입력
keyword = st.text_input("🔍 자격증(종목) 이름을 입력하세요:", placeholder="예: 정보처리")

if keyword:
    filtered = df[df['종목별'].str.contains(keyword, case=False, na=False)]
    
    if not filtered.empty:
        st.success(f"✅ '{keyword}'에 해당하는 데이터 {len(filtered)}건이 검색되었습니다.")
        st.dataframe(filtered.reset_index(drop=True))
    else:
        st.warning(f"❌ '{keyword}'에 해당하는 자격증 종목을 찾을 수 없습니다.")

