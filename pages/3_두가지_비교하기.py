import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_utils import load_data, country_selector

st.set_page_config(
    page_title="행복지수 & GDP 비교하기",
    page_icon="📊",
    layout="wide"
)
st.title("📊 행복지수 & GDP 비교하기")

whr, gdp = load_data()
country = country_selector(set(whr["Country"]) & set(gdp["Country"]), "compare")

if country:
    dfh = whr[whr["Country"].str.lower() == country.lower()].sort_values("Year")
    dfg = gdp[gdp["Country"].str.lower() == country.lower()].sort_values("Year")

    if dfh.empty or dfg.empty:
        st.warning(f"'{country}'에 대한 데이터가 부족합니다. 국가명을 확인해주세요.")
    else:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(
            x=dfh["Year"], y=dfh["Happiness"], name="행복지수",
            line=dict(color="#FF6B6B", width=3), mode="lines+markers"
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=dfg["Year"], y=dfg["GDP"], name="GDP per capita",
            line=dict(color="#4ECDC4", width=3), mode="lines+markers"
        ), secondary_y=True)

        fig.update_layout(
            title=f"{country}: 행복지수 vs GDP per capita",
            template="plotly_white", height=550,
            legend=dict(orientation="h", y=1.1)
        )
        fig.update_yaxes(title_text="행복지수 (0-10)", secondary_y=False)
        fig.update_yaxes(title_text="GDP per capita (US$)", secondary_y=True)

        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("행복지수 데이터")
            st.dataframe(dfh[["Year", "Happiness"]].reset_index(drop=True))
        with col2:
            st.subheader("GDP per capita 데이터")
            st.dataframe(dfg[["Year", "GDP"]].reset_index(drop=True))
