import pandas as pd
import kagglehub
import os
from datetime import datetime

def extract_data():
    """Extract data from Kaggle Superstore dataset"""
    print("🔥 PHASE 1: EXTRACT - Starting data extraction...")
    
    try:
        # Download from Kaggle Hub
        path = kagglehub.dataset_download("ishanshrivastava28/superstore-sales")
        print(f"📥 Downloaded dataset to: {path}")
        
        # Find CSV file
        csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
        if not csv_files:
            raise FileNotFoundError("No CSV file found in downloaded dataset")
        
        data_path = os.path.join(path, csv_files[0])
        
        # Extract raw data
        df = pd.read_csv(data_path, encoding='latin1')
        print(f"📊 Extracted {len(df)} rows from Superstore dataset")
        
        # Save raw data
        os.makedirs('data/raw', exist_ok=True)
        raw_path = 'data/raw/superstore_raw.csv'
        df.to_csv(raw_path, index=False)
        print(f"💾 Saved raw data to: {raw_path}")
        
        return df
        
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        raise

if __name__ == "__main__":
    extract_data()
