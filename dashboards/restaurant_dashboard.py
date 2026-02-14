"""
Restaurant Analytics Dashboard
Afrikana / Chocoberry Restaurants
Built with Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add current directory to path to allow importing local modules
sys.path.append(str(Path(__file__).parent))
from menu_analysis import show_menu_analysis

# ============================================================================
# PASSWORD PROTECTION
# ============================================================================

def check_password():
    """Returns True if user entered correct password."""
    
    def password_entered():
        """Callback when password is entered."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False
    
    # First run - show password input
    if "password_correct" not in st.session_state:
        st.markdown("# 🔒 Dashboard Access")
        st.markdown("### Chocoberry Cardiff - Sales Analytics")
        st.text_input(
            "Enter Password:",
            type="password",
            on_change=password_entered,
            key="password"
        )
        st.info("💡 Enter the dashboard password to continue")
        return False
    
    # Password was incorrect
    elif not st.session_state["password_correct"]:
        st.markdown("# 🔒 Dashboard Access")
        st.markdown("### Chocoberry Cardiff - Sales Analytics")
        st.text_input(
            "Enter Password:",
            type="password",
            on_change=password_entered,
            key="password"
        )
        st.error("❌ Incorrect password. Please try again.")
        return False
    
    # Password correct
    else:
        return True

# Check password before loading dashboard
if not check_password():
    st.stop()

# ============================================================================
# DASHBOARD STARTS HERE (Only accessible after password)
# ============================================================================

