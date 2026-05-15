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

[![Correlation Summary Table](https://i.gyazo.com/1cd94814e25cfcb3cbb5eb856f39b1dc.png)](https://gyazo.com/1cd94814e25cfcb3cbb5eb856f39b1dc)

---

[![Correlation Matrix](https://i.gyazo.com/6d241c4c73cfb9951fdcceb62f600949.png)](https://gyazo.com/6d241c4c73cfb9951fdcceb62f600949)

---

## SAS Analysis

The SAS part of the project mirrors the Python analysis, applied to the same Steam dataset.
Scripts are located in the `sas/` folder and were run on SAS OnDemand for Academics.

---

### Data Import

Imports the raw CSV into a SAS dataset using `PROC IMPORT`, then verifies the structure with `PROC CONTENTS` and previews the first rows with `PROC PRINT`.

![Variable Overview](https://i.imgur.com/2bGc3xn.png)

![First 10 Rows](https://i.imgur.com/ASNbeQ1.png)