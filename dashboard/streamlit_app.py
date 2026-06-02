"""
cameroon food prices, a scrollytelling data story.
single page, dark cinematic, scroll driven narrative.
"""
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix, silhouette_score
from sklearn.cluster import KMeans

from utils.style import inject_shell, COLORS, PLOTLY_TEMPLATE
from utils.data import (
    load_prices, summary_stats,
    train_classifier, fit_clusters, train_forecaster,
    build_bundle,
)


def code_block(label, snippet):
    """a small captioned code snippet, centered, used to surface the real
    notebook logic inside the story without breaking its flow."""
    st.markdown(f'<div class="code-label">{label}</div>', unsafe_allow_html=True)
    st.code(snippet, language="python")


st.set_page_config(
    page_title="cameroon food prices, a data story",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_shell()

df = load_prices()
s = summary_stats(df)

# ---------- hero ----------
st.markdown(
    """
<section class="hero">
    <div class="kicker">a data mining project</div>
    <h1>what 21 years of food prices say about <em>a country in flux</em></h1>
    <p class="lede">
        between 2005 and 2026, the world food programme tracked the price
        of everyday food in 76 markets across cameroon. this is what
        those numbers reveal.
    </p>
    <div class="meta">
        <span>cameroon</span>
        <span>2005 &mdash; 2026</span>
        <span>55,660 observations</span>
    </div>
    <div class="scroll-cue">scroll</div>
</section>
    """,
    unsafe_allow_html=True,
)

# ---------- prologue, the dataset ----------
st.markdown(
    """
<section class="chapter" data-chapter="00" data-chapter-name="prologue">
    <div class="chapter-head">
        <div class="chapter-num reveal">00 / prologue</div>
        <h2 class="reveal">first, the <em>numbers</em>.</h2>
    </div>
    <div class="prose reveal delay-1">
        <p>
            this story rests on a single csv file. it comes from the world
            food programme, the un agency that monitors hunger. in countries
            where food security is fragile, wfp tracks what a kilo of maize
            or a litre of palm oil costs in local markets, month after month.
        </p>
        <p>
            for cameroon, the file covers <strong>21 years</strong> and
            roughly <strong>75,000 raw price observations</strong>. after
            cleaning, <em>55,660 rows remain</em>. that's the body of evidence.
        </p>
    </div>
</section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="bignum-grid reveal">
    <div class="bignum">
        <div class="v">55,660</div>
        <div class="l">records</div>
    </div>
    <div class="bignum">
        <div class="v accent">9 / 10</div>
        <div class="l">regions covered</div>
    </div>
    <div class="bignum">
        <div class="v">76</div>
        <div class="l">markets</div>
    </div>
    <div class="bignum">
        <div class="v">51</div>
        <div class="l">commodities</div>
    </div>
    <div class="bignum">
        <div class="v accent">21</div>
        <div class="l">years of history</div>
    </div>
</div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="prose reveal" style="margin-top: 4rem;">
    <p>
        <strong>nine regions, not ten.</strong> that small gap is the first
        clue. cameroon has ten administrative regions but this dataset only
        covers nine. the missing one is <em>sud</em>, the south.
    </p>
    <p>
        wfp doesn't sample evenly. it follows need. its monitoring is
        concentrated where food insecurity is real, which means the far north
        (boko haram), the northwest and southwest (the anglophone conflict),
        and the east (refugees from the central african republic). the south
        is peaceful and well fed. that's why it isn't in the data.
        humanitarian datasets go where the crisis is.
    </p>
</div>
    """,
    unsafe_allow_html=True,
)

# ---------- chapter 01, the data ----------
st.markdown(
    """
<section class="chapter" data-chapter="01" data-chapter-name="the data">
    <div class="chapter-head">
        <div class="chapter-num reveal">01 / the data</div>
        <h2 class="reveal">before any model, you <em>look</em>.</h2>
    </div>
    <div class="prose reveal delay-1">
        <p>
            you look until the shape of the thing becomes familiar. you let
            the rows breathe. you build the simplest possible charts before
            you build anything clever.
        </p>
        <p>
            four shapes emerge.
        </p>
    </div>
</section>
    """,
    unsafe_allow_html=True,
)

# the code, from 01_data_exploration.ipynb
code_block(
    "from 01_data_exploration.ipynb",
    '''# load the wfp export and keep only retail prices
df = pd.read_csv("wfp_food_prices_cameroon.csv")
df = df[df["pricetype"] == "Retail"]
df = df[df["price"] > 0]                 # drop zero and negative prices
df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month

# 74,955 raw rows become 55,660 clean ones across 9 regions
df.shape''',
)

# chart 1, records by region
st.markdown(
    """
<div class="reveal">
<div class="section-label">first shape</div>
<div class="section-title">a map drawn by where people are hungry</div>
<div class="section-desc">
    extreme nord dominates the dataset by more than three to one. that's
    where boko haram has displaced nearly half a million people. wfp's
    monitoring intensity tells you, indirectly, where the crisis is.
</div>
</div>
    """,
    unsafe_allow_html=True,
)
region_counts = df["admin1"].value_counts().sort_values()
fig = go.Figure(go.Bar(
    x=region_counts.values, y=region_counts.index, orientation="h",
    marker=dict(color=[COLORS["accent"] if r == region_counts.idxmax() else COLORS["brand_2"]
                       for r in region_counts.index]),
    hovertemplate="<b>%{y}</b><br>%{x:,} records<extra></extra>",
))
fig.update_layout(PLOTLY_TEMPLATE["layout"], height=340,
                  xaxis_title="records", yaxis_title=None, showlegend=False)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# chart 2, the long climb
st.markdown(
    """
<div class="reveal">
<div class="section-label">second shape</div>
<div class="section-title">a long, slow climb, then a jump</div>
<div class="section-desc">
    national average price by year. the line drifts up for a decade and a
    half. then in 2020 it accelerates. covid, the russia ukraine war, and
    sustained inflation move the curve into different territory.
</div>
</div>
    """,
    unsafe_allow_html=True,
)
yearly = df.groupby("year")["price"].mean().reset_index()
fig = go.Figure(go.Scatter(
    x=yearly["year"], y=yearly["price"],
    mode="lines+markers",
    line=dict(color=COLORS["accent"], width=2.5, shape="spline", smoothing=0.8),
    marker=dict(size=7, color=COLORS["accent"],
                line=dict(width=1.5, color=COLORS["bg"])),
    fill="tozeroy",
    fillcolor="rgba(245, 158, 11, 0.08)",
    hovertemplate="<b>%{x}</b><br>%{y:.0f} xaf avg<extra></extra>",
))
fig.add_vrect(x0=2019.5, x1=yearly["year"].max() + 0.5,
              fillcolor=COLORS["bad"], opacity=0.06,
              line_width=0, annotation_text="post 2020 inflation",
              annotation_position="top left",
              annotation_font_color=COLORS["text_3"], annotation_font_size=10)
fig.update_layout(PLOTLY_TEMPLATE["layout"], height=340,
                  yaxis_title="average price, xaf", xaxis_title=None)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# chart 3, monthly seasonality
st.markdown(
    """
<div class="reveal">
<div class="section-label">third shape</div>
<div class="section-title">every year, the lean season</div>
<div class="section-desc">
    average price by month, pooled across all years. june, july and august
    sit above the line. last year's harvest is exhausted, this year's isn't
    ready. it's the most predictable annual stress point in the data.
</div>
</div>
    """,
    unsafe_allow_html=True,
)
month_avg = df.groupby("month")["price"].mean()
months = ["jan", "feb", "mar", "apr", "may", "jun",
          "jul", "aug", "sep", "oct", "nov", "dec"]
colors = [COLORS["accent"] if m in [6, 7, 8] else COLORS["brand_2"]
          for m in range(1, 13)]
fig = go.Figure(go.Bar(
    x=months, y=month_avg.values, marker_color=colors,
    hovertemplate="<b>%{x}</b><br>%{y:.0f} xaf<extra></extra>",
))
fig.add_hline(y=month_avg.mean(), line_dash="dash",
              line_color=COLORS["text_3"], annotation_text="annual mean",
              annotation_position="top right",
              annotation_font_color=COLORS["text_3"])
fig.update_layout(PLOTLY_TEMPLATE["layout"], height=320,
                  yaxis_title="average price, xaf", xaxis_title=None,
                  showlegend=False)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# chart 4, top commodities
st.markdown(
    """
<div class="reveal">
<div class="section-label">fourth shape</div>
<div class="section-title">imports cost, staples don't</div>
<div class="section-desc">
    the ten most expensive items per kilo or litre on average. imported and
    processed goods sit at the top, local staples at the bottom. this is the
    geography of a food economy that still pays a premium for what it doesn't
    make at home.
</div>
</div>
    """,
    unsafe_allow_html=True,
)
top10 = df.groupby("commodity")["price"].mean().sort_values(ascending=False).head(10).sort_values()
fig = go.Figure(go.Bar(
    x=top10.values, y=top10.index, orientation="h",
    marker=dict(color=COLORS["accent"], line=dict(color=COLORS["bg"], width=2)),
    hovertemplate="<b>%{y}</b><br>%{x:,.0f} xaf<extra></extra>",
))
fig.update_layout(PLOTLY_TEMPLATE["layout"], height=340,
                  xaxis_title="average price, xaf", yaxis_title=None)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# transition pull quote
st.markdown(
    """
<div class="pullquote reveal">
    these four shapes are the foundation. now we ask
    <span class="accent">harder questions.</span>
</div>
    """,
    unsafe_allow_html=True,
)

# ---------- chapter 02, classification ----------
with st.spinner("training classifier"):
    rc = train_classifier(df)

st.markdown(
    """
<section class="chapter" data-chapter="02" data-chapter-name="classification">
    <div class="chapter-head">
        <div class="chapter-num reveal">02 / classification</div>
        <h2 class="reveal">can a model tell a <em>low price</em> from a <em>high one</em>?</h2>
    </div>
    <div class="prose reveal delay-1">
        <p>
            we labelled every price in the dataset using percentile thresholds.
            for each commodity, the cheapest third becomes <strong>low</strong>,
            the middle third <strong>medium</strong>, the top third
            <strong>high</strong>. expensive maize is judged against other maize,
            not against caviar.
        </p>
        <p>
            then we trained a random forest, a crowd of two hundred small
            decision trees that vote. the question is simple: given the region,
            the commodity, the date, the location, and a sense of recent prices,
            can it guess the right tier?
        </p>
    </div>
</section>
    """,
    unsafe_allow_html=True,
)

# the code, from 02_classification.ipynb
code_block(
    "from 02_classification.ipynb",
    '''# label each price against its OWN commodity's history, not all food
thresh = df.groupby("commodity")["price"].quantile([.33, .66]).unstack()
df["cls"] = "Medium"
df.loc[df.price <= thresh[.33], "cls"] = "Low"
df.loc[df.price >  thresh[.66], "cls"] = "High"

# the features that moved the needle: recent and yearly median price
df["commod_recent_med"] = (df.groupby("commodity")["price"]
    .transform(lambda s: s.shift(1).rolling(50, min_periods=1).median()))

rf = RandomForestClassifier(n_estimators=200, max_depth=15, n_jobs=-1)
rf.fit(X_train, y_train)                 # 0.77 accuracy on the test set''',
)

# 64 → 77 improvement
st.markdown(
    """
<div class="reveal">
<div class="section-label">the arc</div>
<div class="section-title">from 64 percent to 77 percent</div>
<div class="section-desc">
    the first pass used five basic features and got 63 percent. adding four
    more features pushed it to 77. same model. better features.
</div>
</div>
    """,
    unsafe_allow_html=True,
)
fig = go.Figure(go.Bar(
    x=["always guess medium", "basic features", "rich features"],
    y=[35.5, 63.2, rc["accuracy"] * 100],
    marker=dict(color=[COLORS["text_3"], COLORS["brand_2"], COLORS["accent"]]),
    text=[f"{v:.1f}%" for v in [35.5, 63.2, rc["accuracy"] * 100]],
    textposition="outside",
    textfont=dict(family="JetBrains Mono", color=COLORS["text"], size=15),
    hovertemplate="<b>%{x}</b><br>%{y:.1f}%<extra></extra>",
))
fig.update_layout(PLOTLY_TEMPLATE["layout"], height=320,
                  yaxis=dict(title="accuracy", range=[0, 90],
                             ticksuffix="%"),
                  xaxis_title=None, showlegend=False, bargap=0.4)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# big solo stat
st.markdown(
    f"""
<div class="solo-stat reveal">
    <div class="v">{rc['accuracy']*100:.1f}%</div>
    <div class="l">accuracy on the held out test set. that's roughly 41 points above the baseline.</div>
</div>
    """,
    unsafe_allow_html=True,
)

# confusion matrix
st.markdown(
    """
<div class="reveal">
<div class="section-label">where the model wins, and where it slips</div>
<div class="section-title">the confusion matrix</div>
<div class="section-desc">
    each row is what actually happened, each column is what the model guessed.
    the diagonal is where it gets it right. notice the medium class is hardest.
    prices on the boundary easily flip into the neighbouring class.
</div>
</div>
    """,
    unsafe_allow_html=True,
)
cm = confusion_matrix(rc["y_test"], rc["y_pred"])
labels = rc["classes"]
fig = go.Figure(go.Heatmap(
    z=cm, x=labels, y=labels,
    text=cm, texttemplate="%{text}",
    textfont=dict(size=20, color=COLORS["text"], family="JetBrains Mono"),
    colorscale=[[0, COLORS["surface"]], [0.5, COLORS["brand"]], [1, COLORS["accent"]]],
    showscale=False,
    hovertemplate="actual <b>%{y}</b><br>predicted <b>%{x}</b><br>%{z} rows<extra></extra>",
))
fig.update_layout(PLOTLY_TEMPLATE["layout"], height=340,
                  xaxis_title="predicted", yaxis_title="actual",
                  xaxis=dict(side="top"))
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# feature importance
st.markdown(
    """
<div class="reveal">
<div class="section-label">what the model paid attention to</div>
<div class="section-title">historical context beat geography</div>
<div class="section-desc">
    feature importance from the trained forest. the historical commodity price
    features, the ones that tell the model about inflation, did most of the work.
    region and month helped, but secondarily.
</div>
</div>
    """,
    unsafe_allow_html=True,
)
imp = rc["importances"].tail(10)
fig = go.Figure(go.Bar(
    x=imp.values, y=imp.index, orientation="h",
    marker=dict(color=COLORS["accent"]),
    hovertemplate="<b>%{y}</b><br>importance %{x:.3f}<extra></extra>",
))
fig.update_layout(PLOTLY_TEMPLATE["layout"], height=340,
                  xaxis_title="importance", yaxis_title=None)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

st.markdown(
    """
<div class="pullquote reveal">
    so prices are <span class="accent">learnable</span>. but where they sit on
    the map turns out to be a different question.
</div>
    """,
    unsafe_allow_html=True,
)

# ---------- chapter 03, clusters ----------
with st.spinner("clustering markets"):
    rcl = fit_clusters(df, k=4)

st.markdown(
    """
<section class="chapter" data-chapter="03" data-chapter-name="clusters">
    <div class="chapter-head">
        <div class="chapter-num reveal">03 / clusters</div>
        <h2 class="reveal">forget regions. let the <em>data</em> draw the map.</h2>
    </div>
    <div class="prose reveal delay-1">
        <p>
            if we strip away the administrative labels and look only at what
            each of the 76 markets charges for each commodity, do natural
            groups emerge?
        </p>
        <p>
            we asked k means. it's the simplest clustering algorithm in
            existence. you give it a number k and it groups your data points
            into k clumps, putting similar points together. no labels, no
            supervision. just distance.
        </p>
        <p>
            to choose k we used two methods together. the <strong>elbow
            method</strong> looks for the bend in a curve. the
            <strong>silhouette score</strong> measures how cleanly the clusters
            separate. both pointed at four.
        </p>
    </div>
</section>
    """,
    unsafe_allow_html=True,
)

# the code, from 03_clustering.ipynb
code_block(
    "from 03_clustering.ipynb",
    '''# one row per market, one column per commodity, filled with median price
pivot = df.pivot_table(index="market", columns="commodity",
                       values="price", aggfunc="median")
pivot = pivot.dropna(thresh=int(0.3 * len(pivot)), axis=1)
X = StandardScaler().fit_transform(pivot.fillna(pivot.median()))

# k means is told nothing about geography. it only sees prices.
km = KMeans(n_clusters=4, n_init=20, random_state=42)
pivot["cluster"] = km.fit_predict(X)     # four groups emerge''',
)

# elbow + silhouette side by side as a single figure
inertias = []
sil_scores = []
ks = list(range(2, 11))
for k in ks:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    lbl = km.fit_predict(rcl["X"])
    inertias.append(km.inertia_)
    sil_scores.append(silhouette_score(rcl["X"], lbl))

from plotly.subplots import make_subplots
fig = make_subplots(rows=1, cols=2,
                    subplot_titles=("elbow method", "silhouette score"))
fig.add_trace(go.Scatter(
    x=ks, y=inertias, mode="lines+markers",
    line=dict(color=COLORS["accent"], width=2.5),
    marker=dict(size=8, color=COLORS["accent"], line=dict(width=1.5, color=COLORS["bg"])),
    hovertemplate="k=%{x}<br>inertia %{y:.1f}<extra></extra>",
    showlegend=False,
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=ks, y=sil_scores, mode="lines+markers",
    line=dict(color=COLORS["blue"], width=2.5),
    marker=dict(size=8, color=COLORS["blue"], line=dict(width=1.5, color=COLORS["bg"])),
    hovertemplate="k=%{x}<br>silhouette %{y:.3f}<extra></extra>",
    showlegend=False,
), row=1, col=2)
fig.add_vline(x=4, line_dash="dash", line_color=COLORS["text_3"],
              annotation_text="k=4", annotation_font_color=COLORS["text_3"],
              row=1, col=1)
fig.add_vline(x=4, line_dash="dash", line_color=COLORS["text_3"], row=1, col=2)
fig.update_layout(PLOTLY_TEMPLATE["layout"], height=300)
fig.update_xaxes(title_text="k", gridcolor="rgba(255,255,255,0.04)")
fig.update_yaxes(gridcolor="rgba(255,255,255,0.04)")
for ann in fig["layout"]["annotations"]:
    ann["font"] = dict(family="Fraunces", size=14, color=COLORS["text_2"])
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# pca scatter
st.markdown(
    """
<div class="reveal">
<div class="section-label">76 markets in a flat plane</div>
<div class="section-title">four groups, drawn without supervision</div>
<div class="section-desc">
    pca compresses the 38 dimensions (one per commodity) down to two so we can
    see them. each dot is a market, coloured by its cluster. hover any dot.
</div>
</div>
    """,
    unsafe_allow_html=True,
)
pivot = rcl["pivot"]
coords = rcl["coords"]
cluster_names = {
    0: "far north conflict zone",
    1: "urban commercial hubs",
    2: "anglophone southwest",
    3: "eastern refugee corridor",
}
cluster_colors_map = {0: COLORS["bad"], 1: COLORS["accent"],
                      2: COLORS["blue"], 3: COLORS["ok"]}
fig = go.Figure()
for c in sorted(pivot["cluster"].unique()):
    mask = pivot["cluster"] == c
    markets = pivot.index[mask].tolist()
    fig.add_trace(go.Scatter(
        x=coords[mask, 0], y=coords[mask, 1], mode="markers",
        marker=dict(size=13, color=cluster_colors_map[c],
                    line=dict(color=COLORS["bg"], width=2),
                    opacity=0.92),
        name=f"{c:02d} &nbsp; {cluster_names[c]}",
        text=markets,
        hovertemplate="<b>%{text}</b><br>" + cluster_names[c] + "<extra></extra>",
    ))
fig.update_layout(PLOTLY_TEMPLATE["layout"], height=440,
                  xaxis_title=f"pca 1 ({rcl['ev'][0]*100:.1f}% variance)",
                  yaxis_title=f"pca 2 ({rcl['ev'][1]*100:.1f}% variance)",
                  legend=dict(orientation="h", yanchor="bottom", y=1.02,
                              x=0, font=dict(family="JetBrains Mono", size=11)))
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# the reveal
st.markdown(
    """
<div class="pullquote reveal">
    k means didn't know anything about politics or conflict.<br>
    it only saw prices. and it <span class="accent">drew this map</span>.
</div>
    """,
    unsafe_allow_html=True,
)

# cluster cards
cluster_info = [
    (0, "far north conflict zone", COLORS["bad"],
     "northern markets where boko haram has restricted supply. cereals and pulses are elevated. fish is scarce and expensive.",
     "amchidé, fotokol, garoua, maroua"),
    (1, "urban commercial hubs", COLORS["accent"],
     "the big cities. wide commodity range, lower volatility, stable trade networks linking the country to its ports.",
     "bafoussam, bamenda, douala bonaberi, yaoundé"),
    (2, "anglophone southwest", COLORS["blue"],
     "coastal and forest zone markets caught in the anglophone civil conflict. fish more available, road access disrupted.",
     "buea, kumba, limbé, mamfé"),
    (3, "eastern refugee corridor", COLORS["ok"],
     "eastern markets near the central african republic border, absorbing refugee inflow and elevated demand.",
     "bertoua, garoua boulaï, batouri"),
]
cards = ""
for cid, name, color, desc, examples in cluster_info:
    cards += f"""
    <div class="cluster-card reveal" style="border-left-color: {color};">
        <div class="cnum" style="color: {color};">cluster {cid:02d}</div>
        <div class="ctitle">{name}</div>
        <div class="cdesc">{desc}</div>
        <div class="cexamples">includes: {examples}</div>
    </div>"""
st.markdown(f'<div class="cluster-grid">{cards}</div>', unsafe_allow_html=True)

st.markdown(
    """
<div class="prose reveal" style="margin-top: 3rem;">
    <p>
        the four clusters map cleanly onto the three humanitarian response
        zones that actually exist in cameroon, plus the country's stable urban
        core. <em>prices alone told us where the crises are.</em>
    </p>
</div>
    """,
    unsafe_allow_html=True,
)

# ---------- chapter 04, forecasting ----------
with st.spinner("training forecaster"):
    rf = train_forecaster(df)

st.markdown(
    """
<section class="chapter" data-chapter="04" data-chapter-name="forecasting">
    <div class="chapter-head">
        <div class="chapter-num reveal">04 / forecasting</div>
        <h2 class="reveal">how well can we see <em>one month ahead</em>?</h2>
    </div>
    <div class="prose reveal delay-1">
        <p>
            a first attempt at forecasting maize prices got an r squared of
            about <strong>0.48</strong>. honest, but unimpressive. r squared
            measures how much of the variation you can explain. half is not
            enough to plan on.
        </p>
        <p>
            three changes pushed it to <em>0.94 across the top ten commodities</em>.
        </p>
    </div>
</section>
    """,
    unsafe_allow_html=True,
)

# the code, from 04_prediction.ipynb
code_block(
    "from 04_prediction.ipynb",
    '''# predict LOG price so a 10% move counts the same on cheap and dear items
mo["logp"] = np.log(mo["price"])
for lag in range(1, 7):                  # last six months as features
    mo[f"lag_{lag}"] = mo.groupby("commodity")["logp"].shift(lag)

# trees that learn from each other's mistakes, on the top 10 commodities
model = HistGradientBoostingRegressor(
    max_iter=500, max_depth=8, learning_rate=0.05, random_state=42)
model.fit(train[feat], train["logp"])    # pooled r2 = 0.94''',
)

# steps
st.markdown(
    """
<div class="steps reveal">
    <div class="step">
        <div class="step-num">01</div>
        <div class="step-body">
            <div class="stitle">use more data</div>
            <div class="sbody">
                training on the top ten commodities instead of just maize gave
                the model ten times more rows to learn from. the same model
                gets smarter with more data, even when that data is about
                slightly different things.
            </div>
        </div>
    </div>
    <div class="step">
        <div class="step-num">02</div>
        <div class="step-body">
            <div class="stitle">predict log price, not price</div>
            <div class="sbody">
                food prices move in percentages. a ten percent rise on a 100
                xaf item is 10 xaf, but on a 1000 xaf item it's 100 xaf. logging
                the target lets the model treat both rises as the same kind of move.
            </div>
        </div>
    </div>
    <div class="step">
        <div class="step-num">03</div>
        <div class="step-body">
            <div class="stitle">use gradient boosting</div>
            <div class="sbody">
                where a random forest is a crowd of trees voting independently,
                gradient boosting is a sequence of trees that learn from each
                other's mistakes. for time series with trend and seasonality,
                this almost always wins.
            </div>
        </div>
    </div>
</div>
    """,
    unsafe_allow_html=True,
)

# big stat
st.markdown(
    f"""
<div class="solo-stat reveal">
    <div class="v">{rf['r2']:.3f}</div>
    <div class="l">r squared across the top ten commodities. the model explains 94 percent of the month to month variation in cameroon's food economy.</div>
</div>

<div class="bignum-grid reveal">
    <div class="bignum">
        <div class="v accent">{rf['mape']:.1f}%</div>
        <div class="l">mean abs % error</div>
    </div>
    <div class="bignum">
        <div class="v">{rf['mae']:.0f} xaf</div>
        <div class="l">mean abs error</div>
    </div>
    <div class="bignum">
        <div class="v accent">{len(rf['top10'])}</div>
        <div class="l">commodities forecast</div>
    </div>
    <div class="bignum">
        <div class="v">{rf['test']['date'].nunique()}</div>
        <div class="l">test months</div>
    </div>
</div>
    """,
    unsafe_allow_html=True,
)

# actual vs predicted maize
st.markdown(
    """
<div class="reveal">
<div class="section-label">test period</div>
<div class="section-title">actual vs predicted, maize white</div>
<div class="section-desc">
    the orange dashed line is the model. the solid line is what the country
    actually paid. the test period covers the post 2020 inflation wave, the
    hardest possible test for a price model.
</div>
</div>
    """,
    unsafe_allow_html=True,
)
maize_test = rf["test"][rf["test"]["commodity"] == "Maize (white)"].sort_values("date")
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=maize_test["date"], y=maize_test["price"], mode="lines", name="actual",
    line=dict(color=COLORS["text"], width=2.3),
    hovertemplate="%{x|%b %Y}<br>actual %{y:.0f} xaf<extra></extra>",
))
fig.add_trace(go.Scatter(
    x=maize_test["date"], y=maize_test["pred"], mode="lines", name="predicted",
    line=dict(color=COLORS["accent"], width=2.3, dash="dot"),
    hovertemplate="%{x|%b %Y}<br>predicted %{y:.0f} xaf<extra></extra>",
))
fig.update_layout(PLOTLY_TEMPLATE["layout"], height=340,
                  yaxis_title="price, xaf", xaxis_title=None,
                  legend=dict(orientation="h", yanchor="bottom", y=1.02))
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# per commodity performance
st.markdown(
    """
<div class="reveal">
<div class="section-label">where the model excels, and where it struggles</div>
<div class="section-title">accuracy varies by commodity</div>
<div class="section-desc">
    r squared per commodity. staples that are tracked everywhere (maize, beans,
    rice) sit at the top. less tracked items, with fewer training rows, lag
    behind. that's not a model problem, it's a data problem.
</div>
</div>
    """,
    unsafe_allow_html=True,
)
per = rf["per_commodity"].sort_values("r2")
bar_colors = [COLORS["bad"] if r < 0 else (COLORS["accent"] if r > 0.5 else COLORS["warn"])
              for r in per["r2"]]
