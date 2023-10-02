import hashlib
import json
import os
import time
import tldextract
import concurrent.futures

# File paths
blacklist_path = "data/blacklist.txt"
blockchain_data_path = "data/blockchain_data.json"

# Maximum number of transactions to keep in the blockchain
max_transactions = 100000000

import tldextract

def is_valid_fqdn(fqdn):
    # Use tldextract to parse the FQDN
    extracted = tldextract.extract(fqdn)

    # Check if a domain is present and meets validation criteria
    if not extracted.domain:
        return False

    # Check if a TLD is present and meets validation criteria
    if not extracted.suffix:
        return False

    # Additional checks for the domain and TLD format
    # For example, you can check if the domain contains only alphanumeric characters and hyphens
    # You can also check if the TLD is at least 2 characters long
    if not extracted.domain.isalnum() or '-' in extracted.domain:
        return False
    if len(extracted.suffix) < 2:
        return False

    # If all checks pass, consider the FQDN valid
    return True


# Function to calculate hash for a transaction
def calculate_hash(transaction):
    transaction_str = json.dumps(transaction, sort_keys=True)
    return hashlib.sha256(transaction_str.encode()).hexdigest()

# Function to process a batch of rows and create transactions
def process_batch(batch_lines):
    transactions = []

    for line in batch_lines:
        line = line.strip()
        # Skip comments and empty lines
        if line.startswith("#") or not line:
            continue

        # Check if the line is a valid FQDN (you can add more validation here)
        if is_valid_fqdn(line):
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

# Function to save transactions to the blockchain data file
def save_transactions_to_blockchain(transactions):
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
                last_run_time = float(last_run_time_file.read())
                if current_time - last_run_time < interval_seconds:
                    print("Script already ran within the specified interval. Exiting.")
                    exit(0)

        # Read the blacklist file
        with open(blacklist_path, "r") as blacklist_file:
            lines = blacklist_file.readlines()

        print("Processing the blacklist...")
        total_lines = len(lines)
        batch_size = 10000000
        start = 0

        # Process batches concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            while start < total_lines:
                end = min(start + batch_size, total_lines)
                batch_lines = lines[start:end]

                # Process the batch and get transactions
                transactions = process_batch(batch_lines)

                if transactions:
                    # Save the transactions to the blockchain data file
                    if os.path.exists(blockchain_data_path):
                        print(f"Appending {len(transactions)} transactions to the blockchain.")
                    else:
                        print(f"Creating a new blockchain with {len(transactions)} transactions.")

                    save_transactions_to_blockchain(transactions)

                start = end

                # Print progress
                processed_lines = start
                progress_percent = (processed_lines / total_lines) * 100
                print(f"Progress: {processed_lines}/{total_lines} lines processed ({progress_percent:.2f}%)")

        # Update the last run time
        with open(last_run_time_path, "w") as last_run_time_file:
            last_run_time_file.write(str(current_time))

        print(f"Processing completed. {len(transactions)} valid transactions created and saved.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
