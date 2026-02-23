"""
Restaurant Analytics Dashboard
Chocoberry Cardiff
Built with Streamlit - Connected to Supabase
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path
import sys
import logging
import psycopg2
from sqlalchemy import create_engine
from urllib.parse import quote_plus


# Add project paths for imports
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent))
from menu_analysis import show_menu_analysis

# ============================================================================
# PASSWORD PROTECTION
# ============================================================================

def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("# 🔒 Dashboard Access")
        st.markdown("### Chocoberry Cardiff - Sales Analytics")
        st.text_input("Enter Password:", type="password", on_change=password_entered, key="password")
        st.info("💡 Enter the dashboard password to continue")
        return False
    elif not st.session_state["password_correct"]:
        st.markdown("# 🔒 Dashboard Access")
        st.markdown("### Chocoberry Cardiff - Sales Analytics")
        st.text_input("Enter Password:", type="password", on_change=password_entered, key="password")
        st.error("❌ Incorrect password. Please try again.")
        return False
    else:
        return True

if not check_password():
    st.stop()

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Restaurant Analytics Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF6B6B;
        text-align: center;
        padding: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SUPABASE CONNECTION
# ============================================================================


def get_db():
    db_host     = st.secrets["supabase"]["db_host"]
    db_port     = st.secrets["supabase"]["db_port"]
    db_name     = st.secrets["supabase"]["db_name"]
    db_user     = st.secrets["supabase"]["db_user"]
    db_password = quote_plus(st.secrets["supabase"]["db_password"])
    
    connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return create_engine(connection_string)
# ============================================================================
# LOAD DATA FROM SUPABASE
# ============================================================================
@st.cache_data(ttl=30)
def load_data():
    try:
        engine = get_db()

        query = """
        SELECT
            order_id as "Order ID",
            order_time as "Order time",
            property_name as "Property name",
            gross_sales as "Gross sales",
            tax as "Tax on gross sales",
            tips as "Tips",
            delivery_charges as "Delivery charges",
            service_charges as "Service charges",
            additional_charges as "Additional charges",
            charges as "Charges",
            revenue as "Revenue",
            refunds as "Refunds",
            discounts as "Discounts",
            dispatch_type as "Dispatch type",
            payment_method as "Payment method",
            sales_channel_type as "Sales channel type",
            sales_channel_name as "Sales channel name",
            is_preorder as "Is preorder"
        FROM orders
        ORDER BY order_time DESC
        """

        item_query = """
        SELECT
            order_id as "Order ID",
            order_time as "Order time",
            item_name as "Item",
            category as "Category",
            price as "Price",
            quantity as "Quantity",
            revenue as "Revenue"
        FROM order_items
        """

        with engine.connect() as conn:
            sales_data = pd.read_sql_query(query, conn)
            item_data  = pd.read_sql_query(item_query, conn)

        sales_data['Order time'] = pd.to_datetime(
            sales_data['Order time'], format='mixed', dayfirst=False
        )
        if not item_data.empty:
            item_data['Order time'] = pd.to_datetime(
                item_data['Order time'], format='mixed', dayfirst=False
            )

        return sales_data, "supabase", item_data

    except Exception as e:
        logging.error(f"Supabase Load Error: {e}")
        st.error(f"Database error: {e}")
        return None, "error", None
# ============================================================================
# SIDEBAR
# ============================================================================

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3170/3170733.png", width=100)

if st.sidebar.button("🔄 Refresh Data"):
    load_data.clear()
    st.rerun()

# Load Data
sales_data, data_source, item_data = load_data()

if sales_data is None:
    st.error("Error loading data from Supabase.")
    st.stop()

# Sidebar stats
total_db = len(sales_data)
st.sidebar.success(f"🟢 **Live Supabase**")
st.sidebar.caption(f"💎 Total: {total_db:,} orders")
st.sidebar.caption(f"📅 Latest: {sales_data['Order time'].max().strftime('%d %b %Y %H:%M')}")

st.sidebar.title("Filters")

# Date filter
min_date = sales_data['Order time'].min().date()
max_date = sales_data['Order time'].max().date()

st.sidebar.subheader("📅 Date Range")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_sales = sales_data[
        (sales_data['Order time'].dt.date >= start_date) &
        (sales_data['Order time'].dt.date <= end_date)
    ]
else:
    start_date, end_date = min_date, max_date
    filtered_sales = sales_data

# Dispatch filter
st.sidebar.subheader("🚚 Dispatch Type")
all_dispatch_types = ['All'] + list(filtered_sales['Dispatch type'].dropna().unique())
selected_dispatch = st.sidebar.selectbox("Select Dispatch Type", all_dispatch_types)
if selected_dispatch != 'All':
    filtered_sales = filtered_sales[filtered_sales['Dispatch type'] == selected_dispatch]

# Channel filter
st.sidebar.subheader("📱 Sales Channel")
all_channels = ['All'] + list(filtered_sales['Sales channel type'].dropna().unique())
selected_channel = st.sidebar.selectbox("Select Sales Channel", all_channels)
if selected_channel != 'All':
    filtered_sales = filtered_sales[filtered_sales['Sales channel type'] == selected_channel]

st.sidebar.markdown("---")
st.sidebar.info(f"📊 **{len(filtered_sales):,}** transactions selected")

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

st.markdown('<h1 class="main-header">🍽️ Restaurant Analytics Dashboard</h1>', unsafe_allow_html=True)
st.markdown(f"**Analytics Period:** {start_date.strftime('%d %b %Y')} - {end_date.strftime('%d %b %Y')}")

# KPI METRICS
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    total_revenue = filtered_sales['Revenue'].sum()
    revenue_display = f"£{total_revenue/1000:.1f}K" if total_revenue >= 1000 else f"£{total_revenue:,.2f}"
    st.metric("💰 Total Revenue", revenue_display, f"{len(filtered_sales)} orders")
with col2:
    avg_order_value = filtered_sales['Gross sales'].mean()
    st.metric("📊 Average Order", f"£{avg_order_value:.2f}", "Per transaction")
with col3:
    st.metric("🧾 Total Orders", f"{len(filtered_sales):,}", "All time")
with col4:
    total_tax = filtered_sales['Tax on gross sales'].sum()
    tax_display = f"£{total_tax/1000:.1f}K" if total_tax >= 1000 else f"£{total_tax:,.2f}"
    st.metric("💷 Total Tax", tax_display, "Collected")
with col5:
    total_delivery = filtered_sales['Delivery charges'].sum()
    st.metric("📦 Delivery Charges", f"£{total_delivery:,.2f}", "Total delivery fees")

st.markdown("---")

# ============================================================================
# SECTION 1: PERFORMANCE TRENDS
# ============================================================================

st.header("📊 Performance Trends")

daily_data = filtered_sales.groupby(filtered_sales['Order time'].dt.date).agg({
    'Revenue': 'sum',
    'Gross sales': 'sum',
    'Order ID': 'count'
}).reset_index()
daily_data.columns = ['Date', 'Revenue', 'Gross Sales', 'Orders']
daily_data = daily_data.sort_values('Date')
daily_data['Revenue_7d_avg'] = daily_data['Revenue'].rolling(window=7, min_periods=1).mean()
daily_data['Orders_7d_avg'] = daily_data['Orders'].rolling(window=7, min_periods=1).mean()

daily_data['Week'] = pd.to_datetime(daily_data['Date']).dt.isocalendar().week
weekly_data = daily_data.groupby('Week').agg({
    'Revenue': 'sum', 'Orders': 'sum', 'Date': 'min'
}).reset_index().sort_values('Date')

if len(weekly_data) >= 2:
    wow_revenue_change = ((weekly_data.iloc[-1]['Revenue'] - weekly_data.iloc[-2]['Revenue']) / weekly_data.iloc[-2]['Revenue'] * 100)
    wow_orders_change  = ((weekly_data.iloc[-1]['Orders']  - weekly_data.iloc[-2]['Orders'])  / weekly_data.iloc[-2]['Orders']  * 100)
else:
    wow_revenue_change = wow_orders_change = 0

col1, col2 = st.columns(2)
with col1:
    st.subheader("📈 7-Day Rolling Average")
    fig_rolling = go.Figure()
    fig_rolling.add_trace(go.Scatter(x=daily_data['Date'], y=daily_data['Revenue'], name='Daily Revenue', line=dict(color='lightblue', width=1), opacity=0.5))
    fig_rolling.add_trace(go.Scatter(x=daily_data['Date'], y=daily_data['Revenue_7d_avg'], name='7-Day Average', line=dict(color='#FF6B6B', width=3)))
    fig_rolling.update_layout(height=350, xaxis_title="Date", yaxis_title="Revenue (£)", hovermode='x unified')
    st.plotly_chart(fig_rolling, use_container_width=True)
    st.metric("Current 7-Day Average", f"£{daily_data['Revenue_7d_avg'].iloc[-1]:,.2f}/day")

with col2:
    st.subheader("📅 Week-over-Week Growth")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Revenue Growth", f"{wow_revenue_change:+.1f}%", "vs last week")
    with col_b:
        st.metric("Orders Growth", f"{wow_orders_change:+.1f}%", "vs last week")
    recent_weeks = weekly_data.tail(5).copy()
    recent_weeks['Week Start'] = pd.to_datetime(recent_weeks['Date']).dt.strftime('%b %d')
    recent_weeks['Revenue'] = recent_weeks['Revenue'].apply(lambda x: f"£{x:,.0f}")
    recent_weeks['Orders']  = recent_weeks['Orders'].apply(lambda x: f"{x:,.0f}")
    st.dataframe(recent_weeks[['Week Start', 'Revenue', 'Orders']], hide_index=True, use_container_width=True)

st.markdown("---")

# ============================================================================
# SECTION 2: SALES PERFORMANCE
# ============================================================================

st.header("📈 Sales Performance")
tab1, tab2, tab3 = st.tabs(["Daily Sales", "Weekly Trends", "Monthly Overview"])

with tab1:
    fig_daily = px.bar(daily_data, x='Date', y='Revenue', title='Daily Revenue', color='Revenue', color_continuous_scale='Viridis')
    st.plotly_chart(fig_daily, use_container_width=True)

with tab2:
    filtered_sales['Week'] = filtered_sales['Order time'].dt.to_period('W').astype(str)
    weekly_sales = filtered_sales.groupby('Week')['Revenue'].sum().reset_index()
    fig_weekly = px.bar(weekly_sales, x='Week', y='Revenue', title='Weekly Revenue')
    st.plotly_chart(fig_weekly, use_container_width=True)

with tab3:
    filtered_sales['Month'] = filtered_sales['Order time'].dt.to_period('M').astype(str)
    monthly_sales = filtered_sales.groupby('Month')['Revenue'].sum().reset_index()
    fig_monthly = px.bar(monthly_sales, x='Month', y='Revenue', title='Monthly Revenue')
    st.plotly_chart(fig_monthly, use_container_width=True)

st.markdown("---")

# ============================================================================
# SECTION 3: WEEKLY PATTERNS
# ============================================================================

st.header("📅 Weekly Trading Patterns")
col1, col2 = st.columns([2, 1])

pattern_data = filtered_sales.copy()
pattern_data['Day Name'] = pattern_data['Order time'].dt.day_name()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekly_stats = pattern_data.groupby('Day Name').agg({
    'Revenue': 'sum', 'Order ID': 'count', 'Gross sales': 'mean'
}).reindex(day_order).fillna(0).reset_index()
weekly_stats.columns = ['Day', 'Total Revenue', 'Orders', 'Avg Order Value']

busiest_day = weekly_stats.loc[weekly_stats['Total Revenue'].idxmax()]
operating_days = weekly_stats[weekly_stats['Total Revenue'] > 0]
slowest_day = operating_days.loc[operating_days['Total Revenue'].idxmin()] if not operating_days.empty else weekly_stats.iloc[0]

with col1:
    fig_week = px.bar(weekly_stats, x='Day', y='Total Revenue', title='Revenue by Day of Week', color='Total Revenue', color_continuous_scale='Viridis')
    fig_week.update_layout(height=350)
    st.plotly_chart(fig_week, use_container_width=True)

with col2:
    st.subheader("🏆 Day Performance")
    st.success(f"**Busiest:** {busiest_day['Day']}\n\n💰 £{busiest_day['Total Revenue']:,.0f} ({int(busiest_day['Orders'])} orders)")
    st.info(f"**Slowest:** {slowest_day['Day']}\n\n💤 £{slowest_day['Total Revenue']:,.0f} ({int(slowest_day['Orders'])} orders)")
    avg_rev = weekly_stats[weekly_stats['Total Revenue'] > 0]['Total Revenue'].mean()
    st.metric("Avg Daily Revenue", f"£{avg_rev:,.0f}")

st.markdown("---")

# ============================================================================
# SECTION 4: DISPATCH & CHANNELS
# ============================================================================

st.header("📦 Dispatch & Sales Channels")
col1, col2 = st.columns(2)

with col1:
    dispatch_sales = filtered_sales.groupby('Dispatch type').agg({'Gross sales': 'sum'}).reset_index()
    fig_dispatch = px.pie(dispatch_sales, values='Gross sales', names='Dispatch type', title='Revenue by Dispatch Type', hole=0.4)
    st.plotly_chart(fig_dispatch, use_container_width=True)

with col2:
    channel_sales = filtered_sales.groupby('Sales channel name').agg({'Gross sales': 'sum'}).reset_index()
    fig_channel = px.bar(channel_sales, x='Sales channel name', y='Gross sales', title='Revenue by Platform', color='Gross sales')
    st.plotly_chart(fig_channel, use_container_width=True)

st.markdown("---")

# ============================================================================
# SECTION 5: HOURLY ANALYSIS
# ============================================================================

st.header("🕐 Hourly & Meal Period Analysis")

hourly_data = filtered_sales.copy()
hourly_data['Hour'] = hourly_data['Order time'].dt.hour
hourly_stats = hourly_data.groupby('Hour')['Revenue'].sum().reset_index()
all_hours = pd.DataFrame({'Hour': range(24)})
hourly_stats = all_hours.merge(hourly_stats, on='Hour', how='left').fillna(0)
hourly_stats['Hour Label'] = hourly_stats['Hour'].apply(
    lambda h: datetime.strptime(str(int(h)), "%H").strftime("%I %p").lstrip("0")
)

top_3_hours    = hourly_stats.sort_values('Revenue', ascending=False).head(3)
operating_hours = hourly_stats[hourly_stats['Revenue'] > 0]
bottom_3_hours  = operating_hours.sort_values('Revenue').head(3)

def styled_metric_box(hour, revenue, rank, is_peak=True):
    color = "#FF6B6B" if is_peak else "#667eea"
    icon  = "🔥" if is_peak else "💤"
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    st.markdown(f"""
    <div style="background-color:rgba({r},{g},{b},0.1);border-left:5px solid {color};
    padding:15px;border-radius:5px;margin-bottom:10px;display:flex;
    justify-content:space-between;align-items:center;">
        <div style="font-size:1.1em;font-weight:bold;">
            <span style="opacity:0.7;margin-right:8px;">#{rank}</span> {icon} {hour}
        </div>
        <div style="font-size:1.2em;font-weight:bold;color:{color};">£{revenue:,.0f}</div>
    </div>""", unsafe_allow_html=True)

m1, m2 = st.columns(2)
with m1:
    st.subheader("🔥 Top 3 Busiest Hours")
    for i, (_, row) in enumerate(top_3_hours.iterrows(), 1):
        styled_metric_box(row['Hour Label'], row['Revenue'], i, is_peak=True)
with m2:
    st.subheader("💤 Top 3 Quietest Hours")
    for i, (_, row) in enumerate(bottom_3_hours.iterrows(), 1):
        styled_metric_box(row['Hour Label'], row['Revenue'], i, is_peak=False)

st.markdown("##### 📈 24-Hour Activity Trend")
fig_hourly = px.line(hourly_stats, x='Hour', y='Revenue', markers=True)
fig_hourly.update_layout(
    xaxis=dict(tickmode='array', tickvals=hourly_stats['Hour'], ticktext=hourly_stats['Hour Label'], title="Time of Day"),
    yaxis=dict(title="Total Revenue (£)"), height=300
)
st.plotly_chart(fig_hourly, use_container_width=True)

st.subheader("🍱 Meal Period Breakdown")
def categorize_meal_period(hour):
    if 8  <= hour < 12: return "🌅 Breakfast (8am-12pm)"
    elif 12 <= hour < 16: return "🍽️ Lunch (12pm-4pm)"
    elif 16 <= hour < 20: return "🌆 Evening (4pm-8pm)"
    elif 20 <= hour < 24: return "🌙 Dinner (8pm-12am)"
    else: return "🌃 Night Shift (12am-8am)"

meal_data = filtered_sales.copy()
meal_data['Hour'] = meal_data['Order time'].dt.hour
meal_data['Meal Period'] = meal_data['Hour'].apply(categorize_meal_period)
meal_summary = meal_data.groupby('Meal Period').agg({'Revenue': 'sum', 'Order ID': 'count'}).reset_index()
meal_summary.columns = ['Meal Period', 'Revenue', 'Orders']
meal_summary = meal_summary.sort_values('Revenue', ascending=False)

col1, col2 = st.columns([3, 2])
with col1:
    fig_pie = px.pie(meal_summary, values='Revenue', names='Meal Period', title='Sales by Meal Time', color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_pie, use_container_width=True)
with col2:
    st.subheader("🏆 Best & Worst Periods")
    if not meal_summary.empty:
        st.success(f"**Best:** {meal_summary.iloc[0]['Meal Period']} (£{meal_summary.iloc[0]['Revenue']:,.0f})")
        st.error(f"**Slowest:** {meal_summary.iloc[-1]['Meal Period']} (£{meal_summary.iloc[-1]['Revenue']:,.0f})")

# ============================================================================
# SECTION 6: MENU ANALYSIS
# ============================================================================

show_menu_analysis(item_data)

# ============================================================================
# SECTION 7: FULL TRANSACTION HISTORY
# ============================================================================

st.markdown("---")
st.header("📑 Full Transaction History")
st.caption(f"Showing {len(filtered_sales):,} transactions")

st.dataframe(
    filtered_sales[[
        'Order ID', 'Order time', 'Revenue', 'Tax on gross sales',
        'Delivery charges', 'Dispatch type', 'Payment method', 'Sales channel name'
    ]].sort_values('Order time', ascending=False),
    use_container_width=True,
    hide_index=True
)

st.download_button(
    label="📥 Download Full Dataset (CSV)",
    data=filtered_sales.to_csv(index=False).encode('utf-8'),
    file_name=f"chocoberry_sales_export_{datetime.now().strftime('%Y%m%d')}.csv",
    mime='text/csv',
)