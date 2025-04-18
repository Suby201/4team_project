import streamlit as st  # Streamlit 라이브러리 import (웹 앱 개발)
import pandas as pd  # Pandas 라이브러리 import (데이터 조작 및 분석)

# streamlit run my_re.py

class CertificationSearchApp:
    """자격증 종목 통계 검색 앱 클래스"""
    def __init__(self):
        """
        초기화 메서드

        앱의 제목을 설정하고, 데이터를 로드하며, 사용자 입력 위젯을 생성합니다.
        """
        st.title("📘 자격증 종목 통계 검색")  # 앱 제목 표시
        st.markdown("자격증 **종목명**을 입력하면 연도별 응시 및 합격률 데이터를 확인할 수 있습니다.")  # 앱 설명 Markdown 텍스트 표시
        self.df = self._load_data()  # 데이터를 로드하여 클래스 변수에 저장
        # self.keyword = st.text_input("🔍 자격증(종목) 이름을 입력하세요:", placeholder="예: 정보처리")  # 사용자로부터 검색어를 입력받는 텍스트 입력 위젯 생성 (certi_search.py에서 처리)
        self.keyword = None # 검색 키워드를 초기화 (certi_search.py에서 값을 할당할 예정)
        self.certi_name = None # 선택된 자격증명을 저장할 변수 초기화

    @st.cache_data
    def _load_data(_self):  # 첫 번째 인자 이름에 밑줄 추가 (관례)
        """
        데이터를 로드하고 전처리하는 내부 메서드

        CSV 파일을 읽어들이고, 불필요한 컬럼을 제거하며, 컬럼명 공백을 정리합니다.
        @st.cache_data 데코레이터를 사용하여 함수 실행 결과를 캐싱하여 앱 성능을 향상시킵니다.

        Returns:
            pd.DataFrame: 로드 및 전처리된 데이터프레임
        """
        try:
            df = pd.read_csv("data\자격증.csv", encoding='cp949')  # CSV 파일 읽기 (인코딩 지정: CP949는 한글 Windows 환경에서 주로 사용)
            st.success("✅ 자격증 데이터 로드 성공!") # 데이터 로드 성공 메시지 표시
        except FileNotFoundError:
            st.error("❌ 자격증.csv 파일을 찾을 수 없습니다. 앱과 동일한 경로에 파일이 있는지 확인해주세요.")
            return pd.DataFrame() # 파일이 없으면 빈 데이터프레임 반환
        except Exception as e:
            st.error(f"❌ 데이터 로드 중 오류 발생: {e}")
            return pd.DataFrame() # 오류 발생 시 빈 데이터프레임 반환

        df = df.drop(columns=[col for col in df.columns if "Unnamed" in col], errors='ignore')  # "Unnamed"를 포함하는 불필요한 컬럼 제거 (errors='ignore'는 해당 컬럼이 없어도 오류를 발생시키지 않음)
        df.columns = df.columns.str.strip()  # 컬럼명 좌우 공백 제거
        return df  # 전처리된 데이터프레임 반환

    def _format_value(self, x, 항목, 단위):
        """
        수치 데이터에 단위 또는 % 기호를 붙이는 내부 메서드

        데이터의 '항목'에 따라 숫자 값에 적절한 단위(%, 명 등)를 추가합니다.
        결측값은 '-'로 표시하고, 숫자 포맷팅 중 오류가 발생하면 원래 값을 문자열로 반환합니다.

        Args:
            x: 포맷팅할 값
            항목 (str): 데이터의 항목 (예: '합격률', '응시자 수')
            단위 (str): 데이터의 단위 (예: '%', ' 명')

        Returns:
            str: 포맷팅된 문자열
        """
        if pd.isna(x):  # 값이 NaN(결측값)인 경우
            return "-"
        try:
            if "합격률" in 항목:  # 항목이 '합격률'을 포함하는 경우
                return f"{float(x):.1f}%"  # 부동 소수점 형태로 변환하여 소수점 한 자리까지 표시 후 '%' 추가
            else:  # 그 외의 경우 (응시자 수, 합격자 수 등)
                return f"{int(x):,}{단위}"  # 정수 형태로 변환하여 천 단위마다 쉼표를 찍고 단위 추가
        except:  # 숫자 포맷팅 중 오류가 발생한 경우
            return str(x)  # 원래 값을 문자열로 반환

    def display_results(self):
        """검색 결과를 처리하고 표시하는 메서드"""
        if not self.df.empty: # 데이터프레임이 비어있지 않은 경우에만 검색 수행
            if self.keyword:  # 사용자가 검색어를 입력한 경우 (certi_search.py에서 할당)
                filtered = self.df[self.df['종목별'].str.contains(self.keyword, case=False, na=False)].copy()
                filtered = filtered.sort_values(by='종목별',ascending=True)
                # 데이터프레임의 '종목별' 컬럼에서 검색어를 포함하는 행을 찾습니다 (대소문자 구분 없이, NaN 값은 False 처리).
                # .copy()를 사용하여 원본 데이터프레임 변경을 방지합니다.
                # 검색 결과를 '종목별' 컬럼을 기준으로 오름차순 정렬합니다.

                if not filtered.empty:  # 검색 결과가 있는 경우
                    # st.success(f"✅ '{self.keyword}' 관련 항목 {len(filtered)}건이 검색되었습니다.")
                    result_value = filtered['종목별'].unique() # 검색된 종목의 고유한 값들을 추출
                    self.certi_name = st.selectbox("자격증 선택",result_value) # 추출된 고유한 종목명을 Selectbox 형태로 표시하고, 선택된 값을 self.certi_name에 저장

                else:  # 검색 결과가 없는 경우
                    st.warning(f"❌ '{self.keyword}'에 해당하는 자격증 종목이 데이터에 없습니다.")  # 경고 메시지 표시
            else:  # 사용자가 검색어를 입력하지 않은 경우 (certi_search.py에서 초기 상태)
                st.info("왼쪽 검색창에 자격증명을 입력해 주세요.")  # 안내 메시지 표시
        else:
            st.warning("⚠️ 데이터를 불러오는 데 실패했습니다. 파일 경로 및 내용을 확인해주세요.")


if __name__ == '__main__':
    app = CertificationSearchApp()  # CertificationSearchApp 클래스의 인스턴스 생성
    app.display_results()  # 검색 결과를 표시하는 메서드 호출