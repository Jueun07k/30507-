import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ✅ GitHub에서 CSV 파일 읽기
@st.cache_data
def load_data():
    # 따릉이 데이터
    bike_url = 'https://raw.githubusercontent.com/사용자명/저장소명/브랜치명/split_data/data_part_1.csv'
    bike_df = pd.read_csv(bike_url, encoding='cp949')

    # 날씨 데이터
    weather_url = 'https://raw.githubusercontent.com/사용자명/저장소명/브랜치명/weather_data.csv'
    weather_df = pd.read_csv(weather_url)

    # 날짜 전처리
    bike_df['대여일시'] = pd.to_datetime(bike_df['대여일시'])
    bike_df['날짜'] = bike_df['대여일시'].dt.date
    bike_df = bike_df.groupby('날짜').size().reset_index(name='대여건수')

    weather_df['날짜'] = pd.to_datetime(weather_df['날짜']).dt.date

    # 병합
    merged_df = pd.merge(bike_df, weather_df, on='날짜', how='inner')
    return merged_df

# 📊 데이터 불러오기
df = load_data()

st.title("날씨가 따릉이 이용에 미치는 영향")

# 🌦️ 날씨별 대여건수 평균 보기
if '강수량(mm)' in df.columns:
    df['비오는날'] = df['강수량(mm)'] > 0
else:
    df['비오는날'] = False

grouped = df.groupby('비오는날')['대여건수'].mean().reset_index()
grouped['비오는날'] = grouped['비오는날'].map({True: '비 오는 날', False: '맑은 날'})

st.subheader("비 오는 날 vs 맑은 날 평균 대여건수")
st.bar_chart(grouped.set_index('비오는날'))

# 📈 온도별 따릉이 이용량
if '평균기온(°C)' in df.columns:
    st.subheader("기온에 따른 따릉이 이용")
    fig, ax = plt.subplots()
    ax.scatter(df['평균기온(°C)'], df['대여건수'], alpha=0.5)
    ax.set_xlabel('평균기온(°C)')
    ax.set_ylabel('대여건수')
    st.pyplot(fig)

# 📅 날짜별 확인
st.subheader("날짜별 대여건수 및 날씨 정보")
st.dataframe(df.head(20))
