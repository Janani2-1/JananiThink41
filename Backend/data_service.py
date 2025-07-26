import pandas as pd
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DataService:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.dfs = {}
        self.load_data()
    
    def load_data(self):
        """Load all CSV files into memory"""
        try:
            csv_files = [
                'distribution_centers.csv',
                'inventory_items.csv', 
                'order_items.csv',
                'orders.csv',
                'products.csv',
                'users.csv'
            ]
            
            for file in csv_files:
                file_path = os.path.join(self.data_dir, file)
                if os.path.exists(file_path):
                    df_name = file.replace('.csv', '')
                    self.dfs[df_name] = pd.read_csv(file_path)
                    logger.info(f"Loaded {file} with {len(self.dfs[df_name])} rows")
                else:
                    logger.warning(f"File not found: {file_path}")
                    
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            # Create mock data if files don't exist
            self.create_mock_data()
    
    def create_mock_data(self):
        """Create mock data for development/testing"""
        logger.info("Creating mock data for development")
        
        # Mock distribution centers
        self.dfs['distribution_centers'] = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['New York DC', 'California DC', 'Texas DC'],
            'latitude': [40.7128, 34.0522, 31.9686],
            'longitude': [-74.0060, -118.2437, -99.9018]
        })
        
        # Mock products
        self.dfs['products'] = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'cost': [15.00, 45.00, 35.00, 80.00, 25.00],
            'category': ['shirts', 'pants', 'dresses', 'shoes', 'accessories'],
            'name': ['Classic White T-Shirt', 'Slim Fit Jeans', 'Summer Dress', 'Running Shoes', 'Leather Wallet'],
            'brand': ['FashionBrand', 'FashionBrand', 'FashionBrand', 'FashionBrand', 'FashionBrand'],
            'retail_price': [29.99, 79.99, 59.99, 129.99, 39.99],
            'department': ['men', 'men', 'women', 'unisex', 'unisex'],
            'sku': ['TSH001', 'JEA001', 'DRE001', 'SHO001', 'WAL001'],
            'distribution_center_id': [1, 1, 2, 2, 3]
        })
        
        # Mock inventory items
        inventory_data = []
        for product_id in range(1, 6):
            for size in ['S', 'M', 'L', 'XL']:
                for _ in range(50):  # 50 items per size
                    inventory_data.append({
                        'id': len(inventory_data) + 1,
                        'product_id': product_id,
                        'created_at': '2024-01-01 00:00:00',
                        'sold_at': None if len(inventory_data) % 3 != 0 else '2024-03-01 00:00:00',
                        'cost': self.dfs['products'].iloc[product_id-1]['cost'],
                        'product_category': self.dfs['products'].iloc[product_id-1]['category'],
                        'product_name': self.dfs['products'].iloc[product_id-1]['name'],
                        'product_brand': self.dfs['products'].iloc[product_id-1]['brand'],
                        'product_retail_price': self.dfs['products'].iloc[product_id-1]['retail_price'],
                        'product_department': self.dfs['products'].iloc[product_id-1]['department'],
                        'product_sku': self.dfs['products'].iloc[product_id-1]['sku'],
                        'product_distribution_center_id': self.dfs['products'].iloc[product_id-1]['distribution_center_id']
                    })
        
        self.dfs['inventory_items'] = pd.DataFrame(inventory_data)
        
        # Mock orders
        self.dfs['orders'] = pd.DataFrame({
            'order_id': [12345, 12346, 12347],
            'user_id': [1, 2, 3],
            'status': ['shipped', 'processing', 'delivered'],
            'gender': ['M', 'F', 'M'],
            'created_at': ['2024-03-15 10:00:00', '2024-03-16 14:30:00', '2024-03-10 09:15:00'],
            'returned_at': [None, None, None],
            'shipped_at': ['2024-03-16 08:00:00', None, '2024-03-12 10:00:00'],
            'delivered_at': [None, None, '2024-03-14 15:30:00'],
            'num_of_item': [2, 1, 3]
        })
        
        # Mock order items
        self.dfs['order_items'] = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'order_id': [12345, 12345, 12346, 12347, 12347],
            'user_id': [1, 1, 2, 3, 3],
            'product_id': [1, 2, 3, 1, 4],
            'inventory_item_id': [1, 51, 101, 151, 201],
            'status': ['shipped', 'shipped', 'processing', 'delivered', 'delivered'],
            'created_at': ['2024-03-15 10:00:00', '2024-03-15 10:00:00', '2024-03-16 14:30:00', '2024-03-10 09:15:00', '2024-03-10 09:15:00'],
            'shipped_at': ['2024-03-16 08:00:00', '2024-03-16 08:00:00', None, '2024-03-12 10:00:00', '2024-03-12 10:00:00'],
            'delivered_at': [None, None, None, '2024-03-14 15:30:00', '2024-03-14 15:30:00'],
            'returned_at': [None, None, None, None, None]
        })
        
        # Mock users
        self.dfs['users'] = pd.DataFrame({
            'id': [1, 2, 3],
            'first_name': ['John', 'Sarah', 'Mike'],
            'last_name': ['Doe', 'Smith', 'Johnson'],
            'email': ['john.doe@email.com', 'sarah.smith@email.com', 'mike.johnson@email.com'],
            'age': [28, 32, 25],
            'gender': ['M', 'F', 'M'],
            'state': ['NY', 'CA', 'TX'],
            'street_address': ['123 Main St', '456 Oak Ave', '789 Pine Rd'],
            'postal_code': ['10001', '90210', '75001'],
            'city': ['New York', 'Los Angeles', 'Dallas'],
            'country': ['US', 'US', 'US'],
            'latitude': [40.7128, 34.0522, 32.7767],
            'longitude': [-74.0060, -118.2437, -96.7970],
            'traffic_source': ['google', 'facebook', 'instagram'],
            'created_at': ['2023-01-15 00:00:00', '2023-02-20 00:00:00', '2023-03-10 00:00:00']
        })
    
    def get_top_products(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top selling products"""
        try:
            if 'order_items' not in self.dfs or 'products' not in self.dfs:
                return []
            
            # Join order_items with products
            merged = self.dfs['order_items'].merge(
                self.dfs['products'], 
                left_on='product_id', 
                right_on='id', 
                how='inner'
            )
            
            # Filter out returned items
            sold_items = merged[merged['returned_at'].isna()]
            
            # Group by product and count sales
            top_products = sold_items.groupby(['product_id', 'name', 'brand', 'retail_price']).agg({
                'id_x': 'count',  # Count of order items
                'retail_price': 'sum'  # Total revenue
            }).reset_index()
            
            top_products.columns = ['product_id', 'name', 'brand', 'unit_price', 'units_sold', 'total_revenue']
            top_products = top_products.sort_values('units_sold', ascending=False).head(limit)
            
            return top_products.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error getting top products: {e}")
            return []
    
    def get_order_status(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Get order status and details"""
        try:
            if 'orders' not in self.dfs or 'order_items' not in self.dfs or 'products' not in self.dfs:
                return None
            
            # Get order details
            order = self.dfs['orders'][self.dfs['orders']['order_id'] == int(order_id)]
            if order.empty:
                return None
            
            order = order.iloc[0]
            
            # Get order items
            order_items = self.dfs['order_items'][self.dfs['order_items']['order_id'] == int(order_id)]
            
            # Join with products
            items_with_products = order_items.merge(
                self.dfs['products'], 
                left_on='product_id', 
                right_on='id', 
                how='inner'
            )
            
            # Get user details
            user = self.dfs['users'][self.dfs['users']['id'] == order['user_id']]
            user_name = f"{user.iloc[0]['first_name']} {user.iloc[0]['last_name']}" if not user.empty else "Unknown"
            
            return {
                'order_id': order_id,
                'status': order['status'],
                'user_name': user_name,
                'created_at': order['created_at'],
                'shipped_at': order['shipped_at'],
                'delivered_at': order['delivered_at'],
                'returned_at': order['returned_at'],
                'num_of_items': order['num_of_item'],
                'items': items_with_products[['name', 'retail_price', 'status']].to_dict('records'),
                'total_amount': items_with_products['retail_price'].sum()
            }
            
        except Exception as e:
            logger.error(f"Error getting order status: {e}")
            return None
    
    def get_inventory_status(self, product_name: str = None, category: str = None) -> List[Dict[str, Any]]:
        """Get inventory status for products"""
        try:
            if 'inventory_items' not in self.dfs:
                return []
            
            # Filter inventory items
            inventory = self.dfs['inventory_items'].copy()
            
            # Filter by product name if provided
            if product_name:
                inventory = inventory[
                    inventory['product_name'].str.contains(product_name, case=False, na=False)
                ]
            
            # Filter by category if provided
            if category:
                inventory = inventory[
                    inventory['product_category'].str.contains(category, case=False, na=False)
                ]
            
            # Get available stock (items not sold)
            available_stock = inventory[inventory['sold_at'].isna()]
            
            # Group by product and distribution center
            stock_summary = available_stock.groupby([
                'product_name', 
                'product_category', 
                'product_brand', 
                'product_retail_price',
                'product_distribution_center_id'
            ]).size().reset_index(name='available_quantity')
            
            # Add distribution center name
            if 'distribution_centers' in self.dfs:
                stock_summary = stock_summary.merge(
                    self.dfs['distribution_centers'],
                    left_on='product_distribution_center_id',
                    right_on='id',
                    how='left'
                )
            
            return stock_summary.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error getting inventory status: {e}")
            return []
    
    def get_user_orders(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all orders for a user"""
        try:
            if 'orders' not in self.dfs:
                return []
            
            user_orders = self.dfs['orders'][self.dfs['orders']['user_id'] == user_id]
            return user_orders.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error getting user orders: {e}")
            return []
    
    def search_products(self, query: str) -> List[Dict[str, Any]]:
        """Search products by name, category, or brand"""
        try:
            if 'products' not in self.dfs:
                return []
            
            products = self.dfs['products']
            
            # Search in name, category, and brand
            mask = (
                products['name'].str.contains(query, case=False, na=False) |
                products['category'].str.contains(query, case=False, na=False) |
                products['brand'].str.contains(query, case=False, na=False)
            )
            
            matching_products = products[mask]
            return matching_products.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error searching products: {e}")
            return [] 