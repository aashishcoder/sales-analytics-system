from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import sqlite3
import pandas as pd
import os
from datetime import datetime, timedelta
import numpy as np

app = FastAPI(
    title="Tableau Sales Analytics API",
    description="Optimized API for Tableau Web Data Connector",
    version="2.0.0"
)

# Add CORS middleware for Tableau WDC
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
def create_tableau_database():
    """Create comprehensive database for Tableau analytics"""
    conn = sqlite3.connect('tableau_sales.db')
    
    # Create orders table with Tableau-optimized schema
    conn.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            "Order ID" TEXT PRIMARY KEY,
            "Order Date" DATE,
            "Ship Date" DATE,
            "Customer ID" TEXT,
            "Customer Name" TEXT,
            "Segment" TEXT,
            "Product ID" TEXT,
            "Product Name" TEXT,
            "Category" TEXT,
            "Sub-Category" TEXT,
            "Region" TEXT,
            "State" TEXT,
            "Country" TEXT,
            "Postal Code" TEXT,
            "Sales" REAL,
            "Quantity" INTEGER,
            "Discount" REAL,
            "Profit" REAL,
            "Shipping Cost" REAL
        )
    ''')
    
    # Create customers dimension table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            "Customer ID" TEXT PRIMARY KEY,
            "Customer Name" TEXT,
            "Segment" TEXT,
            "City" TEXT,
            "State" TEXT,
            "Country" TEXT,
            "Postal Code" TEXT,
            "Region" TEXT
        )
    ''')
    
    # Create products dimension table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            "Product ID" TEXT PRIMARY KEY,
            "Product Name" TEXT,
            "Category" TEXT,
            "Sub-Category" TEXT
        )
    ''')
    
    # Generate comprehensive sample data
    if not conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]:
        print("Generating Tableau-optimized sample data...")
        
        # Generate realistic sample data
        regions = ['North', 'South', 'East', 'West', 'Central']
        segments = ['Consumer', 'Corporate', 'Home Office']
        categories = ['Technology', 'Furniture', 'Office Supplies']
        sub_categories = {
            'Technology': ['Phones', 'Computers', 'Accessories', 'Monitors'],
            'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Furnishings'],
            'Office Supplies': ['Paper', 'Binders', 'Art', 'Labels']
        }
        
        orders_data = []
        customers_data = []
        products_data = []
        
        # Generate 2000 orders for better Tableau analysis
        for i in range(2000):
            order_date = datetime.now() - timedelta(days=np.random.randint(0, 730))
            ship_date = order_date + timedelta(days=np.random.randint(1, 7))
            
            customer_id = f'CUST{np.random.randint(1, 501):04d}'
            product_id = f'PROD{np.random.randint(1, 201):04d}'
            
            # Realistic pricing by category
            category = np.random.choice(categories)
            if category == 'Technology':
                base_price = np.random.uniform(100, 2000)
            elif category == 'Furniture':
                base_price = np.random.uniform(50, 800)
            else:
                base_price = np.random.uniform(5, 100)
            
            quantity = np.random.randint(1, 10)
            discount = np.random.uniform(0, 0.3)
            sales = base_price * quantity * (1 - discount)
            profit = sales * np.random.uniform(0.1, 0.4)
            shipping_cost = np.random.uniform(5, 50)
            
            orders_data.append({
                'Order ID': f'ORD{i+1:05d}',
                'Order Date': order_date.strftime('%Y-%m-%d'),
                'Ship Date': ship_date.strftime('%Y-%m-%d'),
                'Customer ID': customer_id,
                'Customer Name': f'Customer {customer_id[-3:]}',
                'Segment': np.random.choice(segments),
                'Product ID': product_id,
                'Product Name': f'Product {product_id[-3:]}',
                'Category': category,
                'Sub-Category': np.random.choice(sub_categories[category]),
                'Region': np.random.choice(regions),
                'State': f'State {np.random.randint(1, 51):02d}',
                'Country': 'United States',
                'Postal Code': f'{np.random.randint(10000, 99999)}',
                'Sales': round(sales, 2),
                'Quantity': quantity,
                'Discount': round(discount, 3),
                'Profit': round(profit, 2),
                'Shipping Cost': round(shipping_cost, 2)
            })
        
        # Generate unique customers
        for i in range(1, 501):
            customers_data.append({
                'Customer ID': f'CUST{i:04d}',
                'Customer Name': f'Customer {i}',
                'Segment': np.random.choice(segments),
                'City': f'City {i}',
                'State': f'State {np.random.randint(1, 51):02d}',
                'Country': 'United States',
                'Postal Code': f'{np.random.randint(10000, 99999)}',
                'Region': np.random.choice(regions)
            })
        
        # Generate unique products
        for i in range(1, 201):
            category = np.random.choice(categories)
            products_data.append({
                'Product ID': f'PROD{i:04d}',
                'Product Name': f'Product {i}',
                'Category': category,
                'Sub-Category': np.random.choice(sub_categories[category])
            })
        
        # Insert data
        conn.executemany('''
            INSERT OR REPLACE INTO orders VALUES 
            (:Order ID, :Order Date, :Ship Date, :Customer ID, :Customer Name, :Segment, 
             :Product ID, :Product Name, :Category, :Sub-Category, :Region, :State, :Country, 
             :Postal Code, :Sales, :Quantity, :Discount, :Profit, :Shipping Cost)
        ''', orders_data)
        
        conn.executemany('''
            INSERT OR REPLACE INTO customers VALUES 
            (:Customer ID, :Customer Name, :Segment, :City, :State, :Country, :Postal Code, :Region)
        ''', customers_data)
        
        conn.executemany('''
            INSERT OR REPLACE INTO products VALUES 
            (:Product ID, :Product Name, :Category, :Sub-Category)
        ''', products_data)
        
        conn.commit()
        print(f"Generated {len(orders_data)} orders, {len(customers_data)} customers, {len(products_data)} products")
    
    conn.close()

# Initialize database on startup
create_tableau_database()

@app.get("/")
async def root():
    return {
        "message": "Tableau Sales Analytics API",
        "version": "2.0.0",
        "status": "running",
        "tableau_optimized": True,
        "endpoints": {
            "/tableau/orders": "Orders data for Tableau",
            "/tableau/customers": "Customers data for Tableau", 
            "/tableau/products": "Products data for Tableau",
            "/tableau/kpi": "KPI summary for Tableau",
            "/wdc": "Web Data Connector"
        }
    }

@app.get("/health")
async def health():
    try:
        conn = sqlite3.connect('tableau_sales.db')
        orders_count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        customers_count = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        products_count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        conn.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "tables": {
                "orders": orders_count,
                "customers": customers_count,
                "products": products_count
            }
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/tableau/orders")
async def get_tableau_orders():
    """Optimized orders data for Tableau"""
    try:
        conn = sqlite3.connect('tableau_sales.db')
        df = pd.read_sql('''
            SELECT * FROM orders 
            ORDER BY "Order Date" DESC
        ''', conn)
        conn.close()
        
        csv_data = df.to_csv(index=False)
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=tableau_orders.csv"}
        )
    except Exception as e:
        return {"error": str(e)}

@app.get("/tableau/customers")
async def get_tableau_customers():
    """Customers data for Tableau"""
    try:
        conn = sqlite3.connect('tableau_sales.db')
        df = pd.read_sql('SELECT * FROM customers', conn)
        conn.close()
        
        csv_data = df.to_csv(index=False)
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=tableau_customers.csv"}
        )
    except Exception as e:
        return {"error": str(e)}

@app.get("/tableau/products")
async def get_tableau_products():
    """Products data for Tableau"""
    try:
        conn = sqlite3.connect('tableau_sales.db')
        df = pd.read_sql('SELECT * FROM products', conn)
        conn.close()
        
        csv_data = df.to_csv(index=False)
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=tableau_products.csv"}
        )
    except Exception as e:
        return {"error": str(e)}

@app.get("/tableau/kpi")
async def get_tableau_kpi():
    """Comprehensive KPIs for Tableau dashboards"""
    try:
        conn = sqlite3.connect('tableau_sales.db')
        
        # Overall KPIs
        overall = conn.execute('''
            SELECT 
                COUNT(*) as total_orders,
                SUM(Sales) as total_sales,
                SUM(Profit) as total_profit,
                AVG(Sales) as avg_order_value,
                AVG(Profit) as avg_profit,
                COUNT(DISTINCT "Customer ID") as unique_customers,
                COUNT(DISTINCT "Product ID") as unique_products
            FROM orders
        ''').fetchone()
        
        # Regional KPIs
        regional = conn.execute('''
            SELECT 
                Region,
                COUNT(*) as order_count,
                SUM(Sales) as total_sales,
                SUM(Profit) as total_profit,
                AVG(Sales) as avg_order_value
            FROM orders 
            GROUP BY Region
        ''').fetchall()
        
        # Category KPIs
        category = conn.execute('''
            SELECT 
                Category,
                COUNT(*) as order_count,
                SUM(Sales) as total_sales,
                SUM(Profit) as total_profit,
                AVG(Sales) as avg_order_value
            FROM orders 
            GROUP BY Category
        ''').fetchall()
        
        # Monthly trends
        monthly = conn.execute('''
            SELECT 
                strftime('%Y-%m', "Order Date") as month,
                COUNT(*) as order_count,
                SUM(Sales) as total_sales,
                SUM(Profit) as total_profit
            FROM orders 
            GROUP BY strftime('%Y-%m', "Order Date")
            ORDER BY month
        ''').fetchall()
        
        conn.close()
        
        # Create multi-section CSV for Tableau
        csv_lines = []
        
        # Overall KPIs
        csv_lines.append("KPI_Type,Metric,Value")
        csv_lines.append(f"Overall,Total Orders,{overall[0]}")
        csv_lines.append(f"Overall,Total Sales,{overall[1]}")
        csv_lines.append(f"Overall,Total Profit,{overall[2]}")
        csv_lines.append(f"Overall,Average Order Value,{overall[3]}")
        csv_lines.append(f"Overall,Unique Customers,{overall[5]}")
        csv_lines.append(f"Overall,Unique Products,{overall[6]}")
        
        # Regional KPIs
        for region, count, sales, profit, avg_val in regional:
            csv_lines.append(f"Regional_{region},Order Count,{count}")
            csv_lines.append(f"Regional_{region},Sales,{sales}")
            csv_lines.append(f"Regional_{region},Profit,{profit}")
            csv_lines.append(f"Regional_{region},Avg Order Value,{avg_val}")
        
        # Category KPIs
        for cat, count, sales, profit, avg_val in category:
            csv_lines.append(f"Category_{cat},Order Count,{count}")
            csv_lines.append(f"Category_{cat},Sales,{sales}")
            csv_lines.append(f"Category_{cat},Profit,{profit}")
            csv_lines.append(f"Category_{cat},Avg Order Value,{avg_val}")
        
        # Monthly trends
        for month, count, sales, profit in monthly:
            csv_lines.append(f"Monthly_{month},Order Count,{count}")
            csv_lines.append(f"Monthly_{month},Sales,{sales}")
            csv_lines.append(f"Monthly_{month},Profit,{profit}")
        
        csv_data = "\n".join(csv_lines)
        
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=tableau_kpi.csv"}
        )
    except Exception as e:
        return {"error": str(e)}

@app.get("/tableau/orders/json")
async def get_tableau_orders_json():
    """JSON endpoint for Web Data Connector"""
    try:
        conn = sqlite3.connect('tableau_sales.db')
        df = pd.read_sql('SELECT * FROM orders ORDER BY "Order Date" DESC LIMIT 1000', conn)
        conn.close()
        
        # Convert to Tableau-friendly format
        data = df.to_dict('records')
        return {"data": data}
    except Exception as e:
        return {"error": str(e)}

@app.get("/wdc")
async def wdc_info():
    """Web Data Connector information"""
    return {
        "name": "Tableau Sales Analytics WDC",
        "description": "Web Data Connector for Sales Analytics",
        "endpoints": {
            "data": "/tableau/orders/json",
            "schema": "/tableau/schema"
        }
    }

@app.get("/tableau/schema")
async def get_tableau_schema():
    """Schema information for Web Data Connector"""
    return {
        "id": "sales_analytics",
        "alias": "Sales Analytics",
        "columns": [
            {"id": "order_id", "alias": "Order ID", "dataType": "string"},
            {"id": "order_date", "alias": "Order Date", "dataType": "date"},
            {"id": "customer_id", "alias": "Customer ID", "dataType": "string"},
            {"id": "customer_name", "alias": "Customer Name", "dataType": "string"},
            {"id": "segment", "alias": "Segment", "dataType": "string"},
            {"id": "product_id", "alias": "Product ID", "dataType": "string"},
            {"id": "product_name", "alias": "Product Name", "dataType": "string"},
            {"id": "category", "alias": "Category", "dataType": "string"},
            {"id": "sub_category", "alias": "Sub-Category", "dataType": "string"},
            {"id": "region", "alias": "Region", "dataType": "string"},
            {"id": "state", "alias": "State", "dataType": "string"},
            {"id": "sales", "alias": "Sales", "dataType": "float"},
            {"id": "quantity", "alias": "Quantity", "dataType": "integer"},
            {"id": "discount", "alias": "Discount", "dataType": "float"},
            {"id": "profit", "alias": "Profit", "dataType": "float"},
            {"id": "shipping_cost", "alias": "Shipping Cost", "dataType": "float"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)