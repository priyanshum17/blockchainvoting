# System Architecture

This document outlines the architecture of the Blockchain Voting Application, detailing the components and their interactions.

## Overview

The application is composed of three main layers:

1.  **Smart Contract (Blockchain Layer):** The core logic of the voting system, deployed on an Ethereum-compatible blockchain.
2.  **API Server (Backend Layer):** A Python Flask application that acts as a bridge between users and the blockchain.
3.  **Testing Environment (Development Layer):** A suite of tools and scripts for automated testing and deployment.

## Component Breakdown

### 1. Smart Contract (`Voting.sol`)

- **Language:** Solidity
- **Location:** `core/contract/Voting.sol`

This is the heart of the application. It is an Ethereum smart contract that defines the rules of the voting process.

- **Key Functions:**
  - `initializeCandidates()`: An owner-only function to register the candidates for the election.
  - `vote()`: Allows any user (address) to cast a single vote for a registered candidate.
  - `getCandidateVoteCount()`: A public view function to retrieve the current vote count for a candidate.

- **State Variables:**
  - `voters`: A mapping to track which addresses have already voted.
  - `candidates`: A mapping to store information about each candidate, including their name and vote count.
  - `candidateAddresses`: An array of the addresses of all registered candidates.

### 2. API Server (`app.py`)

- **Framework:** Flask
- **Location:** `app.py`

This server provides a standard RESTful API that allows users to interact with the smart contract without needing to understand the complexities of blockchain technology.

- **Endpoints:**
  - `POST /vote`: Receives a vote from a user and translates it into a transaction on the blockchain by calling the `vote()` function of the smart contract.
  - `GET /results/<candidate_address>`: Queries the smart contract for the vote count of a specific candidate and returns it to the user.

- **Interaction with Blockchain:** The API uses the `Web3.py` library to communicate with the Ethereum blockchain. It reads the contract's address and ABI from the `contract_meta.json` file to know how to interact with the deployed smart contract.

### 3. Control and Deployment Scripts (`core/control/`)

This directory contains the Python scripts responsible for managing the lifecycle of the smart contract and the testing environment.

- **`voting.py`:** Defines the `VotingTestEnvironment` class, which automates the process of:
  1.  Starting a local Ganache blockchain instance.
  2.  Compiling the `Voting.sol` smart contract.
  3.  Deploying the compiled contract to the Ganache instance.
  4.  Initializing the candidates.

- **`service.py`:** Defines the `VoteService` class, which is used by the Flask API to abstract the details of interacting with the smart contract.

- **`compiler.py`:** A utility for compiling Solidity smart contracts using the `solc-x` library.

### 4. Testing (`test/`)

- **Framework:** `pytest`
- **Location:** `test/test_voting_scenarios.py`

The test suite provides comprehensive, automated testing for the smart contract's logic. It uses the `VotingTestEnvironment` to create a fresh, isolated environment for each test run, ensuring that tests are reliable and repeatable.

## Workflow Diagram

```
+-----------------+      +-----------------+      +----------------------+
|      User       |----->|   Flask API     |----->|  Voting Smart        |
| (e.g., via curl)|      |  (app.py)       |      |  Contract (on        |
+-----------------+      +-----------------+      |  Ganache/Ethereum)   |
                         | - /vote         |      +----------------------+
                         | - /results      |               ^
                         +-----------------+               |
                                 |                         |
                                 v                         |
                         +-----------------+               |
                         |  VoteService    |---------------+ 
                         | (service.py)    |
                         +-----------------+
```
