import os
import pandas as pd
import math
import logging

from utils import fetch_data, write_data_to_csv

logging.basicConfig(level=logging.INFO)


def main():
    coin_universe = retrieve_coin_universe()

    file_path = os.path.join(os.path.dirname(__file__), '../data/coin_universe.csv')
    write_data_to_csv(coin_universe, file_path)


def get_total_coins():
    '''
    Retrieve the total number of coins from the CoinMarketCap API
    '''
    #Request listings/latest endpoint to retrieve number of coins
    endpoint = 'v1/cryptocurrency/listings/latest'
    parameters = {
        'start': 1,
        'limit': 1
    }
    data = fetch_data(endpoint, parameters)

    #Extract total number of coins from response
    try:
        num_coins = data['status']['total_count']
        logging.info(f"Total number of coins: {num_coins}")
        return num_coins
    except Exception as e:
        logging.error(f"Error fetching total number of coins: {e}")
        raise


def retrieve_coin_universe(limit = 1000):
    '''
    Retrieve the entire coin universe from the CoinMarketCap API
    '''
    #Retrieve the total number of coins
    num_coins = get_total_coins()

    endpoint = 'v1/cryptocurrency/listings/latest'

    #Determine how many requests we will need to make to retrieve the entire coin universe
    num_pages = math.ceil(num_coins/limit)

    logging.info(f'Fetching data for {num_coins} coins in {num_pages} pages')
    #After each request, we will append all_data with the new data from the requested page
    all_data = []
    #Make paginated requests to the listings/latest endpoint
    for page in range(num_pages):
        start = (page * limit) + 1

        parameters = {
            'start': start,
            'limit': limit
        }
        
        try:
            logging.info(f"Retrieving next {limit} coins. Start={start}")
            data = fetch_data(endpoint, parameters)
            all_data.extend(data['data'])
        except Exception as e:
            logging.error(f'Error retrieving cryptocurrency data for page {page+1}: {e}')
            break
    
    try:
        coin_universe_df = pd.json_normalize(all_data)
        logging.info(f'Successfully retrieved data for {len(all_data)} coins')
        return coin_universe_df
    except Exception as e:
        logging.error(f'Error converting coin universe data to dataframe: {e}')
        raise


if __name__ == '__main__':
    main()