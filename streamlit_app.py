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

# 지도 생성
m = folium.Map(location=[35.1799817, 128.1076213], zoom_start=12)
marker_cluster = MarkerCluster().add_to(m)

# 조건 만족 시 마커 표시
if 선택_시도 and 선택_군구:
    filtered_df = df[(df["시도"] == 선택_시도) & (df["군구"] == 선택_군구)]

    for _, row in filtered_df.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=row.get("기종", "정보 없음")
        ).add_to(marker_cluster)

    st.success(f"{len(filtered_df)}개의 충전소가 표시되었습니다.")
    st.dataframe(filtered_df, height=200)
else:
    st.info("시도와 군구를 선택하면 충전소가 지도에 표시됩니다.")

# 지도 출력
folium_static(m)
