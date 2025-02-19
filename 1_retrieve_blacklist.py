import datetime
import os
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

blacklist_url = "https://get.domainsblacklists.com/blacklist.txt"
local_blacklist_path = os.path.join("data", "blacklist.txt")

def retrieve_and_save_blacklist():
    """
    Retrieves the blacklist from a remote URL and saves it to a local file.
    
    The function checks if the response status code is 200, writes a timestamp and the
    blacklist content to the local file, and prints success or error messages.
    
    Raises:
        requests.RequestException: If an error occurs during the request.
    """
    try:
        response = requests.get(blacklist_url)
        if response.status_code == 200:
            current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(local_blacklist_path, "w") as blacklist_file:
                blacklist_file.write(f"# Blacklist retrieved on {current_timestamp}\n")
                blacklist_file.write(response.text)
            logging.info("Blacklist retrieved and saved successfully.")
        else:
            logging.error(f"Failed to retrieve blacklist. Status Code: {response.status_code}")
    except requests.RequestException as e:
        logging.error(f"An error occurred while making the request: {str(e)}")

if __name__ == "__main__":
    retrieve_and_save_blacklist()

# Example of scheduling this script to run every 2 hours using cron:
# To set up a cron job to run this script every 2 hours, you can add the following line to your crontab:
# 0 */2 * * * /usr/bin/python /path/to/1_retrieve_blacklist.py
# Replace `/usr/bin/python` with the path to your Python interpreter and `/path/to/1_retrieve_blacklist.py` with the actual path to your script.
# This cron job will run the script at the top of every even-numbered hour (e.g., 2:00 AM, 4:00 AM, 6:00 AM, etc.).