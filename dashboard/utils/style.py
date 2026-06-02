"""scrollytelling shell. dark cinematic editorial palette. pure css, no js."""
import streamlit as st

COLORS = {
    "bg":        "#0b0c0e",
    "bg_2":      "#0f1114",
    "surface":   "#15171a",
    "surface_2": "#1d2024",
    "border":    "#2a2d33",
    "text":      "#f5f5f4",
    "text_2":    "#a1a1aa",
    "text_3":    "#71717a",
    "accent":    "#f59e0b",
    "accent_2":  "#fbbf24",
    "brand":     "#1B4D3E",
    "brand_2":   "#2d6a4f",
    "ok":        "#4ade80",
    "warn":      "#fb923c",
    "bad":       "#ef4444",
    "blue":      "#60a5fa",
    "violet":    "#a78bfa",
}

PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor":  "rgba(0,0,0,0)",
        "font": {"family": "Inter, sans-serif", "color": COLORS["text"], "size": 13},
        "title": {"font": {"family": "Fraunces, serif", "size": 22, "color": COLORS["text"]}},
        "xaxis": {
            "gridcolor": "rgba(255,255,255,0.05)",
            "linecolor": COLORS["border"],
            "tickcolor": COLORS["text_3"],
            "zeroline": False,
            "tickfont": {"color": COLORS["text_2"]},
            "title": {"font": {"color": COLORS["text_2"], "size": 12}},
        },
        "yaxis": {
            "gridcolor": "rgba(255,255,255,0.05)",
            "linecolor": COLORS["border"],
            "tickcolor": COLORS["text_3"],
            "zeroline": False,
            "tickfont": {"color": COLORS["text_2"]},
            "title": {"font": {"color": COLORS["text_2"], "size": 12}},
        },
        "colorway": [COLORS["accent"], COLORS["blue"], COLORS["ok"],
                     COLORS["warn"], COLORS["bad"], COLORS["violet"], "#f472b6"],
        "margin": {"l": 60, "r": 30, "t": 50, "b": 50},
        "legend": {"bgcolor": "rgba(0,0,0,0)", "font": {"color": COLORS["text_2"]}},
        "hoverlabel": {"bgcolor": COLORS["surface_2"],
                       "bordercolor": COLORS["border"],
                       "font": {"color": COLORS["text"], "family": "Inter"}},
    }
}


def inject_shell():
    """one big css drop. pure css, no js. everything is visible by default."""
    st.markdown(
        f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,600;9..144,700;9..144,800;9..144,900&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
:root {{
    --bg: {COLORS['bg']};
    --surface: {COLORS['surface']};
    --surface-2: {COLORS['surface_2']};
    --border: {COLORS['border']};
    --text: {COLORS['text']};
    --text-2: {COLORS['text_2']};
    --text-3: {COLORS['text_3']};
    --accent: {COLORS['accent']};
    --accent-2: {COLORS['accent_2']};
    --brand: {COLORS['brand']};
    --ok: {COLORS['ok']};
    --bad: {COLORS['bad']};
    --blue: {COLORS['blue']};
}}

html, body {{
    background: {COLORS['bg']} !important;
    color: {COLORS['text']} !important;
    scroll-behavior: smooth;
}}
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
    background: {COLORS['bg']} !important;
    color: {COLORS['text']} !important;
}}
.stApp *, [data-testid="stAppViewContainer"] * {{
    font-family: 'Inter', sans-serif;
}}
.stApp > header, [data-testid="stHeader"] {{
    background: transparent !important;
    border: none !important;
}}
section[data-testid="stSidebar"], [data-testid="collapsedControl"] {{
    display: none !important;
}}
.block-container,
[data-testid="stMainBlockContainer"],
[data-testid="block-container"] {{
    padding: 0 !important;
    max-width: 100% !important;
    background: {COLORS['bg']} !important;
}}

