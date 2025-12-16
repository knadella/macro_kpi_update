"""
Data fetcher utilities for retrieving macroeconomic data from various sources.
"""

import requests
import zipfile
import io
from typing import Optional
from pathlib import Path
import yaml
import logging

logger = logging.getLogger(__name__)


class DataFetcher:
    """Base class for fetching data from various sources."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the data fetcher with configuration.
        
        Args:
            config_path: Path to the data sources configuration file
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "data_sources.yaml"
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def fetch_statcan_data(self, product_id: str, language: str = "en") -> str:
        """
        Fetch data from Statistics Canada API using getFullTableDownloadCSV.
        Returns the CSV content as a string.
        
        Args:
            product_id: Statistics Canada product ID (PID) - must be 8 digits
            language: Language code (en or fr)
            
        Returns:
            CSV content as string
        """
        base_url = self.config['statcan']['base_url']
        url = f"{base_url}/getFullTableDownloadCSV/{product_id}/{language}"
        
        logger.info(f"Fetching StatCan data from: {url}")
        
        try:
            # Step 1: Get the CSV download URL
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            # Extract download URL
            if not isinstance(result, dict) or 'object' not in result:
                raise ValueError(f"Unexpected API response format: {result}")
            
            download_url = result.get('object')
            logger.info(f"Download URL: {download_url}")
            
            # Step 2: Download the ZIP file
            logger.info("Downloading ZIP file...")
            zip_response = requests.get(download_url, timeout=60)
            zip_response.raise_for_status()
            
            # Step 3: Extract CSV from ZIP
            logger.info("Extracting CSV from ZIP...")
            with zipfile.ZipFile(io.BytesIO(zip_response.content)) as z:
                # Find CSV file (should be {PID}.csv)
                csv_files = [f for f in z.namelist() if f.endswith('.csv') and not f.endswith('_MetaData.csv')]
                
                if not csv_files:
                    raise ValueError("No CSV file found in ZIP archive")
                
                csv_file = csv_files[0]
                logger.info(f"Reading CSV file: {csv_file}")
                
                # Read CSV content
                with z.open(csv_file) as f:
                    csv_content = f.read().decode('utf-8')
            
            logger.info(f"Successfully extracted {len(csv_content)} characters of CSV data")
            return csv_content
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching StatCan data: {e}")
            raise
        except Exception as e:
            logger.error(f"Error processing StatCan data: {e}")
            raise
