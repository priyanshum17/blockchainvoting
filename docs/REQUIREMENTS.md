# Blockchain Voting App Requirements

This document provides a comprehensive guide to the prerequisites, environment configuration, and step-by-step commands required to set up and run the Blockchain Voting Application locally using Ganache.

## 1. Prerequisites

Before proceeding, ensure that your system meets the following software requirements. Detailed installation instructions are provided for each.

*   **Python (3.8+)**: The backend of this application is developed in Python. Download the latest stable version from the official [Python website](https://www.python.org/downloads/).
*   **pip**: The standard package installer for Python. `pip` is typically included with Python installations (version 3.4 and later). You can verify its installation by running `pip --version` in your terminal.
*   **Node.js & npm**: These are essential for installing and managing Ganache. Download the recommended version from the official [Node.js website](https://nodejs.org/en/download/). `npm` (Node Package Manager) is bundled with Node.js.
*   **Ganache**: A personal Ethereum blockchain for local development and testing. Install it globally using `npm`:
    ```bash
    npm install -g ganache-cli
    ```
    *Note: `ganache-cli` is the command-line version, suitable for scripting and automated environments.*
*   **Solidity Compiler (`solc`)**: The `deploy.py` script is designed to automatically install a compatible version of `solc` if it's not found in your system's PATH. However, for manual installation or troubleshooting, refer to the [official Solidity installation guide](https://docs.soliditylang.org/en/latest/installing-solidity.html). For macOS users with Homebrew, you can install it via:
    ```bash
    brew install solidity
    ```

## 2. Environment Variables Configuration

The application relies on a `.env` file to manage sensitive information and configuration parameters securely. This file should be located in the project's root directory.

**To configure, create a file named `.env` in the root of your project and add the following content:**

```dotenv
RPC_URL="http://127.0.0.1:8545"
PRIVATE_KEY="YOUR_GANACHE_ACCOUNT_PRIVATE_KEY"
```

**How to Obtain the Values:**

1.  **`RPC_URL`**: This variable specifies the network address of your local Ganache blockchain. The default value `http://127.0.0.1:8545` is standard for Ganache and should work without modification unless you've configured Ganache to run on a different port.
2.  **`PRIVATE_KEY`**: When you start `ganache-cli`, it will display a list of generated Ethereum accounts, each accompanied by its private key. **It is crucial to copy one of these private keys and paste it as the value for `PRIVATE_KEY` in your `.env` file.**
    *   **Security Warning:** Never use private keys from real-world wallets (e.g., MetaMask, hardware wallets) in your development environment. The private keys provided by Ganache are for local testing only.

## 3. Step-by-Step Deployment and Application Startup

Follow these instructions sequentially from your project's root directory to deploy the smart contract and launch the web application.

### Step 1: Start Your Local Blockchain (Ganache)

Open a new terminal window and execute the following command to start your personal Ethereum blockchain:

```bash
ganache-cli
```

*   **Important:** Keep this terminal window open throughout the entire process. Observe the output for the list of generated accounts and their private keys. You will need one of these private keys for the `.env` file as described in Section 2.

### Step 2: Install Python Dependencies

Navigate to your project's root directory in a *separate* terminal window and install all required Python packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 3: Deploy the Smart Contract

In the same terminal window used for installing Python dependencies, run the deployment script. This script automates several critical tasks:

```bash
python3 deploy.py
```

This script will:
1.  Verify and, if necessary, install the Solidity compiler (`solc`).
2.  Compile the `Voting.sol` smart contract.
3.  Deploy the compiled contract to your running Ganache instance.
4.  Generate a `contract_meta.json` file in your project directory. This file contains the deployed contract's address and Application Binary Interface (ABI), which are essential for the Flask API to interact with the contract.

### Step 4: Run the Flask Web Application

Finally, in a *third* terminal window, start the Python Flask web server:

```bash
python3 app.py
```

The application will now be running and accessible via your web browser at `http://localhost:5001`. For interactive API documentation (Swagger UI), navigate to `http://localhost:5001/apidocs`.
