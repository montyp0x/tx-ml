import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
import os
from src.config import BASE_URL, HEADERS, RAW_TSV_PATH
from src.utils import create_directory, setup_logging
import re

def extract_numeric(text):
    match = re.search(r'[\d\.]+', text.replace(',', ''))
    return match.group() if match else None

def parse_row(row):
    cols = row.find_all('td')
    if len(cols) < 12:
        logging.warning(f"wrong cols num: {len(cols)}")
        return None 

    try:
        tx_hash_elem = cols[1].find('a', class_='myFnExpandBox_searchVal')
        tx_hash = tx_hash_elem.get_text(strip=True) if tx_hash_elem else ''

        method_elem = cols[2].find('span')
        if method_elem:
            method = method_elem.get('title')
            if not method:
                method = method_elem.get('data-bs-title')
            if not method:
                method = method_elem.get_text(strip=True)
        else:
            method = ''

        block_elem = cols[3].find('a')
        block_text = block_elem.get_text(strip=True) if block_elem else ''
        block = int(block_text.replace(',', ''))

        age_elem = cols[4].find('span')
        age = age_elem.get_text(strip=True) if age_elem else ''

        from_address_cell = cols[7]
        from_clipboard_a = from_address_cell.find('a', class_='js-clipboard link-secondary')
        if from_clipboard_a:
            from_addr = from_clipboard_a.get('data-clipboard-text', '').strip().lower()
        else:
            from_addr = ''

        
        to_address_cell = cols[9]
        to_clipboard_a = to_address_cell.find('a', class_='js-clipboard link-secondary')
        if to_clipboard_a:
            to_addr = to_clipboard_a.get('data-clipboard-text', '').strip().lower()
        else:
            to_addr = ''

        value_elem = cols[10].find('span', class_='td_showAmount')
        value_text = value_elem.get_text(separator='', strip=True) if value_elem else ''
        value = extract_numeric(value_text)

        if value:
            value_eth = float(value)
        else:
            logging.warning(f"wrong Value: '{value_text}'")
            return None 

        # Txn Fee
        txn_fee_elem = cols[11]
        txn_fee_text = txn_fee_elem.get_text(separator='', strip=True) if txn_fee_elem else ''
        txn_fee = extract_numeric(txn_fee_text)
        if txn_fee:
            txn_fee_eth = float(txn_fee)
        else:
            logging.warning(f"wrong Txn Fee: '{txn_fee_text}'")
            return None 

        return {
            'TransactionHash': tx_hash,
            'Method': method,
            'BlockNumber': block,
            'Age': age,
            'FromAddress': from_addr,
            'ToAddress': to_addr,
            'Value_ETH': value_eth,
            'TxnFee_ETH': txn_fee_eth
        }
    except Exception as e:
        logging.warning(f"error during parsing row: {e}")
        return None 


def parse_page(page_number):
    url = f"{BASE_URL}?p={page_number}"
    logging.info(f"start parsing page: {url}")

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"error occured on page {page_number} request: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'table'})
    if not table:
        logging.warning(f"table not found on page {page_number}")
        return []

    rows = table.find('tbody').find_all('tr')
    data = []

    for row in rows:
        parsed_data = parse_row(row)
        if parsed_data:
            data.append(parsed_data)
    return data

def main():
    create_directory(os.path.dirname(RAW_TSV_PATH))
    all_transactions = []
    total_pages = 100

    for page in range(1, total_pages + 1):
        logging.info(f"parsing page {page}/{total_pages}")
        transactions = parse_page(page)
        all_transactions.extend(transactions)
        time.sleep(10)

    if all_transactions:
        df = pd.DataFrame(all_transactions)
        df.to_csv(RAW_TSV_PATH, sep='\t', index=False)
        logging.info(f"data is saved in {RAW_TSV_PATH}")
    else:
        logging.warning("txs werent received")

if __name__ == '__main__':
    from src.utils import setup_logging
    setup_logging()
    main()
