BASE_URL = 'https://etherscan.io/txs'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

DATA_DIR = 'data/'
RAW_DIR = DATA_DIR + 'raw/'
PROCESSED_DIR = DATA_DIR + 'processed/'

RAW_TSV_PATH = RAW_DIR + 'etherscan_data.tsv'
RAW_CSV_PATH = RAW_DIR + 'etherscan_data.csv'
RAW_ARFF_PATH = RAW_DIR + 'etherscan_data.arff'

PROCESSED_CSV_PATH = PROCESSED_DIR + 'etherscan_data.csv'
PROCESSED_ARFF_PATH = PROCESSED_DIR + 'etherscan_data.arff'
LOG_FILE = 'logs/parser.log'
