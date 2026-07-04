# 🍬 Nassau Candy Distributor — Decision Intelligence System

A full end-to-end Business Analytics project that transforms static factory assignments into a data-driven decision intelligence system.

## 📌 Project Overview

Nassau Candy Distributor assigns 15 confectionery products across 5 manufacturing factories. This project replaces legacy, rule-based assignments with an ML-powered simulation engine that recommends optimal factory–product configurations based on shipping distance and profitability.

## 🎯 Business Problem

- Products assigned to factories using outdated static rules
- No system to simulate reassignment scenarios before executing them
- Margin erosion in specific product lines (Kazookles: 7.69% vs 66.5% company average)
- No way to quantify operational impact of factory changes at scale

## 🔍 Key Findings

- **Factory concentration risk:** 96.6% of orders handled by just 2 of 5 factories
- **Lead time insight:** Shipping lead time is driven by seasonality (Order Month), not factory choice — an honest null result that redirects focus to distance and margin optimization
- **Root cause analysis:** The Other Factory's low blended margin (7.7–12.1%) is entirely driven by one product (Kazookles) — not the facility itself
- **Top recommendation:** Reassign Nerds, Laffy Taffy, Fun Dip, and Fizzy Lifting Drinks from Sugar Shack for 32–79% distance reduction

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python (Pandas, NumPy) | Data preparation & feature engineering |
| Scikit-learn | Predictive modeling (Linear Regression, Random Forest, Gradient Boosting) |
| K-Means Clustering | Route & product segmentation |
| Haversine Formula | Geographic distance calculation |
| Streamlit | Interactive dashboard deployment |
| Google Colab | Development environment |

## 📊 Project Phases

1. **Data Preparation** — Parsing, encoding, outlier capping, normalization (10,194 orders, 0 nulls)
2. **Feature Engineering** — Haversine distance, temporal features, per-unit efficiency metrics (24 features)
3. **Predictive Modeling** — 3 models trained; Gradient Boosting best (R²=0.044); weak signal honestly reported
4. **Route Clustering** — K-Means identifies 4 clusters: Core High-Volume, Stable Mid-Volume, High-Risk Low-Margin, Long-Distance Niche
5. **Scenario Simulation** — Factory reassignment engine with business-sense guardrail
6. **Streamlit Dashboard** — 4 interactive modules: Factory Simulator, What-If Analysis, Recommendations, Risk & Impact

## 📁 Repository Structure
├── app.py                          # Streamlit dashboard
├── nassau_phase2.csv               # Cleaned feature matrix (10,194 rows)
├── phase5_recommendations.csv      # Ranked reassignment recommendations
├── phase5_full_simulation.csv      # Full factory simulation output
├── model_gb.pkl                    # Gradient Boosting model
├── model_rf.pkl                    # Random Forest model
├── model_lr.pkl                    # Linear Regression model
├── feature_cols.pkl                # Feature column list
├── Nassau_Candy_Research_Paper.docx   # Full 21-page research paper
├── Nassau_Candy_Executive_Summary.docx # 1-page stakeholder summary
└── Data and Outputs/
├── Nassau Candy Distributor.csv
├── route_summary_clustered.csv
├── route_clusters.png
├── phase3_findings.json
├── phase4_findings.json
└── phase5_findings.json

## 📈 Dashboard Modules

- **Factory Simulator** — Select any product, compare distance across all 5 factories
- **What-If Analysis** — Side-by-side current vs recommended factory comparison
- **Recommendations** — Ranked reassignment table with risk filtering
- **Risk & Impact Panel** — Margin alerts, high-risk product identification

## 📄 Deliverables

- 21-page research paper (EDA, methodology, findings, recommendations)
- Live Streamlit dashboard
- 1-page executive summary for government stakeholders
