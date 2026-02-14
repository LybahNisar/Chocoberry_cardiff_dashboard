import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Page Config
st.set_page_config(page_title="Menu Intelligence", page_icon="🍔", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .big-number {
        font-size: 24px;
        font-weight: bold;
        color: #FF4B4B;
    }
</style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_menu_data():
    data_path = Path("data/raw/chocoberry_cardiff")
    
    # Load Best Sellers
    try:
        df_best = pd.read_csv(data_path / "most_sold_items.csv")
        # Clean currency columns
        if 'Sales' in df_best.columns:
            df_best['Sales'] = df_best['Sales'].astype(str).str.replace(',', '').astype(float)
    except Exception:
        df_best = pd.DataFrame()

    # Load Categories
    try:
        df_cat = pd.read_csv(data_path / "best-selling_categories.csv")
        if 'Sales' in df_cat.columns:
            df_cat['Sales'] = df_cat['Sales'].astype(str).str.replace(',', '').astype(float)
    except Exception:
        df_cat = pd.DataFrame()

    return df_best, df_cat

df_best, df_cat = load_menu_data()

# Header
st.title("🍔 Menu Performance Intelligence")
st.markdown("### Deep dive into your Best Sellers, Least Sellers, and Category Performance")

if df_best.empty:
    st.error("⚠️ Menu data not found. Please verify CSV files in data/raw/chocoberry_cardiff/")
    st.stop()

# --- TOP METRICS ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    top_item = df_best.iloc[0]
    st.metric("🏆 #1 Best Seller", top_item['Item'], f"{int(top_item['Items sold'])} Sold")
with col2:
    top_rev_item = df_best.sort_values('Sales', ascending=False).iloc[0]
    st.metric("💰 Highest Revenue Item", top_rev_item['Item'], f"£{top_rev_item['Sales']:,.2f}")
with col3:
    if not df_cat.empty:
        top_cat = df_cat.iloc[0]
        st.metric("📦 Top Category", top_cat['Category'], f"£{top_cat['Sales']:,.2f}")
with col4:
    total_items_sold = df_best['Items sold'].sum()
    st.metric("📊 Total Items Tracked", f"{int(total_items_sold):,}")

st.divider()

# --- ROW 1: ITEM ANALYSIS ---
col_charts1, col_charts2 = st.columns(2)

with col_charts1:
    st.subheader("🏆 Top 10 Items by VOLUME (Quantity Sold)")
    
    # Sort by Qty
    df_vol = df_best.sort_values("Items sold", ascending=True).tail(10)
    
    fig_vol = px.bar(
        df_vol, 
        x="Items sold", 
        y="Item", 
        orientation='h',
        text="Items sold",
        color="Items sold",
        color_continuous_scale="Reds"
    )
    fig_vol.update_layout(showlegend=False, xaxis_title="Quantity Sold", yaxis_title=None)
    st.plotly_chart(fig_vol, use_container_width=True)

with col_charts2:
    st.subheader("💰 Top 10 Items by VALUE (Revenue Generated)")
    
    # Sort by Sales
    df_val = df_best.sort_values("Sales", ascending=True).tail(10)
    
    fig_val = px.bar(
        df_val, 
        x="Sales", 
        y="Item", 
        orientation='h',
        text="Sales",
        text_template="£%{x:,.0f}",
        color="Sales",
        color_continuous_scale="Greens"
    )
    fig_val.update_layout(showlegend=False, xaxis_title="Total Revenue (£)", yaxis_title=None)
    st.plotly_chart(fig_val, use_container_width=True)

# --- ROW 2: CATEGORY ANALYSIS ---
if not df_cat.empty:
    st.subheader("📦 Category Performance Matrix")
    
    fig_cat = px.scatter(
        df_cat,
        x="Items sold",
        y="Sales",
        size="Sales",
        color="Category",
        hover_name="Category",
        text="Category",
        size_max=60,
        height=500
    )
    fig_cat.update_traces(textposition='top center')
    fig_cat.update_layout(
        xaxis_title="Quantity Sold (Popularity)",
        yaxis_title="Total Revenue (Value)",
        showlegend=False
    )
    st.plotly_chart(fig_cat, use_container_width=True)

# --- ROW 3: DATAFRAME VIEW ---
with st.expander("🔍 View Full Menu Data Table"):
    st.dataframe(df_best, use_container_width=True)
