"""
Analysis of What Makes a Video Game Successful
================================================
Steam Trends 2023 dataset – 61,216 games
Success metric: Revenue Estimated
"""

import os
import warnings

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