fig = go.Figure(go.Bar(
    x=per["r2"], y=per["commodity"], orientation="h",
    marker=dict(color=bar_colors),
    text=[f"{r:.2f}" for r in per["r2"]],
    textposition="outside",
    textfont=dict(family="JetBrains Mono", color=COLORS["text"], size=12),
    hovertemplate="<b>%{y}</b><br>r2 = %{x:.3f}<extra></extra>",
))
fig.add_vline(x=0, line_color=COLORS["text_3"], line_width=1)
fig.update_layout(PLOTLY_TEMPLATE["layout"], height=380,
                  xaxis_title="r squared", yaxis_title=None,
                  xaxis=dict(range=[per["r2"].min() - 0.5, 1.1]))
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

st.markdown(
    """
<div class="pullquote reveal">
    the model can forecast next month. but to plan for next year, you have
    to know <span class="accent">where the shocks come from</span>.
</div>
    """,
    unsafe_allow_html=True,
)

# ---------- chapter 05, patterns ----------
st.markdown(
    """
<section class="chapter" data-chapter="05" data-chapter-name="patterns">
    <div class="chapter-head">
        <div class="chapter-num reveal">05 / patterns</div>
        <h2 class="reveal">when the system <em>cracked</em>.</h2>
    </div>
    <div class="prose reveal delay-1">
        <p>
            this last chapter doesn't train a model. it just looks. it asks
            which years saw the biggest moves, which commodities are the most
            unstable, and where the country splits between rich market and
            poor.
        </p>
    </div>
</section>
    """,
    unsafe_allow_html=True,
)

