import pandas as pd
import numpy as np
import os
from datetime import datetime

def transform_data(df):
    """Transform raw data into structured tables following star schema"""
    print("🔧 PHASE 2: TRANSFORM - Starting data transformation...")
    
    try:
        # Orders table (Fact table)
        orders = df[['Order ID', 'Order Date', 'Customer ID', 'Product ID',
                     'Sales', 'Profit', 'Quantity', 'Discount', 'Region']].copy()
        
        # Add calculated columns
        orders['Revenue'] = orders['Sales'] - (orders['Sales'] * orders['Discount'])
        orders['Profit Margin'] = (orders['Profit'] / orders['Revenue']) * 100
        orders['Order Date'] = pd.to_datetime(orders['Order Date'], dayfirst=True).dt.strftime('%Y-%m-%d')
        
        # Handle missing values
        orders['Profit Margin'] = orders['Profit Margin'].fillna(0)
        
        print(f"📈 Transformed orders table: {len(orders)} rows")
        
        # Customers table (Dimension)
        customers = df[['Customer ID', 'Customer Name', 'Segment']].drop_duplicates().copy()
        customers['Customer ID'] = customers['Customer ID'].astype(str)
        customers['Customer Name'] = customers['Customer Name'].astype(str)
        customers['Segment'] = customers['Segment'].astype(str)
        
        print(f"👥 Transformed customers table: {len(customers)} rows")
        
        # Products table (Dimension)
        products = df[['Product ID', 'Category', 'Sub-Category', 'Product Name']].drop_duplicates().copy()
        products['Product ID'] = products['Product ID'].astype(str)
        products['Category'] = products['Category'].astype(str)
        products['Sub-Category'] = products['Sub-Category'].astype(str)
        products['Product Name'] = products['Product Name'].astype(str)
        
        print(f"📦 Transformed products table: {len(products)} rows")
        
        # Calendar table (Dimension)
        unique_dates = pd.to_datetime(df['Order Date'], dayfirst=True).unique()
        calendar = pd.DataFrame({'Date': unique_dates})
        calendar['Date'] = calendar['Date'].dt.strftime('%Y-%m-%d')
        calendar['Year'] = pd.to_datetime(calendar['Date']).dt.year
        calendar['Month'] = calendar['Date'].str[5:7].astype(int)
        calendar['Quarter'] = ((calendar['Month'] - 1) // 3) + 1
        calendar['MonthName'] = pd.to_datetime(calendar['Date']).dt.strftime('%B')
        calendar['DayOfWeek'] = pd.to_datetime(calendar['Date']).dt.dayofweek + 1
        calendar['DayName'] = pd.to_datetime(calendar['Date']).dt.strftime('%A')
        
        print(f"📅 Transformed calendar table: {len(calendar)} rows")
        
        # Save transformed data
        os.makedirs('data/processed', exist_ok=True)
        
        orders.to_csv('data/processed/orders.csv', index=False)
        customers.to_csv('data/processed/customers.csv', index=False)
        products.to_csv('data/processed/products.csv', index=False)
        calendar.to_csv('data/processed/calendar.csv', index=False)
        
        print("💾 All transformed tables saved to data/processed/")
        
        # Data quality report
        print("\n📊 Data Quality Report:")
        print(f"  • Orders: {len(orders)} records")
        print(f"  • Customers: {len(customers)} unique customers")
        print(f"  • Products: {len(products)} unique products")
        print(f"  • Date range: {calendar['Date'].min()} to {calendar['Date'].max()}")
        print(f"  • Total Sales: ${orders['Sales'].sum():,.0f}")
        print(f"  • Total Profit: ${orders['Profit'].sum():,.0f}")
        print(f"  • Avg Order Value: ${orders['Sales'].mean():.0f}")
        
        return orders, customers, products, calendar
        
    except Exception as e:
        print(f"❌ Transformation failed: {e}")
        raise

if __name__ == "__main__":
    # For testing
    from extract import extract_data
    df = extract_data()
    transform_data(df)
