# voting.py  ────────────────────────────────────────────────────────────────
import os
import json
from time import sleep
from typing import List

from web3 import Web3
from web3.exceptions import (
    BadFunctionCallOutput,
    ContractLogicError,        # ← import fixed
)

from core.control.compiler import ContractCompiler
from core.config.credentials import GanacheManager, GanacheCredentials


class VotingTestEnvironment:
    def __init__(
        self,
        contract_path: str,
        contract_name: str,
        candidate_names: List[str],
        num_accounts: int = 5,
        rpc_url: str = "http://127.0.0.1:8545",
    ):
        self.contract_path = contract_path
        self.contract_name = contract_name
        self.candidate_names = candidate_names
        self.num_accounts = num_accounts
        self.rpc_url = rpc_url

        # will be set in start()
        self.manager: GanacheManager | None = None
        self.creds: GanacheCredentials | None = None
        self.w3: Web3 | None = None
        self.account = None
        self.private_key = None
        self.contract = None
        self.contract_address = None
        self.candidate_addresses: list[str] = []

    # ──────────────────────────────────────────────────────────────────
    #  START  (ganache → compile → deploy)
    # ──────────────────────────────────────────────────────────────────
    def start(self):
        self.manager = GanacheManager(output_file="cred/ganache_output.txt")
        self.creds = self.manager.extract_credentials()
        

        # 4) connect to node
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        assert self.w3.is_connected(), "Web3 could not connect to Ganache"

        

        print("\n✅ Available accounts:")
        for i, addr in enumerate(self.creds.accounts):
            print(f"({i}) {addr}")

        # 2) choose two candidates
        # Ensure we have enough accounts before selecting
        if len(self.creds.accounts) < 3:
            raise ValueError("Not enough Ganache accounts available for candidates and deployer.")

        self.candidate_addresses = [
            self.w3.to_checksum_address(self.creds.accounts[1]),
            self.w3.to_checksum_address(self.creds.accounts[2]),
        ]
        print("\n✅ Selected candidates:")
        for addr, name in zip(self.candidate_addresses, self.candidate_names):
            print(f"- {name}: {addr}")
        print(f"🔧 DEBUG: candidate_addresses before constructor: {self.candidate_addresses}")
        print(f"🔧 DEBUG: candidate_names before constructor: {self.candidate_names}")
        print(f"🔧 DEBUG: len(candidate_addresses)={len(self.candidate_addresses)}, len(candidate_names)={len(self.candidate_names)}")

        # 3) compile
        artifact = ContractCompiler(
            contract_path=self.contract_path,
            contract_name=self.contract_name,
            abi_output="cred/MyContract.abi.json",
            bin_output="cred/MyContract.bytecode.txt",
        ).compile()

        # deployer = account[0]
        self.private_key = self.creds.private_keys[0]
        self.account = self.w3.eth.account.from_key(self.private_key)
        print("\n✅ Using deployer account:", self.account.address)

        # 5) Deploy contract
        contract_obj = self.w3.eth.contract(
            abi=artifact.abi,
            bytecode=artifact.bytecode
        )

        try:
            # Let web3.py handle gas estimation and transaction sending
            tx_hash = contract_obj.constructor().transact({'from': self.account.address})

            print(f"\n⏳ Deploying contract… tx: {tx_hash.hex()}")
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

            # Check receipt status
            if receipt['status'] == 0:
                print("🚨 Transaction reverted.")
                raise RuntimeError("Deployment failed: transaction reverted.")

            self.contract_address = receipt.contractAddress
            print(f"✅ Contract deployed at: {self.contract_address}")
            print(f"   Gas used: {receipt.gasUsed}")

            # Initialize candidates after deployment
            self.contract = self.w3.eth.contract(
                address=self.contract_address,
                abi=artifact.abi,
            )
            init_tx_hash = self.contract.functions.initializeCandidates(
                self.candidate_addresses,
                self.candidate_names
            ).transact({'from': self.account.address})
            print(f"\n⏳ Initializing candidates… tx: {init_tx_hash.hex()}")
            init_receipt = self.w3.eth.wait_for_transaction_receipt(init_tx_hash)
            if init_receipt['status'] == 0:
                print("🚨 Candidate initialization reverted.")
                raise RuntimeError("Candidate initialization failed.")
            print("✅ Candidates initialized successfully.")

            with open("contract_meta.json", "w") as f:
                json.dump({
                    "contractAddress": self.contract_address,
                    "abi": artifact.abi
                }, f)

        except Exception as e:
            print(f"🚨 Contract deployment failed: {e}")
            # It's good practice to re-raise or handle the exception properly
            raise

        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=artifact.abi,
        )


    # ──────────────────────────────────────────────────────────────────
    #  vote()
    # ──────────────────────────────────────────────────────────────────
    def vote(self, voter_index: int, candidate_address: str):
        pk   = self.creds.private_keys[voter_index]          # type: ignore
        acct = self.w3.eth.account.from_key(pk)              # type: ignore

        tx = self.contract.functions.vote(candidate_address).build_transaction(
            {
                "from": acct.address,
                "nonce": self.w3.eth.get_transaction_count(acct.address),  # type: ignore
                "gas": 200_000,
                "gasPrice": self.w3.to_wei("1", "gwei"),                   # type: ignore
            }
        )
        signed = self.w3.eth.account.sign_transaction(tx, pk)             # type: ignore
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction) # type: ignore
        self.w3.eth.wait_for_transaction_receipt(tx_hash)                 # type: ignore
        print(f"✅ {acct.address} voted (tx {tx_hash.hex()})")

    # ──────────────────────────────────────────────────────────────────
    #  get_vote_count()
    # ──────────────────────────────────────────────────────────────────
    def get_vote_count(self, candidate_address: str) -> int:
        # tiny retry loop – Ganache sometimes returns 0x for a split second
        for _ in range(3):
            if len(self.w3.eth.get_code(self.contract_address)):           # type: ignore
                break
            sleep(0.2)
        else:
            raise RuntimeError("🚨 Contract byte-code missing; Ganache reset?")

        try:
            votes = self.contract.functions.getCandidateVoteCount(
                candidate_address
            ).call()
            print(f"🔍 {candidate_address} ⇒ {votes} votes")
            return votes
        except BadFunctionCallOutput as err:
            raise RuntimeError("🚨 view call failed – bad ABI / address") from err

    # ──────────────────────────────────────────────────────────────────
    #  terminate()
    # ──────────────────────────────────────────────────────────────────
    def terminate(self):
        if self.manager:
            self.manager.terminate_process()