# the code, from 05_pattern_discovery.ipynb
code_block(
    "from 05_pattern_discovery.ipynb",
    '''# flag any year whose move is more than two std devs from the norm
yoy = df.groupby("year")["price"].mean().pct_change() * 100
anomalies = yoy[yoy > yoy.mean() + 2 * yoy.std()]   # 2008 and 2022

# coefficient of variation ranks how unstable each commodity is
g = df.groupby("commodity")["price"]
cv = (g.std() / g.mean()).sort_values(ascending=False)''',
)

# yoy shocks
yearly_p = df.groupby("year")["price"].mean()
yoy = (yearly_p.pct_change() * 100).dropna()
mean_c = yoy.mean()
std_c = yoy.std()
threshold = mean_c + 2 * std_c

st.markdown(
    """
<div class="reveal">
<div class="section-label">year over year</div>
<div class="section-title">2008 and 2022, the shock years</div>
<div class="section-desc">
    every bar is the percent change from the previous year. amber bars cross
    the two sigma threshold, what statisticians call a real anomaly. 2008 was
    the global food price crisis. 2022 was the post covid wave plus the russia
    ukraine war on grain.
</div>
</div>
    """,
    unsafe_allow_html=True,
)
bc = [COLORS["accent"] if v > threshold else (COLORS["bad"] if v > 0 else COLORS["ok"])
      for v in yoy.values]
