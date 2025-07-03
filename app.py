from flask import Flask, request, jsonify
from flasgger import Swagger
from dotenv import load_dotenv

from core.control.service import VoteService

load_dotenv()

app = Flask(__name__)
swagger = Swagger(app)

vote_service = VoteService(credentials_path="cred/ganache_output.txt")

@app.route("/vote", methods=["POST"])
def vote():
    """
    Vote for a candidate
    ---
    tags:
      - Voting
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - candidate_address
          properties:
            candidate_address:
              type: string
              description: Address of the candidate to vote for
    responses:
      200:
        description: Vote receipt
        schema:
          type: object
          properties:
            status:
              type: string
            receipt:
              type: string
    """
    data = request.get_json()
    candidate_address = data["candidate_address"]
    receipt = vote_service.vote(candidate_address)
    return jsonify({"status": "success", "receipt": str(receipt)})

@app.route("/results/<candidate_address>", methods=["GET"])
def get_results(candidate_address):
    """
    Get vote count for a candidate
    ---
    tags:
      - Voting
    parameters:
      - name: candidate_address
        in: path
        type: string
        required: true
        description: Address of the candidate
    responses:
      200:
        description: Vote count
        schema:
          type: object
          properties:
            candidate:
              type: string
            vote_count:
              type: integer
    """
    count = vote_service.get_candidate_vote_count(candidate_address)
    vote_count = vote_service.get_candidate_vote_count(candidate_address)
    return jsonify({"candidate": candidate_address, "votes": count})

if __name__ == "__main__":
    app.run(debug=True, port=5001)