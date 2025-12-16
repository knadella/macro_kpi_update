# Inflation Pipeline Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    PIPELINE EXECUTION                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Initialize                                         │
│  • Set up logging (file + console)                          │
│  • Create logs directory                                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Initialize Components                              │
│  • DataFetcher: Load config, set up rate limiting           │
│  • DataProcessor: Set up output directory                   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Fetch Data                                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ DataFetcher.fetch_statcan_data()                     │  │
│  │  1. Check rate limits (60 req/min)                  │  │
│  │  2. Build API URL from config                        │  │
│  │  3. Send GET request                                 │  │
│  │  4. Return JSON response                             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Process Raw Data                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ DataProcessor.process_inflation_data()              │  │
│  │  1. Convert JSON → DataFrame                        │  │
│  │  2. Standardize column names (lowercase)            │  │
│  │  3. Map date columns → 'date' (datetime)           │  │
│  │  4. Map value columns → 'cpi_value'                │  │
│  │  5. Return standardized DataFrame                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 5: Calculate Inflation Rates                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ DataProcessor.calculate_inflation_rate()             │  │
│  │  1. Sort by date                                     │  │
│  │  2. Shift CPI by 12 months (year-over-year)         │  │
│  │  3. Calculate: ((current - prev) / prev) × 100      │  │
│  │  4. Add 'inflation_rate' column                      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 6: Save Data                                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ DataProcessor.save_data()                            │  │
│  │  • Generate timestamped filename                     │  │
│  │  • Save as Parquet (efficient storage)               │  │
│  │  • Save as CSV (human-readable)                      │  │
│  │  • Location: data/processed/                         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 7: Print Summary                                      │
│  • Source name                                              │
│  • Number of records                                        │
│  • Date range                                               │
│  • Latest inflation rate                                     │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

```
API Response (JSON)
    │
    ▼
Raw Data Dictionary
    │
    ▼
Pandas DataFrame (standardized)
    │
    ├─→ date: datetime
    └─→ cpi_value: float
    │
    ▼
DataFrame with Calculations
    │
    ├─→ date: datetime
    ├─→ cpi_value: float
    ├─→ cpi_prev_year: float
    └─→ inflation_rate: float (%)
    │
    ▼
Saved Files
    ├─→ inflation_data_statcan_YYYYMMDD_HHMMSS.parquet
    └─→ inflation_data_statcan_YYYYMMDD_HHMMSS.csv
```

## Error Handling

- **Rate Limiting**: Automatic sleep if requests too frequent
- **API Errors**: Caught and logged with full traceback
- **Data Validation**: Checks for empty DataFrames
- **File Errors**: Exceptions raised with context

## Configuration

All data sources configured in `config/data_sources.yaml`:
- API endpoints
- Rate limits
- Series/table IDs
- Authentication settings