# Page configuration
st.set_page_config(
    page_title="Restaurant Analytics Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF6B6B;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# LOAD DATA
@st.cache_data
def load_data():
    """Load all CSV files"""
    data_path = Path(__file__).parent.parent / 'data' / 'raw' / 'chocoberry_cardiff'
    
    try:
        # Load main sales data
        sales_data = pd.read_csv(data_path / 'sales_data.csv')
        sales_data['Order time'] = pd.to_datetime(sales_data['Order time'])
        
        # Convert numeric columns (handles strings with commas)
        numeric_columns = ['Gross sales', 'Tax on gross sales', 'Tips', 'Delivery charges', 
                          'Service charges', 'DRS charges', 'Packaging charges', 
                          'Additional charges', 'Charges', 'Revenue', 'Refunds', 
                          'Revenue after refunds', 'Discounts']
        
        for col in numeric_columns:
            if col in sales_data.columns:
                if sales_data[col].dtype == 'object':
                    sales_data[col] = sales_data[col].str.replace(',', '', regex=False)
                sales_data[col] = pd.to_numeric(sales_data[col], errors='coerce').fillna(0)
        
        return sales_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

sales_data = load_data()

if sales_data is None:
    st.stop()

# SIDEBAR FILTERS
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3170/3170733.png", width=100)
st.sidebar.title("Filters")

# Date range filter
min_date = sales_data['Order time'].min().date()
max_date = sales_data['Order time'].max().date()

st.sidebar.subheader("📅 Date Range")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply date filter
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_sales = sales_data[
        (sales_data['Order time'].dt.date >= start_date) &
        (sales_data['Order time'].dt.date <= end_date)
    ]
else:
    # Default to full range if only one date selected
    start_date = min_date
    end_date = max_date
    filtered_sales = sales_data

# Dispatch type filter
st.sidebar.subheader("🚚 Dispatch Type")
all_dispatch_types = ['All'] + list(filtered_sales['Dispatch type'].unique())
selected_dispatch = st.sidebar.selectbox("Select Dispatch Type", all_dispatch_types)

if selected_dispatch != 'All':
    filtered_sales = filtered_sales[filtered_sales['Dispatch type'] == selected_dispatch]

# Sales channel filter
st.sidebar.subheader("📱 Sales Channel")
all_channels = ['All'] + list(filtered_sales['Sales channel type'].unique())
selected_channel = st.sidebar.selectbox("Select Sales Channel", all_channels)

if selected_channel != 'All':
    filtered_sales = filtered_sales[filtered_sales['Sales channel type'] == selected_channel]

st.sidebar.markdown("---")
st.sidebar.info(f"📊 **{len(filtered_sales):,}** transactions selected")

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

# Header
st.markdown('<h1 class="main-header">🍽️ Restaurant Analytics Dashboard</h1>', unsafe_allow_html=True)
st.markdown(f"**Analytics Period:** {start_date.strftime('%d %b %Y')} - {end_date.strftime('%d %b %Y')}")

# Data quality notice
if end_date >= pd.to_datetime('2026-02-13').date():
    st.info("📊 **Data Quality Notice:** Data for February 13, 2026 is incomplete (partial day). For accurate trend analysis, we recommend using the date range **January 4 - February 12, 2026** (40 complete days).")


# KPI METRICS ROW
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_revenue = filtered_sales['Revenue'].sum()
    revenue_display = f"£{total_revenue/1000:.1f}K" if total_revenue >= 1000 else f"£{total_revenue:,.2f}"
    st.metric("💰 Total Revenue", revenue_display, f"{len(filtered_sales)} orders")

with col2:
    avg_order_value = filtered_sales['Gross sales'].mean()
    st.metric("📊 Average Order", f"£{avg_order_value:.2f}", "Per transaction")

with col3:
    total_orders = len(filtered_sales)
    st.metric("🧾 Total Orders", f"{total_orders:,}", "All time")

with col4:
    total_tax = filtered_sales['Tax on gross sales'].sum()
    tax_display = f"£{total_tax/1000:.1f}K" if total_tax >= 1000 else f"£{total_tax:,.2f}"
    st.metric("💷 Total Tax", tax_display, "Collected")

with col5:
    total_charges = filtered_sales['Charges'].sum()
    st.metric("📦 Delivery Charges", f"£{total_charges:.2f}", "Total fees")

st.markdown("---")

# ============================================================================
# SECTION 1: PERFORMANCE TRENDS
# ============================================================================

st.header("📊 Performance Trends")
st.caption("Track your business momentum with rolling averages and weekly comparisons")

# Calculate 7-day rolling average
daily_data = filtered_sales.groupby(filtered_sales['Order time'].dt.date).agg({
    'Revenue': 'sum',
    'Gross sales': 'sum',
    'Order ID': 'count'
}).reset_index()
daily_data.columns = ['Date', 'Revenue', 'Gross Sales', 'Orders']
daily_data = daily_data.sort_values('Date')

# Add 7-day rolling average
daily_data['Revenue_7d_avg'] = daily_data['Revenue'].rolling(window=7, min_periods=1).mean()
daily_data['Orders_7d_avg'] = daily_data['Orders'].rolling(window=7, min_periods=1).mean()

# Week-over-week calculation
daily_data['Week'] = pd.to_datetime(daily_data['Date']).dt.isocalendar().week
weekly_data = daily_data.groupby('Week').agg({
    'Revenue': 'sum',
    'Orders': 'sum',
    'Date': 'min'  # First day of week
}).reset_index()
weekly_data = weekly_data.sort_values('Date')

# Calculate week-over-week change
if len(weekly_data) >= 2:
    current_week_revenue = weekly_data.iloc[-1]['Revenue']
    last_week_revenue = weekly_data.iloc[-2]['Revenue']
    wow_revenue_change = ((current_week_revenue - last_week_revenue) / last_week_revenue * 100) if last_week_revenue > 0 else 0
    
    current_week_orders = weekly_data.iloc[-1]['Orders']
    last_week_orders = weekly_data.iloc[-2]['Orders']
    wow_orders_change = ((current_week_orders - last_week_orders) / last_week_orders * 100) if last_week_orders > 0 else 0
else:
    wow_revenue_change = 0
    wow_orders_change = 0

col1, col2 = st.columns(2)

with col1:
    # 7-Day Rolling Average Chart
    st.subheader("📈 7-Day Rolling Average Trend")
    fig_rolling = go.Figure()
    
    # Daily revenue (light line)
    fig_rolling.add_trace(go.Scatter(
        x=daily_data['Date'],
        y=daily_data['Revenue'],
        name='Daily Revenue',
        mode='lines',
        line=dict(color='lightblue', width=1),
        opacity=0.5
    ))
    
    # 7-day average (bold line)
    fig_rolling.add_trace(go.Scatter(
        x=daily_data['Date'],
        y=daily_data['Revenue_7d_avg'],
        name='7-Day Average',
        mode='lines',
        line=dict(color='#FF6B6B', width=3)
    ))
    
    fig_rolling.update_layout(height=350, xaxis_title="Date", yaxis_title="Revenue (£)", hovermode='x unified', showlegend=True)
    st.plotly_chart(fig_rolling, use_container_width=True)
    
    current_7d_avg = daily_data['Revenue_7d_avg'].iloc[-1]
    st.metric("Current 7-Day Average", f"£{current_7d_avg:,.2f}/day", "Average daily revenue over last 7 days")

with col2:
    # Week-over-Week Comparison
    st.subheader("📅 Week-over-Week Growth")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Revenue Growth", f"{wow_revenue_change:+.1f}%", "vs last week", delta_color="normal" if wow_revenue_change >= 0 else "inverse")
    with col_b:
        st.metric("Orders Growth", f"{wow_orders_change:+.1f}%", "vs last week", delta_color="normal" if wow_orders_change >= 0 else "inverse")
    
    st.write("**Weekly Performance:**")
    recent_weeks = weekly_data.tail(5).copy()
    recent_weeks['Week Start'] = pd.to_datetime(recent_weeks['Date']).dt.strftime('%b %d')
    recent_weeks['Revenue'] = recent_weeks['Revenue'].apply(lambda x: f"£{x:,.0f}")
    recent_weeks['Orders'] = recent_weeks['Orders'].apply(lambda x: f"{x:,.0f}")
    
    st.dataframe(recent_weeks[['Week Start', 'Revenue', 'Orders']], hide_index=True, use_container_width=True)
    
    # Data quality notice for incomplete weeks
    if len(weekly_data) > 0:
        latest_week_start = pd.to_datetime(weekly_data.iloc[-1]['Date'])
        latest_week_orders = weekly_data.iloc[-1]['Orders']
        
        # Check if current week is incomplete (less than 7 days or unusually low orders)
        days_in_current_week = (pd.to_datetime(max_date) - latest_week_start).days + 1
        
        if days_in_current_week < 7 or latest_week_orders < 800:
            st.info(f"ℹ️ **Data Quality Notice:** The current week (starting {latest_week_start.strftime('%b %d')}) contains only {days_in_current_week} day(s) of data. Week-over-week comparisons may not reflect actual performance. For accurate trend analysis, compare complete weeks only.")

st.markdown("---")

# ============================================================================
# SECTION 2: SALES PERFORMANCE (TABS)
# ============================================================================

st.header("📈 Sales Performance")
tab1, tab2, tab3 = st.tabs(["Daily Sales", "Weekly Trends", "Monthly Overview"])

with tab1:
    st.subheader("Daily Sales Trend")
    fig_daily = px.bar(
        daily_data, x='Date', y='Revenue', title='Daily Revenue',
        color='Revenue', color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_daily, use_container_width=True)

with tab2:
    st.subheader("Weekly Sales")
    filtered_sales['Week'] = filtered_sales['Order time'].dt.to_period('W').astype(str)
    weekly_sales = filtered_sales.groupby('Week')['Revenue'].sum().reset_index()
    fig_weekly = px.bar(weekly_sales, x='Week', y='Revenue', title='Weekly Revenue')
    st.plotly_chart(fig_weekly, use_container_width=True)

with tab3:
    st.subheader("Monthly Sales")
    filtered_sales['Month'] = filtered_sales['Order time'].dt.to_period('M').astype(str)
    monthly_sales = filtered_sales.groupby('Month')['Revenue'].sum().reset_index()
    fig_monthly = px.bar(monthly_sales, x='Month', y='Revenue', title='Monthly Revenue')
    st.plotly_chart(fig_monthly, use_container_width=True)

st.markdown("---")

# ============================================================================
# SECTION 2.5: WEEKLY PATTERNS
# ============================================================================

st.header("📅 Weekly Trading Patterns")
col1, col2 = st.columns([2, 1])

# Data Prep for Weekly Patterns
pattern_data = filtered_sales.copy()
pattern_data['Day Name'] = pattern_data['Order time'].dt.day_name()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Group by Day
weekly_stats = pattern_data.groupby('Day Name').agg({
    'Revenue': 'sum',
    'Order ID': 'count',
    'Gross sales': 'mean'
}).reindex(day_order).fillna(0).reset_index()
weekly_stats.columns = ['Day', 'Total Revenue', 'Orders', 'Avg Order Value']

# Find Busiest/Slowest
if not weekly_stats['Total Revenue'].sum() == 0:
    busiest_day = weekly_stats.loc[weekly_stats['Total Revenue'].idxmax()]
    # Filter for non-zero days to find slowest OPERATING day
    operating_days = weekly_stats[weekly_stats['Total Revenue'] > 0]
    if not operating_days.empty:
        slowest_day = operating_days.loc[operating_days['Total Revenue'].idxmin()]
    else:
        slowest_day = weekly_stats.iloc[0]
else:
    busiest_day = weekly_stats.iloc[0]
    slowest_day = weekly_stats.iloc[0]

with col1:
    fig_week = px.bar(
        weekly_stats, 
        x='Day', 
        y='Total Revenue', 
        title='Average Revenue by Day of Week',
        color='Total Revenue',
        color_continuous_scale='Viridis'
    )
    fig_week.update_layout(height=350, xaxis_title=None)
    st.plotly_chart(fig_week, use_container_width=True)

with col2:
    st.subheader("🏆 Day Performance")
    
    # Busiest Day Card
    st.success(f"**Busiest Day:** {busiest_day['Day']}\n\n💰 £{busiest_day['Total Revenue']:,.0f} ({int(busiest_day['Orders'])} Orders)")
    
    # Slowest Day Card
    st.info(f"**Slowest Day:** {slowest_day['Day']}\n\n💤 £{slowest_day['Total Revenue']:,.0f} ({int(slowest_day['Orders'])} Orders)")
    
    avg_rev = weekly_stats[weekly_stats['Total Revenue']>0]['Total Revenue'].mean() if not weekly_stats[weekly_stats['Total Revenue']>0].empty else 0
    st.metric("Avg Daily Revenue", f"£{avg_rev:,.0f}")

st.markdown("---")

# ============================================================================
# SECTION 3: DISPATCH & CHANNELS
# ============================================================================

st.header("📦 Dispatch & Sales Channels")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Dispatch Type")
    dispatch_sales = filtered_sales.groupby('Dispatch type').agg({'Gross sales': 'sum'}).reset_index()
    fig_dispatch = px.pie(dispatch_sales, values='Gross sales', names='Dispatch type', title='Revenue Share', hole=0.4)
    st.plotly_chart(fig_dispatch, use_container_width=True)

with col2:
    st.subheader("Sales by Channel")
    channel_sales = filtered_sales.groupby('Sales channel name').agg({'Gross sales': 'sum'}).reset_index()
    fig_channel = px.bar(channel_sales, x='Sales channel name', y='Gross sales', title='Revenue by Platform', color='Gross sales')
    st.plotly_chart(fig_channel, use_container_width=True)

st.markdown("---")

# ============================================================================
# SECTION 4: HOURLY & MEAL PERIOD
# ============================================================================

st.header("🕐 Hourly & Meal Period Analysis")

# 1. Precise Hourly Calculation (0-23)
hourly_data = filtered_sales.copy()
hourly_data['Hour'] = hourly_data['Order time'].dt.hour
hourly_stats = hourly_data.groupby('Hour')['Revenue'].sum().reset_index()

# Complete the 0-23 range
all_hours = pd.DataFrame({'Hour': range(24)})
hourly_stats = all_hours.merge(hourly_stats, on='Hour', how='left').fillna(0)

# Identify Peaks
hourly_stats['Hour Label'] = hourly_stats['Hour'].apply(
    lambda h: datetime.strptime(str(int(h)), "%H").strftime("%I %p").lstrip("0")
)

# Identify Top 3 Peaks
top_3_hours = hourly_stats.sort_values('Revenue', ascending=False).head(3)

# Identify Top 3 Slowest (Operating hours -> non-zero revenue)
operating_hours = hourly_stats[hourly_stats['Revenue'] > 0]
bottom_3_hours = operating_hours.sort_values('Revenue', ascending=True).head(3)

# Metrics Columns
m1, m2 = st.columns(2)

def styled_metric_box(hour, revenue, rank, is_peak=True):
    color = "#FF6B6B" if is_peak else "#667eea"
    icon = "🔥" if is_peak else "💤"
    # Convert hex to rgb for rgba background
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    bg_color = f"rgba({r}, {g}, {b}, 0.1)"
    
    st.markdown(f"""
    <div style="
        background-color: {bg_color};
        border-left: 5px solid {color};
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    ">
        <div style="font-size: 1.1em; font-weight: bold;">
            <span style="opacity: 0.7; margin-right: 8px;">#{rank}</span> {icon} {hour}
        </div>
        <div style="font-size: 1.2em; font-weight: bold; color: {color};">
            £{revenue:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with m1:
    st.subheader("🔥 Top 3 Busiest Hours")
    if not top_3_hours.empty:
        for i, (_, row) in enumerate(top_3_hours.iterrows(), 1):
            styled_metric_box(row['Hour Label'], row['Revenue'], i, is_peak=True)
    else:
        st.info("No data available")

with m2:
    st.subheader("💤 Top 3 Quietest Hours")
    if not bottom_3_hours.empty:
        for i, (_, row) in enumerate(bottom_3_hours.iterrows(), 1):
            styled_metric_box(row['Hour Label'], row['Revenue'], i, is_peak=False)
    else:
        st.info("No data available")

st.markdown("##### 📈 24-Hour Activity Trend")
# Line Chart
fig_hourly = px.line(
    hourly_stats, 
    x='Hour', 
    y='Revenue', 
    markers=True
)
fig_hourly.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=hourly_stats['Hour'],
        ticktext=hourly_stats['Hour Label'],
        title="Time of Day"
    ),
    yaxis=dict(title="Total Revenue (£)"),
    height=300,
    margin=dict(l=20, r=20, t=20, b=20)
)
st.plotly_chart(fig_hourly, use_container_width=True)

# Meal Period Analysis (Existing Logic)
st.subheader("🍱 Meal Period Breakdown")

def categorize_meal_period(hour):
    if 8 <= hour < 12: return "🌅 Breakfast (8am-12pm)"
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
    fig_pie = px.pie(meal_summary, values='Revenue', names='Meal Period', title='Sales Share by Meal Time', color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("🏆 Best & Worst Periods")
    if not meal_summary.empty:
        best = meal_summary.iloc[0]
        worst = meal_summary.iloc[-1]
        st.success(f"**Best:** {best['Meal Period']} (£{best['Revenue']:,.0f})")
        st.error(f"**Slowest:** {worst['Meal Period']} (£{worst['Revenue']:,.0f})")

# ============================================================================
# SECTION 5: MENU ANALYSIS (NEW)
# ============================================================================

# This function adds its own header and separator
show_menu_analysis()
