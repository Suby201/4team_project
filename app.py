import streamlit as st
import requests

# 네이버 API 키
CLIENT_ID = "eKGtxOEE_rVXoZmAtDhW"
CLIENT_SECRET = "eWY9QdZ7ti"

# 책 검색 함수
def search_books(query, display=5):
    url = "https://openapi.naver.com/v1/search/book.json"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    params = {
        "query": query,
        "display": display
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        st.error("API 오류 발생")
        return []

# UI 시작
st.set_page_config(page_title="자격증 책 검색기", page_icon="📚")
st.title("📚 자격증 관련 책 검색기")
st.write("검색창에 자격증 이름을 입력하면 관련 서적을 카드 형태로 보여드려요!")

query = st.text_input("🔍 자격증 이름을 입력하세요", "정보처리기사")
display_num = st.slider("📚 책 개수 선택", 1, 10, 5)

if st.button("검색하기"):
    books = search_books(query, display_num)

    if books:
        for book in books:
            # 카드 하나씩 표시
            with st.container():
                cols = st.columns([1, 3])
                with cols[0]:
                    st.image(book['image'], width=100)
                with cols[1]:
                    st.markdown(f"### {book['title']}")
                    st.write(f"**저자**: {book['author']}")
                    st.write(f"**출판사**: {book['publisher']}")
                    st.write(f"**정가**: {book.get('price', '정보 없음')}원")
                    st.write(f"**할인가**: {book.get('discount', '정보 없음')}원")
                    st.markdown(f"[📖 책 보러가기]({book['link']})")
            st.divider()
    else:
        st.info("검색 결과가 없어요 😥")
