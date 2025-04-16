import streamlit as st
import requests

# 네이버 API 키 넣기 (네이버 개발자 센터에서 발급받아야 함)
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
        st.error("책 정보를 가져오는 데 문제가 생겼어요 😥")
        return []

# Streamlit 웹페이지 시작
st.title("📚 자격증 책 검색기")
st.write("자격증 이름을 검색하면 관련 책을 보여드릴게요!")

# 사용자 입력 받기
query = st.text_input("검색할 자격증을 입력하세요", "정보처리기사")
display_num = st.slider("보고 싶은 책 개수", 1, 10, 5)

# 검색 버튼 누르면 결과 보여줌
if st.button("검색하기"):
    books = search_books(query, display_num)
    if books:
        for book in books:
            st.subheader(book['title'])
            st.write(f"저자: {book['author']}")
            st.write(f"출판사: {book['publisher']}")
            st.image(book['image'], width=100)
            st.markdown(f"[책 보러가기]({book['link']})")
            st.write("---")
    else:
        st.info("책을 찾을 수 없어요 🧐")