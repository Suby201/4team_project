from dotenv import load_dotenv
import streamlit as st
import requests
import os

# streamlit run app_re.py

load_dotenv()

class BookSearchApp:
    """자격증 관련 책을 검색하여 보여주는 Streamlit 앱 클래스"""
    def __init__(self):
        """초기화 메서드"""
        # 네이버 API 키 로드
        self.CLIENT_ID = os.getenv("CID")
        self.CLIENT_SECRET = os.getenv("CSEC")

        # UI 설정
        st.title("📚 자격증 관련 책 검색기")
        st.write("검색창에 자격증 이름을 입력하면 관련 서적을 카드 형태로 보여드려요!")

        # 사용자 입력 위젯 생성
        # self.query = st.text_input("🔍 자격증 이름을 입력하세요", placeholder="정보처리기사")
        self.display_num = st.slider("📚 표시할 책 개수 선택", 1, 10, 5)
        self.filter_publisher = st.text_input("출판사 필터 (선택 사항)")

        # 검색 버튼
        self.search_button = st.button("검색하기", on_click=self._set_search_button_clicked)

    def _set_search_button_clicked(self):
        st.session_state['search_button_clicked'] = True

    def search_books(self, query, max_results=100):
        """
        네이버 책 검색 API를 여러 번 호출하여 최대 max_results개의 책 정보를 가져오는 메서드

        Args:
            query (str): 검색어 (자격증 이름)
            max_results (int): 가져올 최대 검색 결과 수 (기본값: 100)

        Returns:
            list: 검색된 책 정보 리스트 (각 책 정보는 딕셔너리 형태), API 오류 발생 시 빈 리스트 반환
        """
        url = "https://openapi.naver.com/v1/search/book.json"
        headers = {
            "X-Naver-Client-Id": self.CLIENT_ID,
            "X-Naver-Client-Secret": self.CLIENT_SECRET
        }
        all_books = []
        start = 1
        display_count = 10  # 한 번에 가져올 책 개수 (최대 100)

        with st.spinner("책 정보를 가져오는 중..."):
            while len(all_books) < max_results:
                params = {
                    "query": query,
                    "display": min(display_count, max_results - len(all_books)),
                    "start": start
                }
                response = requests.get(url, headers=headers, params=params)

                if response.status_code == 200:
                    items = response.json().get('items', [])
                    if not items:
                        break  # 더 이상 결과가 없으면 종료
                    all_books.extend(items)
                    start += display_count
                else:
                    st.error(f"API 오류 발생 (상태 코드: {response.status_code})")
                    return []

        return all_books

    def display_book_results(self):
        """검색된 책 정보를 필터링, 정렬 후 카드 형태로 화면에 표시하는 메서드"""
        all_books = self.search_books(self.query, max_results=100)  # 최대 100개 검색 결과 가져오기

        if not all_books:
            st.info("검색 결과가 없어요 😥")
            return

        filtered_books = all_books
        if self.filter_publisher:
            filtered_books = [book for book in filtered_books if self.filter_publisher.lower() in book['publisher'].lower()]

        if not filtered_books:
            st.info(f"'{self.filter_publisher}' 출판사의 검색 결과가 없어요 😥")
            return

        filtering = st.selectbox("정렬 기준", ['기본', '낮은 가격 순', '높은 가격 순'])
        if filtering == '낮은 가격 순':
            filtered_books = sorted(filtered_books, key=lambda x: int(x.get('discount', x.get('price', '0')).replace(',', '') or 0))
        elif filtering == '높은 가격 순':
            filtered_books = sorted(filtered_books, key=lambda x: int(x.get('discount', x.get('price', '0')).replace(',', '') or 0), reverse=True)

        displayed_books = filtered_books[:self.display_num]  # 선택한 개수만큼만 표시

        if displayed_books:
            for book in displayed_books:
                with st.container():
                    cols = st.columns([1, 3])
                    with cols[0]:
                        st.image(book['image'], width=100)
                    with cols[1]:
                        st.markdown(f"### {book['title']}")
                        st.write(f"**저자**: {book['author']}")
                        st.write(f"**출판사**: {book['publisher']}")
                        st.write(f"**정가**: {book.get('price', '정보 없음')}원")
                        st.write(f"**할인가**: {book.get('discount', book.get('price', '정보 없음'))}원")
                        st.markdown(f"[📖 책 보러가기]({book['link']})")
                    st.divider()
        else:
            st.info("표시할 책이 없어요 😥")

if __name__ == "__main__":
    app = BookSearchApp()
    if st.session_state.get('search_button_clicked'):
        app.display_book_results()