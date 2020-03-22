import argparse
import glob
import pandas as pd
from pathlib import Path


# Read csv files
def read_csv(csv_filepath: str):
    return pd.read_csv(csv_filepath, header=0)

# Read json files
def read_json_folder(json_filepath: str):
    transaction_files = Path(json_filepath).glob('**/*.json')

    return pd.concat(pd.read_json(f, lines=True) for f in transaction_files)


def run_transformations(customers_filepath: str, products_filepath: str, transactions_filepath: str, output_location: str):
    customers_df = read_csv(customers_filepath)

    # Modify products_df
    products_df = read_csv(products_filepath)
    product_list = []
    for row in products_df.iterrows():
        value = row[1][0], row[1][1], row[1][2], row[1][2][0].upper()
        product_list.append(value)

    # Convert list to dataframe and rename columns
    products_df = pd.DataFrame(product_list)
    products_df.columns = ('product_id', 'product_description', 'product_category', 'product_cat')


    transactions_df = read_json_folder(transactions_filepath)


    #print(products_df)
    return get_latest_transaction_date(transactions_df)


def get_latest_transaction_date(transactions):
    latest_purchase = transactions.date_of_purchase.max()
    latest_transaction = transactions[transactions.date_of_purchase == latest_purchase]
    return latest_transaction


def to_canonical_date_str(date_to_transform):
    return date_to_transform.strftime('%Y-%m-%d')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Transations_dataset')
    parser.add_argument('--customers_filepath', required=False, default="/Users/emmanuelsifah/Desktop/Git_Projects/input_data_generator/input_data/starter/customers.csv")
    parser.add_argument('--products_filepath', required=False, default="/Users/emmanuelsifah/Desktop/Git_Projects/input_data_generator/input_data/starter/products.csv")
    parser.add_argument('--transactions_filepath', required=False, default="/Users/emmanuelsifah/Desktop/Git_Projects/input_data_generator/input_data/starter/transactions")
    parser.add_argument('--output_location', required=False, default="./output_data/outputs/")
    args = vars(parser.parse_args())

    run_transformations(args['customers_filepath'], args['products_filepath'], args['transactions_filepath'], args['output_location'])
