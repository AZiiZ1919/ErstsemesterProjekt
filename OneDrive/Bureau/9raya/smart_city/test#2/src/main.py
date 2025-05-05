import pandas as pd
import numpy as np
from pathlib import Path

def load_and_combine_data():
    """Load and combine both datasets, removing duplicates"""
    base_path = Path(r"C:\Users\azizf\OneDrive\Bureau\9raya\smart_city\test#2\data")
    
    # Load datasets with ISO8601 datetime parsing
    df1 = pd.read_csv(base_path / '01-09-03-25-Rathaus-test.csv', 
                     parse_dates=['_time'], 
                     date_parser=lambda x: pd.to_datetime(x, format='ISO8601'))
    df2 = pd.read_csv(base_path / '06-16-03-25-Rathaus-test.csv',
                     parse_dates=['_time'],
                     date_parser=lambda x: pd.to_datetime(x, format='ISO8601'))
    
    # Combine and remove duplicates
    combined = pd.concat([df1, df2]).drop_duplicates()
    return combined

def preprocess_data(df):
    """Preprocess the data according to requirements"""
    # Filter for main entrance only (Haupteingang)
    df = df[df['locationdetail'] == 'Haupteingang']
    
    # Filter only relevant measurement types
    df = df[df['_field'].isin(['incoming', 'outgoing'])]
    
    # Pivot to get incoming/outgoing counts by timestamp
    freq_df = df.pivot_table(index='_time', 
                           columns='_field', 
                           values='_value', 
                           aggfunc='sum',
                           fill_value=0).reset_index()
    
    # Create frequency column by summing incoming and outgoing
    freq_df['frequency'] = freq_df['incoming'] + freq_df['outgoing']
    
    # Sort by time
    freq_df = freq_df.sort_values('_time')
    
    return freq_df[['_time', 'frequency']]

def create_hourly_dataset(df):
    """Create hourly frequency dataset"""
    # Ensure proper datetime index
    df = df.copy()
    df['_time'] = pd.to_datetime(df['_time'], format='ISO8601')
    df = df.set_index('_time')
    
    # Resample to hourly frequency (using 'h')
    hourly = df.resample('h').agg({'frequency': 'sum'}).reset_index()
    
    # Calculate percentage of max (0-100)
    if not hourly.empty and hourly['frequency'].max() > 0:
        max_freq = hourly['frequency'].max()
        hourly['percentage'] = (hourly['frequency'] / max_freq) * 100
    
        # Remove outliers using IQR method
        Q1 = hourly['frequency'].quantile(0.25)
        Q3 = hourly['frequency'].quantile(0.75)
        IQR = Q3 - Q1
        mask = ~((hourly['frequency'] < (Q1 - 1.5 * IQR)) | 
               (hourly['frequency'] > (Q3 + 1.5 * IQR)))
        hourly = hourly[mask]
    
    return hourly

def create_daily_dataset(df):
    """Create daily frequency dataset"""
    # Ensure proper datetime index
    df = df.copy()
    df['_time'] = pd.to_datetime(df['_time'], format='ISO8601')
    df = df.set_index('_time')
    
    # Resample to daily frequency
    daily = df.resample('D').agg({'frequency': 'sum'}).reset_index()
    
    # Calculate percentage of max (0-100)
    if not daily.empty and daily['frequency'].max() > 0:
        max_freq = daily['frequency'].max()
        daily['percentage'] = (daily['frequency'] / max_freq) * 100
    
        # Remove outliers using IQR method
        Q1 = daily['frequency'].quantile(0.25)
        Q3 = daily['frequency'].quantile(0.75)
        IQR = Q3 - Q1
        mask = ~((daily['frequency'] < (Q1 - 1.5 * IQR)) | 
              (daily['frequency'] > (Q3 + 1.5 * IQR)))
        daily = daily[mask]
    
    return daily

def save_results(hourly, daily):
    """Save the processed datasets"""
    output_path = Path(r"C:\Users\azizf\OneDrive\Bureau\9raya\smart_city\test#2\results")
    output_path.mkdir(exist_ok=True)
    
    hourly.to_csv(output_path / 'hourly_visitor_frequency.csv', index=False)
    daily.to_csv(output_path / 'daily_visitor_frequency.csv', index=False)

def main():
    print("Starting data processing...")
    try:
        combined = load_and_combine_data()
        print(f"Loaded {len(combined)} raw records")
        
        processed = preprocess_data(combined)
        print(f"After preprocessing: {len(processed)} timestamps")
        
        print("\nSample processed data:")
        print(processed.head())
        print("\nData types:")
        print(processed.dtypes)
        
        hourly_data = create_hourly_dataset(processed)
        daily_data = create_daily_dataset(processed)
        
        save_results(hourly_data, daily_data)
        
        print("\nProcessing complete!")
        print(f"Hourly data points: {len(hourly_data)}")
        print(f"Daily data points: {len(daily_data)}")
        print("\nHourly data sample:")
        print(hourly_data.head())
        print("\nDaily data sample:")
        print(daily_data.head())
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        print("Please check your input data format and try again.")

if __name__ == '__main__':
    main()