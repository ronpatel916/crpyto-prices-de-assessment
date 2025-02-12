from utils import fetch_data
import pandas as pd
import math



def main():
    coin_universe = retrieve_coin_universe()
    write_universe_to_table(coin_universe)


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
        return num_coins
    except Exception as e:
        print(f"Error fetching total number of coins: {e}")
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
            print(f"Retrieving next {limit} coins. Start={start}")
            data = fetch_data(endpoint, parameters)
            all_data.extend(data['data'])
        except Exception as e:
            print(f'Error retrieving cryptocurrency data for page {page+1}: {e}')
            break
    
    print(f'Successfully retrieved data for {len(all_data)} coins')
    return all_data

    
def write_universe_to_table(data, table_name = 'coin_universe'):
    try:
        file_path = f"data/{table_name}.csv"
        #Read json response into pandas dataframe
        df = pd.json_normalize(data)
        df.to_csv(file_path,index=False)
        print(f"Coin universe data written to file {file_path}")
        return
    except Exception as e:
        print(f'Error creating coin universe table: {e}')
        raise


if __name__ == '__main__':
    main()