# Canadian Macroeconomic KPI Data Pipeline

A data pipeline project for ingesting and processing macroeconomic key performance indicators (KPIs) for Canada.

## Overview

This project provides data pipelines to collect, transform, and store macroeconomic indicators for Canada from various data sources. The pipelines are designed to be modular, scalable, and maintainable.

## Project Structure

```
macro_kpi_update/
├── pipelines/          # Data pipeline scripts
│   └── inflation_pipeline.py  # Inflation data ingestion pipeline
├── data/               # Raw and processed data (gitignored)
│   └── processed/      # Processed data files
├── config/             # Configuration files
│   └── data_sources.yaml  # Data source configurations
├── src/                # Source code and utilities
│   ├── data_fetcher.py    # Data fetching utilities
│   └── data_processor.py  # Data processing utilities
├── tests/              # Unit and integration tests
├── logs/               # Pipeline execution logs
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Features

- Automated data ingestion from multiple sources
- Data validation and quality checks
- Transformations and aggregations
- Storage and archival capabilities
- Monitoring and logging

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd macro_kpi_update
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```


## Data Sources

### Inflation Data

The inflation pipeline supports multiple data sources:

- **Statistics Canada (StatCan)** - Official Canadian government data (default)
- **Bank of Canada** - Central bank economic indicators
- **FRED (Federal Reserve Economic Data)** - International economic data including Canadian CPI

## Usage

### Running the Inflation Pipeline

To ingest inflation data, run:

```bash
python pipelines/inflation_pipeline.py --source statcan
```

Available sources:
- `statcan` - Statistics Canada (default)

The pipeline will:
1. Fetch inflation data from the specified source
2. Process and standardize the data
3. Calculate year-over-year inflation rates
4. Save data in both Parquet and CSV formats to `data/processed/` and `data_outputs`

### Example

```bash
# Use Statistics Canada (default)
python pipelines/inflation_pipeline.py

```


