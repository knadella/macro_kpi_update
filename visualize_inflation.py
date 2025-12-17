#!/usr/bin/env python3
"""
Visualize inflation time series data
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def visualize_inflation_data(csv_file: str = None):
    """
    Visualize inflation time series data.
    
    Args:
        csv_file: Path to CSV file. If None, finds the most recent file.
    """
    # Find the most recent CSV file if not specified
    if csv_file is None:
        data_dir = Path(__file__).parent / "data" / "processed"
        csv_files = list(data_dir.glob("inflation_data_statcan_*.csv"))
        if not csv_files:
            print("No inflation data files found. Run the pipeline first.")
            return
        csv_file = max(csv_files, key=lambda p: p.stat().st_mtime)
        print(f"Using most recent file: {csv_file}")
    
    # Read data
    df = pd.read_csv(csv_file)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Create figure with subplots
    fig, axes = plt.subplots(3, 1, figsize=(14, 12))
    fig.suptitle('Canada Inflation Time Series - All Items', fontsize=16, fontweight='bold')
    
    # Plot 1: CPI Value over time
    ax1 = axes[0]
    ax1.plot(df['date'], df['cpi_value'], linewidth=2, color='#2E86AB')
    ax1.set_title('Consumer Price Index (CPI) - All Items', fontsize=12, fontweight='bold')
    ax1.set_ylabel('CPI Value', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlabel('Date', fontsize=10)
    
    # Add recent data highlight
    recent = df.tail(12)
    ax1.plot(recent['date'], recent['cpi_value'], linewidth=3, color='#A23B72', label='Last 12 months')
    ax1.legend()
    
    # Plot 2: Month-over-Month Inflation
    ax2 = axes[1]
    mom_data = df[df['inflation_mom'].notna()]
    ax2.plot(mom_data['date'], mom_data['inflation_mom'], linewidth=1.5, color='#F18F01', alpha=0.7)
    ax2.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax2.set_title('Month-over-Month (MoM) Inflation Rate', fontsize=12, fontweight='bold')
    ax2.set_ylabel('MoM Inflation (%)', fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlabel('Date', fontsize=10)
    
    # Highlight recent period
    recent_mom = mom_data.tail(12)
    if len(recent_mom) > 0:
        ax2.plot(recent_mom['date'], recent_mom['inflation_mom'], linewidth=2.5, color='#C73E1D', label='Last 12 months')
        ax2.legend()
    
    # Plot 3: Year-over-Year Inflation
    ax3 = axes[2]
    yoy_data = df[df['inflation_yoy'].notna()]
    ax3.plot(yoy_data['date'], yoy_data['inflation_yoy'], linewidth=1.5, color='#06A77D', alpha=0.7)
    ax3.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax3.axhline(y=2, color='red', linestyle=':', linewidth=1, alpha=0.5, label='2% Target')
    ax3.set_title('Year-over-Year (YoY) Inflation Rate', fontsize=12, fontweight='bold')
    ax3.set_ylabel('YoY Inflation (%)', fontsize=10)
    ax3.grid(True, alpha=0.3)
    ax3.set_xlabel('Date', fontsize=10)
    
    # Highlight recent period
    recent_yoy = yoy_data.tail(12)
    if len(recent_yoy) > 0:
        ax3.plot(recent_yoy['date'], recent_yoy['inflation_yoy'], linewidth=2.5, color='#6A0DAD', label='Last 12 months')
        ax3.legend()
    
    plt.tight_layout()
    
    # Save figure
    output_dir = Path(__file__).parent / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "inflation_time_series.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nVisualization saved to: {output_file}")
    
    # Also show the plot
    plt.show()
    
    # Print summary statistics
    print("\n" + "="*70)
    print("Summary Statistics")
    print("="*70)
    print(f"Total data points: {len(df)}")
    print(f"Date range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
    print(f"\nLatest CPI Value: {df['cpi_value'].iloc[-1]:.2f}")
    
    if df['inflation_mom'].notna().any():
        print(f"\nMonth-over-Month Inflation:")
        print(f"  Latest: {df['inflation_mom'].iloc[-1]:.2f}%")
        print(f"  Average (last 12 months): {df['inflation_mom'].tail(12).mean():.2f}%")
        print(f"  Std Dev (last 12 months): {df['inflation_mom'].tail(12).std():.2f}%")
    
    if df['inflation_yoy'].notna().any():
        print(f"\nYear-over-Year Inflation:")
        print(f"  Latest: {df['inflation_yoy'].iloc[-1]:.2f}%")
        print(f"  Average (last 12 months): {df['inflation_yoy'].tail(12).mean():.2f}%")
        print(f"  Std Dev (last 12 months): {df['inflation_yoy'].tail(12).std():.2f}%")
    print("="*70)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Visualize inflation time series data")
    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="Path to CSV file (default: most recent file)"
    )
    
    args = parser.parse_args()
    visualize_inflation_data(args.file)


