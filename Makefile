CONDA_ENV_NAME = voting
PYTHON = python
PIP = pip

.PHONY: all setup clean test run deploy

all: setup test run

setup:
	@echo "Setting up Conda environment and installing dependencies..."
	conda create -n $(CONDA_ENV_NAME) python=3.10 -y || echo "Conda environment already exists or creation failed. Proceeding..."
	conda run -n $(CONDA_ENV_NAME) $(PIP) install -r requirements.txt
	@echo "Setup complete. Activate the environment using 'conda activate $(CONDA_ENV_NAME)'"

clean:
	@echo "Cleaning up..."
	rm -rf venv
	rm -rf .pytest_cache
	# .env file is intentionally NOT removed here. Please manage it manually.
	rm -f contract_address.txt
	rm -f voting_abi.json
	conda env remove -n $(CONDA_ENV_NAME) -y
	@echo "Cleanup complete."

test:
	@echo "Running tests..."
	conda run -n $(CONDA_ENV_NAME) $(PYTHON) -m pytest test/test_service.py

run:
	@echo "Starting Flask application..."
	@echo "Ensure Ganache CLI is running in a separate terminal."
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found. Please create it with ETH_PRIVATE_KEY."; \
		exit 1; \
	fi
	conda run -n $(CONDA_ENV_NAME) $(PYTHON) app.py

deploy:
	@echo "Deploying smart contract..."
	@echo "Ensure Ganache CLI is running in a separate terminal."
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found. Please create it with ETH_PRIVATE_KEY."; \
		exit 1; \
	fi
	conda run -n $(CONDA_ENV_NAME) $(PYTHON) deploy.py