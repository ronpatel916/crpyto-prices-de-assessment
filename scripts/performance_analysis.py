import os
import pandas as pd
from datetime import datetime

from utils import write_data_to_csv


def main():
    coin_prices = read_latest_pricing_file()
    performance_df = calculate_24h_performance_rel_to_btc(coin_prices)

    file_name = f'currency_performance_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    file_path = os.path.join(os.path.dirname(__file__), f'../data/{file_name}')
    write_data_to_csv(performance_df, file_path)
    return

def read_latest_pricing_file():
    '''
    Retrieve latest pricing file
    '''
    # Retrieve file name of latest pricing data file
    try:
        print("Retrieving latest pricing file")
        data_path = os.path.join(os.path.dirname(__file__), '../data')
        pricing_files = [f for f in os.listdir(data_path) if 'pricing_data' in f]
        pricing_files.sort(reverse=True)
        latest_pricing_file = os.path.join(data_path, pricing_files[0])
    except Exception as e:
        print("pricing_data file not found")
        raise
    
    #Read latest pricing data file
    try:
        data = pd.read_csv(latest_pricing_file)
        print(f"Successfully read latest pricing data file {latest_pricing_file}")
        return data
    except Exception as e:
        print(f"Unable to read latest pricing data file {latest_pricing_file} to dataframe")
        raise
    
def calculate_24h_performance_rel_to_btc(df):
    '''
    Calculate 24 hour performance relative to BTC
    '''
    
    try:
        # Convert Datetime columns to datetime objects
        df['quote.USD.last_updated'] = pd.to_datetime(df['quote.USD.last_updated'])
        df['LoadedAt'] = pd.to_datetime(df['LoadedAt'])
    except Exception as e:
        print("Failed to convert datetime columns to datetime")
        raise
    
    try:
        # Extract relevant columns for analysis
        pricing_data = df[['id','symbol','name','quote.USD.price','quote.USD.percent_change_24h','quote.USD.last_updated','LoadedAt']]
        pricing_data.columns = ['id','symbol','name','price','price_percent_change_24h','price_last_updated_timestamp','LoadedAt']

        bitcoin_data = pricing_data[pricing_data['symbol'] == 'BTC'][['symbol','price_percent_change_24h']]
        bitcoin_data.columns = ['BTC','BTC_percent_change_24h']

        perf_comp_data = pricing_data.merge(bitcoin_data, how = 'cross')
        perf_comp_data['performance_vs_BTC'] = perf_comp_data['price_percent_change_24h'] - perf_comp_data['BTC_percent_change_24h']
        perf_comp_data.sort_values('performance_vs_BTC', ascending=True, inplace=True)
        perf_comp_data['analysis_timestamp'] = datetime.now()

        perf_comp_data[['price', 'price_percent_change_24h','BTC_percent_change_24h','performance_vs_BTC']] = perf_comp_data[['price', 'price_percent_change_24h','BTC_percent_change_24h','performance_vs_BTC']].round(6)
        perf_comp_data = perf_comp_data[['symbol','name','price','performance_vs_BTC','price_percent_change_24h','BTC_percent_change_24h','price_last_updated_timestamp','analysis_timestamp','LoadedAt']]
        print("Successfully calculated 24 hour performance relative to BTC")
    except Exception as e:
        print("Failed to calculate 24 hour performance relative to BTC")
        raise

    try:    
        print("Filtering performance data for coins to track")
        # Construct the path to the coins_to_track.csv file
        coins_to_track_path = os.path.join(os.path.dirname(__file__), '../config/coins_to_track.csv')

        # Read the coins_to_track.csv file
        coins_to_track = pd.read_csv(coins_to_track_path)['Symbol'].tolist()
        perf_comp_data = perf_comp_data[perf_comp_data['symbol'].isin(coins_to_track)]
        return perf_comp_data
    except Exception as e:
        print("Failed to filter performance data for coins to track")
        raise


def write_performance_data_to_file(df):
    '''
    Write performance data to csv
    '''
    # Write the performance data to a file
    try:
        file_name = f'data/currency_performance_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        df.to_csv(file_name,index=False)
        print(f"Performance data written to {file_name}")
        return
    except Exception as e:
        print(f"Error writing performance data to file: {e}")
        raise


if __name__ == '__main__':
    main()