import streamlit as st
import plotly.graph_objects as go
from data_utils import load_data, country_selector

st.set_page_config(
    page_title="행복지수 찾기",
    page_icon="😊",
    layout="wide"
)
st.title("😊 행복지수 찾기")
whr, gdp = load_data()

tab1, tab2 = st.tabs(["📈 국가별 추이", "🗺️ 세계 지도"])

with tab1:
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

with tab2:
    years = sorted(whr["Year"].unique(), reverse=True)
    selected_year = st.selectbox("연도 선택", years, key="map_year_happy")

    df_year = whr[whr["Year"] == selected_year].dropna(subset=["Happiness"])

    fig_map = go.Figure(data=go.Choropleth(
        locations=df_year["Country"],
        locationmode="country names",
        z=df_year["Happiness"],
        text=df_year["Country"],
        colorscale=[[0, "#d73027"], [0.5, "#fee08b"], [1, "#1a9850"]],
        colorbar_title="행복지수",
        zmin=whr["Happiness"].min(),
        zmax=whr["Happiness"].max(),
        marker_line_color="white",
        marker_line_width=0.5
    ))

    fig_map.update_layout(
        title=f"{selected_year}년 세계 행복지수 지도",
        geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
        height=600
    )

    st.plotly_chart(fig_map, use_container_width=True)
    st.caption("초록색에 가까울수록 행복지수가 높고, 빨간색에 가까울수록 낮습니다.")
