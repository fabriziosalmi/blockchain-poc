import requests
import datetime
import os

# Define the URL to retrieve the blacklist from
blacklist_url = "https://get.domainsblacklists.com/blacklist.txt"

# Define the local file path to save the retrieved blacklist
local_blacklist_path = "data/blacklist.txt"

# Function to retrieve and save the blacklist
def retrieve_and_save_blacklist():
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(blacklist_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Get the current timestamp
            current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save the blacklist to the local file with timestamp
            with open(local_blacklist_path, "w") as blacklist_file:
                blacklist_file.write(f"# Blacklist retrieved on {current_timestamp}\n")
                blacklist_file.write(response.text)

            print("Blacklist retrieved and saved successfully.")

        else:
            print(f"Failed to retrieve blacklist. Status Code: {response.status_code}")

    except requests.RequestException as e:
        print(f"An error occurred while making the request: {str(e)}")

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    retrieve_and_save_blacklist()

# Example of scheduling this script to run every 2 hours using cron:
# To set up a cron job to run this script every 2 hours, you can add the following line to your crontab:
# 0 */2 * * * /usr/bin/python /path/to/1_retrieve_blacklist.py
# Replace `/usr/bin/python` with the path to your Python interpreter and `/path/to/1_retrieve_blacklist.py` with the actual path to your script.
# This cron job will run the script at the top of every even-numbered hour (e.g., 2:00 AM, 4:00 AM, 6:00 AM, etc.).
