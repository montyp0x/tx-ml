# src/preprocess.py

import pandas as pd
import logging
from src.config import RAW_TSV_PATH, PROCESSED_CSV_PATH
from src.utils import create_directory
import os
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from datetime import datetime
import re

def preprocess_data():
    logging.info("start preprocessing data...")

    create_directory(os.path.dirname(PROCESSED_CSV_PATH))

    df = pd.read_csv(RAW_TSV_PATH, sep='\t')

    target_column = 'Method'

    numerical_cols = ['BlockNumber', 'Value_ETH', 'TxnFee_ETH']
    categorical_cols = ['FromAddress', 'ToAddress', 'Method']

    df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].median())

    for col in categorical_cols:
        df[col] = df[col].fillna('unknown')

    df['AgeUnix'] = df['Age'].apply(parse_age)
    df['AgeUnix'] = df['AgeUnix'].fillna(df['AgeUnix'].median())

    df['FromAddress'] = df['FromAddress'].str.lower()
    df['ToAddress'] = df['ToAddress'].str.lower()
    df['Method'] = df['Method'].str.lower()

    le_from = LabelEncoder()
    df['FromAddressEncoded'] = le_from.fit_transform(df['FromAddress'])

    le_to = LabelEncoder()
    df['ToAddressEncoded'] = le_to.fit_transform(df['ToAddress'])

    scaler = MinMaxScaler()
    numerical_cols_extended = numerical_cols + ['AgeUnix']
    df[numerical_cols_extended] = scaler.fit_transform(df[numerical_cols_extended])

    df = df.drop(['FromAddress', 'ToAddress', 'Age', 'AgeUnix'], axis=1)

    df.to_csv(PROCESSED_CSV_PATH, index=False)
    logging.info(f"preprocessed data is saved in {PROCESSED_CSV_PATH}")

def parse_age(age_str):
    try:
        dt = datetime.strptime(age_str, '%Y-%m-%d %H:%M:%S')
        timestamp = int(dt.timestamp())
        return timestamp
    except ValueError:
        logging.warning(f"incorrect data format: '{age_str}'")
        return None

if __name__ == '__main__':
    from src.utils import setup_logging
    setup_logging()
    preprocess_data()
