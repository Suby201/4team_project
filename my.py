import streamlit as st
import pandas as pd

# 데이터 로드 함수
@st.cache_data
def load_data():
    df = pd.read_csv("자격증.csv", encoding='cp949')
    df = df.drop(columns=[col for col in df.columns if "Unnamed" in col])
    df.columns = df.columns.str.strip()  # 컬럼명 공백 제거
    return df

df = load_data()

# 앱 제목
st.title("📘 자격증 종목 통계 검색")
st.markdown("자격증 **종목명**을 입력하면 연도별 응시 및 합격률 데이터를 확인할 수 있습니다.")

# 사용자 입력
keyword = st.text_input("🔍 자격증(종목) 이름을 입력하세요:", placeholder="예: 정보처리")

if keyword:
    filtered = df[df['종목별'].str.contains(keyword, case=False, na=False)].copy()

    if not filtered.empty:
        st.success(f"✅ '{keyword}' 관련 항목 {len(filtered)}건이 검색되었습니다.")

        # 연도 컬럼 찾기
        year_cols = [col for col in df.columns if '년' in col]

        # 수치에 단위 또는 % 기호 붙이기
        def format_value(x, 항목, 단위):
            if pd.isna(x):
                return "-"
            try:
                if "합격률" in 항목:
                    return f"{float(x):.1f}%"
                else:
                    return f"{int(x):,}{단위}"
            except:
                return str(x)

        for col in year_cols:
            filtered[col] = filtered.apply(lambda row: format_value(row[col], row['항목'], row['단위']), axis=1)

        # 표시 컬럼 구성
        display_cols = ['종목별', '항목'] + year_cols
        st.dataframe(filtered[display_cols].reset_index(drop=True))

    else:
        st.warning(f"❌ '{keyword}'에 해당하는 자격증 종목이 데이터에 없습니다.")
else:
    st.info("좌측 입력란에 자격증명을 입력해 주세요.")
    