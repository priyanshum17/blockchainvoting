import json
import os
from web3 import Web3
from dotenv import load_dotenv

class VoteService:
    def __init__(self, credentials_path: str):
        load_dotenv()
        self.w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
        manager = GanacheManager(output_file=credentials_path)
        manager = GanacheManager(output_file=credentials_path)
        manager = GanacheManager(output_file=credentials_path)
        self.credentials = manager.extract_credentials()
        self.private_key = self.credentials.private_keys[0]
        self.account = self.w3.eth.account.from_key(self.private_key)
        self.w3.eth.default_account = self.account.address
        self.contract = self._get_contract()

    def _get_contract(self):
        with open("contract_meta.json", "r") as f:
            meta = json.load(f)
        return self.w3.eth.contract(address=meta["contractAddress"], abi=meta["abi"])

    def vote(self, candidate_address):
        transaction = self.contract.functions.vote(candidate_address).transact({"from": self.w3.eth.default_account})
        receipt = self.w3.eth.wait_for_transaction_receipt(transaction)
        return receipt

    def get_candidate_vote_count(self, candidate_address):
        return self.contract.functions.getCandidateVoteCount(candidate_address).call()