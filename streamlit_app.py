import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster
import pandas as pd

st.title("전기차 충전소 지도")

# CSV 불러오기
df = pd.read_csv("충전소 위치.csv", encoding='utf-8')
df.columns = df.columns.str.strip()
df["위도"] = pd.to_numeric(df["위도"], errors="coerce")
df["경도"] = pd.to_numeric(df["경도"], errors="coerce")
df = df.dropna(subset=["위도", "경도"])
df[["lat", "lon"]] = df[["위도", "경도"]]

# 시도 선택
시도_목록 = sorted(df["시도"].dropna().unique())
선택_시도 = st.selectbox("시도 선택", [""] + 시도_목록, format_func=lambda x: "선택 안 함" if x == "" else x)

# 군구 선택
if 선택_시도:
    군구_목록 = sorted(df[df["시도"] == 선택_시도]["군구"].dropna().unique())
    선택_군구 = st.selectbox("군/구 선택", [""] + 군구_목록, format_func=lambda x: "선택 안 함" if x == "" else x)
else:
    선택_군구 = ""

# 필터링된 데이터프레임
if 선택_시도 and 선택_군구:
    filtered_df = df[(df["시도"] == 선택_시도) & (df["군구"] == 선택_군구)]
else:
    filtered_df = pd.DataFrame()

# 지도 중심 설정 (선택된 지역이 있다면 그 중심으로 이동)
if not filtered_df.empty:
    지도_중심 = [filtered_df["lat"].mean(), filtered_df["lon"].mean()]
else:
    지도_중심 = [35.1799817, 128.1076213]  # 기본값

# 지도 생성
m = folium.Map(location=지도_중심, zoom_start=13)
marker_cluster = MarkerCluster().add_to(m)

# 마커 표시
for _, row in filtered_df.iterrows():
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=row.get("기종", "정보 없음")
    ).add_to(marker_cluster)

# 지도 출력
folium_static(m)

# 데이터 출력
if not filtered_df.empty:
    st.success(f"{len(filtered_df)}개의 충전소가 표시되었습니다.")
    st.dataframe(filtered_df[["주소", "충전소명", "시설구분", "기종"]], height=200)
else:
    st.info("시도와 군구를 선택하면 충전소가 지도에 표시됩니다.")
