import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    whr = pd.read_csv("data/whr_long.csv")
    gdp = pd.read_csv("data/gdp_long.csv")
    return whr, gdp

def country_selector(countries, key_prefix):
    st.markdown("**국가 선택 또는 직접 입력**")
    mode = st.radio("입력 방식", ["목록에서 선택", "직접 입력"], horizontal=True, key=f"{key_prefix}_mode")
    if mode == "목록에서 선택":
        country = st.selectbox("국가 선택", sorted(countries), key=f"{key_prefix}_select")
    else:
        country = st.text_input("국가명 입력 (영문, 예: South Korea)", key=f"{key_prefix}_text")
    return country
