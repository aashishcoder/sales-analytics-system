import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_sample_database():
    """Create sample database for demo purposes"""
    print("Creating sample database...")
    
    # Create database
    conn = sqlite3.connect('sales_analytics.db')
    
    # Generate sample orders
    orders = []
    for i in range(1000):
        order_date = (datetime.now() - timedelta(days=i%365)).strftime('%Y-%m-%d')
        sales = np.random.uniform(50, 1000)
        profit = sales * np.random.uniform(0.1, 0.3)
        
        orders.append({
            'Order ID': f'ORD{i+1:04d}',
            'Order Date': order_date,
            'Customer ID': f'CUST{(i%100)+1:03d}',
            'Product ID': f'PROD{(i%50)+1:03d}',
            'Sales': sales,
            'Profit': profit,
            'Quantity': np.random.randint(1, 10),
            'Discount': np.random.uniform(0, 0.2),
            'Region': np.random.choice(['North', 'South', 'East', 'West']),
            'Revenue': sales,
            'Profit Margin': (profit / sales) * 100
        })
    
    orders_df = pd.DataFrame(orders)
    
    # Generate sample customers
    customers = []
    for i in range(100):
        customers.append({
            'Customer ID': f'CUST{i+1:03d}',
            'Customer Name': f'Customer {i+1}',
            'Segment': np.random.choice(['Consumer', 'Corporate', 'Home Office'])
        })
    
    customers_df = pd.DataFrame(customers)
    
    # Generate sample products
    products = []
    categories = ['Technology', 'Furniture', 'Office Supplies']
    for i in range(50):
        products.append({
            'Product ID': f'PROD{i+1:03d}',
            'Product Name': f'Product {i+1}',
            'Category': np.random.choice(categories),
            'Sub-Category': f'Sub-{np.random.choice(categories)}'
        })
    
    products_df = pd.DataFrame(products)
    
    # Generate calendar
    dates = []
    for i in range(365):
        date = datetime.now() - timedelta(days=i)
        dates.append({
            'Date': date.strftime('%Y-%m-%d'),
            'Year': date.year,
            'Month': date.month,
            'Quarter': (date.month - 1) // 3 + 1,
            'MonthName': date.strftime('%B'),
            'DayOfWeek': date.weekday() + 1,
            'DayName': date.strftime('%A')
        })
    
    calendar_df = pd.DataFrame(dates)
    
    # Save to database
    orders_df.to_sql('orders', conn, if_exists='replace', index=False)
    customers_df.to_sql('customers', conn, if_exists='replace', index=False)
    products_df.to_sql('products', conn, if_exists='replace', index=False)
    calendar_df.to_sql('calendar', conn, if_exists='replace', index=False)
    
    conn.close()
    print("Sample database created successfully!")

if __name__ == "__main__":
    create_sample_database()
