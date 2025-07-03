import requests
import json
import pandas as pd

# Define the base URL for our API
API_BASE_URL = "http://127.0.0.1:5001"

# The assets on our ledger are the candidates. Let's identify their addresses.
CANDIDATE_ALICE = "0x1C947546EdB66A96b51Ab34bf27285cC981f22F4"
CANDIDATE_BOB = "0xe06BAB2cC49Ea6D68170337eb761d3BDedbe7590"

candidates = {
    "Alice": CANDIDATE_ALICE,
    "Bob": CANDIDATE_BOB
}

def get_results():
    results = []
    for name, address in candidates.items():
        response = requests.get(f"{API_BASE_URL}/results/{address}")
        if response.status_code == 200:
            data = response.json()
            # Ensure the data is in the expected format
            if isinstance(data, dict) and "candidate" in data and "votes" in data:
                 results.append({"candidate": data["candidate"], "votes": data["votes"]})
            else:
                print(f"Error: Unexpected response format for {name}: {data}")

        else:
            print(f"Error fetching results for {name}: {response.status_code}")
    return results

def vote_for_candidate(candidate_address):
    headers = {"Content-Type": "application/json"}
    data = {"candidate_address": candidate_address}
    response = requests.post(f"{API_BASE_URL}/vote", headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print(f"Successfully voted for {candidate_address}")
        return response.json()
    else:
        print(f"Failed to vote for {candidate_address}: {response.status_code} {response.text}")
        return None

with open("results.txt", "w") as f:
    f.write("Initial Vote Counts:\n")
    initial_results = get_results()
    df_initial = pd.DataFrame(initial_results)
    f.write(df_initial.to_string(index=False) + "\n\n")

    # Cast votes
    f.write("Casting Votes...\n")
    vote_for_candidate(CANDIDATE_ALICE)
    vote_for_candidate(CANDIDATE_ALICE)
    vote_for_candidate(CANDIDATE_BOB)

    f.write("\nFinal Vote Counts:\n")
    final_results = get_results()
    df_final = pd.DataFrame(final_results)
    f.write(df_final.to_string(index=False) + "\n")

print("Demo script finished. Results are in results.txt")
