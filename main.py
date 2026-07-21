import streamlit as st


st.set_page_config(
    page_title="행복지수 & GDP 대시보드",
    page_icon="🌍",
    layout="wide"
)
st.title("🌎 세계 행복지수 & GDP 대시보드")
st.markdown("""
이 앱은 **World Happiness Report(세계행복보고서)**와 **World Bank GDP per capita** 데이터를
바탕으로 국가별 행복지수와 경제 수준을 비교, 탐색할 수 있는 대시보드입니다.
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.header("😊 행복지수 (Life Evaluation)")
    st.markdown("""
    행복지수는 각국 국민을 대상으로 한 설문에서 **본인의 삶을 0점(최악)부터
    10점(최고)까지 스스로 평가**하도록 한 **Cantril Ladder(사다리 척도)** 방식의
    3개년 이동평균 값입니다.

    이 지표는 GDP, 사회적 지지, 건강 기대수명, 자유, 관대함, 부패 인식 등
    6가지 요인으로 설명되며, Gallup World Poll 설문 결과를 기반으로 산출됩니다.
    """)
    st.caption("출처: World Happiness Report 2026, Wellbeing Research Centre, University of Oxford — https://worldhappiness.report")

with col2:
    st.header("💰 GDP per capita (1인당 GDP)")
    st.markdown("""
    1인당 GDP는 한 국가의 **국내총생산(GDP)을 인구수로 나눈 값**으로,
    국민 개개인의 평균적인 경제적 생산 수준을 나타내는 지표입니다.

    본 데이터는 현재 미국 달러(current US$) 기준이며, 1960년부터 최근 연도까지의
    시계열 데이터를 포함합니다.
    """)
    st.caption("출처: World Bank, World Development Indicators (NY.GDP.PCAP.CD) — https://data.worldbank.org")

st.divider()

st.info("👈 왼쪽 사이드바에서 하위 페이지(행복지수 찾기 / GDP per capita 찾기 / 두가지 비교하기 / 쌍둥이 국가 찾기)를 선택해 탐색해보세요.")