fig = go.Figure(go.Bar(
    x=yoy.index.astype(int), y=yoy.values, marker_color=bc,
    text=[f"{v:+.0f}%" for v in yoy.values],
    textposition="outside",
    textfont=dict(family="JetBrains Mono", color=COLORS["text_2"], size=10),
    hovertemplate="<b>%{x}</b><br>%{y:+.1f}%<extra></extra>",
))
fig.add_hline(y=0, line_color=COLORS["text_3"], line_width=1)
fig.add_hline(y=threshold, line_dash="dash", line_color=COLORS["accent"],
              annotation_text="anomaly threshold",
              annotation_font_color=COLORS["accent"])
fig.update_layout(PLOTLY_TEMPLATE["layout"], height=340,
                  yaxis_title="year over year %", xaxis_title=None,
                  showlegend=False, bargap=0.25)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# volatility
cv = df.groupby("commodity")["price"].agg(["std", "mean"])
cv["cv"] = cv["std"] / cv["mean"]
cv = cv.sort_values("cv", ascending=False).head(12).sort_values("cv")

st.markdown(
    """
<div class="reveal">
<div class="section-label">volatility ranking</div>
<div class="section-title">animal products and oils are wildest</div>
<div class="section-desc">
    coefficient of variation, the standard deviation divided by the mean.
    higher means more unpredictable. cereals are partly stabilised by
    government policy. animal products and oils are not, and it shows.
</div>
</div>
    """,
    unsafe_allow_html=True,
)
fig = go.Figure(go.Bar(
    x=cv["cv"], y=cv.index, orientation="h",
    marker=dict(color=COLORS["bad"]),
    text=[f"{v:.2f}" for v in cv["cv"]],
    textposition="outside",
    textfont=dict(family="JetBrains Mono", color=COLORS["text_2"], size=11),
    hovertemplate="<b>%{y}</b><br>cv %{x:.2f}<extra></extra>",
))
fig.add_vline(x=0.30, line_dash="dash", line_color=COLORS["accent"],
              annotation_text="cv = 0.30", annotation_font_color=COLORS["accent"])
