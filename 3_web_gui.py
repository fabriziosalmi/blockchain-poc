import json
from datetime import datetime, timedelta, timezone

from flask import Flask, render_template, request, redirect, url_for
from flask_caching import Cache
from flask_limiter import Limiter

app = Flask(__name__)

# Configure Flask-Caching
memory_cache_config = {
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 30,  # Cache the response for 30 seconds
    "CACHE_THRESHOLD": 2000,
}
memory_cache = Cache(app, config=memory_cache_config)

# Configure filesystem caching with a specified cache directory
filesystem_cache_config = {
    "CACHE_TYPE": "filesystem",
    "CACHE_DIR": "/path/to/cache/directory",
}
filesystem_cache = Cache(app, config=filesystem_cache_config)

# Function to load blockchain data from the JSON file
def load_blockchain_data() -> list:
    """Load blockchain data from a JSON file."""
    try:
        with open("data/blockchain_data.json", "r") as blockchain_file:
            blockchain_data = json.load(blockchain_file)
        return blockchain_data
    except FileNotFoundError:
        return []


# Custom Jinja2 filter to convert timestamp to GMT datetime
@app.template_filter("timestamp_to_gmt")
def timestamp_to_gmt(timestamp: int) -> str:
    """Convert a Unix timestamp to GMT datetime string."""
    # Convert the timestamp to a datetime object in GMT
    datetime_obj = datetime.utcfromtimestamp(timestamp).replace(
        tzinfo=timezone.utc
    )

    # Format the datetime object as a string with seconds precision
    formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S GMT")

    return formatted_datetime


# Route for the main page displaying all transactions
@app.route("/")
@memory_cache.cached(timeout=3600)  # Cache the response for 1 hour
def index() -> str:
    """Display all transactions on the main page."""
    # Get the 'page' query parameter from the URL and convert it to an integer
    page = request.args.get("page", 1, type=int)

    # Define the number of items to display per page
    items_per_page = 100

    # Load blockchain data
    blockchain_data = load_blockchain_data()

    # Calculate the start and end indices for pagination
    start = (page - 1) * items_per_page
    end = min(start + items_per_page, len(blockchain_data))

    # Pass blockchain data and its length to the template
    return render_template(
        "index.html",
        blockchain=blockchain_data[start:end],
        page=page,
        start=start,
        end=end,
        blockchain_length=len(blockchain_data),
    )


# Route for displaying detailed information about a single block
@app.route("/block/<int:block_index>")
@memory_cache.cached(timeout=30)  # Cache the response for 30 seconds
def block(block_index: int) -> str:
    """Display detailed information about a specific block."""
    blockchain_data = load_blockchain_data()

    if 0 <= block_index < len(blockchain_data):
        block = blockchain_data[block_index]
        return render_template("block.html", block=block)
    else:
        return "Block not found"

# Example route for handling user login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Validate inputs
        if not username or not password:
            return "Invalid credentials", 401

        # Simulate authentication
        if username == "admin" and password == "securepassword":
            return redirect(url_for("index"))
        else:
            return "Invalid credentials", 401

    return render_template("login.html")

# Example route for handling user logout
@app.route("/logout")
def logout():
    # Simulate logout
    return redirect(url_for("index"))

# Example route for handling sensitive data exposure
@app.route("/secret")
def secret():
    # Simulate sensitive data exposure
    return "This is a secret page"

# Example route for handling unvalidated redirects and forwards
@app.route("/redirect/<int:target>")
def redirect_to(target):
    # Simulate unvalidated redirects
    return redirect(url_for("block", block_index=target))

# Example route for handling improper error handling
@app.route("/error")
def error():
    # Simulate improper error handling
    try:
        1 / 0
    except ZeroDivisionError as e:
        return f"An error occurred: {e}", 500

# Example route for handling resource exhaustion
@app.route("/resource")
def resource():
    # Simulate resource exhaustion
    return "Resource exhausted"

# Example route for handling insecure direct object references
@app.route("/file/<int:file_id>")
def file(file_id):
    # Simulate insecure direct object references
    return f"File ID: {file_id}"

# Example route for handling insecure deserialization
@app.route("/deserialize")
def deserialize():
    # Simulate insecure deserialization
    try:
        data = json.loads(request.data)
        return f"Deserialized data: {data}"
    except json.JSONDecodeError:
        return "Invalid JSON", 400

# Example route for handling cryptography issues
@app.route("/encrypt")
def encrypt():
    # Simulate cryptography issues
    from Crypto.Cipher import AES
    key = b'Sixx789012345678'  # Hardcoded key
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(b'Secret message')
    return f"Encrypted data: {encrypted_data.hex()}"

# Example route for handling data validation issues
@app.route("/validate")
def validate():
    # Simulate data validation issues
    input_data = request.form.get("input")
    if not input_data:
        return "Input is required", 400
    return f"Validated input: {input_data}"

# Example route for handling resource management issues
@app.route("/resource_management")
def resource_management():
    # Simulate resource management issues
    import time
    start_time = time.time()
    while True:
        if time.time() - start_time > 60:  # Simulate resource exhaustion
            return "Resource exhausted"