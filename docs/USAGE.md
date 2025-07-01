# API Usage

This document provides detailed instructions on how to interact with the Blockchain Voting API.

## Base URL

The API is served from `http://127.0.0.1:5001` by default.

## Endpoints

### 1. Vote for a Candidate

This endpoint allows a user to cast a vote for a specific candidate. The vote is sent as a transaction to the deployed `Voting` smart contract.

- **URL:** `/vote`
- **Method:** `POST`
- **Headers:**
  - `Content-Type: application/json`
- **Body:**
  ```json
  {
    "candidate_address": "<CANDIDATE_ETHEREUM_ADDRESS>"
  }
  ```
- **Parameters:**
  - `candidate_address` (string, required): The Ethereum address of the candidate to vote for.

- **Success Response (200 OK):**
  ```json
  {
    "status": "success",
    "receipt": "<TRANSACTION_RECEIPT_OBJECT>"
  }
  ```
  The `receipt` object contains detailed information about the transaction that was mined on the blockchain.

- **Example (`curl`):**
  ```bash
  curl -X POST -H "Content-Type: application/json" \
  -d '{"candidate_address": "0x73F830209917126FCDB8968F44bd3239f655817A"}' \
  http://127.0.0.1:5001/vote
  ```

### 2. Get Vote Count for a Candidate

This endpoint retrieves the current vote count for a specific candidate from the smart contract.

- **URL:** `/results/<candidate_address>`
- **Method:** `GET`
- **Parameters:**
  - `candidate_address` (string, required, in URL path): The Ethereum address of the candidate.

- **Success Response (200 OK):**
  ```json
  {
    "candidate": "<CANDIDATE_ETHEREUM_ADDRESS>",
    "vote_count": <INTEGER_VOTE_COUNT>
  }
  ```

- **Example (`curl`):**
  ```bash
  curl http://127.0.0.1:5001/results/0x73F830209917126FCDB8968F44bd3239f655817A
  ```

## Finding Candidate Addresses

The addresses for the candidates are determined during the contract deployment process. When you run `python3 test1.py`, the script will output the selected candidates and their corresponding Ethereum addresses. You must use these addresses when interacting with the API.

Example output from `test1.py`:

```
✅ Selected candidates:
- Alice: 0x73F830209917126FCDB8968F44bd3239f655817A
- Bob: 0x01b7182845f99ed8b66fF275491cc3718D812a3d
```