/* css-only scroll progress bar using scroll-timeline (Chrome 115+) */
@supports (animation-timeline: scroll()) {{
    .scroll-progress {{
        position: fixed; top: 0; left: 0; height: 3px; width: 100%;
        transform-origin: 0 0;
        transform: scaleX(0);
        background: linear-gradient(90deg, {COLORS['accent']}, {COLORS['accent_2']});
        z-index: 9999;
        animation: progress linear;
        animation-timeline: scroll(root);
        box-shadow: 0 0 12px rgba(245, 158, 11, 0.5);
    }}
    @keyframes progress {{ to {{ transform: scaleX(1); }} }}
}}

/* fallback static accent line at top */
@supports not (animation-timeline: scroll()) {{
    .scroll-progress {{
        position: fixed; top: 0; left: 0; height: 3px; width: 100%;
        background: linear-gradient(90deg, {COLORS['accent']}, transparent 30%);
        z-index: 9999; opacity: 0.6;
    }}
}}

/* hero */
.hero {{
    min-height: 92vh;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 4rem 2rem 8rem;
    text-align: center;
    position: relative;
    background: radial-gradient(ellipse at top, rgba(245,158,11,0.06), transparent 60%);
}}
.hero .kicker {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: {COLORS['accent']};
    margin-bottom: 2rem;
    animation: fadeUp 700ms cubic-bezier(0.2, 0.8, 0.2, 1) 100ms both;
}}
.hero h1 {{
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: clamp(2.6rem, 7vw, 5.5rem);
    line-height: 1.04;
    letter-spacing: -0.03em;
    color: {COLORS['text']};
    margin: 0 0 2rem;
    max-width: 22ch;
    animation: fadeUp 900ms cubic-bezier(0.2, 0.8, 0.2, 1) 300ms both;
}}
.hero h1 em {{
    font-style: italic;
    color: {COLORS['accent']};
    font-weight: 500;
}}
.hero .lede {{
    font-family: 'Fraunces', serif;
    font-size: clamp(1.1rem, 1.7vw, 1.45rem);
    line-height: 1.55;
    color: {COLORS['text_2']};
    max-width: 60ch;
    margin: 0 auto;
    animation: fadeUp 1000ms cubic-bezier(0.2, 0.8, 0.2, 1) 600ms both;
}}
.hero .meta {{
    margin-top: 4rem;
    display: flex; gap: 2.5rem; flex-wrap: wrap;
    justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: {COLORS['text_3']};
    animation: fadeUp 1000ms cubic-bezier(0.2, 0.8, 0.2, 1) 900ms both;
}}
.hero .meta span {{ color: {COLORS['text_2']}; }}
.scroll-cue {{
    margin-top: 3rem;
    color: {COLORS['text_3']};
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
    animation: fadeUp 800ms ease 1200ms both, bounce 2s ease-in-out 2.5s infinite;
}}
.scroll-cue::after {{ content: ' \\2193'; }}

/* chapter blocks */
.chapter {{
    padding: 7rem 0 4rem;
    border-top: 1px solid {COLORS['border']};
    position: relative;
}}
.chapter-head {{
    max-width: 760px; margin: 0 auto;
    padding: 0 2rem 2.5rem;
}}
.chapter-num {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: {COLORS['accent']};
    margin-bottom: 1.5rem;
    animation: fadeUp 700ms ease both;
}}
.chapter h2 {{
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: clamp(2.2rem, 4.5vw, 3.6rem);
    line-height: 1.08;
    letter-spacing: -0.025em;
    color: {COLORS['text']};
    margin: 0 0 2rem;
    animation: fadeUp 800ms ease 100ms both;
}}
.chapter h2 em {{ font-style: italic; color: {COLORS['accent']}; font-weight: 500; }}

.prose {{
    max-width: 680px; margin: 0 auto;
    padding: 0 2rem;
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    line-height: 1.75;
    color: {COLORS['text_2']};
}}
.prose p {{ margin: 0 0 1.4rem; }}
.prose strong {{ color: {COLORS['text']}; font-weight: 500; }}
.prose em {{ color: {COLORS['accent']}; font-style: italic; }}

