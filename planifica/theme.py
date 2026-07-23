from __future__ import annotations

import streamlit as st

BG_MAIN = "#D5E9E2"
BG_SIDEBAR = "#C6E0D6"
BG_SURFACE = "#FFFFFF"
BRAND_GREEN = "#044A30"
BORDER_SOFT = "#B8D4C8"

APP_NAME = "PlanificaDeporte"
TAGLINE = "Tu primer Plan Estratégico Institucional — clubes, federaciones y asociaciones"
FOOTER = "Observatorio de Inteligencia Artificial · Metodología COI (2020)"



def inject_theme() -> None:
    st.markdown(
        f"""
        <style>
        [data-testid="stHeader"] [data-testid="stToolbar"] {{
            display: none !important;
        }}
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        section.main,
        section.main > div,
        .main .block-container {{
            background-color: {BG_MAIN} !important;
        }}
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] > div {{
            background-color: {BG_SIDEBAR} !important;
        }}
        [data-testid="stHeader"] {{
            background-color: {BG_MAIN} !important;
        }}
        details[data-testid="stExpander"],
        [data-testid="stDataFrame"],
        div[data-testid="stMetric"] {{
            background-color: {BG_SURFACE} !important;
            border: 1px solid {BORDER_SOFT};
            border-radius: 0.5rem;
        }}
        .stButton > button,
        [data-testid="stBaseButton-secondary"],
        [data-testid="stBaseButton-primary"],
        [data-testid="stSidebar"] .stButton > button {{
            background: #ffffff !important;
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 1px solid {BORDER_SOFT} !important;
            border-radius: 0.75rem !important;
            box-shadow: none !important;
        }}
        .stButton > button:hover,
        [data-testid="stBaseButton-secondary"]:hover,
        [data-testid="stBaseButton-primary"]:hover {{
            background: #f8fafc !important;
            border-color: {BORDER_SOFT} !important;
        }}
        .pd-metric {{
            background-color: {BG_SURFACE};
            border: 1px solid {BORDER_SOFT};
            border-radius: 0.5rem;
            padding: 0.75rem 0.5rem;
            text-align: center;
        }}
        .pd-metric-label {{ font-size: 0.85rem; color: #475569; }}
        .pd-metric-value {{ font-size: 1.6rem; font-weight: 600; color: #0f172a; }}
        .pd-doc {{
            background: {BG_SURFACE};
            border: 1px solid {BORDER_SOFT};
            border-radius: 0.75rem;
            padding: 1.25rem 1.35rem 1.5rem;
            color: #0f172a;
            line-height: 1.45;
        }}
        .pd-doc-header h2 {{
            margin: 0.35rem 0 0.85rem;
            color: {BRAND_GREEN};
            font-size: 1.45rem;
            font-weight: 700;
            line-height: 1.2;
        }}
        .pd-doc-badge {{
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: {BRAND_GREEN};
            background: #e8f3ee;
            border: 1px solid {BORDER_SOFT};
            border-radius: 999px;
            padding: 0.2rem 0.65rem;
        }}
        .pd-meta {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.65rem;
            margin-bottom: 1.1rem;
        }}
        .pd-meta > div {{
            background: #f7fbf9;
            border: 1px solid {BORDER_SOFT};
            border-radius: 0.5rem;
            padding: 0.55rem 0.7rem;
        }}
        .pd-meta span {{
            display: block;
            font-size: 0.75rem;
            color: #64748b;
            margin-bottom: 0.15rem;
        }}
        .pd-meta strong {{
            font-size: 0.95rem;
            color: #0f172a;
            font-weight: 600;
        }}
        .pd-doc h3 {{
            margin: 1.15rem 0 0.55rem;
            color: {BRAND_GREEN};
            font-size: 1.05rem;
            font-weight: 700;
            border-bottom: 1px solid {BORDER_SOFT};
            padding-bottom: 0.3rem;
        }}
        .pd-field {{
            margin-bottom: 0.65rem;
        }}
        .pd-field-label {{
            font-size: 0.78rem;
            font-weight: 600;
            color: #475569;
            margin-bottom: 0.15rem;
        }}
        .pd-field-body p {{
            margin: 0 0 0.25rem;
            font-size: 0.95rem;
            white-space: pre-wrap;
        }}
        .pd-empty {{ color: #94a3b8; font-style: italic; }}
        .pd-grid-2 {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.55rem 0.85rem;
        }}
        .pd-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
            margin: 0.35rem 0 0.75rem;
        }}
        .pd-table th, .pd-table td {{
            border: 1px solid {BORDER_SOFT};
            padding: 0.4rem 0.5rem;
            text-align: left;
            vertical-align: top;
            background: {BG_SURFACE};
        }}
        .pd-table th {{
            background: #eef6f2;
            color: {BRAND_GREEN};
            font-weight: 600;
        }}
        .pd-action {{
            background: #f7fbf9;
            border: 1px solid {BORDER_SOFT};
            border-radius: 0.5rem;
            padding: 0.65rem 0.75rem;
            margin: 0 0 0.55rem;
        }}
        .pd-action-title {{
            font-weight: 600;
            color: {BRAND_GREEN};
            margin-bottom: 0.35rem;
            font-size: 0.95rem;
        }}
        .pd-action-meta {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.25rem 0.75rem;
            font-size: 0.85rem;
            color: #334155;
        }}
        .pd-doc-footer {{
            margin-top: 1.25rem;
            padding-top: 0.75rem;
            border-top: 1px solid {BORDER_SOFT};
            font-size: 0.78rem;
            color: #64748b;
        }}
        @media (max-width: 720px) {{
            .pd-meta, .pd-grid-2 {{ grid-template-columns: 1fr; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:8px;">
          <div style="background:{BRAND_GREEN};color:white;width:72px;height:72px;
            border-radius:50%;display:flex;align-items:center;justify-content:center;
            font-weight:700;font-size:1.5rem;">P</div>
          <div>
            <div style="font-size:2rem;font-weight:700;color:{BRAND_GREEN};line-height:1.1;">{APP_NAME}</div>
            <div style="color:#64748b;font-size:1rem;">{TAGLINE}</div>
            <div style="color:#94a3b8;font-size:0.88rem;margin-top:2px;">{FOOTER}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str) -> None:
    import html

    st.markdown(
        f"""
        <div class="pd-metric">
          <div class="pd-metric-label">{html.escape(label)}</div>
          <div class="pd-metric-value">{html.escape(value)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
