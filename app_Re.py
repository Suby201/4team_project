from dotenv import load_dotenv  # .env 파일에서 환경 변수를 로드하는 라이브러리
import streamlit as st  # Streamlit 라이브러리 import (웹 앱 개발)
import requests  # HTTP 요청을 보내는 라이브러리
import os  # 운영체제 관련 기능을 제공하는 라이브러리

# streamlit run app_re.py

load_dotenv()  # .env 파일에서 환경 변수를 로드합니다. (네이버 API 키 등을 읽어옴)

class BookSearchApp:
    """자격증 관련 책을 검색하여 보여주는 Streamlit 앱 클래스"""
    def __init__(self):
        """초기화 메서드"""
        # 네이버 API 키 로드
        self.CLIENT_ID = os.getenv("CID")  # 환경 변수 "CID"에서 네이버 Client ID를 가져와 저장
        self.CLIENT_SECRET = os.getenv("CSEC")  # 환경 변수 "CSEC"에서 네이버 Client Secret을 가져와 저장

        # UI 설정
        st.title("📚 자격증 관련 책 검색기")  # 앱의 제목을 표시
        st.write("검색창에 자격증 이름을 입력하면 관련 서적을 카드 형태로 보여드려요!")  # 앱에 대한 간단한 설명을 화면에 표시

        # 사용자 입력 위젯 생성
        self.display_num = st.slider("📚 표시할 책 개수 선택", 1, 10, 5)  # 표시할 책의 개수를 선택하는 슬라이더 위젯 생성 (최소 1개, 최대 10개, 기본값 5개)
        self.filter_publisher = st.text_input("출판사 필터 (선택 사항)")  # 출판사로 검색 결과를 필터링할 수 있는 텍스트 입력 위젯 생성

        # 검색 버튼
        self.search_button = st.button("검색하기", on_click=self._set_search_button_clicked)  # "검색하기" 버튼 생성, 클릭 시 _set_search_button_clicked 메서드 호출

    def _set_search_button_clicked(self):
        """검색 버튼 클릭 상태를 세션 상태에 저장하는 내부 메서드"""
        st.session_state['search_button_clicked'] = True  # 'search_button_clicked' 키로 True 값을 Streamlit 세션 상태에 저장
                                                        # 세션 상태는 앱이 다시 실행되어도 값을 유지하는 공간입니다.

    def search_books(self, query, max_results=100):
        """
        네이버 책 검색 API를 여러 번 호출하여 최대 max_results개의 책 정보를 가져오는 메서드

        Args:
            query (str): 검색어 (자격증 이름)
            max_results (int): 가져올 최대 검색 결과 수 (기본값: 100)

        Returns:
            list: 검색된 책 정보 리스트 (각 책 정보는 딕셔너리 형태), API 오류 발생 시 빈 리스트 반환
        """
        url = "https://openapi.naver.com/v1/search/book.json"  # 네이버 책 검색 API 엔드포인트 URL
        headers = {
            "X-Naver-Client-Id": self.CLIENT_ID,  # 네이버 API Client ID를 요청 헤더에 포함
            "X-Naver-Client-Secret": self.CLIENT_SECRET  # 네이버 API Client Secret을 요청 헤더에 포함
        }
        all_books = []  # 검색된 모든 책 정보를 저장할 빈 리스트 초기화
        start = 1  # API 검색 시작 위치 (페이지) 초기화
        display_count = 10  # 한 번의 API 호출로 가져올 책 개수 (최대 100)

        with st.spinner("책 정보를 가져오는 중..."):  # Streamlit의 로딩 스피너를 표시하며 내부 코드 실행
            while len(all_books) < max_results:  # 가져온 책의 수가 최대 결과 수보다 작을 동안 반복
                params = {
                    "query": query,  # 검색어 파라미터
                    "display": min(display_count, max_results - len(all_books)),  # 한 번에 가져올 개수 설정 (남은 결과 수와 display_count 중 작은 값)
                    "start": start  # 검색 시작 위치 파라미터
                }
                response = requests.get(url, headers=headers, params=params)  # 네이버 책 검색 API에 GET 요청을 보냄

                if response.status_code == 200:  # HTTP 상태 코드가 200 (성공)인 경우
                    items = response.json().get('items', [])  # JSON 응답에서 'items' 키의 값(책 정보 리스트)을 가져옴, 없으면 빈 리스트 반환
                    if not items:  # 가져온 책 정보 리스트가 비어있으면 (더 이상 검색 결과가 없으면)
                        break  # while 루프 종료
                    all_books.extend(items)  # 가져온 책 정보 리스트를 전체 책 리스트에 추가
                    start += display_count  # 다음 API 호출을 위한 시작 위치 증가
                else:  # HTTP 상태 코드가 200이 아닌 경우 (API 오류 발생)
                    st.error(f"API 오류 발생 (상태 코드: {response.status_code})")  # 오류 메시지 표시
                    return []  # 빈 리스트 반환

        return all_books  # 검색된 모든 책 정보가 담긴 리스트 반환

    def display_book_results(self):
        """검색된 책 정보를 필터링, 정렬 후 카드 형태로 화면에 표시하는 메서드"""
        all_books = self.search_books(self.query, max_results=100)  # 최대 100개의 검색 결과 가져오기

        if not all_books:  # 검색 결과가 없는 경우
            st.info("검색 결과가 없어요 😥")  # 정보 메시지 표시
            return

        filtered_books = all_books  # 초기 필터링된 책 리스트는 모든 검색 결과
        if self.filter_publisher:  # 출판사 필터가 입력된 경우
            filtered_books = [book for book in filtered_books if self.filter_publisher.lower() in book['publisher'].lower()]
            # 필터링된 책 리스트를 업데이트: 입력된 출판사를 (대소문자 구분 없이) 포함하는 책만 남김

        if not filtered_books:  # 필터링 후 책이 없는 경우
            st.info(f"'{self.filter_publisher}' 출판사의 검색 결과가 없어요 😥")  # 해당 출판사의 검색 결과가 없다는 정보 메시지 표시
            return

        filtering = st.selectbox("정렬 기준", ['기본', '낮은 가격 순', '높은 가격 순'])  # 정렬 기준을 선택하는 Selectbox 위젯 생성
        if filtering == '낮은 가격 순':
            filtered_books = sorted(filtered_books, key=lambda x: int(x.get('discount', x.get('price', '0')).replace(',', '') or 0))
            # 필터링된 책을 'discount' (할인가) 또는 'price' (정가)를 기준으로 낮은 가격 순으로 정렬
            # 가격 정보가 없거나 숫자로 변환할 수 없으면 0으로 처리
        elif filtering == '높은 가격 순':
            filtered_books = sorted(filtered_books, key=lambda x: int(x.get('discount', x.get('price', '0')).replace(',', '') or 0), reverse=True)
            # 필터링된 책을 'discount' (할인가) 또는 'price' (정가)를 기준으로 높은 가격 순으로 정렬
            # 가격 정보가 없거나 숫자로 변환할 수 없으면 0으로 처리, reverse=True로 내림차순 정렬

        displayed_books = filtered_books[:self.display_num]  # 선택한 개수만큼만 필터링된 책 리스트에서 슬라이싱하여 가져옴

        if displayed_books:  # 표시할 책이 있는 경우
            for book in displayed_books:  # 각 책에 대해 반복
                with st.container():  # Streamlit 컨테이너 생성 (책 정보 그룹화)
                    cols = st.columns([1, 3])  # 1:3 비율로 두 개의 컬럼 생성 (이미지, 텍스트 정보)
                    with cols[0]:  # 첫 번째 컬럼 (이미지 영역)
                        st.image(book['image'], width=100)  # 책 이미지 표시 (최대 너비 100px)
                    with cols[1]:  # 두 번째 컬럼 (텍스트 정보 영역)
                        st.markdown(f"### {book['title']}")  # 책 제목을 Markdown 형식의 h3 태그로 표시
                        st.write(f"**저자**: {book['author']}")  # 저자 정보 표시 (볼드체 적용)
                        st.write(f"**출판사**: {book['publisher']}")  # 출판사 정보 표시
                        st.write(f"**정가**: {book.get('price', '정보 없음')}원")  # 정가 정보 표시 (없으면 '정보 없음')
                        st.write(f"**할인가**: {book.get('discount', book.get('price', '정보 없음'))}원")  # 할인가 정보 표시 (없으면 정가 또는 '정보 없음')
                        st.markdown(f"[📖 책 보러가기]({book['link']})")  # 책 상세 페이지 링크를 Markdown 형식으로 표시
                    st.divider()  # 각 책 정보 사이에 구분선 추가
        else:  # 표시할 책이 없는 경우
            st.info("표시할 책이 없어요 😥")  # 정보 메시지 표시

if __name__ == "__main__":
    app = BookSearchApp()  # BookSearchApp 클래스의 인스턴스 생성
    if st.session_state.get('search_button_clicked'):  # 세션 상태에 'search_button_clicked' 키가 있고 값이 True이면 (검색 버튼이 눌렸으면)
        app.display_book_results()  # 책 검색 결과 표시 메서드 호출