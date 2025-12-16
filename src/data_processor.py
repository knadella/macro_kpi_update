"""
Data processing utilities for cleaning and transforming macroeconomic data.
"""

import pandas as pd
from typing import Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """Utilities for processing and cleaning macroeconomic data."""
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize the data processor.
        
        Args:
            output_dir: Directory to save processed data
        """
        if output_dir is None:
            output_dir = Path(__file__).parent.parent / "data" / "processed"
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def process_inflation_data(self, raw_data, source: str = "statcan") -> pd.DataFrame:
        """
        Process raw inflation data into a standardized DataFrame.
        
        Args:
            raw_data: Raw data from the API (Dict for JSON APIs, str for CSV)
            source: Source of the data (statcan, bank_of_canada, fred)
            
        Returns:
            Processed DataFrame with standardized columns
        """
        if source == "statcan":
            return self._process_statcan_inflation(raw_data)
        elif source == "bank_of_canada":
            return self._process_boc_inflation(raw_data)
        elif source == "fred":
            return self._process_fred_inflation(raw_data)
        else:
            raise ValueError(f"Unknown data source: {source}")
    
    def _process_statcan_inflation(self, raw_data: str) -> pd.DataFrame:
        """
        Process Statistics Canada inflation data from CSV.
        Filters for Canada and "All-items" product group.
        
        Args:
            raw_data: CSV content as string (from getFullTableDownloadCSV)
            
        Returns:
            Processed DataFrame with date and cpi_value columns
        """
        try:
            from io import StringIO
            
            # Read CSV from string
            df = pd.read_csv(StringIO(raw_data))
            
            logger.info(f"Loaded CSV with {len(df)} rows and {len(df.columns)} columns")
            
            # Standardize column names (lowercase)
            df.columns = df.columns.str.strip().str.lower()
            
            # Filter for Canada
            if 'geo' not in df.columns:
                raise ValueError("GEO column not found in data")
            
            df = df[df['geo'].str.lower() == 'canada'].copy()
            logger.info(f"After filtering for Canada: {len(df)} rows")
            
            # Filter for "All-items" product group (exact match, not variants)
            # The column name might be "Products and product groups" or similar
            product_col = None
            for col in df.columns:
                if 'product' in col.lower():
                    product_col = col
                    break
            
            if product_col:
                # Filter for EXACTLY "All-items" (not "All-items excluding..." variants)
                df = df[df[product_col].str.strip() == 'All-items'].copy()
                logger.info(f"After filtering for exact 'All-items': {len(df)} rows")
            
            # Get date column
            if 'ref_date' not in df.columns:
                raise ValueError("REF_DATE column not found in data")
            
            # Convert date to datetime
            df['date'] = pd.to_datetime(df['ref_date'], errors='coerce')
            
            # Get value column
            if 'value' not in df.columns:
                raise ValueError("VALUE column not found in data")
            
            # Create result DataFrame
            result_df = pd.DataFrame({
                'date': df['date'],
                'cpi_value': pd.to_numeric(df['value'], errors='coerce')
            })
            
            # Remove rows with missing dates or values
            result_df = result_df.dropna(subset=['date', 'cpi_value'])
            
            # Sort by date
            result_df = result_df.sort_values('date').reset_index(drop=True)
            
            # Remove duplicates (keep first occurrence for each date)
            result_df = result_df.drop_duplicates(subset=['date'], keep='first')
            
            logger.info(f"Final processed data: {len(result_df)} records")
            logger.info(f"Date range: {result_df['date'].min()} to {result_df['date'].max()}")
            
            return result_df
            
        except Exception as e:
            logger.error(f"Error processing StatCan CSV data: {e}")
            raise
    
    def _process_boc_inflation(self, raw_data: Dict[str, Any]) -> pd.DataFrame:
        """Process Bank of Canada inflation data."""
        try:
            # Bank of Canada API structure
            observations = raw_data.get('observations', [])
            
            data = []
            for obs in observations:
                data.append({
                    'date': obs.get('d'),
                    'cpi_value': obs.get('v')
                })
            
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            
            return df
            
        except Exception as e:
            logger.error(f"Error processing Bank of Canada data: {e}")
            raise
    
    def _process_fred_inflation(self, raw_data: Dict[str, Any]) -> pd.DataFrame:
        """Process FRED inflation data."""
        try:
            observations = raw_data.get('observations', [])
            
            data = []
            for obs in observations:
                data.append({
                    'date': obs.get('date'),
                    'cpi_value': obs.get('value')
                })
            
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            
            # FRED uses '.' for missing values
            df['cpi_value'] = pd.to_numeric(df['cpi_value'], errors='coerce')
            
            return df
            
        except Exception as e:
            logger.error(f"Error processing FRED data: {e}")
            raise
    
    def calculate_inflation_rates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate both month-over-month (MoM) and year-over-year (YoY) inflation rates.
        
        Args:
            df: DataFrame with 'date' and 'cpi_value' columns (must be sorted by date)
            
        Returns:
            DataFrame with added 'inflation_mom' and 'inflation_yoy' columns
        """
        df = df.copy()
        df = df.sort_values('date').reset_index(drop=True)
        
        # Month-over-month inflation
        df['cpi_prev_month'] = df['cpi_value'].shift(1)
        df['inflation_mom'] = ((df['cpi_value'] - df['cpi_prev_month']) / df['cpi_prev_month']) * 100
        
        # Year-over-year inflation (12 months ago)
        df['cpi_prev_year'] = df['cpi_value'].shift(12)
        df['inflation_yoy'] = ((df['cpi_value'] - df['cpi_prev_year']) / df['cpi_prev_year']) * 100
        
        # Drop intermediate columns
        df = df.drop(columns=['cpi_prev_month', 'cpi_prev_year'])
        
        return df
    
    def save_data(self, df: pd.DataFrame, filename: str, format: str = 'parquet'):
        """
        Save processed data to file.
        
        Args:
            df: DataFrame to save
            filename: Name of the file (without extension)
            format: File format ('parquet', 'csv', 'json')
        """
        filepath = self.output_dir / f"{filename}.{format}"
        
        if format == 'parquet':
            df.to_parquet(filepath, index=False)
        elif format == 'csv':
            df.to_csv(filepath, index=False)
        elif format == 'json':
            df.to_json(filepath, orient='records', date_format='iso')
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        logger.info(f"Data saved to {filepath}")

