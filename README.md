# Analysis of What Makes a Video Game Successful

An analysis done in Python and SAS on a dataset of 61,216 video games listed on the Steam platform.
The goal is to identify what metrics a video game requires to be considered "successful", measured primarily by estimated revenue.

**Live app:** [Open on Streamlit Cloud](https://neaguandrei23-analysis-of-what-makes-a-video-g-pythonapp-eug4n3.streamlit.app/)

---

## Prerequisites

Install all dependencies before running the project locally:

```
pip install streamlit pandas numpy matplotlib seaborn geopandas mapclassify geodatasets
```

To launch the app:

```
cd python
streamlit run app.py
```

---

## Dataset Preview

[![Dataset Preview](https://i.gyazo.com/bdd57a7b8c577e3adba0f1e260dbcb89.png)](https://gyazo.com/bdd57a7b8c577e3adba0f1e260dbcb89)

---

## Global Revenue Distribution

[![Global Revenue Distribution](https://i.gyazo.com/2d71aac3160360ab0d5e0837c15102b0.png)](https://gyazo.com/2d71aac3160360ab0d5e0837c15102b0)

---

## Revenue Distribution

[![Revenue Distribution](https://i.gyazo.com/cd4883279b7435e9d2c174eb42ac6ce5.png)](https://gyazo.com/cd4883279b7435e9d2c174eb42ac6ce5)

---

## Revenue vs Number of Reviews

[![Revenue vs Number of Reviews](https://i.gyazo.com/70b572f7120cce67afe3ec68544323a5.png)](https://gyazo.com/70b572f7120cce67afe3ec68544323a5)

---

## Revenue vs Review Score

[![Revenue vs Review Score](https://i.gyazo.com/c81e7d0d9dd1268ed9a3b7f3c3cd1793.png)](https://gyazo.com/c81e7d0d9dd1268ed9a3b7f3c3cd1793)

---

## Revenue vs Launch Price

[![Revenue vs Launch Price](https://i.gyazo.com/c8561b2609f89651836d47603da0b2d5.png)](https://gyazo.com/c8561b2609f89651836d47603da0b2d5)

---

## Revenue vs Genre / Tags

[![Revenue vs Genre / Tags](https://i.gyazo.com/b3ea7adf37c528df580fc9a13fc72463.png)](https://gyazo.com/b3ea7adf37c528df580fc9a13fc72463)

---

## Revenue vs Release Year

[![Revenue vs Release Year](https://i.gyazo.com/468537d5f45f53b3b08dc78d1fff3c9d.png)](https://gyazo.com/468537d5f45f53b3b08dc78d1fff3c9d)

---

## Correlation Summary

**Correlation Summary Table**

[![Correlation Summary Table](https://i.gyazo.com/1cd94814e25cfcb3cbb5eb856f39b1dc.png)](https://gyazo.com/1cd94814e25cfcb3cbb5eb856f39b1dc)

---

**Correlation Matrix**

[![Correlation Matrix](https://i.gyazo.com/6d241c4c73cfb9951fdcceb62f600949.png)](https://gyazo.com/6d241c4c73cfb9951fdcceb62f600949)

---

## SAS Analysis

The SAS part of the project mirrors the Python analysis, applied to the same Steam dataset.
Scripts are located in the `sas/` folder and were run on SAS OnDemand for Academics.

---

## Data Import

Imports the raw CSV into a SAS dataset using `PROC IMPORT`, then verifies the structure with `PROC CONTENTS` and previews the first rows with `PROC PRINT`.

**Variable Overview**

![Variable Overview](https://i.imgur.com/2bGc3xn.png)

**First 10 Rows**

![First 10 Rows](https://i.imgur.com/ASNbeQ1.png)

---

## Data Cleaning

DATA step that converts character columns (`Revenue Estimated`, `Reviews Score Fancy`) to numeric using `COMPRESS` and `INPUT`, extracts `Release_Year` from the parsed date, sets missing launch prices to 0, and filters to games with positive revenue only.

**Cleaned Preview**

![Cleaned Preview](https://i.imgur.com/Nv5DIXF.png)

---

## Formats, Descriptive Statistics, and Tabular Reporting

Defines user-defined formats (`rev_tier`, `price_tier`, `score_band`) for readable output. `PROC MEANS` computes descriptive statistics for all key variables. `PROC FREQ` shows the distribution of games across revenue tiers. `PROC TABULATE` cross-tabulates median revenue by review score band and price tier.

**Descriptive Statistics**

![Descriptive Statistics](https://i.imgur.com/80mS8zi.png)

**Revenue Tier Frequency**

![Revenue Tier Frequency](https://i.imgur.com/ALIhyHN.png)

**Revenue by Score and Price**

![Revenue by Score and Price](https://i.imgur.com/7ABlP8B.png)

---

## Graphical Analysis

`PROC SGPLOT` generates four charts: a log-scale histogram of revenue distribution, a bar chart of median revenue by review score band, a bar chart of median revenue by price tier, and a scatter plot of review score vs revenue.

**Revenue Distribution Histogram**

![Revenue Distribution Histogram](https://i.imgur.com/3bBVQIt.png)

**Median Revenue by Score Band**

![Median Revenue by Score Band](https://i.imgur.com/JVXA58g.png)

**Median Revenue by Price Tier**

![Median Revenue by Price Tier](https://i.imgur.com/jHa6g4t.png)

**Review Score vs Revenue Scatter**

![Review Score vs Revenue Scatter](https://i.imgur.com/hbriL6Z.png)

---

## Correlation and Regression

`PROC CORR` computes Spearman correlations between revenue and the three numeric predictors (reviews total, review score, launch price), mirroring the Python app results. `PROC REG` fits a multiple linear regression on log-transformed revenue to quantify each predictor's contribution.

**Spearman Correlations**

![Spearman Correlations](https://i.imgur.com/5EbSHIP.png)

**Regression Output**

![Regression Output](https://i.imgur.com/pipEu07.png)

---

## Array-Based Performance Flagging

A DATA step uses arrays to flag each game as high or low performing across three metrics simultaneously (revenue, review score, launch price), then counts how many metrics each game scores high on. `PROC FREQ` and `PROC MEANS` summarise the results.

**High-Performance Count Distribution**

![High-Performance Count Distribution](https://i.imgur.com/fW8NB3F.png)

**Mean Revenue by High-Performance Count**

![Mean Revenue by High-Performance Count](https://i.imgur.com/bHaX62I.png)

---

## Combining Datasets

`PROC SQL` aggregates the dataset into a year-level summary (game count, median and mean revenue per year). A `MERGE` then attaches those year-level figures back to each individual game row, enriching the dataset for further analysis.

**Year Summary Table**

![Year Summary Table Part 1](https://i.imgur.com/4NuXYVK.png)

![Year Summary Table Part 2](https://i.imgur.com/poTA8UF.png)

**Enriched Dataset Preview**

![Enriched Dataset Preview](https://i.imgur.com/ozf3p8n.png)

---

## Machine Learning

A binary target (`High_Revenue = 1` if revenue ≥ $100k) is created, then two models are trained. `PROC HPSPLIT` builds a pruned decision tree showing which variables split the data most cleanly. `PROC HPFOREST` trains a random forest and produces a variable importance table ranking `Reviews_Total`, `Review_Score`, `Launch_Price`, and `Release_Year` by predictive power.

**Target Class Distribution**

![Target Class Distribution](https://i.imgur.com/kRQrjPI.png)

**Decision Tree**

![Decision Tree](https://i.imgur.com/NzybecQ.png)

**Random Forest Variable Importance**

![Random Forest Variable Importance](https://i.imgur.com/ifnPHtt.png)
