# Blockchain Voting Application

This project is a simple, decentralized voting application built on the Ethereum blockchain. It demonstrates the core principles of smart contract development, deployment, and interaction through a web API.

## Features

- **Decentralized Voting:** All votes are recorded on an Ethereum-based blockchain, ensuring transparency and immutability.
- **Smart Contract:** A Solidity-based smart contract governs the voting logic, including candidate registration and vote tallying.
- **RESTful API:** A Flask-based API provides a user-friendly interface for casting votes and viewing results without requiring direct blockchain interaction.
- **Automated Testing:** A comprehensive test suite using `pytest` ensures the reliability and correctness of the smart contract and its interactions.

## Technology Stack

- **Blockchain:** Solidity, Ethereum
- **Backend:** Python, Flask
- **Blockchain Interaction:** Web3.py
- **Local Development:** Ganache, `solc-x`

## Getting Started

### Prerequisites

- **Node.js & npm:** Required for Ganache.
- **Python 3.10+:** With `pip` for package management.
- **Solidity Compiler (`solc`):** The project uses `solc-x` which is installed via `pip`, but a system-wide installation can be helpful.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd blockchain-voting-app
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Ganache:**
    ```bash
    npm install -g ganache-cli
    ```

### Running the Application

1.  **Start Ganache:**
    Open a new terminal and run:
    ```bash
    ganache-cli
    ```
    This will start a local Ethereum blockchain instance.

2.  **Deploy the Contract:**
    In another terminal, run the following command to compile and deploy the `Voting.sol` contract to your local Ganache instance. This script also creates the `contract_meta.json` file needed by the API.
    ```bash
    python3 test1.py
    ```
    Take note of the candidate addresses printed in the output.

3.  **Run the Flask API:**
    ```bash
    python3 app.py
    ```
    The API server will start on `http://127.0.0.1:5001`.

## Project Structure

```
/
├── core/               # Core application logic
│   ├── contract/       # Solidity smart contract
│   └── control/        # Python scripts for control and interaction
├── cred/               # Compiled contract artifacts and credentials
├── docs/               # Project documentation
├── test/               # Pytest test files
├── app.py              # Flask API application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```
---