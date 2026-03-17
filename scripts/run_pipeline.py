#!/usr/bin/env python3
"""
Sales Analytics ETL Pipeline
===========================

This script runs the complete ETL pipeline:
1. Extract data from Kaggle
2. Transform to star schema
3. Load into database
"""

import logging
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def run_pipeline():
    """Execute the complete ETL pipeline"""
    start_time = datetime.now()
    logging.info("🚀 Starting Sales Analytics ETL Pipeline")
    
    try:
        # Phase 1: Extract
        logging.info("🔥 PHASE 1: EXTRACT")
        raw_df = extract_data()
        
        # Phase 2: Transform
        logging.info("🔧 PHASE 2: TRANSFORM")
        orders, customers, products, calendar = transform_data(raw_df)
        
        # Phase 3: Load
        logging.info("🗄️  PHASE 3: LOAD")
        success = load_data(orders, customers, products, calendar)
        
        if success:
            end_time = datetime.now()
            duration = end_time - start_time
            logging.info(f"✅ Pipeline completed successfully in {duration.total_seconds():.2f} seconds")
            return True
        else:
            logging.error("❌ Pipeline failed during loading phase")
            return False
            
    except Exception as e:
        logging.error(f"❌ Pipeline failed: {e}")
        return False

def validate_pipeline():
    """Validate pipeline results"""
    try:
        from etl.load import get_database_connection
        import pandas as pd
        
        engine = get_database_connection()
        
        # Test queries
        queries = {
            'total_orders': 'SELECT COUNT(*) as count FROM orders',
            'total_sales': 'SELECT SUM(Sales) as total FROM orders',
            'unique_customers': 'SELECT COUNT(*) as count FROM customers',
            'date_range': 'SELECT MIN("Order Date") as min_date, MAX("Order Date") as max_date FROM orders'
        }
        
        results = {}
        for name, query in queries.items():
            df = pd.read_sql(query, engine)
            results[name] = df.iloc[0].to_dict()
        
        logging.info("🔍 Pipeline Validation Results:")
        for name, result in results.items():
            logging.info(f"  • {name}: {result}")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Validation failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 SALES ANALYTICS ETL PIPELINE")
    print("=" * 60)
    
    # Run pipeline
    success = run_pipeline()
    
    if success:
        # Validate results
        validate_pipeline()
        print("\n🎉 Pipeline executed successfully!")
        print("📊 Database is ready for API and dashboard connections")
    else:
        print("\n❌ Pipeline failed. Check logs for details.")
        sys.exit(1)
