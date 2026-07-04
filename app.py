import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(page_title="Nassau Candy — Factory Optimizer", layout="wide")

def show_metric(label, value):
    st.markdown(f"""
    <div style="background-color:#1a1a2e; padding:12px; border-radius:8px; margin-bottom:8px;">
        <p style="color:#999; font-size:13px; margin:0;">{label}</p>
        <p style="color:#fff; font-size:24px; font-weight:600; margin:0;">{value}</p>
    </div>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('nassau_phase2.csv')
    recs = pd.read_csv('phase5_recommendations.csv')
    sims = pd.read_csv('phase5_full_simulation.csv')
    return df, recs, sims

df, recs, sims = load_data()

@st.cache_data
def load_raw():
    raw = pd.read_csv('Nassau Candy Distributor.csv')
    raw['True_Margin_Pct'] = (raw['Gross Profit'] / raw['Sales']) * 100
    factory_map = {
        'Wonka Bar - Nutty Crunch Surprise': "Lot\'s O\' Nuts",
        'Wonka Bar - Fudge Mallows': "Lot\'s O\' Nuts",
        'Wonka Bar -Scrumdiddlyumptious': "Lot\'s O\' Nuts",
        'Wonka Bar - Milk Chocolate': "Wicked Choccy\'s",
        'Wonka Bar - Triple Dazzle Caramel': "Wicked Choccy\'s",
        'Laffy Taffy': 'Sugar Shack', 'SweeTARTS': 'Sugar Shack',
        'Nerds': 'Sugar Shack', 'Fun Dip': 'Sugar Shack',
        'Fizzy Lifting Drinks': 'Sugar Shack',
        'Everlasting Gobstopper': 'Secret Factory',
        'Hair Toffee': 'The Other Factory',
        'Lickable Wallpaper': 'Secret Factory',
        'Wonka Gum': 'Secret Factory', 'Kazookles': 'The Other Factory',
    }
    raw['Factory'] = raw['Product Name'].map(factory_map)
    return raw

df_raw = load_raw()


st.title("🏭 Nassau Candy — Factory Optimization Dashboard")
st.markdown("Decision intelligence for shipping efficiency & profitability")

st.sidebar.header("Controls")
products = sorted(recs['Product'].unique())
selected_product = st.sidebar.selectbox("Select Product", products)

priority = st.sidebar.slider(
    "Optimization Priority: Speed ←→ Profit",
    min_value=0, max_value=100, value=50
)

risk_filter = st.sidebar.multiselect(
    "Filter by Risk Level",
    options=['Low Risk', 'Medium Risk', 'High Risk'],
    default=['Low Risk', 'Medium Risk', 'High Risk']
)

tab1, tab2, tab3, tab4 = st.tabs([
    "🔧 Factory Simulator", "🔁 What-If Analysis",
    "📊 Recommendations", "⚠️ Risk & Impact"
])

# MODULE 1
with tab1:
    st.subheader(f"Predicted performance across factories — {selected_product}")
    product_sims = sims[sims['Product'] == selected_product].sort_values('Weighted_Avg_Distance_km')

    col1, col2 = st.columns([2, 1])
    with col1:
        chart_data = product_sims.set_index('Factory')[['Weighted_Avg_Distance_km']]
        st.bar_chart(chart_data, color="#1D9E75")
    with col2:
        current_row = product_sims[product_sims['Is_Current']].iloc[0]
        show_metric("Current Factory", current_row['Factory'])
        show_metric("Current Avg Distance", f"{current_row['Weighted_Avg_Distance_km']:.0f} km")
        show_metric("Current Margin", f"{current_row['Current_Margin_Pct']:.1f}%")
        show_metric("Total Orders", f"{int(current_row['Current_Orders'])}")

    st.markdown("#### Factory comparison table")
    st.dataframe(product_sims[['Factory','Is_Current','Weighted_Avg_Distance_km']], use_container_width=True, hide_index=True)

# MODULE 2
with tab2:
    st.subheader(f"Current vs Recommended — {selected_product}")
    rec_row = recs[recs['Product'] == selected_product].iloc[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("##### 📍 Current Setup")
        st.info(f"**Factory:** {rec_row['Current_Factory']}  \n**Distance:** {rec_row['Current_Distance_km']:.0f} km  \n**Margin:** {rec_row['Current_Margin_Pct']:.1f}%")
    with col2:
        st.markdown("##### 🎯 Recommended Setup")
        st.success(f"**Factory:** {rec_row['Recommended_Factory']}  \n**Distance:** {rec_row['Recommended_Distance_km']:.0f} km  \n**Improvement:** {rec_row['Distance_Reduction_Pct']:.1f}%")
    with col3:
        st.markdown("##### 📈 Impact")
        show_metric("Distance Reduction", f"{rec_row['Distance_Reduction_Pct']:.1f}%")
        show_metric("Orders Affected", f"{int(rec_row['Orders'])}")
        show_metric("Profit at Stake", f"${rec_row['Current_Total_Profit']:,.2f}")

    st.markdown("---")
    compare_data = pd.DataFrame({
        'Distance (km)': [rec_row['Current_Distance_km'], rec_row['Recommended_Distance_km']]
    }, index=['Current', 'Recommended'])
    st.bar_chart(compare_data)

# MODULE 3
with tab3:
    st.subheader("Ranked Factory Reassignment Recommendations")
    filtered_recs = recs[recs['Risk_Flag'].isin(risk_filter)].sort_values('Recommendation_Score', ascending=False)
    st.dataframe(filtered_recs[['Product','Current_Factory','Recommended_Factory','Action_Label','Distance_Reduction_Pct','Current_Margin_Pct','Risk_Flag','Recommendation_Score']], use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Top 10 by Recommendation Score")
        top10 = filtered_recs.head(10).set_index('Product')[['Recommendation_Score']]
        st.bar_chart(top10)
    with col2:
        st.markdown("#### Distance Reduction vs Margin")
        scatter_data = filtered_recs[['Distance_Reduction_Pct','Current_Margin_Pct']]
        st.scatter_chart(scatter_data, x='Distance_Reduction_Pct', y='Current_Margin_Pct')

# MODULE 4
with tab4:
    st.subheader("Risk & Impact Panel")
    high_risk = recs[recs['Risk_Flag'] == 'High Risk']

    col1, col2, col3 = st.columns(3)
    with col1: show_metric("High Risk Products", len(high_risk))
    with col2: show_metric("Total Profit at Stake", f"${high_risk['Profit_At_Stake'].sum():,.2f}")
    with col3: show_metric("Avg Margin (High Risk)", f"{high_risk['Current_Margin_Pct'].mean():.1f}%")

    if len(high_risk) > 0:
        st.warning("⚠️ These products have margins below 20% — reassignment alone may not fix profitability. A cost/pricing review is recommended.")
        st.dataframe(high_risk[['Product','Current_Factory','Current_Margin_Pct','Orders','Profit_At_Stake']], use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### Profit Impact Stability by Risk Tier")
    risk_summary = recs.groupby('Risk_Flag').agg(Products=('Product','count'), Avg_Margin=('Current_Margin_Pct','mean'), Total_Profit=('Profit_At_Stake','sum')).round(2)
    st.dataframe(risk_summary, use_container_width=True)

with tab4:
    st.markdown("---")
    st.markdown("#### Factory-level vs product-level risk")
    st.caption("The Other Factory looks risky overall because Kazookles (96 orders, 7.7% margin) dominates its order volume. Hair Toffee, also made there, is actually healthy (77.8% margin) but only has 4 orders.")
    product_risk = df_raw.groupby('Product Name').agg(
        Factory=('Factory','first'), Orders=('Order ID','count'),
        True_Margin_Pct=('True_Margin_Pct','mean')
    ).round(2).sort_values('True_Margin_Pct')
    st.dataframe(product_risk, use_container_width=True)

st.markdown("---")
st.caption("Nassau Candy Distributor — Decision Intelligence Dashboard")
