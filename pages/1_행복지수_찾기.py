import streamlit as st
import plotly.graph_objects as go
from data_utils import load_data, country_selector

st.title("😊 행복지수 찾기")

whr, gdp = load_data()
country = country_selector(whr["Country"].unique(), "happy")

if country:
    df = whr[whr["Country"].str.lower() == country.lower()].sort_values("Year")
    if df.empty:
        st.warning(f"'{country}'에 대한 데이터를 찾을 수 없습니다. 국가명을 확인해주세요.")
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["Year"], y=df["Happiness"],
            mode="lines+markers", name=country,
            line=dict(color="#FF6B6B", width=3),
            marker=dict(size=8)
        ))
        fig.update_layout(
            title=f"{country} 행복지수 추이",
            xaxis_title="연도", yaxis_title="행복지수 (0-10)",
            template="plotly_white", height=500
        )
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df[["Year", "Happiness"]].reset_index(drop=True))
