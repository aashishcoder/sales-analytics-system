from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(orders, customers, products, calendar):
    """Load transformed data into database with proper schema"""
    print("🗄️  PHASE 3: LOAD - Starting data loading...")
    
    try:
        # Create database engine (SQLite for now, can upgrade to PostgreSQL)
        engine = create_engine("sqlite:///sales_analytics.db", echo=False)
        logging.info("Database engine created")
        
        # Create tables with proper schema
        create_tables(engine)
        
        # Load data into tables
        tables_data = [
            ('orders', orders),
            ('customers', customers),
            ('products', products),
            ('calendar', calendar)
        ]
        
        for table_name, df in tables_data:
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            logging.info(f"✅ Loaded {len(df)} rows into {table_name} table")
        
        # Create indexes for performance
        create_indexes(engine)
        
        # Verify data integrity
        verify_data(engine)
        
        print("🎉 Data loading completed successfully!")
        return True
        
    except SQLAlchemyError as e:
        logging.error(f"❌ Database error: {e}")
        return False
    except Exception as e:
        logging.error(f"❌ Loading failed: {e}")
        return False

def create_tables(engine):
    """Create tables with proper schema"""
    with engine.connect() as conn:
        # Orders table (Fact table)
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS orders (
                "Order ID" TEXT PRIMARY KEY,
                "Order Date" DATE,
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
        """))
        
        # Customers table (Dimension)
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS customers (
                "Customer ID" TEXT PRIMARY KEY,
                "Customer Name" TEXT,
                "Segment" TEXT
            )
        """))
        
        # Products table (Dimension)
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS products (
                "Product ID" TEXT PRIMARY KEY,
                "Category" TEXT,
                "Sub-Category" TEXT,
                "Product Name" TEXT
            )
        """))
        
        # Calendar table (Dimension)
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS calendar (
                "Date" DATE PRIMARY KEY,
                "Year" INTEGER,
                "Month" INTEGER,
                "Quarter" INTEGER,
                "MonthName" TEXT,
                "DayOfWeek" INTEGER,
                "DayName" TEXT
            )
        """))
        
        conn.commit()
        logging.info("✅ Database tables created")

def create_indexes(engine):
    """Create indexes for better performance"""
    with engine.connect() as conn:
        # Orders table indexes
        conn.execute(text('CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders("Customer ID")'))
        conn.execute(text('CREATE INDEX IF NOT EXISTS idx_orders_product ON orders("Product ID")'))
        conn.execute(text('CREATE INDEX IF NOT EXISTS idx_orders_date ON orders("Order Date")'))
        conn.execute(text('CREATE INDEX IF NOT EXISTS idx_orders_region ON orders("Region")'))
        
        # Calendar table index
        conn.execute(text('CREATE INDEX IF NOT EXISTS idx_calendar_date ON calendar("Date")'))
        
        conn.commit()
        logging.info("✅ Database indexes created")

def verify_data(engine):
    """Verify data integrity after loading"""
    with engine.connect() as conn:
        # Check row counts
        orders_count = conn.execute(text("SELECT COUNT(*) FROM orders")).scalar()
        customers_count = conn.execute(text("SELECT COUNT(*) FROM customers")).scalar()
        products_count = conn.execute(text("SELECT COUNT(*) FROM products")).scalar()
        calendar_count = conn.execute(text("SELECT COUNT(*) FROM calendar")).scalar()
        
        # Check totals
        total_sales = conn.execute(text("SELECT SUM(Sales) FROM orders")).scalar()
        total_profit = conn.execute(text("SELECT SUM(Profit) FROM orders")).scalar()
        
        print(f"\n📊 Database Verification:")
        print(f"  • Orders: {orders_count:,} records")
        print(f"  • Customers: {customers_count:,} unique")
        print(f"  • Products: {products_count:,} unique")
        print(f"  • Calendar: {calendar_count:,} days")
        print(f"  • Total Sales: ${total_sales:,.0f}")
        print(f"  • Total Profit: ${total_profit:,.0f}")

def get_database_connection():
    """Get database connection for API"""
    return create_engine("sqlite:///sales_analytics.db")

if __name__ == "__main__":
    # For testing
    from extract import extract_data
    from transform import transform_data
    
    df = extract_data()
    orders, customers, products, calendar = transform_data(df)
    load_data(orders, customers, products, calendar)
