import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

def load_menu_data(data_path):
    """Load menu performance CSVs"""
    try:
        most_sold = pd.read_csv(data_path / 'most_sold_items.csv')
        least_sold = pd.read_csv(data_path / 'least_sold_items.csv')
        categories = pd.read_csv(data_path / 'best-selling_categories.csv')
        
        # Clean data (remove commas and convert to numeric)
        for df in [most_sold, least_sold, categories]:
            if 'Sales' in df.columns and df['Sales'].dtype == 'object':
                df['Sales'] = pd.to_numeric(df['Sales'].astype(str).str.replace(',', ''), errors='coerce')
            if 'Items sold' in df.columns and df['Items sold'].dtype == 'object':
                df['Items sold'] = pd.to_numeric(df['Items sold'].astype(str).str.replace(',', ''), errors='coerce')
                
        return most_sold, least_sold, categories
    except Exception as e:
        st.error(f"Error loading menu data: {e}")
        return None, None, None

def show_menu_analysis():
    st.markdown("---")
    st.header("🍔 Menu Analysis")
    st.caption("Detailed breakdown of top sellers, categories, and slow-moving items")
    
    # Path to data
    data_path = Path(__file__).parent.parent / 'data' / 'raw' / 'chocoberry_cardiff'
    most_sold, least_sold, categories = load_menu_data(data_path)
    
    if most_sold is None:
        return

    # --- TOP 10 ITEMS ---
    st.subheader("🏆 Top 10 Best Sellers")
    col1, col2 = st.columns(2)
    
    with col1:
        # By Revenue
        fig_rev = px.bar(
            most_sold.head(10), 
            x='Sales', 
            y='Item', 
            orientation='h',
            title="Top 10 by Revenue (£)",
            color='Sales',
            color_continuous_scale='Greens'
        )
        fig_rev.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_rev, use_container_width=True)
        
    with col2:
        # By Volume
        sorted_vol = most_sold.sort_values('Items sold', ascending=False).head(10)
        fig_vol = px.bar(
            sorted_vol, 
            x='Items sold', 
            y='Item', 
            orientation='h',
            title="Top 10 by Quantity Sold",
            color='Items sold',
            color_continuous_scale='Blues'
        )
        fig_vol.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_vol, use_container_width=True)

    # --- CATEGORY ANALYSIS ---
    st.subheader("📂 Category Performance")
    col3, col4 = st.columns(2)
    
    with col3:
        fig_cat = px.pie(
            categories, 
            values='Sales', 
            names='Category', 
            title="Revenue Share by Category",
            hole=0.4
        )
        st.plotly_chart(fig_cat, use_container_width=True)
        
    with col4:
        st.markdown("### 💡 Insights")
        if not categories.empty:
            # Sort by sales descending
            cats_sorted = categories.sort_values('Sales', ascending=False)
            top_cat = cats_sorted.iloc[0]
            st.info(f"**Top Category:** {top_cat['Category']} (£{top_cat['Sales']:,.2f})")
            st.write("This category generates the highest revenue for your store.")

    # --- LEAST SOLD ---
    st.subheader("📉 Slowest Moving Items (Bottom 10)")
    
    # Format for display
    display_least = least_sold[['Item', 'Items sold', 'Sales']].head(10).copy()
    display_least['Sales'] = display_least['Sales'].apply(lambda x: f"£{x:,.2f}")
    
    st.dataframe(
        display_least,
        use_container_width=True,
        hide_index=True
    )

if __name__ == "__main__":
    show_menu_analysis()
