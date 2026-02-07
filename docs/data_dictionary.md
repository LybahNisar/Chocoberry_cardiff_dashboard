# Data Dictionary - Restaurant Analytics Dashboard

## Overview
This document explains each CSV file exported from Flipdish and their columns.

---

## File: sales_data.csv (177 KB)
**Description:** Detailed transaction-level data - most comprehensive file

**Columns:**
- `Property name` - Branch/store identifier (e.g., "20 - Chocoberry")
- `Order ID` - Unique order identifier
- `Order time` - Timestamp of order
- `Source` - Where order originated (In store, deliveroo, Uber Eats, etc.)
- `Dispatch type` - Delivery method (Dine In, Delivery, Collection)
- `Channel` - Sales channel (POS, UrbanPiper, etc.)
- `Sales channel name` - Delivery partner name
- `Sales channel type` - Type of channel
- `Payment method` - How customer paid (Credit, Cash, Paid online, Unpaid)
- `Is preorder` - Whether order was pre-ordered (Yes/No)
- `Refund status` - Order refund status (No = not refunded)
- `Gross sales` - Total revenue before deductions
- `Tax on gross sales` - Tax amount
- `Tips` - Tip amount
- `Charges` - Additional charges
- `Refunds` - Refund amounts
- `Revenue` - Net revenue
- `Discounts` - Discount amounts
- `Packaging` - Packaging charges
- `Additional charges` - Other charges

**Use Cases:**
- Transaction-level analysis
- Order patterns by hour/day
- Customer payment preferences
- Channel performance detail

---

## File: sales_overview.csv
**Description:** High-level summary metrics

**Contains:**
- Aggregate totals
- Key performance indicators
- Period summaries

---

## File: gross_sales_per_day.csv
**Description:** Daily sales totals

**Use Cases:**
- Daily trend analysis
- Day-over-day comparison
- Identify sales spikes/drops

---

## File: gross_sales_per_day_of_week.csv
**Description:** Sales patterns by day of week (Mon-Sun)

**Use Cases:**
- Weekly seasonality analysis
- Identify busiest days
- Staff scheduling optimization

---

## File: gross_sales_by_hour_of_day.csv
**Description:** Hourly sales patterns (24-hour breakdown)

**Use Cases:**
- Identify peak hours (lunch: 12-2pm, dinner: 7-9pm)
- Demand forecasting
- Optimize staff shifts

---

## File: gross_sales_by_dispatch_type.csv
**Description:** Sales breakdown by order fulfillment type

**Values:**
- **Delivery** - Orders delivered to customer
- **Dine In** - In-restaurant dining
- **Collection** / **Take Away** - Customer pickup

**Use Cases:**
- Delivery vs dine-in revenue split
- Channel strategy optimization

---

## File: gross_sales_by_sales_channel.csv
**Description:** Sales breakdown by delivery partner/channel

**Channels:**
- **Deliveroo**
- **Just Eat**
- **Uber Eats**
- **POS** - Direct in-store orders
- **Urban Piper** - May include Talabat and other aggregators

**Use Cases:**
- Partner performance comparison
- Commission cost analysis
- Marketing spend allocation

---

## File: gross_sales_by_payment_method.csv
**Description:** Sales breakdown by payment type

**Payment Methods:**
- **Credit** - Credit/debit card
- **Cash**
- **Paid online** - Pre-paid online orders
- **Unpaid** - Orders not yet paid
- **Mix** - Multiple payment methods

**Use Cases:**
- Cash vs digital payment trends
- Payment processing optimization

---

## File: revenue_summary.csv
**Description:** Revenue breakdown and calculations

**Metrics:**
- Gross sales
- Tax on gross sales
- Tips
- Charges
- Revenue (after deductions)
- Refunds
- Revenue after refunds

---

## File: revenue_after_refunds.csv
**Description:** Net revenue after accounting for refunds

---

## File: charges_summary.csv
**Description:** Breakdown of additional charges

**Charge Types:**
- Delivery charges
- Service charges
- DRS charges (Deposit Return Scheme)
- Packaging charges
- Additional charges

---

## File: total_charges.csv
**Description:** Aggregated charge totals

---

## Data Quality Notes

### Missing Data
- Menu item-level detail (Flipdish export error)
- Item costs (need from client)
- Commission rates (need from client)

### Data Period
- Current data: Last 180 days (Aug 2025 - Feb 2026)
- Branch coverage: Chocoberry Cardiff only (as of Feb 4, 2026)

### Calculations Needed
- **Profit Margin** = (Revenue - Costs) / Revenue × 100
- **Net Channel Revenue** = Channel Revenue - Commission Fees
- **Average Order Value** = Total Revenue / Order Count
- **Orders per Hour** = Count of orders in each hour slot
