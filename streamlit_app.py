import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster
import pandas as pd

st.title("충전소")

# CSV 로딩
df = pd.read_csv("충전소 위치.csv", encoding='utf-8')

# 컬럼명 공백 제거
df.columns = df.columns.str.strip()

# 위도, 경도 숫자로 변환 (문자열 등 비정상값 NaN으로 처리)
df["위도"] = pd.to_numeric(df["위도"], errors="coerce")
df["경도"] = pd.to_numeric(df["경도"], errors="coerce")

# NaN 제거
df = df.dropna(subset=["위도", "경도"])

# lat/lon 컬럼 만들기
df[["lat", "lon"]] = df[["위도", "경도"]]

# 지도 생성
m = folium.Map(location=[35.1799817, 128.1076213], zoom_start=11)
marker_cluster = MarkerCluster().add_to(m)

# 상위 100개만 표시 (테스트용)
sample_df = df.head(100)

for _, row in sample_df.iterrows():
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=row.get("기종", "정보 없음")
    ).add_to(marker_cluster)

# 마커 추가
#for _, row in df.iterrows():
#    folium.CircleMarker(
#        location=[row["lat"], row["lon"]],
#        radius=5,
#        color='blue',
#        fill=True,
#        fill_opacity=0.7,
#       popup=row.get("기종", "정보 없음")
#    ).add_to(marker_cluster)

# 지도 출력
folium_static(m)

# 데이터프레임 확인
st.dataframe(df, height=200)
