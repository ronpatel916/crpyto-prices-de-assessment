import os
import pandas as pd
import datetime as datetime

from utils import write_data_to_csv


def main():
    avg_performance_df = calculate_average_24h_performance_per_coin()
    if not avg_performance_df.empty:
        #Write average performance data to file
        file_name = 'data/average_performance.csv'
        file_path = os.path.join(os.path.dirname(__file__), f'../data/{file_name}')
        write_data_to_csv(avg_performance_df, file_path)


def calculate_average_24h_performance_per_coin():
    print("Retrieving file names for all currency performance data files")
    #Retrieve all currency performance data files previously run 
    data_path = os.path.join(os.path.dirname(__file__), '../data')
    performance_files = [f for f in os.listdir(data_path) if 'currency_performance_data' in f]

    #Exit Function if no performance data files are found
    if not performance_files:
        print("No performance data files found")
        return pd.DataFrame.empty()
    
    try:
        #create list to store dataframe from each file
        dataframes = []
        #Iterate through each file and append to list of dataframes
        for file in performance_files:
            df = pd.read_csv(os.path.join(data_path,file))
            dataframes.append(df)
    except Exception as e:
        print(f"Error reading performance data files: {e}")
        raise

    try:
        #Concatenate all dataframes into one
        all_performance_data = pd.concat(dataframes,ignore_index=True)

        #Calculate average performance per coin
        average_performance = all_performance_data[['symbol','performance_vs_BTC']] \
            .groupby('symbol') \
            .mean('performance_vs_BTC') \
            .sort_values('performance_vs_BTC')\
            .reset_index()
        average_performance['performance_vs_BTC'] = average_performance['performance_vs_BTC'].round(4)
        
        #Add calculation timestamp
        average_performance['calculation_timestamp'] = datetime.now()
        return average_performance
    except Exception as e:
        print(f"Error calculating average performance: {e}")
        raise


if __name__ == '__main__':
    main()