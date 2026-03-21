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
# Section 1 – Geospatial: Simulated Revenue by Region (GeoPandas)
# ══════════════════════════════════════════════════════════════════════════════
st.header("Simulated Global Revenue Distribution")
st.markdown(
    "The dataset contains no geographic data. Revenue is **simulated** by distributing "
    "total estimated revenue across major regions using assumed market shares: "
    "**North America 35 %**, **Europe 30 %**, **Asia 35 %**. "
    "Within each region, each country receives a share proportional to its population."
)


@st.cache_data(show_spinner="Building choropleth map…")
def build_choropleth(total_revenue: float):
    import geopandas as gpd

    # naturalearth_lowres was removed in geopandas 1.0; fetch directly from
    # the Natural Earth CDN (same host geodatasets uses for its downloads).
    NE_URL = (
        "https://naciscdn.org/naturalearth/110m/cultural/"
        "ne_110m_admin_0_countries.zip"
    )
    world = gpd.read_file(NE_URL)

    REGION_SHARES = {
        "North America": 0.35,
        "Europe": 0.30,
        "Asia": 0.35,
    }

    # Population totals per modelled region
    region_pop = {
        region: world.loc[world["CONTINENT"] == region, "POP_EST"].sum()
        for region in REGION_SHARES
    }

    def assign_revenue(row):
        share = REGION_SHARES.get(row["CONTINENT"], 0.0)
        rpop = region_pop.get(row["CONTINENT"], 1)
        if rpop == 0:
            return 0.0
        return share * total_revenue * (row["POP_EST"] / rpop)

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
ax_map.set_title("Simulated Video-Game Revenue by Country", fontsize=14, pad=12)
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
