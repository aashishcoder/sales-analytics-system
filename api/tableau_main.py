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

@app.get("/kpi")
async def get_kpi():
    try:
        conn = sqlite3.connect('sales_analytics.db')
        
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

@app.get("/tableau/sales")
async def get_tableau_sales():
    """Tableau-compatible CSV export"""
    try:
        conn = sqlite3.connect('sales_analytics.db')
        df = pd.read_sql("SELECT * FROM orders", conn)
        conn.close()
        
        csv_data = df.to_csv(index=False)
        
        from fastapi.responses import Response
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=tableau_sales_data.csv"}
        )
    except Exception as e:
        return {"error": str(e)}

@app.get("/tableau/kpi")
async def get_tableau_kpi():
    """Tableau-compatible KPI CSV"""
    try:
        conn = sqlite3.connect('sales_analytics.db')
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*), SUM(Sales), SUM(Profit), AVG(Sales) FROM orders")
        orders, sales, profit, avg_sales = cursor.fetchone()
        
        cursor.execute("SELECT Region, COUNT(*), SUM(Sales), SUM(Profit) FROM orders GROUP BY Region")
        regional_data = cursor.fetchall()
        
        conn.close()
        
        csv_lines = []
        csv_lines.append("KPI_Type,Metric,Value")
        csv_lines.append(f"Overall,Total Orders,{orders}")
        csv_lines.append(f"Overall,Total Sales,{sales}")
        csv_lines.append(f"Overall,Total Profit,{profit}")
        csv_lines.append(f"Overall,Average Order Value,{avg_sales}")
        
        for region, count, reg_sales, reg_profit in regional_data:
            csv_lines.append(f"Regional_{region},Order Count,{count}")
            csv_lines.append(f"Regional_{region},Sales,{reg_sales}")
            csv_lines.append(f"Regional_{region},Profit,{reg_profit}")
        
        csv_data = "\n".join(csv_lines)
        
        from fastapi.responses import Response
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=tableau_kpi_data.csv"}
        )
    except Exception as e:
        return {"error": str(e)}

# Create sample data on startup
@app.on_event("startup")
async def startup_event():
    if not os.path.exists('sales_analytics.db'):
        print("Creating sample database...")
        conn = sqlite3.connect('sales_analytics.db')
        
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
