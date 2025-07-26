# Data Directory

This directory contains the CSV files for the E-commerce Customer Support Chatbot.

## Required CSV Files

Place your CSV files in this directory with the following names:

1. `distribution_centers.csv` - Distribution center information
2. `inventory_items.csv` - Inventory item details
3. `order_items.csv` - Order item information
4. `orders.csv` - Order details
5. `products.csv` - Product catalog
6. `users.csv` - User information

## Data Schema

### distribution_centers.csv
- `id`: Unique identifier for each distribution center
- `name`: Name of the distribution center
- `latitude`: Latitude coordinate
- `longitude`: Longitude coordinate

### inventory_items.csv
- `id`: Unique identifier for each inventory item
- `product_id`: Associated product ID
- `created_at`: When the inventory item was created
- `sold_at`: When the item was sold (NULL if available)
- `cost`: Cost of the inventory item
- `product_category`: Product category
- `product_name`: Product name
- `product_brand`: Product brand
- `product_retail_price`: Retail price
- `product_department`: Department
- `product_sku`: SKU
- `product_distribution_center_id`: Distribution center ID

### order_items.csv
- `id`: Unique identifier for each order item
- `order_id`: Associated order ID
- `user_id`: User who placed the order
- `product_id`: Associated product ID
- `inventory_item_id`: Associated inventory item ID
- `status`: Status of the order item
- `created_at`: When the order item was created
- `shipped_at`: When the item was shipped
- `delivered_at`: When the item was delivered
- `returned_at`: When the item was returned

### orders.csv
- `order_id`: Unique identifier for each order
- `user_id`: User who placed the order
- `status`: Status of the order
- `gender`: Gender information
- `created_at`: When the order was created
- `returned_at`: When the order was returned
- `shipped_at`: When the order was shipped
- `delivered_at`: When the order was delivered
- `num_of_item`: Number of items in the order

### products.csv
- `id`: Unique identifier for each product
- `cost`: Cost of the product
- `category`: Product category
- `name`: Product name
- `brand`: Product brand
- `retail_price`: Retail price
- `department`: Department
- `sku`: SKU
- `distribution_center_id`: Associated distribution center ID

### users.csv
- `id`: Unique identifier for each user
- `first_name`: First name
- `last_name`: Last name
- `email`: Email address
- `age`: Age
- `gender`: Gender
- `state`: State
- `street_address`: Street address
- `postal_code`: Postal code
- `city`: City
- `country`: Country
- `latitude`: Latitude coordinate
- `longitude`: Longitude coordinate
- `traffic_source`: Traffic source
- `created_at`: When the user account was created

## Development

If you don't have the CSV files, the application will automatically create mock data for development purposes.

## Production

For production deployment, ensure all CSV files are present and contain real data. 