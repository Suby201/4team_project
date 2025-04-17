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
        st.set_page_config(page_title="자격증 책 검색기", page_icon="📚")
        st.title("📚 자격증 관련 책 검색기")
        st.write("검색창에 자격증 이름을 입력하면 관련 서적을 카드 형태로 보여드려요!")

        # 사용자 입력 위젯 생성
        self.query = st.text_input("🔍 자격증 이름을 입력하세요", "정보처리기사")
        self.display_num = st.slider("📚 책 개수 선택", 1, 10, 5)

        # 검색 버튼
        if st.button("검색하기"):
            self.display_book_results()

    def search_books(self, query, display=5):
        """
        네이버 책 검색 API를 호출하여 책 정보를 가져오는 메서드

        Args:
            query (str): 검색어 (자격증 이름)
            display (int): 검색 결과에 표시할 책의 개수 (기본값: 5)

        Returns:
            list: 검색된 책 정보 리스트 (각 책 정보는 딕셔너리 형태), API 오류 발생 시 빈 리스트 반환
        """
        url = "https://openapi.naver.com/v1/search/book.json"
        headers = {
            "X-Naver-Client-Id": self.CLIENT_ID,
            "X-Naver-Client-Secret": self.CLIENT_SECRET
        }
        params = {
            "query": query,
            "display": display
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json().get('items', [])  # 검색 결과가 있으면 'items' 리스트 반환, 없으면 빈 리스트 반환
        else:
            st.error("API 오류 발생")
            return []

    def display_book_results(self):
        """검색된 책 정보를 카드 형태로 화면에 표시하는 메서드"""
        books = self.search_books(self.query, self.display_num)

        if books:
            for book in books:
                # 카드 하나씩 표시
                with st.container():
                    cols = st.columns([1, 3])  # 이미지와 정보 영역을 1:3 비율로 나누는 컬럼 생성
                    with cols[0]:
                        st.image(book['image'], width=100)  # 책 이미지 표시 (최대 너비 100px)
                    with cols[1]:
                        st.markdown(f"### {book['title']}")  # 책 제목을 h3 태그로 강조
                        st.write(f"**저자**: {book['author']}")  # 저자 정보 표시 (볼드체)
                        st.write(f"**출판사**: {book['publisher']}")  # 출판사 정보 표시
                        st.write(f"**정가**: {book.get('price', '정보 없음')}원")  # 정가 정보 표시 (없으면 '정보 없음' 출력)
                        st.write(f"**할인가**: {book.get('discount', '정보 없음')}원")  # 할인가 정보 표시 (없으면 '정보 없음' 출력)
                        st.markdown(f"[📖 책 보러가기]({book['link']})")  # 책 링크를 Markdown 형태로 표시
                st.divider()  # 각 책 카드 사이에 구분선 추가
        else:
            st.info("검색 결과가 없어요 😥")  # 검색 결과가 없을 때 안내 메시지 표시

if __name__ == "__main__":
    app = BookSearchApp()  # BookSearchApp 클래스의 인스턴스 생성