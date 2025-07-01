# Blockchain Voting App Requirements

This document outlines the prerequisites, environment variables, and commands required to deploy the smart contract and run the web application locally using Ganache.

## 1. Prerequisites

Before you begin, ensure you have the following software installed on your system:

*   **Python (3.8+)**: The backend is written in Python. You can download it from [python.org](https://python.org).
*   **pip**: The Python package installer. It usually comes with Python.
*   **Node.js & npm**: Required for installing Ganache. You can download it from [nodejs.org](https://nodejs.org).
*   **Ganache**: A personal Ethereum blockchain for local development. Install it globally via npm:
    ```bash
    npm install -g ganache
    ```
*   **Solidity Compiler (`solc`)**: The `deploy.py` script will attempt to install `solc` for you if it's not found in your system's PATH. However, a manual installation is recommended if the automatic one fails. For macOS with Homebrew, you can use:
    ```bash
    brew install solidity
    ```
    For other operating systems, refer to the [official Solidity installation guide](https://docs.soliditylang.org/en/v0.8.26/installing-solidity.html).

## 2. Environment Variables

The application requires a `.env` file in the project's root directory to store sensitive information and configuration.

**Create a file named `.env` and add the following content:**

```
RPC_URL="http://127.0.0.1:8545"
PRIVATE_KEY="YOUR_GANACHE_ACCOUNT_PRIVATE_KEY"
```

**How to get the values:**

1.  **`RPC_URL`**: This is the network address of your local Ganache blockchain. The default value `http://127.0.0.1:8545` should work if you run Ganache with its standard configuration.
2.  **`PRIVATE_KEY`**: When you start Ganache, it will display a list of generated accounts, each with a corresponding private key. Copy one of these private keys and paste it as the value for `PRIVATE_KEY`. **Do not use the private key from a real-world wallet.**

## 3. Step-by-Step Commands for Deployment

Follow these steps in order from your project's root directory to get the application running.

### Step 1: Start Your Local Blockchain

Use the provided shell script to start Ganache. This will launch a local Ethereum node.

```bash
sh start_ganache.sh
```

**Keep this terminal window open.** Look for the list of accounts and private keys that Ganache prints to the console. You will need one of the private keys for your `.env` file.

### Step 2: Install Python Dependencies

Install all the required Python packages listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Step 3: Deploy the Smart Contract

Run the `deploy.py` script. This script will:
1.  Check for the Solidity compiler (`solc`).
2.  Compile the `Voting.sol` smart contract.
3.  Deploy the contract to your running Ganache instance.
4.  Create a `contract_meta.json` file containing the deployed contract's address and ABI.

```bash
python3 deploy.py
```

After this step, you will have a `contract_meta.json` file in your project directory.

### Step 4: Run the Flask Web Application

Finally, start the Python web server.

```bash
python3 app.py
```

The application will now be running and accessible at `http://localhost:5001`. You can view the interactive API documentation (Swagger UI) by navigating to `http://localhost:5001/apidocs` in your web browser.
