# Domains Blacklists on the Blockchain

## Description

This project, **Domains Blacklists on the Blockchain**, leverages blockchain technology to create a transparent and verifiable system for managing and accessing domain blacklists. Instead of relying on centralized databases, we use a blockchain to record and validate blacklisted domains, enhancing security, integrity, and trust.

The project includes scripts for retrieving domain blacklists from various sources, processing them, creating blockchain transactions for each domain, and providing a user-friendly web interface to explore the blacklisted domains and their associated blockchain records.

## Features

*   **Decentralized Blacklist:** Uses blockchain technology to store and manage domain blacklists, eliminating single points of failure and enhancing security.
*   **Transparency and Verifiability:** All blacklist additions and changes are recorded on the blockchain, providing an immutable and auditable history.
*   **Web Interface:** Provides an easy-to-use web interface to search, view, and explore the blacklisted domains and their corresponding blockchain transactions.
*   **Automated Retrieval and Processing:** Scripts automate the process of retrieving, processing, and adding new domains to the blockchain blacklist.
*   **Multiple Blacklist Sources:** Can be configured to fetch blacklists from various reputable sources.

## Table of Contents

*   [Installation](#installation)
    *   [Prerequisites](#prerequisites)
    *   [Installation Steps](#installation-steps)
*   [Usage](#usage)
*   [Contributing](#contributing)
*   [License](#license)
*   [Acknowledgements](#acknowledgements)

## Installation

### Prerequisites

*   Python 3.7+ (Recommended to use a virtual environment)
*   Flask
*   `tldextract`
*   Other dependencies listed in `requirements.txt`

### Installation Steps

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/fabriziosalmi/blockchain-poc.git
    ```

2.  **Navigate to the project directory:**

    ```sh
    cd blockchain-poc
    ```

3.  **(Recommended) Create a virtual environment:**

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

4.  **Install the required dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the scripts in the following order:**

    *   `1_retrieve_blacklist.py`: Retrieves the blacklist data from specified sources.
    *   `2_process_blacklist.py`: Processes the retrieved data and creates blockchain transactions for each domain.
    *   `3_web_gui.py`: Starts the Flask web interface.

    ```sh
    python 1_retrieve_blacklist.py
    python 2_process_blacklist.py
    python 3_web_gui.py
    ```

2.  **Access the web interface:** Open a web browser and navigate to `http://localhost:5000` to access the web interface and explore the blacklisted domains.

## Contributing

Contributions are welcome! Whether you're fixing a bug, adding a new feature, or improving the documentation, your help is greatly appreciated.

Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for detailed guidelines on how to contribute to this project, including coding standards, pull request process, and more.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Acknowledgements

This project relies on the following open-source libraries and resources:

*   [Flask](https://flask.palletsprojects.com/): For creating the web interface.
*   [tldextract](https://pypi.org/project/tldextract/): For reliably separating the TLD, domain and subdomains from a URL.
*   [Requests](https://pypi.org/project/requests/): For making HTTP requests to retrieve blacklist data.
*   [Other Open-Source Libraries (check requirements.txt)](#): Thanks to all the contributors of the libraries used in this project!
