import json
from flask import Flask, render_template, request
from flask_limiter import Limiter
from flask_caching import Cache
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

# Configure Flask-Caching
memory_cache_config = {'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 300, 'CACHE_THRESHOLD': 2000}
memory_cache = Cache(app, config=memory_cache_config)

# Configure filesystem caching with a specified cache directory
filesystem_cache_config = {'CACHE_TYPE': 'filesystem', 'CACHE_DIR': '/path/to/cache/directory'}
filesystem_cache = Cache(app, config=filesystem_cache_config)

# Function to load blockchain data from the JSON file
def load_blockchain_data():
    try:
        with open("data/blockchain_data.json", "r") as blockchain_file:
            blockchain_data = json.load(blockchain_file)
        return blockchain_data
    except FileNotFoundError:
        return []

# Custom Jinja2 filter to convert timestamp to GMT datetime
@app.template_filter("timestamp_to_gmt")
def timestamp_to_gmt(timestamp):
    # Convert the timestamp to a datetime object in GMT
    datetime_obj = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)

    # Format the datetime object as a string with seconds precision
    formatted_datetime = datetime_obj.strftime('%Y-%m-%d %H:%M:%S GMT')

    return formatted_datetime

# Route for the main page displaying all transactions
@app.route("/")
@memory_cache.cached(timeout=3600)  # Cache the response for 1 hour (adjust as needed)
def index():
    # Get the 'page' query parameter from the URL and convert it to an integer
    page = int(request.args.get("page", 1))

    # Define the number of items to display per page
    items_per_page = 100  # Adjust as needed

    # Load blockchain data
    blockchain_data = load_blockchain_data()

    # Calculate the start and end indices for pagination
    start = (page - 1) * items_per_page
    end = start + items_per_page

    # Pass blockchain data and its length to the template
    return render_template("index.html", blockchain=blockchain_data[start:end], page=page, start=start, end=end, blockchain_length=len(blockchain_data))

# Route for displaying detailed information about a single block
@app.route("/block/<int:block_index>")
@memory_cache.cached(timeout=30)  # Cache the response for 30 seconds (antiflood)
def block(block_index):
    blockchain_data = load_blockchain_data()

    if block_index >= 0 and block_index < len(blockchain_data):
        block = blockchain_data[block_index]
        return render_template("block.html", block=block)
    else:
        return "Block not found"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