.pullquote {{
    max-width: 880px; margin: 4rem auto;
    padding: 0 2rem;
    font-family: 'Fraunces', serif;
    font-size: clamp(1.5rem, 2.8vw, 2.2rem);
    line-height: 1.35;
    color: {COLORS['text']};
    text-align: center;
    font-weight: 400;
    font-style: italic;
    letter-spacing: -0.015em;
}}
.pullquote .accent {{ color: {COLORS['accent']}; font-style: normal; font-weight: 600; }}

.section-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: {COLORS['text_3']};
    margin: 4rem 0 1rem;
    text-align: center;
}}
.section-title {{
    font-family: 'Fraunces', serif;
    font-weight: 500;
    font-size: clamp(1.6rem, 3vw, 2.3rem);
    line-height: 1.18;
    color: {COLORS['text']};
    text-align: center;
    max-width: 22ch;
    margin: 0 auto 1rem;
    letter-spacing: -0.02em;
}}
.section-desc {{
    text-align: center;
    color: {COLORS['text_2']};
    font-size: 1.02rem;
    line-height: 1.65;
    max-width: 60ch;
    margin: 0 auto 2.5rem;
    font-family: 'Inter', sans-serif;
}}

/* big number stat blocks */
.bignum-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 0;
    max-width: 1100px;
    margin: 4rem auto;
    padding: 0 2rem;
    border-top: 1px solid {COLORS['border']};
    border-bottom: 1px solid {COLORS['border']};
}}
.bignum {{
    padding: 2.5rem 1.5rem;
    text-align: center;
    border-right: 1px solid {COLORS['border']};
}}
.bignum:last-child {{ border-right: none; }}
.bignum .v {{
    font-family: 'Fraunces', serif;
    font-weight: 500;
    font-size: clamp(2.4rem, 4vw, 3.5rem);
    line-height: 1;
    letter-spacing: -0.03em;
    color: {COLORS['text']};
    margin-bottom: 0.6rem;
    font-variant-numeric: tabular-nums;
}}
.bignum .v.accent {{ color: {COLORS['accent']}; }}
.bignum .l {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: {COLORS['text_3']};
}}

/* solo big stat */
.solo-stat {{
    text-align: center;
    padding: 4rem 2rem;
    max-width: 900px;
    margin: 0 auto;
}}
.solo-stat .v {{
    font-family: 'Fraunces', serif;
    font-weight: 500;
    font-size: clamp(5rem, 13vw, 10rem);
    line-height: 0.9;
    letter-spacing: -0.05em;
    color: {COLORS['accent']};
    margin-bottom: 1.5rem;
    font-variant-numeric: tabular-nums;
    animation: scaleIn 1200ms cubic-bezier(0.2, 0.8, 0.2, 1) both;
}}
.solo-stat .l {{
    font-family: 'Fraunces', serif;
    font-style: italic;
    font-size: clamp(1.15rem, 2vw, 1.55rem);
    color: {COLORS['text_2']};
    line-height: 1.45;
    max-width: 44ch;
    margin: 0 auto;
}}

/* cluster cards */
.cluster-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1rem;
    max-width: 1100px;
    margin: 3rem auto;
    padding: 0 2rem;
}}
.cluster-card {{
    background: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-left-width: 4px;
    border-radius: 14px;
    padding: 1.75rem;
    transition: transform 250ms cubic-bezier(0.2, 0.8, 0.2, 1),
                border-color 250ms ease;
}}
.cluster-card:hover {{ transform: translateY(-4px); }}
.cluster-card .cnum {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}}
.cluster-card .ctitle {{
    font-family: 'Fraunces', serif;
    font-size: 1.35rem;
    font-weight: 600;
    color: {COLORS['text']};
    margin-bottom: 0.75rem;
    letter-spacing: -0.01em;
    line-height: 1.2;
}}
.cluster-card .cdesc {{
    color: {COLORS['text_2']};
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 1rem;
    font-family: 'Inter', sans-serif;
}}
.cluster-card .cexamples {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.76rem;
    color: {COLORS['text_3']};
    line-height: 1.6;
    padding-top: 1rem;
    border-top: 1px solid {COLORS['border']};
}}

