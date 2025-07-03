# API Usage Guide

This document provides a detailed guide on how to interact with the Blockchain Voting Application's RESTful API. The API serves as the primary interface for users to cast votes and retrieve real-time voting results from the Ethereum blockchain.

## Base URL

All API endpoints are accessible via the following base URL when running the application locally:

`http://127.0.0.1:5001`

## API Endpoints

### 1. Cast a Vote for a Candidate

This endpoint allows an authenticated user to submit a vote for a specific candidate. The vote is recorded as a transaction on the deployed `Voting` smart contract, ensuring immutability and transparency.

*   **URL:** `/vote`
*   **Method:** `POST`
*   **Headers:**
    *   `Content-Type: application/json`
*   **Request Body (JSON):**
    ```json
    {
      "candidate_id": <INTEGER_CANDIDATE_ID>
    }
    ```
    *   **`candidate_id`** (integer, required): The unique numerical ID of the candidate you wish to vote for. These IDs are assigned during the contract deployment and candidate initialization process.

*   **Success Response (HTTP 200 OK):**
    ```json
    {
      "status": "success",
      "message": "Vote cast successfully",
      "transaction_hash": "0x...",
      "receipt": { /* ... transaction receipt details ... */ }
    }
    ```
    *   `status`: Indicates the success of the operation.
    *   `message`: A descriptive message confirming the vote.
    *   `transaction_hash`: The unique hash of the blockchain transaction that recorded the vote. You can use this hash to track the transaction on a blockchain explorer.
    *   `receipt`: A comprehensive object containing detailed information about the mined transaction on the blockchain (e.g., gas used, block number).

*   **Error Response (HTTP 400 Bad Request / 500 Internal Server Error):**
    ```json
    {
      "status": "error",
      "message": "<Error Description>"
    }
    ```
    Possible errors include invalid `candidate_id`, voting outside the active period, or attempting to vote multiple times from the same address.

*   **Example (`curl`):**
    To cast a vote for candidate with ID `0` (e.g., Alice):
    ```bash
    curl -X POST -H "Content-Type: application/json" \
    -d '{"candidate_id": 0}' \
    http://127.0.0.1:5001/vote
    ```

### 2. Retrieve Current Vote Counts

This endpoint allows anyone to query the current vote counts for all registered candidates directly from the smart contract. This is a read-only operation and does not require a blockchain transaction.

*   **URL:** `/results`
*   **Method:** `GET`
*   **Parameters:** None

*   **Success Response (HTTP 200 OK):**
    ```json
    {
      "status": "success",
      "results": [
        {
          "id": 0,
          "name": "Alice",
          "vote_count": 5
        },
        {
          "id": 1,
          "name": "Bob",
          "vote_count": 3
        }
      ]
    }
    ```
    *   `status`: Indicates the success of the operation.
    *   `results`: An array of objects, each representing a candidate with their `id`, `name`, and current `vote_count`.

*   **Example (`curl`):**
    ```bash
    curl http://127.0.0.1:5001/results
    ```

## Understanding Candidate IDs

Candidate IDs are numerical identifiers assigned during the smart contract deployment and initialization phase. When you run the `deploy.py` script, it will output the selected candidates along with their corresponding IDs. It is crucial to use these specific IDs when interacting with the `/vote` endpoint.

**Example output from `deploy.py` (illustrative):**

```
✅ Selected candidates:
- Candidate: Alice, ID: 0
- Candidate: Bob, ID: 1
- Candidate: Charlie, ID: 2
```

Always refer to the output of your `deploy.py` script to get the correct candidate IDs for your local deployment.
