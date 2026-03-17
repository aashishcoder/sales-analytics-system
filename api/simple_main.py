from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import pandas as pd
import os

app = FastAPI(title="Sales Analytics API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Sales Analytics API", "status": "running"}

@app.get("/health")
async def health():
    try:
        # Test database connection
        conn = sqlite3.connect('sales_analytics.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM orders")
        count = cursor.fetchone()[0]
        conn.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "orders_count": count
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@app.get("/kpi/csv")
async def get_kpi_csv():
    try:
        conn = sqlite3.connect('sales_analytics.db')
        
        # Simple KPIs
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*), SUM(Sales), SUM(Profit) FROM orders")
        orders, sales, profit = cursor.fetchone()
        
        conn.close()
        
        # Create CSV response
        csv_data = f"Metric,Value\nTotal Orders,{orders}\nTotal Sales,{sales}\nTotal Profit,{profit}"
        
        from fastapi.responses import Response
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=kpi_data.csv"}
        )
    except Exception as e:
        return {"error": str(e)}

@app.get("/sales/csv")
async def get_sales_csv():
    try:
        conn = sqlite3.connect('sales_analytics.db')
        df = pd.read_sql("SELECT * FROM orders", conn)
        conn.close()
        
        # Convert to CSV
        csv_data = df.to_csv(index=False)
        
        from fastapi.responses import Response
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=sales_data.csv"}
        )
    except Exception as e:
        return {"error": str(e)}

@app.get("/kpi")
async def get_kpi():
    try:
        conn = sqlite3.connect('sales_analytics.db')
        
        # Simple KPIs
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*), SUM(Sales), SUM(Profit) FROM orders")
        orders, sales, profit = cursor.fetchone()
        
        conn.close()
        
        return {
            "total_orders": orders,
            "total_sales": sales,
            "total_profit": profit
        }
    except Exception as e:
        return {"error": str(e)}

# Create sample data on startup
@app.on_event("startup")
async def startup_event():
    if not os.path.exists('sales_analytics.db'):
        print("Creating sample database...")
        conn = sqlite3.connect('sales_analytics.db')
        
        # Create orders table
        conn.execute('''
            CREATE TABLE orders (
                "Order ID" TEXT PRIMARY KEY,
                "Order Date" TEXT,
                "Customer ID" TEXT,
                "Product ID" TEXT,
                "Sales" REAL,
                "Profit" REAL,
                "Quantity" INTEGER,
                "Discount" REAL,
                "Region" TEXT,
                "Revenue" REAL,
                "Profit Margin" REAL
            )
        ''')
        
        # Insert sample data
        sample_data = [
            ('ORD0001', '2024-01-01', 'CUST001', 'PROD001', 100.0, 20.0, 2, 0.0, 'North', 200.0, 10.0),
            ('ORD0002', '2024-01-02', 'CUST002', 'PROD002', 150.0, 30.0, 1, 0.1, 'South', 135.0, 22.2),
            ('ORD0003', '2024-01-03', 'CUST003', 'PROD003', 200.0, 50.0, 3, 0.0, 'East', 600.0, 25.0),
        ]
        
        conn.executemany('''
            INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_data)
        
        conn.commit()
        conn.close()
        print("Sample database created!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
