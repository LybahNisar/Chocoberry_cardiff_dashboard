"""
Flipdish API Integration Module
================================
Fetches live order data from Flipdish API using Bearer Token.

Endpoint: GET https://api.flipdish.co/api/v1.0/orders
Auth: Bearer token generated from Flipdish Developer Portal

Field Mapping (API -> CSV columns):
    OrderId          -> Order ID
    PlacedTime       -> Order time
    Amount           -> Revenue
    OrderItemsAmount -> Gross sales
    TotalTax         -> Tax on gross sales
    TipAmount        -> Tips
    DeliveryAmount   -> Delivery charges
    ServiceChargeAmount -> Service charges
    DeliveryType     -> Dispatch type
    PaymentAccountType -> Payment method
    AppType          -> Sales channel type
    OrderItems[].Name -> Item (NEW - enables item trends!)
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class FlipDishAPI:
    """
    Flipdish API client using Bearer Token authentication.
    
    Usage:
        api = FlipDishAPI(bearer_token, app_id)
        df = api.fetch_all_orders()
    """
    
    API_BASE = "https://api.flipdish.co"
    
    def __init__(self, bearer_token, app_id="br1153"):
        self.bearer_token = bearer_token
        self.app_id = app_id
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {bearer_token}",
            "Accept": "application/json",
        })
    
    def _get(self, endpoint, params=None):
        """Make authenticated GET request."""
        url = f"{self.API_BASE}{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                logger.error("Bearer token expired or invalid")
                return None
            else:
                logger.warning(f"API returned {response.status_code}: {response.text[:200]}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
    
    def get_stores(self):
        """Get list of stores."""
        data = self._get(f"/api/v1.0/{self.app_id}/stores")
        if data and isinstance(data, dict):
            return data.get("Data", [])
        return []
    
    def fetch_orders_page(self, page=1, limit=50):
        """
        Fetch a single page of orders.
        
        Returns:
            tuple: (orders_list, total_count)
        """
        data = self._get("/api/v1.0/orders", params={"page": page, "limit": limit})
        
        if data and isinstance(data, dict):
            orders = data.get("Data", [])
            total = data.get("TotalRecordCount", 0)
            return orders, total
        
        return [], 0
    
    def fetch_all_orders(self, max_orders=None, progress_callback=None):
        """
        Fetch ALL orders across all pages.
        
        Args:
            max_orders: Maximum number of orders to fetch (None = all)
            progress_callback: callable(current_count, total_count)
            
        Returns:
            pd.DataFrame: Orders in CSV-compatible format
        """
        all_orders = []
        page = 1
        total_count = None
        
        while True:
            orders, total = self.fetch_orders_page(page=page, limit=50)
            
            if total_count is None:
                total_count = total
                logger.info(f"Total orders available: {total_count}")
            
            if not orders:
                break
            
            all_orders.extend(orders)
            
            if progress_callback:
                progress_callback(len(all_orders), total_count)
            
            # Check if we have all orders
            if max_orders and len(all_orders) >= max_orders:
                all_orders = all_orders[:max_orders]
                break
            
            if len(all_orders) >= total_count:
                break
            
            if len(orders) < 50:
                break
            
            page += 1
        
        if not all_orders:
            return pd.DataFrame()
        
        # Transform to CSV format
        return self._transform_orders(all_orders)
    
    def _transform_orders(self, orders_list):
        """
        Transform API orders to match CSV column structure.
        
        API fields (confirmed from test):
            OrderId, PlacedTime, Amount, OrderItemsAmount, TotalTax,
            TipAmount, DeliveryAmount, ServiceChargeAmount, ProcessingFee,
            DeliveryType, PaymentAccountType, AppType, OrderItems[], etc.
        
        CSV columns (your dashboard expects):
            Order ID, Order time, Revenue, Gross sales, Tax on gross sales,
            Tips, Delivery charges, Service charges, Charges, Dispatch type,
            Payment method, Sales channel type, etc.
        """
        rows = []
        
        for order in orders_list:
            # Base order data
            row = {
                "Order ID": order.get("OrderId"),
                "Order time": order.get("PlacedTime"),
                "Property name": "Chocoberry Cardiff",
                
                # Financial - map API fields to CSV columns
                "Gross sales": float(order.get("OrderItemsAmount", 0) or 0),
                "Tax on gross sales": float(order.get("TotalTax", 0) or 0),
                "Tips": float(order.get("TipAmount", 0) or 0),
                "Delivery charges": float(order.get("DeliveryAmount", 0) or 0),
                "Service charges": float(order.get("ServiceChargeAmount", 0) or 0),
                "DRS charges": 0.0,
                "Packaging charges": 0.0,
                "Additional charges": float(order.get("ProcessingFee", 0) or 0),
                "Revenue": float(order.get("Amount", 0) or 0),
                "Refunds": float(order.get("RefundedAmount", 0) or 0),
                "Discounts": 0.0,
                
                # Order details
                "Dispatch type": order.get("DeliveryType", "Unknown"),
                "Payment method": order.get("PaymentAccountType", "Unknown"),
                "Sales channel type": order.get("AppType", "Unknown"),
                "Sales channel name": "Chocoberry Cardiff",
                "Source": order.get("AppType", "Unknown"),
                "Channel": order.get("AppType", "Unknown"),
                "Refund status": "",
                "Is preorder": "Yes" if order.get("IsPreOrder") else "No",
            }
            
            # Calculate derived fields
            row["Charges"] = (
                row["Delivery charges"] + row["Service charges"] + 
                row["Additional charges"]
            )
            row["Revenue after refunds"] = row["Revenue"] - row["Refunds"]
            
            # Extract store name if available
            store = order.get("Store")
            if isinstance(store, dict):
                row["Property name"] = store.get("Name", "Chocoberry Cardiff")
                row["Sales channel name"] = store.get("Name", "Chocoberry Cardiff")
            
            # Extract channel info
            channel = order.get("Channel")
            if isinstance(channel, dict):
                channel_name = channel.get("Source") or channel.get("Name")
                if channel_name:
                    row["Sales channel name"] = channel_name
            
            # Map DeliveryType values to match CSV format
            dispatch_mapping = {
                "Pickup": "Collection",
                "Delivery": "Delivery",
                "DineIn": "Dine In",
                "TableService": "Dine In",
            }
            row["Dispatch type"] = dispatch_mapping.get(
                row["Dispatch type"], row["Dispatch type"]
            )
            
            # Extract voucher discount
            voucher = order.get("Voucher")
            if isinstance(voucher, dict):
                discount = voucher.get("Amount", 0) or 0
                row["Discounts"] = float(discount)
            
            rows.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(rows)
        
        # Parse dates
        df["Order time"] = pd.to_datetime(df["Order time"], errors="coerce")
        
        # Ensure numeric columns
        numeric_cols = [
            "Gross sales", "Tax on gross sales", "Tips", "Delivery charges",
            "Service charges", "DRS charges", "Packaging charges",
            "Additional charges", "Charges", "Revenue", "Refunds",
            "Revenue after refunds", "Discounts"
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        
        # Sort by date (newest first, matching CSV)
        df = df.sort_values("Order time", ascending=False).reset_index(drop=True)
        
        return df
    
    def extract_order_items(self, orders_list):
        """
        Extract item-level data from orders.
        This enables the Item Trends feature!
        
        Returns:
            pd.DataFrame: Item-level data with columns:
                Order ID, Order time, Item, Category, Price, Quantity
        """
        items = []
        
        for order in orders_list:
            order_id = order.get("OrderId")
            order_time = order.get("PlacedTime")
            
            order_items = order.get("OrderItems", [])
            if not order_items:
                continue
            
            for item in order_items:
                items.append({
                    "Order ID": order_id,
                    "Order time": order_time,
                    "Item": item.get("Name", "Unknown"),
                    "Category": item.get("MenuSectionName", "Unknown"),
                    "Price": float(item.get("Price", 0) or 0),
                    "Quantity": 1,
                    "Revenue": float(item.get("PriceIncludingOptionSetItems", 0) or item.get("Price", 0) or 0),
                })
        
        if not items:
            return pd.DataFrame()
        
        df = pd.DataFrame(items)
        df["Order time"] = pd.to_datetime(df["Order time"], errors="coerce")
        
        return df
    
    def sync_to_db(self, db_path='restaurant_data.db'):
        """
        Sync live API orders to local SQLite database.
        
        This implements the "Store & Forward" architecture:
        1. Fetch all recent orders from API across all pages
        2. Insert new orders into DB (ignore existing)
        3. Insert line items into DB
        
        Returns:
            int: Number of new orders added
        """
        import sqlite3
        
        new_orders_count = 0
        page = 1
        
        # Start DB connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            while True:
                # Fetch recent orders (paged)
                orders, total = self.fetch_orders_page(page=page, limit=50)
                if not orders:
                    break
                
                for order in orders:
                    order_id = str(order.get('OrderId'))
                    
                    # Check if exists
                    cursor.execute("SELECT 1 FROM orders WHERE order_id = ?", (order_id,))
                    if cursor.fetchone():
                        continue
                    
                    # Map dispatch type to match CSV naming
                    dispatch_mapping = {
                        "Pickup": "Collection",
                        "DineIn": "Dine In",
                        "TableService": "Dine In",
                    }
                    raw_dispatch = order.get('DeliveryType', 'Unknown')
                    mapped_dispatch = dispatch_mapping.get(raw_dispatch, raw_dispatch)
                    
                    # Map payment type
                    raw_payment = order.get('PaymentAccountType', 'Unknown')
                    
                    cursor.execute('''
                    INSERT INTO orders (
                        order_id, order_time, property_name, gross_sales, tax, tips,
                        delivery_charges, service_charges, additional_charges, charges,
                        revenue, refunds, discounts, dispatch_type, payment_method,
                        sales_channel_type, sales_channel_name, is_preorder, status, raw_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        order_id,
                        order.get('PlacedTime'),
                        order.get('Store', {}).get('Name', 'Chocoberry Cardiff'),
                        order.get('OrderItemsAmount', 0) or 0,
                        order.get('TotalTax', 0) or 0,
                        order.get('TipAmount', 0) or 0,
                        order.get('DeliveryAmount', 0) or 0,
                        order.get('ServiceChargeAmount', 0) or 0,
                        order.get('ProcessingFee', 0) or 0,
                        0, # charges
                        order.get('Amount', 0) or 0,
                        order.get('RefundedAmount', 0) or 0,
                        order.get('Voucher', {}).get('Amount', 0) or 0,
                        mapped_dispatch,
                        raw_payment,
                        order.get('AppType', 'Unknown'),
                        order.get('Channel', {}).get('Source', 'Unknown'),
                        'Yes' if order.get('IsPreOrder') else 'No',
                        order.get('OrderState', 'Unknown'),
                        str(order)
                    ))
                    
                    # Insert Order Items
                    items = order.get('OrderItems', [])
                    for item in items:
                        cursor.execute('''
                        INSERT INTO order_items (
                            order_id, order_time, item_name, category, price, quantity, revenue
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            order_id,
                            order.get('PlacedTime'),
                            item.get('Name', 'Unknown'),
                            item.get('MenuSectionName', 'Unknown'),
                            item.get('Price', 0) or 0,
                            1, # Quantity usually 1 in this list structure
                            item.get('PriceIncludingOptionSetItems', 0) or item.get('Price', 0)
                        ))
                    
                    new_orders_count += 1
                
                # Check if we have fetched all orders from the API
                if len(orders) < 50:
                    # We reached the end of the API window
                    break
                    
                page += 1
                
            conn.commit()
            
        except Exception as e:
            logger.error(f"DB Sync Failed: {e}")
            conn.rollback()
        finally:
            conn.close()
            
        if new_orders_count > 0:
            logger.info(f"Synced {new_orders_count} new orders to DB.")
            
        return new_orders_count

    def test_connection(self):
        """
        Quick connection test.
        Returns: dict with status info
        """
        result = {"connected": False, "stores": [], "total_orders": 0, "error": None}
        try:
            stores = self.get_stores()
            if stores:
                result["connected"] = True
                result["stores"] = [{"name": s.get("Name"), "id": s.get("StoreId")} for s in stores if isinstance(s, dict)]
            _, total = self.fetch_orders_page(page=1, limit=1)
            result["total_orders"] = total
        except Exception as e:
            result["error"] = str(e)
        return result
