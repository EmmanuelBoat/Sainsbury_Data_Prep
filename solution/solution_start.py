import argparse
import glob
import pandas as pd
from pathlib import Path


def read_csv(csv_filepath: str):
    return pd.read_csv(csv_filepath, header=0)


def read_json_folder(json_filepath: str):
    #transactions_files = glob.glob("{}*/*.json".format(json_folder))
    transaction_files = Path(json_filepath).glob('**/*.json')

    return pd.concat(pd.read_json(f, lines=True) for f in transaction_files)


def run_transformations(customers_filepath: str, products_filepath: str, transactions_filepath: str, output_location: str):
    customers_df = read_csv(customers_filepath)
    products_df = read_csv(products_filepath)
    transactions_df = read_json_folder(transactions_filepath)

    return get_latest_transaction_date(transactions_df)


def get_latest_transaction_date(transactions):
    latest_purchase = transactions.date_of_purchase.max()
    latest_transaction = transactions[transactions.date_of_purchase == latest_purchase]
    return latest_transaction


def to_canonical_date_str(date_to_transform):
    return date_to_transform.strftime('%Y-%m-%d')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Transations_dataset')
    parser.add_argument('--customers_filepath', required=False, default="./input_data_generator/input_data/starter/customers.csv")
    parser.add_argument('--products_filepath', required=False, default="./input_data_generator/input_data/starter/products.csv")
    parser.add_argument('--transactions_filepath', required=False, default="./input_data_generator/input_data/starter/transactions")
    parser.add_argument('--output_location', required=False, default="./output_data/outputs/")
    args = vars(parser.parse_args())

    run_transformations(args['customers_filepath'], args['products_filepath'], args['transactions_filepath'], args['output_location'])
