# Domains Blacklists Blockchain

## Description
Domains Blacklists Blockchain is a project aimed at retrieving, processing, and displaying domain blacklists using blockchain technology. It provides a web interface for users to view detailed information about blacklisted domains and offers enhanced security and integrity through blockchain.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation
### Prerequisites
- Python 3.x
- Flask
- Other dependencies listed in `requirements.txt`

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/fabriziosalmi/domains-blacklists-blockchain.git
   ```
2. Navigate to the project directory:
   ```sh
   cd domains-blacklists-blockchain
   ```
3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
1. Run the scripts in the following order:
   - `1_retrieve_blacklist.py` to retrieve the blacklist.
   - `2_process_blacklist.py` to process the blacklist and create transactions.
   - `3_web_gui.py` to start the web interface.

2. Open a web browser and navigate to `http://localhost:5000` to access the web interface.

## Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated. Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Contact
- Fabrizio Salmi - [Github Profile](https://github.com/fabriziosalmi)
- Project Link: [https://github.com/fabriziosalmi/domains-blacklists-blockchain](https://github.com/fabriziosalmi/domains-blacklists-blockchain)

## Acknowledgements
- [Flask](https://flask.palletsprojects.com/)
- [tldextract](https://pypi.org/project/tldextract/)
- [Other Libraries](#)
