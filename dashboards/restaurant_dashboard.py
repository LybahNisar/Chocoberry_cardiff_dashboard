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
    /* Make metric text visible */
    .stMetric {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    .stMetric label {
        color: #333333 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #1f1f1f !important;
        font-size: 1.5rem !important;
        font-weight: bold !important;
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }
    .stMetric [data-testid="stMetricDelta"] {
        color: #666666 !important;
    }
</style>
""", unsafe_allow_html=True)

# Data loading function with caching
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
                sales_data[col] = pd.to_numeric(sales_data[col], errors='coerce').fillna(0)
        
        # Load summary files
        sales_overview = pd.read_csv(data_path / 'sales_overview.csv')
        sales_overview['Order time'] = pd.to_datetime(sales_overview['Order time'], errors='coerce')
        
        gross_sales_per_day = pd.read_csv(data_path / 'gross_sales_per_day.csv')
        gross_sales_by_dispatch = pd.read_csv(data_path / 'gross_sales_by_dispatch_type.csv')
        gross_sales_by_hour = pd.read_csv(data_path / 'gross_sales_by_hour_of_day.csv')
        gross_sales_by_channel = pd.read_csv(data_path / 'gross_sales_by_sales_channel.csv')
        gross_sales_by_day_of_week = pd.read_csv(data_path / 'gross_sales_per_day_of_week.csv')
        
        return {
            'sales_data': sales_data,
            'sales_overview': sales_overview,
            'gross_sales_per_day': gross_sales_per_day,
            'gross_sales_by_dispatch': gross_sales_by_dispatch,
            'gross_sales_by_hour': gross_sales_by_hour,
            'gross_sales_by_channel': gross_sales_by_channel,
            'gross_sales_by_day_of_week': gross_sales_by_day_of_week
        }
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Load data
data = load_data()

if data is None:
    st.stop()

# Extract dataframes
sales_data = data['sales_data']
sales_overview = data['sales_overview']

# ============================================================================
# SIDEBAR - Filters
# ============================================================================

st.sidebar.title("🎛️ Dashboard Controls")

# Date range filter
st.sidebar.subheader("📅 Date Range")
min_date = sales_data['Order time'].min().date()
max_date = sales_data['Order time'].max().date()

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
st.markdown(f"<p style='text-align: center; color: #666; font-size: 1.2rem;'>Chocoberry Cardiff | {start_date.strftime('%b %d, %Y')} - {end_date.strftime('%b %d, %Y')}</p>", unsafe_allow_html=True)
st.markdown("---")

# ============================================================================
# KPI METRICS ROW
# ============================================================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_revenue = filtered_sales['Revenue'].sum()
    # Format large numbers with K suffix to prevent truncation
    revenue_display = f"£{total_revenue/1000:.1f}K" if total_revenue >= 1000 else f"£{total_revenue:,.2f}"
    st.metric(
        label="💰 Total Revenue",
        value=revenue_display,
        delta=f"{len(filtered_sales)} orders"
    )

with col2:
    avg_order_value = filtered_sales['Gross sales'].mean()
    st.metric(
        label="📊 Average Order",
        value=f"£{avg_order_value:.2f}",
        delta=f"Per transaction"
    )

with col3:
    total_orders = len(filtered_sales)
    st.metric(
        label="🧾 Total Orders",
        value=f"{total_orders:,}",
        delta=f"All time"
    )

with col4:
    total_tax = filtered_sales['Tax on gross sales'].sum()
    # Format large numbers with K suffix to prevent truncation
    tax_display = f"£{total_tax/1000:.1f}K" if total_tax >= 1000 else f"£{total_tax:,.2f}"
    st.metric(
        label="💷 Total Tax",
        value=tax_display,
        delta="Collected"
    )

with col5:
    total_charges = filtered_sales['Charges'].sum()
    st.metric(
        label="📦 Delivery Charges",
        value=f"£{total_charges:.2f}",
        delta="Total fees"
    )


st.markdown("---")

# ============================================================================
# PERFORMANCE TRENDS ANALYSIS
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
    
    fig_rolling.update_layout(
        height=350,
        xaxis_title="Date",
        yaxis_title="Revenue (£)",
        hovermode='x unified',
        showlegend=True
    )
    
    st.plotly_chart(fig_rolling, use_container_width=True)
    
    # Current 7-day average
    current_7d_avg = daily_data['Revenue_7d_avg'].iloc[-1]
    st.metric(
        "Current 7-Day Average", 
        f"£{current_7d_avg:,.2f}/day",
        help="Average daily revenue over the last 7 days"
    )

with col2:
    # Week-over-Week Comparison
    st.subheader("📅 Week-over-Week Growth")
    
    # Show week comparison metrics
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.metric(
            "Revenue Growth",
            f"{wow_revenue_change:+.1f}%",
            delta=f"vs last week",
            delta_color="normal" if wow_revenue_change >= 0 else "inverse"
        )
    
    with col_b:
        st.metric(
            "Orders Growth",
            f"{wow_orders_change:+.1f}%",
            delta=f"vs last week",
            delta_color="normal" if wow_orders_change >= 0 else "inverse"
        )
    
    # Weekly breakdown table
    st.write("**Weekly Performance:**")
    
    if len(weekly_data) >= 5:
        recent_weeks = weekly_data.tail(5).copy()
    else:
        recent_weeks = weekly_data.copy()
    
    recent_weeks['Week Start'] = pd.to_datetime(recent_weeks['Date']).dt.strftime('%b %d')
    recent_weeks['Revenue'] = recent_weeks['Revenue'].apply(lambda x: f"£{x:,.0f}")
    recent_weeks['Orders'] = recent_weeks['Orders'].apply(lambda x: f"{x:,.0f}")
    
    st.dataframe(
        recent_weeks[['Week Start', 'Revenue', 'Orders']],
        hide_index=True,
        use_container_width=True
    )
    
    # Trend indicator
    if wow_revenue_change > 5:
        st.success("🚀 Strong growth this week!")
    elif wow_revenue_change > 0:
        st.info("📈 Growing steadily")
    elif wow_revenue_change > -5:
        st.warning("📊 Revenue slightly down")
    else:
        st.error("⚠️ Significant decline - investigate!")

st.markdown("---")

# ============================================================================
# REQUIREMENT 1: SALES DASHBOARDS
# ============================================================================

st.header("📈 Sales Performance")

tab1, tab2, tab3 = st.tabs(["Daily Sales", "Weekly Trends", "Monthly Overview"])

with tab1:
    st.subheader("Daily Sales Trend")
    
    # Group by date
    daily_sales = filtered_sales.groupby(filtered_sales['Order time'].dt.date).agg({
        'Gross sales': 'sum',
        'Revenue': 'sum',
        'Order ID': 'count'
    }).reset_index()
    daily_sales.columns = ['Date', 'Gross Sales', 'Revenue', 'Orders']
    
    # Create line chart
    fig_daily = go.Figure()
    fig_daily.add_trace(go.Scatter(
        x=daily_sales['Date'],
        y=daily_sales['Gross Sales'],
        name='Gross Sales',
        line=dict(color='#667eea', width=3),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.1)'
    ))
    fig_daily.add_trace(go.Scatter(
        x=daily_sales['Date'],
        y=daily_sales['Revenue'],
        name='Revenue',
        line=dict(color='#FF6B6B', width=2, dash='dash')
    ))
    
    fig_daily.update_layout(
        title="Daily Sales Performance",
        xaxis_title="Date",
        yaxis_title="Amount (£)",
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig_daily, use_container_width=True)
    
    # Show data table
    st.dataframe(daily_sales.style.format({
        'Gross Sales': '£{:,.2f}',
        'Revenue': '£{:,.2f}',
        'Orders': '{:,.0f}'
    }), use_container_width=True)

with tab2:
    st.subheader("Weekly Sales Analysis")
    
    # Group by week
    filtered_sales['Week'] = filtered_sales['Order time'].dt.to_period('W')
    weekly_sales = filtered_sales.groupby('Week').agg({
        'Gross sales': 'sum',
        'Revenue': 'sum',
        'Order ID': 'count'
    }).reset_index()
    weekly_sales['Week'] = weekly_sales['Week'].astype(str)
    weekly_sales.columns = ['Week', 'Gross Sales', 'Revenue', 'Orders']
    
    # Bar chart
    fig_weekly = px.bar(
        weekly_sales,
        x='Week',
        y='Gross Sales',
        title="Weekly Gross Sales",
        color='Gross Sales',
        color_continuous_scale='Viridis'
    )
    fig_weekly.update_layout(height=400)
    st.plotly_chart(fig_weekly, use_container_width=True)

with tab3:
    st.subheader("Monthly Revenue Overview")
    
    # Group by month
    filtered_sales['Month'] = filtered_sales['Order time'].dt.to_period('M')
    monthly_sales = filtered_sales.groupby('Month').agg({
        'Gross sales': 'sum',
        'Revenue': 'sum',
        'Order ID': 'count'
    }).reset_index()
    monthly_sales['Month'] = monthly_sales['Month'].astype(str)
    monthly_sales.columns = ['Month', 'Gross Sales', 'Revenue', 'Orders']
    
    # Create bar chart
    fig_monthly = go.Figure(data=[
        go.Bar(name='Gross Sales', x=monthly_sales['Month'], y=monthly_sales['Gross Sales'], marker_color='#667eea'),
        go.Bar(name='Revenue', x=monthly_sales['Month'], y=monthly_sales['Revenue'], marker_color='#FF6B6B')
    ])
    fig_monthly.update_layout(
        title="Monthly Sales Comparison",
        barmode='group',
        height=400
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

st.markdown("---")

# ============================================================================
# MEAL PERIOD ANALYSIS
# ============================================================================

st.header("🍽️ Meal Period Analysis")
st.caption("Sales breakdown by meal times: Breakfast, Lunch, Evening, Dinner, Night Shift")

# Define meal periods
def categorize_meal_period(hour):
    if 8 <= hour < 12:
        return "🌅 Breakfast (8am-12pm)"
    elif 12 <= hour < 16:
        return "🍽️ Lunch (12pm-4pm)"
    elif 16 <= hour < 20:
        return "🌆 Evening (4pm-8pm)"
    elif 20 <= hour < 24:
        return "🌙 Dinner (8pm-12am)"
    else:  # 0-7 hours
        return "🌃 Night Shift (12am-8am)"

# Add meal period to data
meal_data = filtered_sales.copy()
meal_data['Hour'] = meal_data['Order time'].dt.hour
meal_data['Meal Period'] = meal_data['Hour'].apply(categorize_meal_period)

# Calculate metrics by meal period
meal_summary = meal_data.groupby('Meal Period').agg({
    'Revenue': 'sum',
    'Gross sales': 'sum',
    'Order ID': 'count'
}).reset_index()
meal_summary.columns = ['Meal Period', 'Revenue', 'Gross Sales', 'Orders']

# Calculate percentages
total_revenue = meal_summary['Revenue'].sum()
meal_summary['% of Sales'] = (meal_summary['Revenue'] / total_revenue * 100).round(1)
meal_summary['Avg Order Value'] = (meal_summary['Gross Sales'] / meal_summary['Orders']).round(2)

# Sort by revenue descending
meal_summary = meal_summary.sort_values('Revenue', ascending=False)

# Create two columns
col1, col2 = st.columns([3, 2])

with col1:
    # Pie chart
    st.subheader("📊 Revenue Distribution by Meal Period")
    
    fig_pie = px.pie(
        meal_summary,
        values='Revenue',
        names='Meal Period',
        title='Sales Share by Meal Time',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    # Top performers
    st.subheader("🏆 Best & Worst Performers")
    
    best_period = meal_summary.iloc[0]
    worst_period = meal_summary.iloc[-1]
    
    st.success(f"**Best: {best_period['Meal Period']}**")
    st.write(f"- Revenue: £{best_period['Revenue']:,.2f}")
    st.write(f"- Share: {best_period['% of Sales']:.1f}%")
    st.write(f"- Orders: {best_period['Orders']:,.0f}")
    
    st.markdown("---")
    
    st.error(f"**Slowest: {worst_period['Meal Period']}**")
    st.write(f"- Revenue: £{worst_period['Revenue']:,.2f}")
    st.write(f"- Share: {worst_period['% of Sales']:.1f}%")
    st.write(f"- Orders: {worst_period['Orders']:,.0f}")

# Detailed table
st.subheader("📋 Detailed Meal Period Breakdown")

# Format the dataframe
display_summary = meal_summary.copy()
display_summary['Revenue'] = display_summary['Revenue'].apply(lambda x: f"£{x:,.2f}")
display_summary['Gross Sales'] = display_summary['Gross Sales'].apply(lambda x: f"£{x:,.2f}")
display_summary['Orders'] = display_summary['Orders'].apply(lambda x: f"{x:,.0f}")
display_summary['% of Sales'] = display_summary['% of Sales'].apply(lambda x: f"{x:.1f}%")
display_summary['Avg Order Value'] = display_summary['Avg Order Value'].apply(lambda x: f"£{x:.2f}")

st.dataframe(display_summary, hide_index=True, use_container_width=True)

# Insights
st.info("💡 **Pro Tip**: Focus marketing efforts on your slowest period to balance revenue throughout the day!")

st.markdown("---")

# ============================================================================
# REQUIREMENT 2: DELIVERY VS DINE-IN ANALYSIS
# ============================================================================

st.header("🚚 Delivery vs Dine-In Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Dispatch Type")
    
    # Group by dispatch type
    dispatch_sales = filtered_sales.groupby('Dispatch type').agg({
        'Gross sales': 'sum',
        'Order ID': 'count'
    }).reset_index()
    dispatch_sales.columns = ['Dispatch Type', 'Total Sales', 'Orders']
    
    # Pie chart
    fig_dispatch = px.pie(
        dispatch_sales,
        values='Total Sales',
        names='Dispatch Type',
        title="Revenue Distribution by Dispatch Type",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_dispatch.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_dispatch, use_container_width=True)

with col2:
    st.subheader("Order Count by Type")
    
    # Bar chart for order count
    fig_dispatch_orders = px.bar(
        dispatch_sales,
        x='Dispatch Type',
        y='Orders',
        title="Number of Orders by Dispatch Type",
        color='Orders',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig_dispatch_orders, use_container_width=True)

# Dispatch type breakdown table
st.subheader("Detailed Breakdown")
dispatch_sales['Avg Order Value'] = dispatch_sales['Total Sales'] / dispatch_sales['Orders']
st.dataframe(dispatch_sales.style.format({
    'Total Sales': '£{:,.2f}',
    'Orders': '{:,.0f}',
    'Avg Order Value': '£{:,.2f}'
}), use_container_width=True)

st.markdown("---")

# ============================================================================
# REQUIREMENT 3: SALES CHANNEL ANALYSIS
# ============================================================================

st.header("📱 Sales Channel Performance")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Sales Channel")
    
    # Group by sales channel
    channel_sales = filtered_sales.groupby('Sales channel type').agg({
        'Gross sales': 'sum',
        'Order ID': 'count'
    }).reset_index().sort_values('Gross sales', ascending=False)
    channel_sales.columns = ['Channel', 'Total Sales', 'Orders']
    
    # Horizontal bar chart
    fig_channel = px.bar(
        channel_sales,
        y='Channel',
        x='Total Sales',
        orientation='h',
        title="Sales by Channel",
        color='Total Sales',
        color_continuous_scale='Sunset'
    )
    st.plotly_chart(fig_channel, use_container_width=True)

with col2:
    st.subheader("Channel Market Share")
    
    # Donut chart
    fig_channel_pie = px.pie(
        channel_sales,
        values='Total Sales',
        names='Channel',
        hole=0.4,
        title="Market Share by Channel"
    )
    st.plotly_chart(fig_channel_pie, use_container_width=True)

# Channel comparison table
st.subheader("Channel Performance Metrics")
channel_sales['Avg Order'] = channel_sales['Total Sales'] / channel_sales['Orders']
channel_sales['Market Share %'] = (channel_sales['Total Sales'] / channel_sales['Total Sales'].sum() * 100).round(2)
st.dataframe(channel_sales.style.format({
    'Total Sales': '£{:,.2f}',
    'Orders': '{:,.0f}',
    'Avg Order': '£{:,.2f}',
    'Market Share %': '{:.2f}%'
}), use_container_width=True)

st.markdown("---")

# ============================================================================
# REQUIREMENT 4: DEMAND FORECASTING & PEAK HOURS
# ============================================================================

st.header("⏰ Demand Forecasting & Peak Hours Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Hourly Sales Pattern")
    
    # Group by hour
    hourly_sales = filtered_sales.copy()
    hourly_sales['Hour'] = hourly_sales['Order time'].dt.hour
    hourly_pattern = hourly_sales.groupby('Hour').agg({
        'Gross sales': 'sum',
        'Order ID': 'count'
    }).reset_index()
    hourly_pattern.columns = ['Hour', 'Total Sales', 'Orders']
    
    # Line chart for hourly pattern
    fig_hourly = go.Figure()
    fig_hourly.add_trace(go.Scatter(
        x=hourly_pattern['Hour'],
        y=hourly_pattern['Total Sales'],
        mode='lines+markers',
        name='Sales',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8)
    ))
    fig_hourly.update_layout(
        title="Sales by Hour of Day",
        xaxis_title="Hour (24h format)",
        yaxis_title="Total Sales (£)",
        height=400
    )
    st.plotly_chart(fig_hourly, use_container_width=True)

with col2:
    st.subheader("Order Volume by Hour")
    
    # Bar chart for order count
    fig_hourly_orders = px.bar(
        hourly_pattern,
        x='Hour',
        y='Orders',
        title="Number of Orders by Hour",
        color='Orders',
        color_continuous_scale='Reds'
    )
    fig_hourly_orders.update_layout(height=400)
    st.plotly_chart(fig_hourly_orders, use_container_width=True)

# Helper function to format hour as 12-hour AM/PM
def format_hour_12h(hour):
    hour = int(hour)
    if hour == 0:
        return "12:00 AM"
    elif hour < 12:
        return f"{hour}:00 AM"
    elif hour == 12:
        return "12:00 PM"
    else:
        return f"{hour - 12}:00 PM"

# Peak hours identification
st.subheader("🔥 Peak Hours Identification")

top_hours = hourly_pattern.nlargest(5, 'Total Sales')[['Hour', 'Total Sales', 'Orders']].copy()
top_hours['Avg Order Value'] = top_hours['Total Sales'] / top_hours['Orders']
top_hours['Time'] = top_hours['Hour'].apply(format_hour_12h)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🥇 Peak Hour", top_hours.iloc[0]['Time'], f"£{top_hours.iloc[0]['Total Sales']:,.0f}")

with col2:
    st.metric("🥈 2nd Peak", top_hours.iloc[1]['Time'], f"£{top_hours.iloc[1]['Total Sales']:,.0f}")

with col3:
    st.metric("🥉 3rd Peak", top_hours.iloc[2]['Time'], f"£{top_hours.iloc[2]['Total Sales']:,.0f}")

st.dataframe(top_hours[['Time', 'Total Sales', 'Orders', 'Avg Order Value']].style.format({
    'Total Sales': '£{:,.2f}',
    'Orders': '{:,.0f}',
    'Avg Order Value': '£{:,.2f}'
}), use_container_width=True)

# Slowest hours analysis
st.subheader("🌙 Slowest Hours (Cost Optimization Opportunities)")
st.caption("Identify quiet periods for reduced staffing or targeted promotions")

# Get slowest 5 hours (excluding hours with 0 orders)
slow_hours = hourly_pattern[hourly_pattern['Orders'] > 0].nsmallest(5, 'Total Sales')[['Hour', 'Total Sales', 'Orders']].copy()
slow_hours['Avg Order Value'] = slow_hours['Total Sales'] / slow_hours['Orders']
slow_hours['Time'] = slow_hours['Hour'].apply(format_hour_12h)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🌙 Slowest Hour", slow_hours.iloc[0]['Time'], f"£{slow_hours.iloc[0]['Total Sales']:,.0f}")

with col2:
    st.metric("💤 2nd Slowest", slow_hours.iloc[1]['Time'], f"£{slow_hours.iloc[1]['Total Sales']:,.0f}")

with col3:
    st.metric("😴 3rd Slowest", slow_hours.iloc[2]['Time'], f"£{slow_hours.iloc[2]['Total Sales']:,.0f}")

st.dataframe(slow_hours[['Time', 'Total Sales', 'Orders', 'Avg Order Value']].style.format({
    'Total Sales': '£{:,.2f}',
    'Orders': '{:,.0f}',
    'Avg Order Value': '£{:,.2f}'
}), use_container_width=True)

st.info("💡 **Pro Tip**: Consider running promotions during these hours or reducing staffing to optimize costs.")

st.markdown("---")

# Day of week analysis
st.subheader("📅 Weekly Pattern Analysis")

col1, col2 = st.columns(2)

with col1:
    # Group by day of week
    dow_sales = filtered_sales.copy()
    dow_sales['Day of Week'] = dow_sales['Order time'].dt.day_name()
    dow_pattern = dow_sales.groupby('Day of Week').agg({
        'Gross sales': 'sum',
        'Order ID': 'count'
    }).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    dow_pattern = dow_pattern.reset_index()
    dow_pattern.columns = ['Day', 'Total Sales', 'Orders']
    
    # Bar chart
    fig_dow = px.bar(
        dow_pattern,
        x='Day',
        y='Total Sales',
        title="Sales by Day of Week",
        color='Total Sales',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_dow, use_container_width=True)

with col2:
    # Highlight busiest days
    st.write("**Busiest Days:**")
    busiest_days = dow_pattern.nlargest(3, 'Total Sales')
    for idx, row in busiest_days.iterrows():
        st.success(f"**{row['Day']}**: £{row['Total Sales']:,.2f} ({row['Orders']} orders)")

st.markdown("---")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.caption("Dashboard built with ❤️ using Streamlit | Data from Flipdish POS")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
