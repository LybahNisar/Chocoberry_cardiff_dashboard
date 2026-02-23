import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

def show_menu_analysis(item_data=None):
    st.markdown("---")
    st.header("🍔 Menu Analysis")
    st.caption("Detailed breakdown of top sellers, categories, and slow-moving items")

    # ── DATA SOURCE LOGIC ──────────────────────────────────
    if item_data is not None and not item_data.empty:
        st.sidebar.info("✨ Using Live Item Details")

        most_sold = item_data.groupby('Item').agg({
            'Revenue': 'sum',
            'Quantity': 'sum'
        }).reset_index()
        most_sold.columns = ['Item', 'Sales', 'Items sold']
        most_sold = most_sold.sort_values('Sales', ascending=False)

        categories = item_data.groupby('Category').agg({
            'Revenue': 'sum',
            'Quantity': 'sum'
        }).reset_index()
        categories.columns = ['Category', 'Sales', 'Items sold']

        least_sold = most_sold.sort_values('Items sold', ascending=True)

    else:
        # Fallback to static CSVs if no live item data
        data_path = Path(__file__).parent.parent / 'data' / 'raw' / 'chocoberry_cardiff'
        try:
            most_sold   = pd.read_csv(data_path / 'most_sold_items.csv')
            least_sold  = pd.read_csv(data_path / 'least_sold_items.csv')
            categories  = pd.read_csv(data_path / 'best-selling_categories.csv')

            for df in [most_sold, least_sold, categories]:
                if 'Sales' in df.columns and df['Sales'].dtype == 'object':
                    df['Sales'] = pd.to_numeric(
                        df['Sales'].astype(str).str.replace(',', ''), errors='coerce'
                    )
                if 'Items sold' in df.columns and df['Items sold'].dtype == 'object':
                    df['Items sold'] = pd.to_numeric(
                        df['Items sold'].astype(str).str.replace(',', ''), errors='coerce'
                    )
            st.sidebar.warning("⚠️ Using Static CSV Data")

        except Exception as e:
            st.info("No menu data available yet. Menu analysis will populate as new orders come in via webhook.")
            return

    if most_sold is None or most_sold.empty:
        st.info("No menu data available yet.")
        return

    # ── TOP 10 ITEMS ───────────────────────────────────────
    st.subheader("🏆 Top 10 Best Sellers")
    col1, col2 = st.columns(2)

    with col1:
        fig_rev = px.bar(
            most_sold.head(10),
            x='Sales',
            y='Item',
            orientation='h',
            title="Top 10 by Revenue (£)",
            color='Sales',
            color_continuous_scale='Greens'
        )
        fig_rev.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_rev, use_container_width=True)

    with col2:
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
        fig_vol.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_vol, use_container_width=True)

    # ── CATEGORY ANALYSIS ──────────────────────────────────
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
            cats_sorted = categories.sort_values('Sales', ascending=False)
            top_cat     = cats_sorted.iloc[0]
            worst_cat   = cats_sorted.iloc[-1]
            st.info(f"**Top Category:** {top_cat['Category']} (£{top_cat['Sales']:,.2f})")
            st.warning(f"**Lowest Category:** {worst_cat['Category']} (£{worst_cat['Sales']:,.2f})")
            st.write("Focus promotions on your lowest performing category to boost revenue.")

    # ── LEAST SOLD ─────────────────────────────────────────
    st.subheader("📉 Slowest Moving Items (Bottom 10)")
    display_least = least_sold[['Item', 'Items sold', 'Sales']].head(10).copy()
    display_least['Sales'] = display_least['Sales'].apply(lambda x: f"£{x:,.2f}")
    st.dataframe(display_least, use_container_width=True, hide_index=True)

    # ── ITEM PERFORMANCE TRENDS ────────────────────────────
    st.markdown("---")
    st.subheader("📈 Item Performance Trends")
    st.caption("Track how your top items perform over time")

    try:
        if item_data is not None and not item_data.empty:
            sales_df_for_trends = item_data.copy()
        else:
            data_path = Path(__file__).parent.parent / 'data' / 'raw' / 'chocoberry_cardiff'
            sales_df_for_trends = pd.read_csv(data_path / 'sales_data.csv')
            sales_df_for_trends['Order time'] = pd.to_datetime(sales_df_for_trends['Order time'])

        top_5_items = most_sold.head(5)['Item'].tolist()
        tab1, tab2 = st.tabs(["📅 Daily Trends", "📊 Weekly Trends"])

        with tab1:
            st.markdown("**Daily sales for top 5 items**")
            if 'Item' in sales_df_for_trends.columns:
                top_items_daily = sales_df_for_trends[
                    sales_df_for_trends['Item'].isin(top_5_items)
                ].copy()
                top_items_daily['Date'] = pd.to_datetime(
                    top_items_daily['Order time']
                ).dt.date

                daily_trends = top_items_daily.groupby(['Date', 'Item']).agg({
                    'Revenue': 'sum',
                    'Quantity': 'sum'
                }).reset_index()
                daily_trends.columns = ['Date', 'Item', 'Revenue', 'Quantity']

                fig_daily = px.line(
                    daily_trends,
                    x='Date',
                    y='Revenue',
                    color='Item',
                    title='Daily Revenue by Top 5 Items',
                    markers=True
                )
                fig_daily.update_layout(hovermode='x unified')
                st.plotly_chart(fig_daily, use_container_width=True)
            else:
                st.info("Item-level daily data will appear as new webhook orders come in.")

        with tab2:
            st.markdown("**Weekly sales for top 5 items**")
            if 'Item' in sales_df_for_trends.columns:
                top_items_weekly = sales_df_for_trends[
                    sales_df_for_trends['Item'].isin(top_5_items)
                ].copy()
                top_items_weekly['Week'] = pd.to_datetime(
                    top_items_weekly['Order time']
                ).dt.to_period('W').astype(str)

                weekly_trends = top_items_weekly.groupby(['Week', 'Item']).agg({
                    'Revenue': 'sum',
                    'Quantity': 'sum'
                }).reset_index()
                weekly_trends.columns = ['Week', 'Item', 'Revenue', 'Quantity']

                fig_weekly = px.bar(
                    weekly_trends,
                    x='Week',
                    y='Revenue',
                    color='Item',
                    title='Weekly Revenue by Top 5 Items',
                    barmode='group'
                )
                st.plotly_chart(fig_weekly, use_container_width=True)

                st.markdown("**Weekly Summary Table**")
                pivot_table = weekly_trends.pivot(
                    index='Week', columns='Item', values='Revenue'
                ).fillna(0)
                pivot_table = pivot_table.apply(
                    lambda x: x.map(lambda y: f"£{y:,.0f}")
                )
                st.dataframe(pivot_table, use_container_width=True)
            else:
                st.info("Item-level weekly data will appear as new webhook orders come in.")

    except Exception as e:
        st.warning(f"⚠️ Could not load trend data: {e}")
        st.info("Trend analysis will populate automatically as new orders arrive via webhook.")

if __name__ == "__main__":
    show_menu_analysis()

