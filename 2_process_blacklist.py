import concurrent.futures
import hashlib
import json
import os
import time

import tldextract

# File paths
blacklist_path = "data/blacklist.txt"
blockchain_data_path = "data/blockchain_data.json"

# Maximum number of transactions to keep in the blockchain
max_transactions = 1000000

def is_valid_fqdn(fqdn: str) -> bool:
    """
    Validates a given FQDN using tldextract.

    Args:
        fqdn (str): The FQDN to validate.

    Returns:
        bool: True if the FQDN is valid, False otherwise.
    """
    extracted = tldextract.extract(fqdn)
    
    # Check if a domain and TLD are present
    if not extracted.domain or not extracted.suffix:
        return False

    # Additional checks for domain and TLD format
    if not extracted.domain.isalnum() or "-" in extracted.domain:
        return False
    if len(extracted.suffix) < 2:
        return False

    # If all checks pass, consider the FQDN valid
    return True


def calculate_hash(transaction: dict) -> str:
    """
    Calculates the SHA-256 hash of a transaction.

    Args:
        transaction (dict): The transaction to hash.

    Returns:
        str: The hexadecimal representation of the hash.
    """
    transaction_str = json.dumps(transaction, sort_keys=True)
    return hashlib.sha256(transaction_str.encode()).hexdigest()


def process_batch(batch_lines: list) -> list:
    """
    Processes a batch of lines from the blacklist, creating transactions.

    Args:
        batch_lines (list): A list of lines to process.

    Returns:
        list: A list of transactions created from the batch.
    """
    transactions = []

    for line in batch_lines:
        line = line.strip()
        # Skip comments and empty lines
        if line.startswith("#") or not line:
            continue

        # Check if the line is a valid FQDN
        if not is_valid_fqdn(line):
            continue

        # Create a transaction
        transaction = {
            "fqdn": line,
            "timestamp": str(time.time()),  # Use current timestamp
            "previous_hash": "",  # Will be filled later when added to the blockchain
        }
        # Calculate hash for the current transaction
        transaction["hash"] = calculate_hash(transaction)
        # Generate a serial value
        transactions.append(transaction)

    return transactions


def save_transactions_to_blockchain(transactions: list) -> None:
    """
    Saves a list of transactions to the blockchain data file.

    Args:
        transactions (list): The list of transactions to save.
    """
    blockchain_data = []

    try:
        # Load existing blockchain data if available
        if os.path.exists(blockchain_data_path):
            with open(blockchain_data_path, "r") as blockchain_file:
                blockchain_data = json.load(blockchain_file)

        # Append new transactions to the existing data
        blockchain_data.extend(transactions)

        # Prune old transactions if the maximum limit is exceeded
        if len(blockchain_data) > max_transactions:
            blockchain_data = blockchain_data[-max_transactions:]

        # Save the updated blockchain data
        with open(blockchain_data_path, "w") as blockchain_file:
            json.dump(blockchain_data, blockchain_file, indent=4)

    except FileNotFoundError:
        # If the data file doesn't exist, create it with the new transactions
        with open(blockchain_data_path, "w") as blockchain_file:
            json.dump(transactions, blockchain_file, indent=4)


if __name__ == "__main__":
    try:
        # Check if the script should run based on a defined interval (e.g., every 2 hours)
        current_time = time.time()
        interval_seconds = 2 * 60 * 60  # 2 hours in seconds
        last_run_time_path = "data/last_run_time.txt"

        if os.path.exists(last_run_time_path):
            with open(last_run_time_path, "r") as last_run_time_file:
                try:
                    last_run_time = float(last_run_time_file.read())
                except ValueError:
                    print("Invalid last run time in file. Resetting.")
                    last_run_time = 0
                if current_time - last_run_time < interval_seconds:
                    print(
                        "Script already ran within the specified interval. Exiting."
                    )
                    exit(0)

        # Read the blacklist file
        with open(blacklist_path, "r") as blacklist_file:
            lines = blacklist_file.readlines()

        print("Processing the blacklist...")
        total_lines = len(lines)
        batch_size = 1000000
        start = 0

        # Process batches concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            while start < total_lines:
                end = min(start + batch_size, total_lines)
                batch_lines = lines[start:end]

                # Process the batch and get transactions
                try:
                    transactions = process_batch(batch_lines)
                except Exception as e:
                    print(f"Error processing batch: {str(e)}")
                    continue

                if transactions:
                    # Save the transactions to the blockchain data file
                    try:
                        save_transactions_to_blockchain(transactions)
                    except Exception as e:
                        print(f"Error saving transactions: {str(e)}")
                        continue

                start = end

                # Print progress
                processed_lines = start
                progress_percent = (processed_lines / total_lines) * 100
                print(
                    f"Progress: {processed_lines}/{total_lines} lines processed ({progress_percent:.2f}%)"
                )

        # Update the last run time
        with open(last_run_time_path, "w") as last_run_time_file:
            last_run_time_file.write(str(current_time))

        print(
            f"Processing completed. {len(transactions)} valid transactions created and saved."
        )

    except Exception as e:
        print(f"An error occurred: {str(e)}")