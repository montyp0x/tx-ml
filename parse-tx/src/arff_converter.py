import pandas as pd
import arff
import logging
from src.config import PROCESSED_CSV_PATH, PROCESSED_ARFF_PATH
from src.utils import create_directory
import os

def convert_to_arff():
    logging.info("start converting in arff...")

    create_directory(os.path.dirname(PROCESSED_ARFF_PATH))

    df = pd.read_csv(PROCESSED_CSV_PATH)

    methods = df['Method'].unique().tolist()
    methods = [method.lower() for method in methods]

    attributes = [
        ('TransactionHash', 'STRING'),
        ('Method', methods),  # NOMINAL 
        ('BlockNumber', 'NUMERIC'),
        ('FromAddressEncoded', 'NUMERIC'),
        ('ToAddressEncoded', 'NUMERIC'),
        ('Value_ETH', 'NUMERIC'),
        ('TxnFee_ETH', 'NUMERIC')
    ]

    data = df[[
        'TransactionHash',
        'Method',
        'BlockNumber',
        'FromAddressEncoded',
        'ToAddressEncoded',
        'Value_ETH',
        'TxnFee_ETH'
    ]].values.tolist()

    arff_dict = {
        'description': 'Etherscan Transactions Dataset',
        'relation': 'etherscan_transactions',
        'attributes': attributes,
        'data': data
    }

    with open(PROCESSED_ARFF_PATH, 'w') as f:
        arff.dump(arff_dict, f)
    logging.info(f"arff data saved in {PROCESSED_ARFF_PATH}")

if __name__ == '__main__':
    from src.utils import setup_logging
    setup_logging()
    convert_to_arff()
