# Cryptocurrency Analysis Pipeline

This project is a data pipeline that tracks cryptocurrency prices using the CoinMarketCap API.

## Prerequisites

- Python 3.7 or later version
- Pipenv

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/ronpatel916/crypto-prices-de-assessment.git
    cd crypto-prices-de-assessment
    ```

2. **Install Pipenv:**

    If Pipenv is not installed, install it using pip:

    ```sh
    pip install pipenv
    ```

3. **Install dependencies:**

    Navigate to the project directory and install the required packages using Pipenv:

    ```sh
    pipenv install
    ```

4. **Set up environment variables:**

    If you do not already have a CoinMarketCap API Key, get yourself a free API key for basic, personal use [here](https://coinmarketcap.com/api/pricing/)

    In the `.env` file, replace your_coinmarketcap_api_key and add your CoinMarketCap API key:

    ```env
    COINMARKETCAP_API_KEY="your_coinmarketcap_api_key"
    ```

## Running the Pipeline

1. **Activate the Pipenv shell:**

    ```sh
    pipenv shell
    ```

2. **Run the orchestration script:**

    The orchestration script will run the entire pipeline, executing each script in sequence.

    ```sh
    python orchestrate_pipeline.py
    ```

## Project Structure

- `.env`: Environment variables file containing the CoinMarketCap API key.

- `orchestrate_pipeline.py`: Orchestrates the execution of the above scripts in sequence.

- `config/`
  - `coins_to_track.csv`: CSV file containing the list of coins to track. This file will serve as a configuration table for analysts to pick and choose which coins they want to follow.

- `scripts/`
  - `task1_fetch_coin_universe.py`: Retrieves the entire universe of coins from the CoinMarketCap API
  - `task2_process_pricing_data.py`: Cleans the coin universe data and filters for the coins we want to track in `config/coins_to_track.csv` as well as BTC if not included, generating a pricing file for these coins
  - `task3_performance_analysis.py`: Analyzes the 24h price performance of the tracked coins relative to Bitcoin 24h price performance.
  - `task4_average_performance.py`: Calculates the average 24-hour performance of each tracked coin relative to Bitcoin over each run.

- `data/`: Directory where the fetched and processed data is stored.


## Notes

- The output files requested for this assignment can be found in the `data/` directory
    - `coin_universe.csv` will be the output file for Task 1
    - `pricing_data_{date}.csv` will be the output files for Task 2
    - `currency_performance_data_{date}.csv` will be the output files for Task 3
        - For Task 3 sorting, I chose to sort by the absolute value of the difference between bitcoin and the currency to sort by magnitude of change rather than direction.
    - `average_performance.csv` will be the output of the Python function requested for Task 4

- The pipeline is designed to stop if any script fails, preventing downstream scripts from running.

- I made a few design decisions for the sake of simplicity and ease of setup for this assignment that I would not make in a production environment.
    - I have stored the CoinMarketCap API Key in a .env file. In a production environment, I would not store an API Key or any other secret in an environment file, but would use a vault such as AWS Secrets Manager to store these secrets and retrieve the key from there.
    - For the sake of simplicity for this assignment, I chose to orchestrate simply with the subprocess library in orchestrate_pipeline.py. In a production environment, I would opt to a more suitable orchestrationt tool such as Airflow or Prefect. These tools utilize DAGs to organize dependencies and relationships between tasks and dictate how they should be run, and allow for better control over orchestration. The User Interface of these tools are also really convenient to allow for de-bugging data pipelines and manually triggering runs after failures.

- I utilized the tenacity python library to implement retry with a wait time of 20 seconds between retry for the API requests to CoinMarketCap. This was to add resiliency to the data pipeline, allowing the pipeline to re-attempt the API connection and request in case of networking issues or throttling. The Free subscription has a throttling rate of 30 Requests per minute, so we wait 20 seconds between failures to allow time to pass to avoid being throttled again. 

- I used the API endpoint `v1/cryptocurrency/listings/latest` to retrieve both the coin metadata and the pricing. I was going to use `/v2/cryptocurrency/quotes/latest` to retrieve price after retrieving the listings, but I found that the quote columns in the `v1/cryptocurrency/listings/latest` was sufficient for this project. If we had a paid subscription to this API, this would allow us to save credits. 