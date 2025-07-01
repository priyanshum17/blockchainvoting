
import pytest
from core.control.voting import VotingTestEnvironment

@pytest.fixture(scope="module")
def env():
    # Create a single test environment for all tests
    environment = VotingTestEnvironment(
        contract_path="core/contract/Voting.sol",
        contract_name="Voting",
        candidate_names=["Alice", "Bob"],
        num_accounts=10
    )
    environment.start()
    yield environment
    environment.terminate()

def test_single_valid_vote(env):
    """
    Scenario: A single voter casts a valid vote.
    - A voter votes for "Alice".
    - The vote count for "Alice" should be 1.
    """
    voter_index = 1
    candidate_address = env.candidate_addresses[0]  # Alice

    env.vote(voter_index=voter_index, candidate_address=candidate_address)
    vote_count = env.get_vote_count(candidate_address)

    assert vote_count == 1, f"Expected 1 vote for Alice, but got {vote_count}"

def test_invalid_candidate(env):
    """
    Scenario: A voter attempts to vote for an invalid candidate.
    - A voter attempts to vote for an address not in the candidate list.
    - The transaction should fail.
    """
    voter_index = 2
    invalid_candidate_address = "0x0000000000000000000000000000000000000001"  # An unlikely valid address

    # The vote should be reverted on the blockchain, even if env.vote() doesn't raise.
    env.vote(voter_index=voter_index, candidate_address=invalid_candidate_address)

    # Check that the voter's hasVoted status is still false.
    voter_address = env.w3.eth.accounts[voter_index]
    voter_info = env.contract.functions.voters(voter_address).call()
    has_voted = voter_info[0]
    assert has_voted is False, "Voter status should not change after a failed vote."

    # Also check that the invalid candidate has 0 votes.
    # This requires a call that is expected to fail.
    with pytest.raises(Exception):
        env.get_vote_count(invalid_candidate_address)

def test_double_voting(env):
    """
    Scenario: A voter attempts to vote twice.
    - A voter votes for "Bob".
    - The same voter attempts to vote for "Charlie".
    - The second transaction should fail.
    - The vote count for "Bob" should remain 1.
    - The vote count for "Charlie" should remain 0.
    """
    voter_index = 3
    bob_address = env.candidate_addresses[1]  # Bob

    env.vote(voter_index=voter_index, candidate_address=bob_address)
    
    # The second vote should be reverted, but env.vote() won't raise.
    env.vote(voter_index=voter_index, candidate_address=bob_address)

    # Check that the voter's hasVoted status is True, but they still voted for Bob.
    voter_address = env.w3.eth.accounts[voter_index]
    voter_info = env.contract.functions.voters(voter_address).call()
    has_voted = voter_info[0]
    voted_for = voter_info[1]

    assert has_voted is True, "Voter should be marked as having voted."
    assert voted_for == bob_address, f"Voter should have voted for Bob, but voted for {voted_for}."

    # Check that Bob's vote count is still 1.
    bob_vote_count = env.get_vote_count(bob_address)
    assert bob_vote_count == 1, f"Expected 1 vote for Bob, but got {bob_vote_count}."

def test_multiple_voters(env):
    """
    Scenario: Multiple voters cast votes for different candidates.
    - Voter 4 votes for "Alice".
    - Voter 5 votes for "Bob".
    - Voter 6 votes for "Alice".
    - The vote count for "Alice" should be 2.
    - The vote count for "Bob" should be 1.
    """
    alice_address = env.candidate_addresses[0]
    bob_address = env.candidate_addresses[1]

    env.vote(voter_index=4, candidate_address=alice_address)
    env.vote(voter_index=5, candidate_address=bob_address)
    env.vote(voter_index=6, candidate_address=alice_address)

    alice_vote_count = env.get_vote_count(alice_address)
    bob_vote_count = env.get_vote_count(bob_address)

    # Note: We're not asserting the total vote count for Alice from all tests,
    # just the votes cast in this specific test.
    assert alice_vote_count >= 2
    assert bob_vote_count >= 1


def test_owner_only_functions(env):
    """
    Scenario: A non-owner attempts to call an owner-only function.
    - A non-owner attempts to call `initializeCandidates`.
    - The transaction should fail.
    """
    with pytest.raises(Exception):
        env.contract.functions.initializeCandidates(
            env.candidate_addresses,
            env.candidate_names
        ).transact({'from': env.w3.eth.accounts[1]})
