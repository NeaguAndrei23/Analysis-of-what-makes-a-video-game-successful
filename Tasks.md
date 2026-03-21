#  Video Game Success Analysis Project (Python)

##  Project Objective

The goal of this project is to analyze the factors that influence the **financial success of video games**, where success is defined primarily by:

> **Revenue Estimated**

Additionally, the project will explore the relationship between:
- Revenue and number of reviews
- Revenue and review scores

---

##  Dataset Overview

The dataset is a `.csv` file containing video game data with columns such as:

- Title
- Reviews Total
- Reviews Score Fancy
- Release Date
- Launch Price
- Tags / Modified Tags
- Revenue Estimated
- App ID / Steam Page

---

##  Progress

### Completed
- [x] Project scaffolding — `python/app.py` (Streamlit), `requirements.txt`
- [x] Data loading & cleaning (`load_data` with `@st.cache_data`)
  - `Revenue Estimated` — stripped `$`/`,`/whitespace, cast to float, rows with no revenue dropped
  - `Launch Price` — stripped `$`/`,`/whitespace, free-to-play mapped to `0.0`
  - `Reviews Score Fancy` — stripped `%`, cast to float
  - `Reviews Total` — coerced to numeric
  - `Release Date` → `Release Year` — parsed datetime, extracted nullable int year
- [x] Data preview and descriptive statistics displayed in app
- [x] PRELIMINARY STEP: GeoPandas choropleth map (simulated revenue by region)
- [x] Revenue distribution (EDA)
- [x] Revenue vs Number of Reviews
- [x] Revenue vs Review Score
- [x] Revenue vs Launch Price
- [x] Revenue vs Genre / Tags
- [x] Revenue vs Release Year

### To Do
- [ ] Correlation summary

---

#  PRELIMINARY STEP: Geospatial Simulation (GeoPandas Requirement)

##  Context

The dataset does **not contain geographic information** (e.g., country, region).

However, to fulfill the requirement of using **GeoPandas**, a **simulated geographic distribution** of revenue will be created.

---

##  Approach: Simulated Global Revenue Distribution

### Idea:

Assign estimated revenue across major global regions using assumed market shares:

- North America → 35%
- Europe → 30%
- Asia → 35%

This allows us to:
- Introduce geographic analysis
- Visualize revenue distribution globally
- Use GeoPandas meaningfully despite missing location data

---

##  Implementation Plan

### Tasks:

1. Load a world map dataset using GeoPandas:
   - Use built-in dataset (`naturalearth_lowres`)

2. Create a simulated revenue variable:
   - Based on country population or proportional distribution

3. Assign revenue values:
   - Use proportional scaling (e.g., based on population or fixed percentages)

4. Generate a choropleth map:
   - Color countries by simulated revenue

---

##  Example Logic

```python
import geopandas as gpd

# Load world dataset
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Simulate revenue distribution (example logic)
world['simulated_revenue'] = world['pop_est'] * 0.1

# Plot map
world.plot(column='simulated_revenue', legend=True)