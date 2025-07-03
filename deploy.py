from core.control.voting import VotingTestEnvironment

# Create test environment
env = VotingTestEnvironment(
    contract_path="core/contract/Voting.sol",
    contract_name="Voting",
    candidate_names=["Alice", "Bob"],
    num_accounts=5
)

# Start environment (Ganache + compile + deploy)
env.start()
env.manager.is_process_alive()
# Simulate voting
env.vote(voter_index=1, candidate_address=env.candidate_addresses[0])
env.manager.is_process_alive()
env.vote(voter_index=2, candidate_address=env.candidate_addresses[1])
env.manager.is_process_alive()
env.vote(voter_index=3, candidate_address=env.candidate_addresses[0])
env.manager.is_process_alive()
# Query results
env.get_vote_count(env.candidate_addresses[0])
env.manager.is_process_alive()

env.get_vote_count(env.candidate_addresses[1])
env.manager.is_process_alive()


# Terminate Ganache
# env.terminate()