fig.update_layout(PLOTLY_TEMPLATE["layout"], height=380,
                  xaxis_title="coefficient of variation", yaxis_title=None)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# regions
region_avg = df.groupby("admin1")["price"].mean().sort_values()
st.markdown(
    """
<div class="reveal">
<div class="section-label">geographic divide</div>
<div class="section-title">where food costs the most</div>
<div class="section-desc">
    the far north and adamaoua sit at the top despite being the poorest
    regions, because supply is fragile and roads are bad. the centre is
    cheapest, because it grows most of what the country eats.
</div>
</div>
    """,
    unsafe_allow_html=True,
)
fig = go.Figure(go.Bar(
    x=region_avg.values, y=region_avg.index, orientation="h",
    marker=dict(color=region_avg.values,
                colorscale=[[0, COLORS["ok"]], [0.5, COLORS["warn"]], [1, COLORS["bad"]]],
                showscale=False),
    text=[f"{v:.0f}" for v in region_avg.values],
    textposition="outside",
    textfont=dict(family="JetBrains Mono", color=COLORS["text_2"], size=12),
    hovertemplate="<b>%{y}</b><br>%{x:.0f} xaf avg<extra></extra>",
))
fig.update_layout(PLOTLY_TEMPLATE["layout"], height=340,
                  xaxis_title="average price, xaf", yaxis_title=None)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ---------- conclusion ----------
