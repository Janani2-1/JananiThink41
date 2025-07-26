import os
import pandas as pd
from sqlalchemy.orm import Session
from app.core.db import SessionLocal, engine
from app.models.user import User
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.models.inventory_item import InventoryItem
from app.models.distribution_center import DistributionCenter
from app.models.base import Base
from datetime import datetime

def parse_datetime(val):
    if pd.isna(val):
        return None
    try:
        return pd.to_datetime(val)
    except Exception:
        return None

def load_users(session, df):
    for _, row in df.iterrows():
        user = User(
            id=row['id'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            email=row['email'],
            age=row.get('age'),
            gender=row.get('gender'),
            state=row.get('state'),
            street_address=row.get('street_address'),
            postal_code=row.get('postal_code'),
            city=row.get('city'),
            country=row.get('country'),
            latitude=row.get('latitude'),
            longitude=row.get('longitude'),
            traffic_source=row.get('traffic_source'),
            created_at=parse_datetime(row.get('created_at')),
        )
        session.merge(user)
    session.commit()

def load_distribution_centers(session, df):
    for _, row in df.iterrows():
        dc = DistributionCenter(
            id=row['id'],
            name=row['name'],
            latitude=row.get('latitude'),
            longitude=row.get('longitude'),
        )
        session.merge(dc)
    session.commit()

def load_products(session, df):
    for _, row in df.iterrows():
        product = Product(
            id=row['id'],
            cost=row.get('cost'),
            category=row.get('category'),
            name=row.get('name'),
            brand=row.get('brand'),
            retail_price=row.get('retail_price'),
            department=row.get('department'),
            sku=row.get('sku'),
            distribution_center_id=row.get('distribution_center_id'),
        )
        session.merge(product)
    session.commit()

def load_inventory_items(session, df):
    for _, row in df.iterrows():
        item = InventoryItem(
            id=row['id'],
            product_id=row.get('product_id'),
            created_at=parse_datetime(row.get('created_at')),
            sold_at=parse_datetime(row.get('sold_at')),
            cost=row.get('cost'),
            product_category=row.get('product_category'),
            product_name=row.get('product_name'),
            product_brand=row.get('product_brand'),
            product_retail_price=row.get('product_retail_price'),
            product_department=row.get('product_department'),
            product_sku=row.get('product_sku'),
            product_distribution_center_id=row.get('product_distribution_center_id'),
        )
        session.merge(item)
    session.commit()

def load_orders(session, df):
    for _, row in df.iterrows():
        order = Order(
            order_id=row['order_id'],
            user_id=row.get('user_id'),
            status=row.get('status'),
            gender=row.get('gender'),
            created_at=parse_datetime(row.get('created_at')),
            returned_at=parse_datetime(row.get('returned_at')),
            shipped_at=parse_datetime(row.get('shipped_at')),
            delivered_at=parse_datetime(row.get('delivered_at')),
            num_of_item=row.get('num_of_item'),
        )
        session.merge(order)
    session.commit()

def load_order_items(session, df):
    for _, row in df.iterrows():
        item = OrderItem(
            id=row['id'],
            order_id=row.get('order_id'),
            user_id=row.get('user_id'),
            product_id=row.get('product_id'),
            inventory_item_id=row.get('inventory_item_id'),
            status=row.get('status'),
            created_at=parse_datetime(row.get('created_at')),
            shipped_at=parse_datetime(row.get('shipped_at')),
            delivered_at=parse_datetime(row.get('delivered_at')),
            returned_at=parse_datetime(row.get('returned_at')),
        )
        session.merge(item)
    session.commit()

def main():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    data_dir = os.path.join(os.path.dirname(__file__), '../../data')
    
    # Load users
    users_csv = os.path.join(data_dir, 'users.csv')
    if os.path.exists(users_csv):
        users_df = pd.read_csv(users_csv)
        load_users(session, users_df)
    
    # Load distribution centers
    dc_csv = os.path.join(data_dir, 'distribution_centers.csv')
    if os.path.exists(dc_csv):
        dc_df = pd.read_csv(dc_csv)
        load_distribution_centers(session, dc_df)
    
    # Load products
    products_csv = os.path.join(data_dir, 'products.csv')
    if os.path.exists(products_csv):
        products_df = pd.read_csv(products_csv)
        load_products(session, products_df)
    
    # Load inventory items
    inventory_csv = os.path.join(data_dir, 'inventory_items.csv')
    if os.path.exists(inventory_csv):
        inventory_df = pd.read_csv(inventory_csv)
        load_inventory_items(session, inventory_df)
    
    # Load orders
    orders_csv = os.path.join(data_dir, 'orders.csv')
    if os.path.exists(orders_csv):
        orders_df = pd.read_csv(orders_csv)
        load_orders(session, orders_df)
    
    # Load order items
    order_items_csv = os.path.join(data_dir, 'order_items.csv')
    if os.path.exists(order_items_csv):
        order_items_df = pd.read_csv(order_items_csv)
        load_order_items(session, order_items_df)
    
    session.close()
    print('Data loaded successfully!')

if __name__ == '__main__':
    main() 