import os
import pandas as pd
from datetime import datetime
import logging

from utils import write_data_to_csv

logging.basicConfig(level=logging.INFO)

def main():
    coin_universe_data = process_coin_universe_data()
    coins_to_track = read_coins_to_track()
    pricing_data = generate_pricing_file(coin_universe_data, coins_to_track)

    #Write pricing data to file
    file_name = f'pricing_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    file_path = os.path.join(os.path.dirname(__file__), f'../data/{file_name}')
    write_data_to_csv(pricing_data, file_path)

    return

def process_coin_universe_data():
    '''
    Read coin universe data from file and process
    '''
    try:
        # Construct the path to the coin universe data file
        coin_universe_path = os.path.join(os.path.dirname(__file__), '../data/coin_universe.csv')

        # Read the coin universe data from the file
        logging.info(f"Reading coin universe data from {coin_universe_path}")
        data = pd.read_csv(coin_universe_path)
    except Exception as e:
        logging.error(f"Error reading coin universe data file: {e}")
        raise

    try:
        logging.info(f"Cleaning coin universe data")
        # Convert Datetime columns to datetime objects
        data['date_added'] = pd.to_datetime(data['date_added'])
        data['last_updated'] = pd.to_datetime(data['last_updated'])
        data['quote.USD.last_updated'] = pd.to_datetime(data['quote.USD.last_updated'])
            
        # Drop duplicate symbols by sorting by cmc rank
        data.sort_values(['cmc_rank'], ascending=True).reset_index(drop=True)
        data.drop_duplicates(subset=['symbol'],keep='first',inplace=True,ignore_index=True)
        logging.info(f"Removed duplicate symbols from coin universe data")
        return data
    except Exception as e:
        logging.error(f"Error cleaning coin universe data: {e}")
        raise
    

def read_coins_to_track():
    '''
    Read the coins_to_track.csv file
    '''
    try:
        # Construct the path to the coins_to_track.csv file
        coins_to_track_path = os.path.join(os.path.dirname(__file__), '../config/coins_to_track.csv')
        # Read the coins_to_track.csv file
        coins_to_track = pd.read_csv(coins_to_track_path)['Symbol'].tolist()

        #If BTC is not in the coins to track, add it to the list for future performance calculation purposes
        if 'BTC' not in coins_to_track:
            logging.info("BTC not in coins to track. Adding BTC to dataset")
            coins_to_track.extend(['BTC'])

        return coins_to_track
    except Exception as e:
        logging.error(f"Error reading coins to track file: {e}")
        raise

def generate_pricing_file(coin_universe, coins_to_track):
    '''
    Generate a pricing file for the coins to track
    '''

    #Filter the coin universe dataset to only include the coins we want to track
    try:
        # Select the columns we want to keep   
        pricing_data = coin_universe[['id','symbol','name','cmc_rank'] + coin_universe.columns[coin_universe.columns.str.contains('quote.USD')].to_list()]
        # Filter the dataset to only include the coins we want to track
        pricing_data = pricing_data[pricing_data['symbol'].isin(coins_to_track)]
        logging.info(f"Filtered coin universe dataset to generate pricing dataset for tracked coins")
    except Exception as e:
        logging.error(f"Error filtering coin universe dataset to generate pricing dataset for tracked coins: {e}")

    # Add columns to the pricing data and sort
    try:
        # Add a column to indicate when the data was loaded
        current_timestamp = datetime.now()
        pricing_data['LoadedAt'] = current_timestamp

        # Add a column to indicate if the coin is in the top 10 in market cap of coins
        pricing_data['IsTopCurrency'] = pricing_data['cmc_rank'] <= 10
        pricing_data.sort_values('cmc_rank', ascending=True, inplace=True)
        logging.info(f"Added columns LoadedAt and IsTopCurrency to pricing data")
        return pricing_data
    except:
        logging.error(f"Error adding columns to pricing data: {e}")
        raise


if __name__ == '__main__':
    main()