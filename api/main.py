from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import logging
from datetime import datetime
from typing import List, Dict, Any

# Import database connection
import sys
import os
from sqlalchemy import create_engine, text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Sales Analytics API",
    description="REST API for Sales Analytics Dashboard",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get database engine
def get_engine():
    """Create database engine"""
    return create_engine("sqlite:///sales_analytics.db", echo=False)

# Initialize engine
engine = get_engine()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Sales Analytics API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "/sales": "Get all sales data",
            "/kpi": "Get key performance indicators",
            "/customers": "Get customer data",
            "/products": "Get product data",
            "/regions": "Get regional sales data",
            "/health": "Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        with engine.connect() as conn:
            from sqlalchemy import text
            conn.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.get("/sales")
async def get_sales(limit: int = 1000, offset: int = 0):
    """Get sales data with pagination"""
    try:
        query = f"""
        SELECT 
            "Order ID", "Order Date", "Customer ID", "Product ID",
            Sales, Profit, Quantity, Discount, Region, Revenue, "Profit Margin"
        FROM orders 
        ORDER BY "Order Date" DESC
        LIMIT {limit} OFFSET {offset}
        """
        
        df = pd.read_sql(query, engine)
        return {
            "data": df.to_dict(orient="records"),
            "total": len(df),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Error fetching sales data: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch sales data")

@app.get("/kpi")
async def get_kpi():
    """Get key performance indicators"""
    try:
        query = """
        SELECT 
            SUM(Sales) as total_sales,
            SUM(Profit) as total_profit,
            COUNT(*) as total_orders,
            AVG(Sales) as avg_order_value,
            AVG("Profit Margin") as avg_profit_margin,
            COUNT(DISTINCT "Customer ID") as unique_customers,
            COUNT(DISTINCT "Product ID") as unique_products
        FROM orders
        """
        
        df = pd.read_sql(query, engine)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No KPI data found")
        
        kpi_data = df.iloc[0].to_dict()
        
        # Format numbers
        kpi_data['total_sales'] = float(kpi_data['total_sales'])
        kpi_data['total_profit'] = float(kpi_data['total_profit'])
        kpi_data['avg_order_value'] = float(kpi_data['avg_order_value'])
        kpi_data['avg_profit_margin'] = float(kpi_data['avg_profit_margin'])
        
        return kpi_data
        
    except Exception as e:
        logger.error(f"Error fetching KPI data: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch KPI data")

@app.get("/customers")
async def get_customers():
    """Get customer data"""
    try:
        query = """
        SELECT c."Customer ID", c."Customer Name", c.Segment,
               COUNT(o."Order ID") as order_count,
               COALESCE(SUM(o.Sales), 0) as total_sales,
               COALESCE(AVG(o.Sales), 0) as avg_order_value
        FROM customers c
        LEFT JOIN orders o ON c."Customer ID" = o."Customer ID"
        GROUP BY c."Customer ID", c."Customer Name", c.Segment
        ORDER BY total_sales DESC
        """
        
        df = pd.read_sql(query, engine)
        return df.to_dict(orient="records")
        
    except Exception as e:
        logger.error(f"Error fetching customer data: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch customer data")

@app.get("/products")
async def get_products():
    """Get product data"""
    try:
        query = """
        SELECT p."Product ID", p."Product Name", p.Category, p."Sub-Category",
               COUNT(o."Order ID") as order_count,
               COALESCE(SUM(o.Sales), 0) as total_sales,
               COALESCE(SUM(o.Profit), 0) as total_profit,
               COALESCE(AVG(o."Profit Margin"), 0) as avg_profit_margin
        FROM products p
        LEFT JOIN orders o ON p."Product ID" = o."Product ID"
        GROUP BY p."Product ID", p."Product Name", p.Category, p."Sub-Category"
        ORDER BY total_sales DESC
        """
        
        df = pd.read_sql(query, engine)
        return df.to_dict(orient="records")
        
    except Exception as e:
        logger.error(f"Error fetching product data: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch product data")

@app.get("/regions")
async def get_regions():
    """Get regional sales data"""
    try:
        query = """
        SELECT 
            Region,
            COUNT(*) as order_count,
            SUM(Sales) as total_sales,
            SUM(Profit) as total_profit,
            AVG(Sales) as avg_order_value,
            AVG("Profit Margin") as avg_profit_margin,
            COUNT(DISTINCT "Customer ID") as unique_customers
        FROM orders
        GROUP BY Region
        ORDER BY total_sales DESC
        """
        
        df = pd.read_sql(query, engine)
        return df.to_dict(orient="records")
        
    except Exception as e:
        logger.error(f"Error fetching regional data: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch regional data")

@app.get("/sales-trends")
async def get_sales_trends():
    """Get sales trends over time"""
    try:
        query = """
        SELECT 
            c."Year",
            c."Month",
            c."MonthName",
            SUM(o.Sales) as total_sales,
            SUM(o.Profit) as total_profit,
            COUNT(*) as order_count
        FROM orders o
        JOIN calendar c ON o."Order Date" = c."Date"
        GROUP BY c."Year", c."Month", c."MonthName"
        ORDER BY c."Year", c."Month"
        """
        
        df = pd.read_sql(query, engine)
        return df.to_dict(orient="records")
        
    except Exception as e:
        logger.error(f"Error fetching sales trends: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch sales trends")

@app.get("/top-products")
async def get_top_products(limit: int = 10):
    """Get top performing products"""
    try:
        query = f"""
        SELECT 
            p."Product Name",
            p.Category,
            SUM(o.Sales) as total_sales,
            SUM(o.Profit) as total_profit,
            COUNT(*) as order_count
        FROM orders o
        JOIN products p ON o."Product ID" = p."Product ID"
        GROUP BY p."Product ID", p."Product Name", p.Category
        ORDER BY total_sales DESC
        LIMIT {limit}
        """
        
        df = pd.read_sql(query, engine)
        return df.to_dict(orient="records")
        
    except Exception as e:
        logger.error(f"Error fetching top products: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch top products")

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Sales Analytics API")
    print("📊 API Documentation: http://localhost:8000/docs")
    print("🔗 Health Check: http://localhost:8000/health")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