st.markdown(
    """
<section class="chapter" data-chapter="06" data-chapter-name="conclusion">
    <div class="chapter-head">
        <div class="chapter-num reveal">06 / conclusion</div>
        <h2 class="reveal">what the <em>data</em> said.</h2>
    </div>
</section>

<div class="takeaway-list">
    <div class="takeaway reveal">
        <div class="tnum">01</div>
        <div class="tbody">
            food prices in cameroon are <em>structured, not chaotic</em>. a
            classifier reads them at 77 percent accuracy. a forecaster gets
            0.94 r squared. that's evidence of order.
        </div>
    </div>
    <div class="takeaway reveal delay-1">
        <div class="tnum">02</div>
        <div class="tbody">
            the biggest predictor isn't where, it's <em>when</em>. recent
            history and inflation context beat geography for guessing the
            next price.
        </div>
    </div>
    <div class="takeaway reveal delay-2">
        <div class="tnum">03</div>
        <div class="tbody">
            markets quietly <em>map onto the country's crisis geography</em>.
            four clusters emerge from prices alone and line up with the three
            humanitarian response zones plus the stable urban core.
        </div>
    </div>
    <div class="takeaway reveal delay-3">
        <div class="tnum">04</div>
        <div class="tbody">
            <em>2008 and 2022</em> were the system shocks of this century.
            the global food crisis and the post covid wave both showed up
            cleanly without anyone labelling them.
        </div>
    </div>
</div>

<div class="pullquote reveal" style="margin-top: 5rem; margin-bottom: 3rem;">
    five chapters, four takeaways, one quiet conclusion:
    <span class="accent">numbers, given time, will tell on the world.</span>
</div>
    """,
    unsafe_allow_html=True,
)

# ---------- download bundle ----------
st.markdown(
    """
<div class="reveal" style="text-align:center; max-width:640px; margin:2rem auto 0; padding:0 2rem;">
    <div class="section-label" style="margin-top:0;">take it with you</div>
    <div class="section-title" style="max-width:30ch;">the whole project, in one download</div>
    <div class="section-desc">
        the five jupyter notebooks, the cleaned dataset, the original raw
        export, and the full written report, zipped together. everything
        behind this story.
    </div>
</div>
    """,
    unsafe_allow_html=True,
)
st.download_button(
    label="download the full project  (.zip)",
    data=build_bundle(),
    file_name="cameroon_food_prices_project.zip",
    mime="application/zip",
)

st.markdown(
    """
<div class="story-footer">
    source &middot; world food programme price data for cameroon &middot;
    2005 to 2026 &middot; 55,660 cleaned observations
</div>
    """,
    unsafe_allow_html=True,
)
