import streamlit as st
import pandas as pd
from data_utils import load_data, country_selector

st.set_page_config(
    page_title="쌍둥이국가 찾기",
    page_icon="👯‍♀️",
    layout="wide"
)
st.title("👯‍♀️쌍둥이국가 찾기")
st.caption("선택한 국가와 행복지수·GDP per capita가 가장 비슷한 국가 3곳을 각각 찾아줍니다 (최신 연도 기준).")

whr, gdp = load_data()
common_countries = sorted(set(whr["Country"]) & set(gdp["Country"]))
country = country_selector(common_countries, "twin")

n_similar = st.slider("보여줄 유사 국가 수", 1, 10, 3)

if country:
    latest_whr_year = whr["Year"].max()
    latest_gdp_year = gdp["Year"].max()

    whr_latest = whr[whr["Year"] == latest_whr_year].dropna(subset=["Happiness"])
    gdp_latest = gdp[gdp["Year"] == latest_gdp_year].dropna(subset=["GDP"])

    target_h = whr_latest[whr_latest["Country"].str.lower() == country.lower()]
    target_g = gdp_latest[gdp_latest["Country"].str.lower() == country.lower()]

    if target_h.empty or target_g.empty:
        st.warning(f"'{country}'에 대한 최신 데이터가 부족합니다. 국가명을 확인해주세요.")
    else:
        target_happiness = target_h["Happiness"].values[0]
        target_gdp = target_g["GDP"].values[0]

        st.markdown(f"### 🎯 기준 국가: **{country}** ({latest_whr_year}년 기준)")
        col1, col2 = st.columns(2)
        col1.metric("행복지수", f"{target_happiness:.3f}")
        col2.metric("GDP per capita", f"${target_gdp:,.0f}")

        st.divider()

        whr_others = whr_latest[whr_latest["Country"].str.lower() != country.lower()].copy()
        whr_others["diff"] = (whr_others["Happiness"] - target_happiness).abs()
        similar_happiness = whr_others.nsmallest(n_similar, "diff")

        gdp_others = gdp_latest[gdp_latest["Country"].str.lower() != country.lower()].copy()
        gdp_others["diff"] = (gdp_others["GDP"] - target_gdp).abs()
        similar_gdp = gdp_others.nsmallest(n_similar, "diff")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("😊 행복지수 쌍둥이 국가")
            st.dataframe(
                similar_happiness[["Country", "Happiness"]]
                .rename(columns={"Happiness": "행복지수"})
                .reset_index(drop=True)
            )
        with col2:
            st.subheader("💰 GDP per capita 쌍둥이 국가")
            st.dataframe(
                similar_gdp[["Country", "GDP"]]
                .rename(columns={"GDP": "GDP per capita"})
                .reset_index(drop=True)
            )