/* step list */
.steps {{
    max-width: 720px; margin: 4rem auto;
    padding: 0 2rem;
}}
.step {{
    display: flex; gap: 2rem;
    padding: 2rem 0;
    border-bottom: 1px solid {COLORS['border']};
}}
.step:last-child {{ border-bottom: none; }}
.step-num {{
    font-family: 'Fraunces', serif;
    font-size: 2.5rem;
    font-weight: 400;
    color: {COLORS['accent']};
    line-height: 1;
    min-width: 4rem;
    font-variant-numeric: tabular-nums;
}}
.step-body .stitle {{
    font-family: 'Fraunces', serif;
    font-size: 1.35rem;
    font-weight: 600;
    color: {COLORS['text']};
    margin-bottom: 0.6rem;
    line-height: 1.3;
}}
.step-body .sbody {{
    color: {COLORS['text_2']};
    font-size: 1rem;
    line-height: 1.65;
    font-family: 'Inter', sans-serif;
}}

/* takeaways */
.takeaway-list {{
    max-width: 820px; margin: 3rem auto;
    padding: 0 2rem;
}}
.takeaway {{
    display: grid;
    grid-template-columns: 4rem 1fr;
    gap: 2rem;
    padding: 2rem 0;
    border-bottom: 1px solid {COLORS['border']};
}}
.takeaway:last-child {{ border-bottom: none; }}
.takeaway .tnum {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    color: {COLORS['accent']};
    padding-top: 0.4rem;
}}
.takeaway .tbody {{
    font-family: 'Fraunces', serif;
    font-size: 1.3rem;
    line-height: 1.5;
    color: {COLORS['text']};
    font-weight: 400;
}}
.takeaway .tbody em {{ color: {COLORS['accent']}; font-style: italic; font-weight: 500; }}

/* footer */
.story-footer {{
    text-align: center;
    padding: 5rem 2rem 3rem;
    color: {COLORS['text_3']};
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.15em;
    border-top: 1px solid {COLORS['border']};
    margin-top: 4rem;
}}

/* center each chart: a block with max-width + auto margins. the chart is
   responsive (use_container_width=True) so it fills this width and never
   gets clipped, it just resizes. margin auto centers it reliably. */
[data-testid="stPlotlyChart"] {{
    max-width: 880px;
    margin: 1.25rem auto 3.5rem !important;
    padding: 0 1.25rem;
    background: transparent !important;
    width: 100% !important;
    overflow: visible !important;
}}
[data-testid="stPlotlyChart"] > div,
[data-testid="stPlotlyChart"] .js-plotly-plot,
[data-testid="stPlotlyChart"] .plot-container,
[data-testid="stPlotlyChart"] .svg-container {{
    width: 100% !important;
    margin: 0 auto !important;
}}
.js-plotly-plot, .plot-container {{ background: transparent !important; }}

/* code snippets: centered, narrow, monospace, themed to the page */
[data-testid="stCode"], .stCode {{
    max-width: 760px;
    margin: 0.25rem auto 3rem !important;
    width: 100%;
}}
[data-testid="stCode"] pre, .stCode pre {{
    background: #111317 !important;
    border: 1px solid {COLORS['border']} !important;
    border-radius: 12px !important;
    padding: 1.1rem 1.25rem !important;
}}
[data-testid="stCode"] code, .stCode code,
[data-testid="stCode"] pre *, .stCode pre * {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
    line-height: 1.7 !important;
}}
.code-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: {COLORS['text_3']};
    text-align: center;
    margin: 2.5rem 0 0.5rem;
}}

/* download button, amber, centered. the element container and the button
   wrapper are both forced full-width so the flex centering has room to work. */
[data-testid="stDownloadButton"] {{
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
    margin: 1rem auto 1rem !important;
}}
[data-testid="stElementContainer"]:has([data-testid="stDownloadButton"]) {{
    width: 100% !important;
}}
[data-testid="stDownloadButton"] button {{
    background: {COLORS['accent']} !important;
    color: #1a1205 !important;
    border: none !important;
    border-radius: 999px !important;
    padding: 0.85rem 2.2rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
    transition: transform 200ms cubic-bezier(0.2,0.8,0.2,1), box-shadow 200ms ease !important;
    box-shadow: 0 8px 30px rgba(245,158,11,0.25) !important;
}}
[data-testid="stDownloadButton"] button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 40px rgba(245,158,11,0.4) !important;
    color: #1a1205 !important;
}}
[data-testid="stDownloadButton"] button p {{
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 600 !important;
}}

