import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import st_folium

st.set_page_config(page_title="서울 맛집 지도 🍰", page_icon="🍜", layout="wide")

# 로그인 되었는지 체크
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔐 먼저 로그인해주세요!")
    st.stop()

# ---------------------- CSS 파스텔 테마 ----------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
html, body, [class*="css"] {
    font-family: 'Jua', sans-serif;
    background-color: #fffdfa;
}
.card {
    padding: 15px;
    border-radius: 15px;
    background: #fff5f8;
    margin-bottom: 12px;
    border: 2px solid #ffd6e8;
}
.card:hover {
    background: #ffe9f1;
    transition: 0.3s;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- 상단 제목 ----------------------
st.title("🏙️ 광진구 감성 맛집 지도 🍰")
st.write("원하는 **음식 종류**와 **동(지역)** 을 선택해보세요! 지도와 카드에 귀엽게 표시해드립니다 🧸✨")

# ---------------------- 동/음식 필터 ----------------------
food_type = st.multiselect("🍴 음식 종류", ["한식", "중식", "양식"], default=["한식"])
dong = st.multiselect("📍 지역 (동)", ["자양동", "화양동", "광장동", "중곡동"], default=["자양동"])

st.write("---")

# ---------------------- 서울시 공공데이터 연동 ----------------------
st.subheader("🔗 서울시 맛집 데이터 불러오기 (선택)")

api_key = st.text_input("서울시 공공데이터 API Key (없으면 비워두세요)", type="password")

def load_seoul_data(api_key):
    try:
        url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/LocalRestaurantInfo/1/200/"
        response = requests.get(url)
        data = response.json()
        rows = data["LocalRestaurantInfo"]["row"]
        df = pd.DataFrame(rows)
        return df
    except:
        return None

if api_key:
    df = load_seoul_data(api_key)
    if df is not None:
        st.success("✅ 공공데이터 불러오기 성공!")
    else:
        st.error("❌ API Key 오류 또는 데이터 불러오기 실패. 샘플 데이터로 대체합니다.")
        api_key = ""

# ---------------------- 샘플 데이터 (API 없을 경우 사용) ----------------------
if not api_key:
    df = pd.DataFrame([
        ["자양칼국수", "한식", "자양동", 37.5315, 127.0858, "칼국수 / 수제비 맛집"],
        ["차이나문", "중식", "자양동", 37.5320, 127.0820, "정통 중국요리"],
        ["파스타리아", "양식", "화양동", 37.5423, 127.0708, "감성 파스타 맛집"]
    ], columns=["name", "type", "dong", "lat", "lon", "info"])

# ---------------------- 필터 적용 ----------------------
filtered = df[(df["type"].isin(food_type)) & (df["dong"].isin(dong))]

# ---------------------- 지도 ----------------------
st.subheader("🗺️ 지도에서 위치 보기")

map_center = [filtered.iloc[0]["lat"], filtered.iloc[0]["lon"]] if len(filtered) else [37.5385, 127.0825]
m = folium.Map(location=map_center, zoom_start=15)

for _, row in filtered.iterrows():
    folium.Marker([row["lat"], row["lon"]], popup=row["name"], tooltip=row["info"]).add_to(m)

st_folium(m, use_container_width=True, height=450)

st.write("---")

# ---------------------- 카드형 리스트 ----------------------
st.subheader("📋 맛집 리스트")

if len(filtered):
    for _, r in filtered.iterrows():
        st.markdown(f"""
        <div class="card">
        <h3>🍽️ {r['name']}</h3>
        <p>• 종류: {r['type']} <br>
        • 위치: {r['dong']} <br>
        • 소개: {r['info']}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("🧸 조건에 맞는 맛집이 없어요! 필터를 바꿔보세요 🌱")
