from __future__ import annotations

import json
from html import escape
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "cases.csv"
META_PATH = ROOT / "data" / "meta.json"
HERO_IMAGE_B64_PATH = ROOT / "assets" / "jangbogo-hero-v2.b64"

NAVY = "#06121F"
NAVY_2 = "#0A2035"
PANEL = "#0C2A43"
MINT = "#71D7C5"
GOLD = "#F5C451"
ICE = "#EAF2F8"
MUTED = "#91A8B8"
RED = "#FF7A6E"


st.set_page_config(
    page_title="SUBMARINE HW",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data() -> tuple[pd.DataFrame, dict]:
    data = pd.read_csv(DATA_PATH)
    with META_PATH.open("r", encoding="utf-8") as handle:
        meta = json.load(handle)
    data["opened_year"] = pd.to_numeric(data["opened_year"], errors="coerce")
    data["length_m"] = pd.to_numeric(data["length_m"], errors="coerce")
    data["relevance"] = pd.to_numeric(data["relevance"], errors="coerce")
    data["priority"] = pd.to_numeric(data["priority"], errors="coerce")
    return data, meta


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap');

        :root {{
            --navy: {NAVY}; --navy2: {NAVY_2}; --panel: {PANEL};
            --mint: {MINT}; --gold: {GOLD}; --ice: {ICE}; --muted: {MUTED};
        }}
        html, body, [class*="css"] {{ font-family: 'IBM Plex Sans KR', sans-serif; }}
        .stApp {{
            background:
                radial-gradient(circle at 88% 4%, rgba(24, 110, 133, .20), transparent 28rem),
                linear-gradient(180deg, #06121F 0%, #071827 55%, #06121F 100%);
            color: var(--ice);
        }}
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #071522 0%, #091D2E 100%);
            border-right: 1px solid rgba(113, 215, 197, .18);
        }}
        [data-testid="stSidebar"] hr {{ border-color: rgba(145,168,184,.18); }}
        [data-testid="stHeader"] {{ background: transparent; }}
        .block-container {{ padding-top: 1.6rem; padding-bottom: 4rem; max-width: 1500px; }}

        .brand {{ display:flex; gap:.8rem; align-items:center; margin: .4rem 0 1.5rem; }}
        .brand-mark {{
            width:42px; height:42px; border-radius:50%; display:grid; place-items:center;
            border:1px solid rgba(113,215,197,.55); color:var(--mint);
            box-shadow:0 0 24px rgba(113,215,197,.12); font-family:'IBM Plex Mono';
        }}
        .brand-title {{ font-weight:700; letter-spacing:.14em; font-size:1rem; color:var(--ice); }}
        .brand-sub {{ color:var(--muted); font-size:.68rem; letter-spacing:.08em; margin-top:.2rem; }}

        .hero {{
            position:relative; overflow:hidden; min-height:315px; border-radius:20px;
            padding:2.1rem 2.3rem; margin-bottom:1rem;
            border:1px solid rgba(113,215,197,.22);
            background:linear-gradient(120deg, rgba(11,44,69,.98), rgba(7,27,43,.94));
            box-shadow:0 20px 55px rgba(0,0,0,.18);
        }}
        .hero::before {{
            content:""; position:absolute; inset:0; z-index:1;
            background-image:linear-gradient(rgba(113,215,197,.045) 1px, transparent 1px),
                             linear-gradient(90deg, rgba(113,215,197,.045) 1px, transparent 1px);
            background-size:34px 34px; mask-image:linear-gradient(90deg, black, transparent 85%);
        }}
        .hero::after {{
            content:""; position:absolute; inset:0; z-index:1;
            background:linear-gradient(90deg, rgba(4,17,29,.98) 0%, rgba(4,17,29,.90) 37%, rgba(4,17,29,.26) 68%, rgba(4,17,29,.08) 100%);
        }}
        .hero-visual {{
            position:absolute; inset:0; width:100%; height:100%; object-fit:cover;
            object-position:center; opacity:.94;
        }}
        .hero-copy {{ position:relative; z-index:2; width:53%; }}
        .eyebrow {{ font:600 .72rem 'IBM Plex Mono'; color:var(--mint); letter-spacing:.14em; text-transform:uppercase; }}
        .hero h1 {{ font-size:clamp(2rem, 4vw, 3.5rem); line-height:1.03; margin:.65rem 0 .9rem; color:#F4F8FB; letter-spacing:-.04em; }}
        .hero p {{ color:#B8CAD5; max-width:720px; font-size:1rem; line-height:1.65; margin:0; }}
        .hero-meta {{ display:flex; flex-wrap:wrap; gap:.55rem; align-items:center; margin-top:1.2rem; }}
        .status-chip {{
            display:inline-flex; align-items:center; gap:.45rem;
            padding:.4rem .72rem; border-radius:999px; color:#CDEBE6; background:rgba(113,215,197,.08);
            border:1px solid rgba(113,215,197,.22); font:500 .72rem 'IBM Plex Mono';
        }}
        .status-dot {{ width:7px; height:7px; background:var(--mint); border-radius:50%; box-shadow:0 0 10px var(--mint); }}
        .reporter-chip {{
            display:inline-flex; align-items:center; gap:.48rem; padding:.4rem .72rem; border-radius:999px;
            color:var(--ice); background:rgba(245,196,81,.09); border:1px solid rgba(245,196,81,.30);
            font-size:.75rem;
        }}
        .reporter-label {{ color:var(--gold); font:600 .68rem 'IBM Plex Mono'; letter-spacing:.07em; }}

        .metric-card {{
            min-height:126px; border-radius:14px; padding:1rem 1.05rem;
            border:1px solid rgba(145,168,184,.16); background:rgba(10,32,53,.72);
        }}
        .metric-label {{ font:500 .68rem 'IBM Plex Mono'; color:var(--muted); letter-spacing:.08em; text-transform:uppercase; }}
        .metric-value {{ font:700 2rem 'IBM Plex Mono'; color:var(--ice); margin:.45rem 0 .25rem; }}
        .metric-foot {{ color:var(--mint); font-size:.76rem; }}

        .section-kicker {{ font:600 .68rem 'IBM Plex Mono'; color:var(--mint); letter-spacing:.14em; text-transform:uppercase; margin-top:1.6rem; }}
        .section-title {{ font-size:1.55rem; font-weight:700; color:var(--ice); margin:.28rem 0 .25rem; letter-spacing:-.02em; }}
        .section-copy {{ color:var(--muted); font-size:.88rem; margin-bottom:1rem; }}

        .priority-card {{
            min-height:184px; border-radius:14px; padding:1.15rem; position:relative; overflow:hidden;
            border:1px solid rgba(113,215,197,.17); background:linear-gradient(160deg, rgba(12,42,67,.92), rgba(8,27,43,.92));
        }}
        .priority-no {{ font:600 .7rem 'IBM Plex Mono'; color:var(--gold); letter-spacing:.12em; }}
        .priority-card h3 {{ margin:.55rem 0 .45rem; font-size:1.08rem; color:var(--ice); }}
        .priority-card p {{ color:var(--muted); font-size:.8rem; line-height:1.55; }}
        .priority-tag {{ display:inline-block; margin-top:.5rem; color:var(--mint); font:500 .68rem 'IBM Plex Mono'; }}

        .brief {{ border-left:3px solid var(--gold); background:rgba(245,196,81,.065); border-radius:0 12px 12px 0; padding:1rem 1.2rem; color:#CBD8E0; line-height:1.65; }}
        .warning-card {{ border:1px solid rgba(255,122,110,.22); background:rgba(255,122,110,.055); padding:.85rem 1rem; border-radius:12px; margin:.45rem 0; }}
        .warning-title {{ color:#FF9C92; font-weight:600; font-size:.83rem; }}
        .warning-copy {{ color:#B8CAD5; font-size:.77rem; margin-top:.25rem; }}
        .source-link a {{ color:var(--mint)!important; text-decoration:none; }}
        .case-head {{ border-top:1px solid rgba(113,215,197,.2); padding-top:1rem; margin-top:.6rem; }}
        .mono {{ font-family:'IBM Plex Mono'; }}
        .case-metric-grid {{
            display:grid; grid-template-columns:repeat(2, minmax(0, 1fr));
            gap:.75rem; margin:1rem 0 1.35rem;
        }}
        .case-metric {{
            min-width:0; min-height:108px; padding:1rem 1.1rem; border-radius:14px;
            border:1px solid rgba(145,168,184,.22); background:rgba(10,32,53,.72);
        }}
        .case-metric-label {{
            color:var(--muted); font-size:.78rem; font-weight:600; margin-bottom:.55rem;
        }}
        .case-metric-value {{
            color:var(--ice); font-size:clamp(1.15rem, 2.3vw, 1.55rem); font-weight:700;
            line-height:1.3; overflow-wrap:anywhere; word-break:keep-all;
        }}

        div[data-testid="stMetric"] {{
            background:rgba(10,32,53,.72); border:1px solid rgba(145,168,184,.16);
            padding:1rem; border-radius:14px;
        }}
        div[data-testid="stDataFrame"] {{ border:1px solid rgba(145,168,184,.16); border-radius:12px; overflow:hidden; }}
        .stTabs [data-baseweb="tab-list"] {{ gap:.35rem; }}
        .stTabs [data-baseweb="tab"] {{ background:rgba(10,32,53,.65); border-radius:9px; padding:.45rem .8rem; }}
        .stTabs [aria-selected="true"] {{ color:var(--gold)!important; border-bottom-color:var(--gold)!important; }}
        a {{ color:var(--mint); }}
        @media (max-width: 800px) {{
            .hero {{ min-height:340px; padding:1.5rem; }}
            .hero-copy {{ width:100%; }}
            .hero-visual {{ object-position:66% center; opacity:.54; }}
            .hero::after {{ background:linear-gradient(90deg, rgba(4,17,29,.96), rgba(4,17,29,.72) 68%, rgba(4,17,29,.26)); }}
        }}
        @media (max-width: 540px) {{ .case-metric-grid {{ grid-template-columns:1fr; }} }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def section(kicker: str, title: str, copy: str = "") -> None:
    st.markdown(
        f'<div class="section-kicker">{kicker}</div><div class="section-title">{title}</div>'
        f'<div class="section-copy">{copy}</div>',
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, foot: str) -> None:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div><div class="metric-foot">{foot}</div></div>',
        unsafe_allow_html=True,
    )


def plot_theme(fig: go.Figure, height: int = 420) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=12, r=12, t=36, b=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Sans KR", color=ICE),
        title_font=dict(size=14, color=ICE),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=MUTED)),
        hoverlabel=dict(bgcolor=NAVY_2, bordercolor=MINT, font_color=ICE),
    )
    return fig


def render_sidebar(meta: dict) -> str:
    with st.sidebar:
        st.markdown(
            '<div class="brand"><div class="brand-mark">S</div><div>'
            '<div class="brand-title">SUBMARINE HW</div><div class="brand-sub">HERITAGE WATCH</div>'
            '</div></div>',
            unsafe_allow_html=True,
        )
        page = st.radio(
            "NAVIGATION",
            ["작전 개요", "사례 탐색", "의사결정 매트릭스", "데이터 정합성", "조사 로드맵"],
            label_visibility="collapsed",
        )
        st.divider()
        st.caption("DATA STATUS")
        st.markdown(f"**{meta['phase']}**")
        st.caption(f"기준일  {meta['as_of']}")
        st.markdown(
            '<div class="status-chip"><span class="status-dot"></span> RESEARCH ACTIVE</div>',
            unsafe_allow_html=True,
        )
        st.divider()
        st.caption("MISSION NOTE")
        st.write(meta["priority_message"])
        st.caption(meta["disclaimer"])
    return page


def render_hero(meta: dict) -> None:
    hero_image = HERO_IMAGE_B64_PATH.read_text(encoding="ascii").strip()
    st.markdown(
        f"""
        <div class="hero">
          <img class="hero-visual" src="data:image/webp;base64,{hero_image}" alt="장형우 소령과 Type 209 계열 잠수함 합성 이미지">
          <div class="hero-copy">
            <div class="eyebrow">Heritage Mission · Jang Bogo Class</div>
            <h1>퇴역 장보고함<br>전시 벤치마킹</h1>
            <p>국내외 잠수함 박물관의 보존·안전·관람·운영 데이터를 하나의 작전 화면으로 통합합니다.</p>
            <div class="hero-meta">
              <div class="status-chip"><span class="status-dot"></span>{meta['phase']} · {meta['as_of']}</div>
              <div class="reporter-chip"><span class="reporter-label">보고자</span><strong>장형우 소령</strong></div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def overview_page(data: pd.DataFrame, meta: dict) -> None:
    render_hero(meta)
    current = data[data["status"].isin(["운영", "제한 공개"])]
    cols = st.columns(4)
    with cols[0]:
        metric_card("CASES", f"{len(data):02d}", "국내외 구조화 사례")
    with cols[1]:
        metric_card("ACTIVE", f"{len(current):02d}", "현재·제한 공개")
    with cols[2]:
        metric_card("PRIMARY", f"{(data['confidence'] == 'A').sum():02d}", "A급 근거 사례")
    with cols[3]:
        metric_card("TYPE 209", "01", "직접 비교군 확인")

    section("MISSION PRIORITY", "우선 벤치마크", "장보고함 의사결정에 직접 영향을 주는 4개 시설입니다.")
    cards = [
        ("01 · DIRECT", "PROTEUS / 그리스", "같은 HDW Type 209 계열. 원형성·비군사화·초기 운영을 직접 비교합니다.", "TYPE 209/1100"),
        ("02 · SYSTEM", "U17 / 독일", "실내 육상형의 브리지·인원계수·환기·화재감지 패키지입니다.", "INDOOR / 30 PAX"),
        ("03 · SCALE", "HMAS Ovens / 호주", "89.9m 선체의 신규 입·출구·난간·보존공사로 규모가 가장 가깝습니다.", "LAND / 89.9 M"),
        ("04 · FLOW", "JDS Akishio / 일본", "박물관 상층에서 함내로 직접 연결해 날씨·대기·피난을 통합합니다.", "BUILDING LINK"),
    ]
    columns = st.columns(4)
    for column, (no, title, body, tag) in zip(columns, cards):
        with column:
            st.markdown(
                f'<div class="priority-card"><div class="priority-no">{no}</div><h3>{title}</h3>'
                f'<p>{body}</p><div class="priority-tag">{tag}</div></div>',
                unsafe_allow_html=True,
            )

    section("GLOBAL PICTURE", "사례 분포와 전시 방식", "점을 선택하면 시설·함정·상태를 확인할 수 있습니다.")
    left, right = st.columns([1.65, 1])
    with left:
        color_map = {"국내": GOLD, "유럽": MINT, "미주": "#70A7FF", "아시아": "#CE8DFF", "오세아니아": "#FF8D75"}
        fig = px.scatter_geo(
            data,
            lat="lat",
            lon="lon",
            color="region",
            size="relevance",
            hover_name="case_name",
            hover_data={"vessel": True, "country": True, "display_mode": True, "status": True, "lat": False, "lon": False, "relevance": False},
            color_discrete_map=color_map,
            projection="natural earth",
        )
        fig.update_geos(
            bgcolor="rgba(0,0,0,0)", showland=True, landcolor="#0B2A40", showocean=True,
            oceancolor="#061522", showcountries=True, countrycolor="#315064", coastlinecolor="#315064",
        )
        fig.update_traces(marker=dict(line=dict(width=1, color="#06121F"), opacity=.9))
        st.plotly_chart(plot_theme(fig, 410), use_container_width=True, config={"displayModeBar": False})
    with right:
        modes = data.assign(mode_group=data["display_mode"].replace({
            r".*실내.*": "실내·연결 육상", r".*야외 육상.*": "야외 육상", r".*수상.*": "수상 계류·고정",
        }, regex=True))
        mode_counts = modes.groupby("mode_group").size().reset_index(name="cases")
        fig = px.pie(mode_counts, names="mode_group", values="cases", hole=.7, color_discrete_sequence=[MINT, GOLD, "#4E83A6", "#8E6CB4"])
        fig.update_traces(textinfo="percent+label", textfont_size=11, marker=dict(line=dict(color=NAVY, width=2)))
        fig.add_annotation(text=f"<b>{len(data)}</b><br><span style='font-size:11px'>CASES</span>", showarrow=False, font=dict(color=ICE, size=20))
        st.plotly_chart(plot_theme(fig, 410), use_container_width=True, config={"displayModeBar": False})

    section("COMMAND BRIEF", "현재의 설계 가설")
    st.markdown(
        '<div class="brief"><b>실내 또는 반실내 육상 거치</b>를 우선 기준안으로 검토합니다. '
        '보존환경·연중 운영·관람동선에는 유리하지만, 압력선체 개조와 인양·기초 비용을 '
        '수상 계류안의 30년 dry dock·부식 비용과 같은 기준으로 비교해야 합니다.</div>',
        unsafe_allow_html=True,
    )


def explorer_page(data: pd.DataFrame) -> None:
    section("CASE LIBRARY", "사례 탐색", "필터와 상세 패널로 근거·경고·적용 시사점을 함께 확인합니다.")
    f1, f2, f3, f4 = st.columns(4)
    regions = f1.multiselect("지역", sorted(data["region"].unique()), default=sorted(data["region"].unique()))
    statuses = f2.multiselect("운영 상태", sorted(data["status"].unique()), default=sorted(data["status"].unique()))
    confidence = f3.multiselect(
        "근거 신뢰도 등급",
        ["A", "B", "C", "D"],
        default=["A", "B", "C"],
        help="A: 공식자료+교차검증 · B: 공식자료 또는 신뢰 가능한 2개 출처 · C: 신뢰 가능한 1개 출처 · D: 추가 검증 필요",
    )
    min_rel = f4.slider(
        "장보고함 적용성 (최소)",
        1,
        5,
        3,
        help="장보고함 전시 계획에 직접 참고할 수 있는 정도입니다. 5점이 가장 높습니다.",
    )
    filtered = data[
        data["region"].isin(regions)
        & data["status"].isin(statuses)
        & data["confidence"].isin(confidence)
        & (data["relevance"] >= min_rel)
    ].copy()

    st.caption(f"조건에 맞는 사례 {len(filtered)}개 · 표는 가로로 스크롤할 수 있습니다.")
    display = filtered[["case_name", "vessel", "country", "class_type", "display_mode", "status", "length_m", "relevance", "confidence", "priority"]].rename(
        columns={
            "case_name": "전시시설명",
            "vessel": "전시 함정",
            "country": "국가",
            "class_type": "함급·형식",
            "display_mode": "전시 형태",
            "status": "공개 상태",
            "length_m": "전장",
            "relevance": "장보고함 적용성",
            "confidence": "근거 신뢰도",
            "priority": "현장조사 우선순위",
        }
    )
    st.dataframe(
        display.sort_values(["현장조사 우선순위", "근거 신뢰도"]),
        use_container_width=True,
        hide_index=True,
        height=460,
        column_config={
            "전시시설명": st.column_config.TextColumn(width=210),
            "전시 함정": st.column_config.TextColumn(width=155),
            "국가": st.column_config.TextColumn(width=90),
            "함급·형식": st.column_config.TextColumn(width=170),
            "전시 형태": st.column_config.TextColumn(width=145),
            "공개 상태": st.column_config.TextColumn(width=135),
            "전장": st.column_config.NumberColumn(format="%.1f m", width=90),
            "장보고함 적용성": st.column_config.ProgressColumn(
                help="장보고함 전시 계획에 대한 적용 가능성 (5점 만점)", min_value=1, max_value=5, format="%d / 5", width=145
            ),
            "근거 신뢰도": st.column_config.TextColumn(
                help="자료의 검증 수준: A가 가장 높고 D는 추가 검증 필요", width=120
            ),
            "현장조사 우선순위": st.column_config.NumberColumn(
                help="사례의 품질 등급이 아니라 후속 심층조사 순서입니다.", format="%d순위", width=155
            ),
        },
    )

    if filtered.empty:
        st.info("필터 조건에 맞는 사례가 없습니다.")
        return

    section("CASE DETAIL", "선택 사례 상세")
    choice = st.selectbox("시설 선택", filtered.sort_values(["priority", "case_name"])["case_name"], label_visibility="collapsed")
    row = filtered.loc[filtered["case_name"] == choice].iloc[0]
    st.markdown(f"### {row['case_name']}")
    st.caption(f"{row['vessel']} · {row['country']} {row['city']} · {row['class_type']}")
    case_metrics = [
        ("전시 형태", row["display_mode"]),
        ("공개 상태", row["status"]),
        ("전장", f"{row['length_m']:.1f} m"),
        ("근거 신뢰도", f"{row['confidence']}등급"),
    ]
    metric_html = "".join(
        f'<div class="case-metric"><div class="case-metric-label">{escape(label)}</div>'
        f'<div class="case-metric-value">{escape(str(value))}</div></div>'
        for label, value in case_metrics
    )
    st.markdown(f'<div class="case-metric-grid">{metric_html}</div>', unsafe_allow_html=True)

    st.markdown("**장보고함 적용 시사점**")
    st.write(row["insight"])
    st.markdown("**관람·접근성**")
    st.write(f"{row['accessibility']} · {row['throughput']}")
    st.markdown("**보존·공개 비용**")
    st.write(f"{row['conservation']} · {row['cost_public']}")
    st.markdown("**DATA WARNING**")
    st.markdown(
        f'<div class="warning-card"><div class="warning-title">확인 필요</div>'
        f'<div class="warning-copy">{escape(str(row["data_warning"]))}</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown("**PRIMARY SOURCE**")
    st.markdown(f"[공식·준공식 자료 열기 ↗]({row['source_url']})")
    st.caption(f"Case ID  {row['id']}  ·  현장조사 {int(row['priority'])}순위")


def decision_page() -> None:
    section("OPTION ANALYSIS", "거치방식 의사결정 매트릭스", "현재 사례 근거를 바탕으로 한 상대평가입니다. 기술조사 후 점수를 갱신해야 합니다.")
    decision = pd.DataFrame(
        {
            "평가축": ["보존환경", "연중 운영", "관람동선", "원형성", "접근성", "초기비용", "장기비용 예측성"],
            "실내 육상": [5, 5, 5, 3, 5, 2, 4],
            "야외 육상": [3, 3, 4, 3, 3, 3, 3],
            "수상 계류": [2, 3, 2, 5, 2, 4, 2],
        }
    )
    tabs = st.tabs(["레이더 비교", "근거 매트릭스", "결정 게이트"])
    with tabs[0]:
        fig = go.Figure()
        colors = {"실내 육상": MINT, "야외 육상": GOLD, "수상 계류": "#70A7FF"}
        for option in colors:
            fig.add_trace(go.Scatterpolar(r=decision[option], theta=decision["평가축"], fill="toself", name=option, line_color=colors[option], opacity=.58))
        fig.update_layout(
            polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 5], gridcolor="#29475B", color=MUTED), angularaxis=dict(gridcolor="#29475B", color=ICE)),
        )
        st.plotly_chart(plot_theme(fig, 520), use_container_width=True, config={"displayModeBar": False})
    with tabs[1]:
        st.dataframe(decision, use_container_width=True, hide_index=True)
        st.caption("5점이 상대적으로 유리합니다. 초기비용 점수는 비용이 낮을수록 높습니다.")
        evidence = pd.DataFrame(
            [
                ["실내 육상", "U17 · Akishio · Le Redoutable", "HVAC·화재감지·건물 연결", "인양·기초·절개 CAPEX"],
                ["야외 육상", "HMAS Ovens · U 995 · Kursura", "전면 정비 접근·독립 동선", "염풍·UV·우천·고온"],
                ["수상 계류", "Espadon · Bowfin · Growler", "운용상태 외관·흘수 맥락", "수면선 부식·dry dock·조위"],
            ],
            columns=["대안", "대표 근거", "강점", "핵심 위험"],
        )
        st.dataframe(evidence, use_container_width=True, hide_index=True)
    with tabs[2]:
        gates = [
            ("GATE 01", "함체 상태", "현 두께·부식지도·피로·용접부 조사"),
            ("GATE 02", "비군사화", "배터리·연료·무기·유해물질 인수조건"),
            ("GATE 03", "관람 안전", "입출구·대피시간·회차당 인원·접근성"),
            ("GATE 04", "30년 LCC", "초기 조성·정기보존·중정비·철거충당"),
        ]
        cols = st.columns(4)
        for col, (num, title, body) in zip(cols, gates):
            with col:
                st.markdown(f'<div class="priority-card"><div class="priority-no">{num}</div><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)


def quality_page(data: pd.DataFrame) -> None:
    section("EVIDENCE CONTROL", "데이터 정합성", "좋은 대시보드는 불확실성을 숨기지 않고 의사결정 앞에 배치합니다.")
    q1, q2, q3 = st.columns(3)
    q1.metric("A/B급 사례", f"{data['confidence'].isin(['A','B']).mean():.0%}")
    q2.metric("경고 등록", f"{data['data_warning'].notna().sum()}건")
    q3.metric("공식 링크", f"{data['source_url'].str.startswith('http').mean():.0%}")

    left, right = st.columns([1, 1.25])
    with left:
        counts = data.groupby("confidence").size().reindex(["A", "B", "C", "D"], fill_value=0).reset_index(name="사례")
        fig = px.bar(counts, x="confidence", y="사례", color="confidence", color_discrete_map={"A": MINT, "B": "#70A7FF", "C": GOLD, "D": RED}, text="사례")
        fig.update_layout(showlegend=False, xaxis_title="신뢰도", yaxis_title="사례 수", xaxis=dict(gridcolor="#29475B"), yaxis=dict(gridcolor="#29475B"))
        st.plotly_chart(plot_theme(fig, 330), use_container_width=True, config={"displayModeBar": False})
    with right:
        missing_terms = ["미공개", "미확인"]
        check_cols = ["accessibility", "throughput", "conservation", "cost_public", "visitors_public"]
        missing = []
        for col in check_cols:
            ratio = data[col].fillna("").astype(str).apply(lambda x: any(term in x for term in missing_terms)).mean()
            missing.append({"항목": col, "추가 확인 필요": ratio})
        miss = pd.DataFrame(missing)
        labels = {"accessibility": "접근성", "throughput": "수용량", "conservation": "보존", "cost_public": "비용", "visitors_public": "방문객"}
        miss["항목"] = miss["항목"].map(labels)
        fig = px.bar(miss, x="추가 확인 필요", y="항목", orientation="h", text=miss["추가 확인 필요"].map(lambda x: f"{x:.0%}"), color_discrete_sequence=[GOLD])
        fig.update_layout(xaxis_tickformat=".0%", xaxis_title="사례 중 비율", yaxis_title="", xaxis=dict(gridcolor="#29475B"), yaxis=dict(gridcolor="#29475B"))
        st.plotly_chart(plot_theme(fig, 330), use_container_width=True, config={"displayModeBar": False})

    section("CONFLICT LOG", "핵심 상충·미확인 목록", "현재 판단에 영향이 큰 항목을 우선 표시합니다.")
    warnings = data[data["data_warning"].notna()].sort_values(["priority", "confidence"]).head(12)
    for _, row in warnings.iterrows():
        st.markdown(
            f'<div class="warning-card"><div class="warning-title">{row["case_name"]} · {row["confidence"]}급</div>'
            f'<div class="warning-copy">{row["data_warning"]}</div></div>',
            unsafe_allow_html=True,
        )


def roadmap_page() -> None:
    section("NEXT MISSION", "조사·개발 로드맵", "운영기관 회신과 현장실사 결과를 같은 데이터 구조에 누적합니다.")
    phases = [
        ("완료", "PHASE 1", "공개자료 베이스라인", "사례 구조화 · 출처 등급 · 경고 로그"),
        ("다음", "PHASE 2", "기관 서면질의", "해외 6곳 · 국내 5곳 · 동일 10문항"),
        ("계획", "PHASE 3", "현장실사", "동선 측정 · 운영 인터뷰 · 보존 상태"),
        ("계획", "PHASE 4", "대안 비교설계", "CAPEX · 30년 LCC · 처리량 · 원형성"),
    ]
    cols = st.columns(4)
    for col, (state, no, title, body) in zip(cols, phases):
        with col:
            st.markdown(
                f'<div class="priority-card"><div class="priority-no">{state} · {no}</div>'
                f'<h3>{title}</h3><p>{body}</p></div>',
                unsafe_allow_html=True,
            )

    section("STANDARD QUESTIONS", "운영기관 표준 질의서", "답변을 수치화해 사례 데이터에 병합할 수 있도록 설계합니다.")
    questions = [
        "함정 소유권·대여기간·최종 철거 의무는 누구에게 있는가?",
        "인수 당시 비군사화 및 유해물질 조사 항목은 무엇이었는가?",
        "압력선체 신규 개구부의 위치·치수·구조 보강 방식은 무엇인가?",
        "최대 동시수용인원·회차 시간·시간당 실제 처리량은 얼마인가?",
        "최장 피난거리와 정전·화재 시 목표 대피시간은 얼마인가?",
        "환기량·목표 온습도·제습·염분·응결 관리 기준은 무엇인가?",
        "선체 두께 측정·도장·음극방식·구조검사의 주기는?",
        "최근 5년 평균 운영비와 함체 보존비는 각각 얼마인가?",
        "승선 불가자를 위한 동등한 대체경험은 무엇인가?",
        "개관 후 가장 큰 설계 오류와 다시 설계할 항목은 무엇인가?",
    ]
    for idx, question in enumerate(questions, 1):
        st.markdown(f"**{idx:02d}** &nbsp; {question}")

    section("MAINTAINABILITY", "대시보드 업데이트 방법")
    st.code(
        "# 1. data/cases.csv에 사례 행 추가\n"
        "# 2. confidence(A/B/C/D), status, data_warning 기록\n"
        "# 3. git add . && git commit -m \"data: add new museum case\"\n"
        "# 4. git push",
        language="bash",
    )
    st.caption("CSV 변경만으로 지도·지표·표·정합성 화면이 함께 갱신됩니다.")


data, meta = load_data()
inject_css()
page = render_sidebar(meta)

if page == "작전 개요":
    overview_page(data, meta)
elif page == "사례 탐색":
    explorer_page(data)
elif page == "의사결정 매트릭스":
    decision_page()
elif page == "데이터 정합성":
    quality_page(data)
else:
    roadmap_page()

