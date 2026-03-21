"""
Analysis of What Makes a Video Game Successful
================================================
Steam Trends 2023 dataset – 61,216 games
Success metric: Revenue Estimated
"""

import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="What Makes a Video Game Successful?",
    layout="wide",
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "dataIN", "Steam Trends 2023.csv")


# ══════════════════════════════════════════════════════════════════════════════
# Data loading & cleaning
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner="Loading and cleaning dataset...")
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Revenue Estimated: strip $, commas, whitespace
    df["Revenue Estimated"] = (
        df["Revenue Estimated"]
        .astype(str)
        .str.replace(r"[\$,\s]", "", regex=True)
        .replace("nan", np.nan)
        .astype(float)
    )

    # Launch Price: same treatment; map free-to-play strings to 0
    df["Launch Price"] = (
        df["Launch Price"]
        .astype(str)
        .str.replace(r"[\$,\s]", "", regex=True)
        .replace({"nan": np.nan, "Free": "0", "FreeToPlay": "0"})
        .astype(float)
    )

    # Reviews Score Fancy: strip %
    df["Reviews Score Fancy"] = (
        df["Reviews Score Fancy"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .replace("nan", np.nan)
        .astype(float)
    )

    # Reviews Total: force numeric
    df["Reviews Total"] = pd.to_numeric(df["Reviews Total"], errors="coerce")

    # Release Year: parse date then extract year
    df["Release Date"] = pd.to_datetime(df["Release Date"], dayfirst=True, errors="coerce")
    df["Release Year"] = df["Release Date"].dt.year.astype("Int64")
    df["Release Date"] = df["Release Date"].dt.date

    # Keep only rows with positive revenue
    df = df.dropna(subset=["Revenue Estimated"])
    df = df[df["Revenue Estimated"] > 0].reset_index(drop=True)

    return df


df = load_data(DATA_PATH)

# ══════════════════════════════════════════════════════════════════════════════
# App
# ══════════════════════════════════════════════════════════════════════════════
st.title("What Makes a Video Game Successful?")
st.markdown(
    f"**Dataset:** Steam Trends 2023 &nbsp;|&nbsp; "
    f"**Games after cleaning:** {len(df):,} &nbsp;|&nbsp; "
    f"**Total estimated revenue:** ${df['Revenue Estimated'].sum() / 1e9:.2f}B"
)

st.subheader("Cleaned Data Preview")
st.dataframe(df[["Title", "Revenue Estimated", "Reviews Total", "Reviews Score Fancy",
                  "Launch Price", "Release Date", "Release Year", "Tags"]].head(50),
             use_container_width=True)

st.subheader("Descriptive Statistics")
st.dataframe(
    df[["Revenue Estimated", "Reviews Total", "Reviews Score Fancy", "Launch Price"]]
    .describe()
    .round(2),
    use_container_width=True,
)

# ══════════════════════════════════════════════════════════════════════════════
# Section 1 – Geospatial: Revenue by Region (GeoPandas)
# ══════════════════════════════════════════════════════════════════════════════
st.header("Global Revenue Distribution")
st.markdown(
    "Revenue is distributed using **real market share data from Newzoo** for the top 10 gaming markets. "
    "The remaining 15 % of the global market (countries outside the top 10) is distributed "
    "proportionally by population — a hybrid approach between real data and population proxy."
)


@st.cache_data(show_spinner="Building choropleth map...")
def build_choropleth(total_revenue: float):
    import geopandas as gpd

    NE_URL = (
        "https://naciscdn.org/naturalearth/110m/cultural/"
        "ne_110m_admin_0_countries.zip"
    )
    world = gpd.read_file(NE_URL)

    # Newzoo top-10 gaming markets (USD billions).
    # Top-10 total = $154.6B, assumed to represent ~82% of the global market.
    # Each country's share = their revenue / ($154.6B / 0.85).
    GLOBAL_TOTAL_B = 188.8  # Newzoo global games market total (USD billions)
    TOP10_SHARES = {
        "China":                    53.2 / GLOBAL_TOTAL_B,
        "United States of America": 49.8 / GLOBAL_TOTAL_B,
        "Japan":                    17.6 / GLOBAL_TOTAL_B,
        "South Korea":               7.8 / GLOBAL_TOTAL_B,
        "Germany":                   7.0 / GLOBAL_TOTAL_B,
        "United Kingdom":            6.6 / GLOBAL_TOTAL_B,
        "France":                    4.1 / GLOBAL_TOTAL_B,
        "Canada":                    3.1 / GLOBAL_TOTAL_B,
        "Brazil":                    2.7 / GLOBAL_TOTAL_B,
        "Mexico":                    2.7 / GLOBAL_TOTAL_B,
    }
    REST_OF_WORLD_SHARE = 1.0 - sum(TOP10_SHARES.values())  # ~18 %

    # Population of countries outside the top 10 (used to split the residual share)
    top10_names = set(TOP10_SHARES.keys())
    rest_pop = world.loc[~world["NAME"].isin(top10_names), "POP_EST"].sum()

    def assign_revenue(row):
        name = row["NAME"]
        if name in TOP10_SHARES:
            return TOP10_SHARES[name] * total_revenue
        pop = row["POP_EST"]
        if rest_pop == 0 or pop <= 0:
            return 0.0
        return REST_OF_WORLD_SHARE * total_revenue * (pop / rest_pop)

    world["simulated_revenue"] = world.apply(assign_revenue, axis=1)
    return world


world_gdf = build_choropleth(float(df["Revenue Estimated"].sum()))

fig_map, ax_map = plt.subplots(1, 1, figsize=(14, 7))
world_gdf.plot(
    column="simulated_revenue",
    ax=ax_map,
    legend=True,
    legend_kwds={
        "label": "Simulated Revenue (USD)",
        "orientation": "horizontal",
        "shrink": 0.6,
    },
    cmap="YlOrRd",
    missing_kwds={"color": "lightgrey", "label": "No data"},
    linewidth=0.3,
    edgecolor="0.5",
)
ax_map.set_title("Video-Game Revenue by Country (Newzoo top 10 real shares + population proxy for rest of world)", fontsize=13, pad=12)
ax_map.axis("off")
st.pyplot(fig_map)
plt.close(fig_map)

# ══════════════════════════════════════════════════════════════════════════════
# Section 2 – Revenue Distribution (EDA)
# ══════════════════════════════════════════════════════════════════════════════
st.header("Revenue Distribution")
st.markdown(
    "Distribution of *Revenue Estimated* across all games. "
    "Shown on a log₁₀ scale due to the strong right skew."
)

log_rev = np.log10(df["Revenue Estimated"])

fig_eda, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(log_rev, bins=60, color="steelblue", edgecolor="white", linewidth=0.4)
axes[0].set_xlabel("log₁₀(Revenue Estimated USD)")
axes[0].set_ylabel("Number of Games")
axes[0].set_title("Revenue Distribution (log scale)")

axes[1].boxplot(
    log_rev,
    vert=True,
    patch_artist=True,
    boxprops=dict(facecolor="steelblue", alpha=0.6),
    medianprops=dict(color="white", linewidth=2),
)
axes[1].set_ylabel("log₁₀(Revenue Estimated USD)")
axes[1].set_title("Revenue Box Plot (log scale)")
axes[1].set_xticks([])

fig_eda.tight_layout()
st.pyplot(fig_eda)
plt.close(fig_eda)

pcts = [10, 25, 50, 75, 90, 95, 99]
pct_df = pd.DataFrame({
    "Percentile": [f"{p}th" for p in pcts],
    "Revenue (USD)": [f"${df['Revenue Estimated'].quantile(p / 100):,.0f}" for p in pcts],
})
st.dataframe(pct_df, use_container_width=False, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# Section 3 – Revenue vs Number of Reviews
# ══════════════════════════════════════════════════════════════════════════════
st.header("Revenue vs Number of Reviews")
st.markdown(
    "Both axes are on a log₁₀ scale. The hexbin density plot reveals the joint "
    "distribution across all games; brighter cells contain more games."
)

rev_reviews = df.dropna(subset=["Reviews Total"]).copy()
rev_reviews = rev_reviews[rev_reviews["Reviews Total"] > 0]

log_rev_r = np.log10(rev_reviews["Revenue Estimated"])
log_reviews = np.log10(rev_reviews["Reviews Total"])

from scipy import stats as sp_stats
r_rr, p_rr = sp_stats.spearmanr(log_reviews, log_rev_r)

fig_rr, ax_rr = plt.subplots(figsize=(9, 6))
hb = ax_rr.hexbin(log_reviews, log_rev_r, gridsize=50, cmap="YlOrRd", mincnt=1)
plt.colorbar(hb, ax=ax_rr, label="Number of games")
# OLS trend line
m, b, *_ = sp_stats.linregress(log_reviews, log_rev_r)
x_line = np.linspace(log_reviews.min(), log_reviews.max(), 200)
ax_rr.plot(x_line, m * x_line + b, color="steelblue", linewidth=1.8, label=f"OLS fit  (slope={m:.2f})")
ax_rr.set_xlabel("log₁₀(Reviews Total)")
ax_rr.set_ylabel("log₁₀(Revenue Estimated USD)")
ax_rr.set_title(f"Revenue vs Reviews Total  —  Spearman r = {r_rr:.3f}  (p {'< 0.001' if p_rr < 0.001 else f'= {p_rr:.3f}'})")
ax_rr.legend()
fig_rr.tight_layout()
st.pyplot(fig_rr)
plt.close(fig_rr)

col1, col2 = st.columns(2)
col1.metric("Spearman r", f"{r_rr:.3f}")
col2.metric("Games included", f"{len(rev_reviews):,}")

# ══════════════════════════════════════════════════════════════════════════════
# Section 4 – Revenue vs Review Score
# ══════════════════════════════════════════════════════════════════════════════
st.header("Revenue vs Review Score")
st.markdown(
    "Left: hexbin density (log revenue vs review score %). "
    "Right: median revenue by score band to show the central tendency."
)

rev_score = df.dropna(subset=["Reviews Score Fancy"]).copy()
rev_score = rev_score[rev_score["Reviews Score Fancy"] > 0]

log_rev_s = np.log10(rev_score["Revenue Estimated"])
score = rev_score["Reviews Score Fancy"]

r_rs, p_rs = sp_stats.spearmanr(score, log_rev_s)

# Score bands
bins_s = [0, 20, 40, 60, 70, 80, 90, 100]
labels_s = ["0–20", "20–40", "40–60", "60–70", "70–80", "80–90", "90–100"]
rev_score["Score Band"] = pd.cut(score, bins=bins_s, labels=labels_s, right=True)
band_stats = (
    rev_score.groupby("Score Band", observed=True)["Revenue Estimated"]
    .agg(median="median", count="count")
    .reset_index()
)

fig_rs, (ax_rs1, ax_rs2) = plt.subplots(1, 2, figsize=(14, 6))

hb2 = ax_rs1.hexbin(score, log_rev_s, gridsize=40, cmap="YlOrRd", mincnt=1)
plt.colorbar(hb2, ax=ax_rs1, label="Number of games")
ax_rs1.set_xlabel("Review Score (%)")
ax_rs1.set_ylabel("log₁₀(Revenue Estimated USD)")
ax_rs1.set_title(f"Density  —  Spearman r = {r_rs:.3f}")

ax_rs2.bar(band_stats["Score Band"].astype(str), band_stats["median"] / 1e6,
           color="steelblue", edgecolor="white")
for i, row in band_stats.iterrows():
    ax_rs2.text(i, row["median"] / 1e6 + 0.02 * band_stats["median"].max() / 1e6,
                f'n={row["count"]:,}', ha="center", va="bottom", fontsize=8)
ax_rs2.set_xlabel("Score Band (%)")
ax_rs2.set_ylabel("Median Revenue (USD millions)")
ax_rs2.set_title("Median Revenue by Score Band")
ax_rs2.tick_params(axis="x", rotation=30)

fig_rs.tight_layout()
st.pyplot(fig_rs)
plt.close(fig_rs)

col3, col4 = st.columns(2)
col3.metric("Spearman r", f"{r_rs:.3f}")
col4.metric("Games included", f"{len(rev_score):,}")

# ══════════════════════════════════════════════════════════════════════════════
# Section 5 – Revenue vs Launch Price
# ══════════════════════════════════════════════════════════════════════════════
st.header("Revenue vs Launch Price")
st.markdown(
    "Left: log-log hexbin for paid games (Launch Price > 0). "
    "Right: median revenue by price tier (including free-to-play)."
)

rev_price = df.dropna(subset=["Launch Price"]).copy()

# Price tiers (including free)
price_bins = [-0.01, 0.0, 4.99, 9.99, 19.99, 29.99, np.inf]
price_labels = ["Free", "$0.01–$4.99", "$5–$9.99", "$10–$19.99", "$20–$29.99", "$30+"]
rev_price["Price Tier"] = pd.cut(rev_price["Launch Price"], bins=price_bins, labels=price_labels)

tier_stats = (
    rev_price.groupby("Price Tier", observed=True)["Revenue Estimated"]
    .agg(median="median", count="count")
    .reset_index()
)

paid = rev_price[rev_price["Launch Price"] > 0].copy()
log_rev_p = np.log10(paid["Revenue Estimated"])
log_price = np.log10(paid["Launch Price"])
r_rp, p_rp = sp_stats.spearmanr(log_price, log_rev_p)

fig_rp, (ax_rp1, ax_rp2) = plt.subplots(1, 2, figsize=(14, 6))

hb3 = ax_rp1.hexbin(log_price, log_rev_p, gridsize=40, cmap="YlOrRd", mincnt=1)
plt.colorbar(hb3, ax=ax_rp1, label="Number of games")
ax_rp1.set_xlabel("log₁₀(Launch Price USD)")
ax_rp1.set_ylabel("log₁₀(Revenue Estimated USD)")
ax_rp1.set_title(f"Paid games only  —  Spearman r = {r_rp:.3f}")

ax_rp2.bar(tier_stats["Price Tier"].astype(str), tier_stats["median"] / 1e6,
           color="steelblue", edgecolor="white")
for i, row in tier_stats.iterrows():
    ax_rp2.text(i, row["median"] / 1e6 + 0.02 * tier_stats["median"].max() / 1e6,
                f'n={row["count"]:,}', ha="center", va="bottom", fontsize=8)
ax_rp2.set_xlabel("Price Tier")
ax_rp2.set_ylabel("Median Revenue (USD millions)")
ax_rp2.set_title("Median Revenue by Price Tier")
ax_rp2.tick_params(axis="x", rotation=30)

fig_rp.tight_layout()
st.pyplot(fig_rp)
plt.close(fig_rp)

col5, col6, col7 = st.columns(3)
col5.metric("Spearman r (paid)", f"{r_rp:.3f}")
col6.metric("Paid games", f"{len(paid):,}")
col7.metric("Free-to-play games", f"{len(rev_price[rev_price['Launch Price'] == 0]):,}")
