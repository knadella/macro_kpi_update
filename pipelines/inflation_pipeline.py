#!/usr/bin/env python3
"""
Inflation Data Pipeline
Ingests and processes Canadian inflation data from various sources.
"""

import sys
from pathlib import Path
import logging
from datetime import datetime
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_fetcher import DataFetcher
from src.data_processor import DataProcessor
import pandas as pd



def main(source: str = "statcan"):
    """
    Main pipeline function to ingest and process inflation data.
    
    Args:
        source: Data source to use ('statcan', 'bank_of_canada', 'fred')
    """
    logger.info(f"Starting inflation data pipeline from source: {source}")
    
    try:
        # Initialize components
        fetcher = DataFetcher()
        processor = DataProcessor()
        
        # Fetch data
        #logger.info(f"Fetching inflation data from {source}...")
        
        if source == "statcan":
            config = fetcher.config['statcan']
            product_id = config['endpoints']['inflation']['product_id']
            raw_data = fetcher.fetch_statcan_data(product_id, language="en")
        
        elif source == "bank_of_canada":
            config = fetcher.config['bank_of_canada']
            series = config['endpoints']['inflation']['series']
            raw_data = fetcher.fetch_bank_of_canada_data(series)
        
        elif source == "fred":
            config = fetcher.config['fred']
            series = config['endpoints']['inflation']['series']
            raw_data = fetcher.fetch_fred_data(series)
        
        else:
            raise ValueError(f"Unknown source: {source}")
        
       # logger.info("Data fetched successfully")
        
        # Process data
        #logger.info("Processing data...")
        df = processor.process_inflation_data(raw_data, source=source)
        
        if df.empty:
            #logger.warning("No data returned from source")
            return
        
        #logger.info(f"Processed {len(df)} records")
        
        # Calculate inflation rates (MoM, YoY, and 3-month trend)
        #logger.info("Calculating inflation rates (MoM, YoY, and 3-month trend)...")
        df = processor.calculate_inflation_rates(df)
        
        # Format output with required fields
        output_df = pd.DataFrame({
            'Update Date': datetime.now().strftime('%Y-%m-%d'),
            'Yr': df['date'].dt.year,
            'Mnth': df['date'].dt.month,
            'Inflation Value': df['cpi_value'],
            'YoY Value': df['inflation_yoy'],
            'MoM Value': df['inflation_mom'],
            '3 Month Trend': df['trend_3m']
        })
        
        # Save processed data to data/processed (for internal use with timestamp)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"inflation_data_{source}_{timestamp}"
        processor.save_data(output_df, filename, format='parquet')
        
        # Save CSV to data_outputs folder with fixed filename (overwrites on each run)
        output_dir = Path(__file__).parent.parent / "data_outputs"
        output_dir.mkdir(parents=True, exist_ok=True)
        csv_path = output_dir / "inflation_data.csv"
        output_df.to_csv(csv_path, index=False)
        #logger.info(f"CSV saved to {csv_path}")
        
        #logger.info("Pipeline completed successfully")
        
        # Print summary
        print("\n" + "="*70)
        print("Pipeline Summary - Canada Inflation (All-items)")
        print("="*70)
        print(f"Source: {source}")
        print(f"Records processed: {len(output_df)}")
        print(f"Date range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
        
        # Show latest values
        latest = output_df.iloc[-1]
        latest_date = df.iloc[-1]['date']
        print(f"\nLatest data point ({latest_date.strftime('%Y-%m')}):")
        print(f"  Inflation Value: {latest['Inflation Value']:.2f}")
        if pd.notna(latest['MoM Value']):
            print(f"  Month-over-Month: {latest['MoM Value']:.2f}%")
        if pd.notna(latest['YoY Value']):
            print(f"  Year-over-Year: {latest['YoY Value']:.2f}%")
        
        # Show recent trends
        recent = output_df.tail(12)
        print(f"\nRecent 12 months average:")
        if recent['MoM Value'].notna().any():
            print(f"  Average MoM: {recent['MoM Value'].mean():.2f}%")
        if recent['YoY Value'].notna().any():
            print(f"  Average YoY: {recent['YoY Value'].mean():.2f}%")
        
        print("="*70 + "\n")
        
    except Exception as e:
        #logger.error(f"Pipeline failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Ingest Canadian inflation data")
    parser.add_argument(
        "--source",
        type=str,
        default="statcan",
        choices=["statcan", "bank_of_canada", "fred"],
        help="Data source to use (default: statcan)"
    )
    
    args = parser.parse_args()
    main(source=args.source)


