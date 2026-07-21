import streamlit as st
import plotly.graph_objects as go
from data_utils import load_data, country_selector

st.title("💰 1인당 GDP 찾기")

whr, gdp = load_data()

tab1, tab2 = st.tabs(["📈 국가별 추이", "🗺️ 세계 지도"])

with tab1:
    country = country_selector(gdp["Country"].unique(), "gdp")

    if country:
        df = gdp[gdp["Country"].str.lower() == country.lower()].sort_values("Year")
        if df.empty:
            st.warning(f"'{country}'에 대한 데이터를 찾을 수 없습니다. 국가명을 확인해주세요.")
        else:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["Year"], y=df["GDP"],
                mode="lines+markers", name=country,
                line=dict(color="#4ECDC4", width=3),
                marker=dict(size=6)
            ))
            fig.update_layout(
                title=f"{country} 1인당 GDP 추이",
                xaxis_title="연도", yaxis_title="1인당 GDP (current US$)",
                template="plotly_white", height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df[["Year", "GDP"]].reset_index(drop=True))

with tab2:
    years = sorted(gdp["Year"].unique(), reverse=True)
    selected_year = st.selectbox("연도 선택", years, key="map_year_gdp")

    df_year = gdp[gdp["Year"] == selected_year].dropna(subset=["GDP"])

    fig_map = go.Figure(data=go.Choropleth(
        locations=df_year["Country"],
        locationmode="country names",
        z=df_year["GDP"],
        text=df_year["Country"],
        colorscale=[[0, "#d73027"], [0.5, "#fee08b"], [1, "#1a9850"]],
        colorbar_title="1인당 GDP (US$)",
        marker_line_color="white",
        marker_line_width=0.5
    ))

    fig_map.update_layout(
        title=f"{selected_year}년 세계 1인당 GDP 지도",
        geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
        height=600
    )

    st.plotly_chart(fig_map, use_container_width=True)
    st.caption("초록색에 가까울수록 1인당 GDP가 높고, 빨간색에 가까울수록 낮습니다. (연도별 최대/최소 기준 상대 색상)")
