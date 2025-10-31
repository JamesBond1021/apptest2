import streamlit as st

st.set_page_config(page_title="서울 맛집&관광 추천 🍰", page_icon="🏙️", layout="centered")

# 회원 데이터 저장용
if "users" not in st.session_state:
    st.session_state.users = {}   # {아이디: 비밀번호}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# CSS + 애니메이션 효과
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

html, body, [class*="css"]  {
    font-family: 'Jua', sans-serif;
}

.wave {
  animation: waveAnim 2s infinite;
}

@keyframes waveAnim {
  0% {transform: rotate(0deg);}
  50% {transform: rotate(10deg);}
  100% {transform: rotate(0deg);}
}
</style>
""", unsafe_allow_html=True)


# ------------------- 메인 화면 UI -------------------
st.markdown("<h1 style='text-align:center;'>🏙️ 서울 구경 가자! 🍡</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>맛집도 찾고 🎀 관광지도 찾아보는 귀여운 웹앱이에요 💗</p>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;' class='wave'>( ๑>ᴗ<๑ )و ✨</h2>", unsafe_allow_html=True)


# ------------------- 로그인 / 회원가입 구역 -------------------
tab_login, tab_signup = st.tabs(["🔑 로그인", "🌱 회원가입"])

# 로그인 탭
with tab_login:
    st.subheader("🔑 로그인하기")

    login_id = st.text_input("아이디")
    login_pw = st.text_input("비밀번호", type="password")

    if st.button("로그인 🚪"):
        if login_id in st.session_state.users and st.session_state.users[login_id] == login_pw:
            st.session_state.logged_in = True
            st.success("로그인 성공! 🌟 곧 이동합니다...")
            st.switch_page("pages/main.py")
        else:
            st.error("아이디 또는 비밀번호가 틀렸어요 😢")


# 회원가입 탭
with tab_signup:
    st.subheader("🌱 회원가입하기")
    
    new_id = st.text_input("새 아이디")
    new_pw = st.text_input("새 비밀번호", type="password")
    new_pw_check = st.text_input("비밀번호 확인", type="password")

    if st.button("회원가입 완료 🎉"):
        if new_id in st.session_state.users:
            st.error("이미 존재하는 아이디예요! 😭")
        elif new_pw != new_pw_check:
            st.error("비밀번호가 일치하지 않아요 ❌")
        elif new_id == "":
            st.error("아이디를 입력해 주세요!")
        else:
            st.session_state.users[new_id] = new_pw
            st.success("회원가입 성공! ✨ 이제 로그인 탭에서 로그인해주세요 😊")


st.markdown("---")
st.markdown("<p style='text-align:center; font-size:15px;'>Made with 💗 for Teenagers</p>", unsafe_allow_html=True)
