// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Voting {

    struct Voter {
        bool hasVoted;
        address votedFor;
    }

    struct Candidate {
        string name;
        uint voteCount;
    }

    mapping(address => Voter) public voters;
    mapping(address => Candidate) public candidates;
    address[] public candidateAddresses;

    address public owner;
    bool private initialized;

    constructor() {
        owner = msg.sender;
        initialized = false;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function.");
        _;
    }

    function initializeCandidates(address[] memory _candidateAddresses, string[] memory _candidateNames) public onlyOwner {
        require(!initialized, "Already initialized");
        require(_candidateAddresses.length == _candidateNames.length, "Candidate addresses and names arrays must have same length");
        for (uint i = 0; i < _candidateAddresses.length; i++) {
            candidates[_candidateAddresses[i]] = Candidate(_candidateNames[i], 0);
            candidateAddresses.push(_candidateAddresses[i]);
        }
        initialized = true;
    }

    function vote(address candidateAddress) public {
        require(!voters[msg.sender].hasVoted, "You have already voted.");
        require(bytes(candidates[candidateAddress].name).length > 0, "Invalid candidate.");

        voters[msg.sender].hasVoted = true;
        voters[msg.sender].votedFor = candidateAddress;
        candidates[candidateAddress].voteCount++;
    }

    function getCandidateVoteCount(address candidateAddress) public view returns (uint) {
        require(bytes(candidates[candidateAddress].name).length > 0, "Invalid candidate.");
        return candidates[candidateAddress].voteCount;
    }
}