/* scroll-driven entry animations using view-timeline (Chrome 115+, Edge) */
@supports (animation-timeline: view()) {{
    [data-testid="stPlotlyChart"] {{
        animation: chartReveal linear both;
        animation-timeline: view();
        animation-range: entry 0% entry 65%;
    }}
    @keyframes chartReveal {{
        from {{ opacity: 0; transform: translateY(50px) scale(0.96); }}
        to   {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}
    .section-label, .section-title, .section-desc {{
        animation: textReveal linear both;
        animation-timeline: view();
        animation-range: entry 0% entry 55%;
    }}
    @keyframes textReveal {{
        from {{ opacity: 0; transform: translateY(28px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}
    .pullquote {{
        animation: quoteReveal linear both;
        animation-timeline: view();
        animation-range: entry 0% entry 70%;
    }}
    @keyframes quoteReveal {{
        from {{ opacity: 0; transform: translateY(40px); filter: blur(4px); }}
        to   {{ opacity: 1; transform: translateY(0); filter: blur(0); }}
    }}
    .chapter-num, .chapter h2 {{
        animation: chapterReveal linear both;
        animation-timeline: view();
        animation-range: entry 0% entry 60%;
    }}
    @keyframes chapterReveal {{
        from {{ opacity: 0; transform: translateY(30px); letter-spacing: 0.1em; }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}
    .bignum {{
        animation: numReveal linear both;
        animation-timeline: view();
        animation-range: entry 0% entry 60%;
    }}
    @keyframes numReveal {{
        from {{ opacity: 0; transform: translateY(24px) scale(0.94); }}
        to   {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}
    .cluster-card {{
        animation: cardReveal linear both;
        animation-timeline: view();
        animation-range: entry 0% entry 60%;
    }}
    @keyframes cardReveal {{
        from {{ opacity: 0; transform: translateY(32px) scale(0.95); }}
        to   {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}
    .step, .takeaway {{
        animation: rowReveal linear both;
        animation-timeline: view();
        animation-range: entry 0% entry 55%;
    }}
    @keyframes rowReveal {{
        from {{ opacity: 0; transform: translateX(-24px); }}
        to   {{ opacity: 1; transform: translateX(0); }}
    }}
    .solo-stat .v {{
        animation: bigStatReveal linear both;
        animation-timeline: view();
        animation-range: entry 0% entry 50%;
    }}
    @keyframes bigStatReveal {{
        from {{ opacity: 0; transform: scale(0.7); filter: blur(8px); }}
        to   {{ opacity: 1; transform: scale(1); filter: blur(0); }}
    }}
}}

/* streamlit elements that may leak through */
.stMarkdown, .stMarkdown p, .stMarkdown li {{
    color: {COLORS['text_2']};
}}
.stMarkdown a {{
    color: {COLORS['accent']};
}}
[data-testid="stCaptionContainer"] {{
    color: {COLORS['text_3']} !important;
    text-align: center;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.15em;
}}

/* page load reveal, applied once on initial paint */
.reveal {{
    animation: fadeUp 800ms cubic-bezier(0.2, 0.8, 0.2, 1) both;
}}
.reveal.delay-1 {{ animation-delay: 80ms; }}
.reveal.delay-2 {{ animation-delay: 160ms; }}
.reveal.delay-3 {{ animation-delay: 240ms; }}
.reveal.delay-4 {{ animation-delay: 320ms; }}

@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(18px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes scaleIn {{
    from {{ opacity: 0; transform: scale(0.85); }}
    to   {{ opacity: 1; transform: scale(1); }}
}}
@keyframes bounce {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(6px); }}
}}

@media (prefers-reduced-motion: reduce) {{
    *, *::before, *::after {{
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }}
}}
</style>

<div class="scroll-progress"></div>
        """,
        unsafe_allow_html=True,
    )
