# ============================================================
# 영화 데이터 그래프 도감 1 - 시간
# ------------------------------------------------------------
# - KOBIS 일별 박스오피스 10위권 데이터(1년치, 365일)를 가지고
#   "시간"에 따른 변화를 보여주는 그래프들을 모아두는 도감입니다.
# - 앞으로 그래프가 계속 늘어날 예정이라, 그래프마다 번호가 붙은
#   구역(section)으로 나눠뒀습니다. 새 그래프를 추가할 땐 그 구역
#   패턴을 그대로 복사해서 아래에 이어 붙이면 됩니다.
# - 초보자를 위해 곳곳에 한국어 주석을 달아두었습니다.
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# 0. 기본 설정
# ------------------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎞️",
    layout="wide",
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


# ------------------------------------------------------------
# 1. 데이터 불러오기
# ------------------------------------------------------------
# st.cache_data : 한 번 불러온 데이터는 저장해두고 재사용해서,
# 페이지를 새로고침해도 매번 인터넷에서 다시 받아오지 않습니다.
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_URL)

    # '날짜' 열은 20250901처럼 하이픈 없는 여덟 자리 숫자로 되어 있습니다.
    # 문자열로 바꾼 뒤 진짜 날짜(datetime) 타입으로 변환합니다.
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")

    return df


df = load_data()

# ------------------------------------------------------------
# 2. 화면 제목
# ------------------------------------------------------------
st.title("🎞️ 영화 데이터 그래프 도감 1 - 시간")
st.markdown(
    "KOBIS 일별 박스오피스 10위권 데이터(1년치)를 가지고, "
    "**시간이 지나면서 영화 데이터가 어떻게 변하는지** 보여주는 그래프 모음입니다."
)

st.divider()

# ============================================================
# 구역 1. 영화별 일별 관객수 변화
# ============================================================
st.header("① 영화별 일별 관객수 변화")
st.markdown("궁금한 영화를 골라서, 그 영화의 날짜별 하루 관객수(일관객) 흐름을 살펴보세요.")

# 영화명을 가나다순으로 정렬해서 드롭다운에 보여줍니다.
movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요",
    movie_list,
    key="movie_select_1",
)

# 선택한 영화의 데이터만 뽑아서, 날짜 순서대로 정렬합니다.
movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}' 날짜별 일관객 변화",
)

# 마우스를 올렸을 때 날짜와 관객수가 보기 좋게 나오도록 설정합니다.
fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)
fig1.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객(명)",
    hovermode="x unified",
)

st.plotly_chart(fig1, width="stretch", key="chart_1")

# '이 그래프로 알 수 있는 것' 문구를 적어 넣을 자리입니다.
# 그래프를 보고 알게 된 점을 한 문장으로 직접 적어보세요.
st.text_input(
    "📝 이 그래프로 알 수 있는 것",
    placeholder="예: 이 영화는 개봉 첫 주에 관객이 가장 많았고, 이후 빠르게 줄어들었다.",
    key="insight_1",
)

st.divider()

# ============================================================
# 구역 2. 일관객 합계 상위 5편 비교
# ============================================================
st.header("② 일관객 합계 상위 5편 비교")
st.markdown(
    "이 기간 동안 일관객(하루 관객수)을 모두 더했을 때 합계가 가장 큰 5편을 뽑아, "
    "날짜별 일관객을 한 그래프에 겹쳐서 보여줍니다. "
    "범례의 영화 이름을 클릭하면 그 영화의 선을 껐다 켰다 할 수 있어요."
)

# 영화별로 일관객을 모두 더해서, 합계가 큰 순서로 5편을 뽑습니다.
top5_totals = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)
top5_names = top5_totals.index.tolist()

# 상위 5편에 해당하는 데이터만 뽑아서, 날짜 순서대로 정렬합니다.
top5_df = df[df["영화명"].isin(top5_names)].sort_values("날짜")

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 상위 5편의 날짜별 일관객 비교",
    category_orders={"영화명": top5_names},  # 범례를 합계 순서대로 정렬
)

fig2.update_traces(
    hovertemplate="영화: %{fullData.name}<br>날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)
fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객(명)",
    hovermode="x unified",
    legend_title_text="영화명 (클릭해서 켜고 끄기)",
)

st.plotly_chart(fig2, width="stretch", key="chart_2")

st.text_input(
    "📝 이 그래프로 알 수 있는 것",
    placeholder="예: 상위 5편 중에서도 특정 영화가 특정 시기에 압도적으로 관객이 몰렸다.",
    key="insight_2",
)

st.divider()

# ============================================================
# 구역 3. (다음 그래프를 추가할 자리)
# ------------------------------------------------------------
# 새로운 그래프를 추가하려면 아래 패턴을 그대로 따라 하면 됩니다.
#
# st.header("③ 그래프 제목")
# st.markdown("그래프에 대한 간단한 설명")
# ... (데이터 가공 + plotly 그래프 그리기) ...
# st.plotly_chart(fig3, width="stretch", key="chart_3")
# st.text_input("📝 이 그래프로 알 수 있는 것", key="insight_3")
# st.divider()
# ============================================================
