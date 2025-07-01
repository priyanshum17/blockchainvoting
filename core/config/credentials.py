import subprocess
import time
import re
import os
from typing import List, Optional, IO
from pydantic import BaseModel


class GanacheCredentials(BaseModel):
    accounts: List[str]
    private_keys: List[str]


class GanacheManager:
    def __init__(
        self,
        num_accounts: int = 10,
        output_file: str = "output.txt",
        wait_seconds: int = 5
    ):
        self.num_accounts = num_accounts
        self.output_file = output_file
        self.wait_seconds = wait_seconds
        self.process: Optional[subprocess.Popen] = None
        self.output_handle: Optional[IO] = None
        self.credentials: Optional[GanacheCredentials] = None

    def start_ganache(self):
        """
        Starts ganache-cli and writes output to a file.
        """
        print(f"Starting ganache-cli with {self.num_accounts} accounts...")
        self.output_handle = open(self.output_file, "w")
        self.process = subprocess.Popen(
            ["ganache-cli", "--accounts", str(self.num_accounts)],
            stdout=self.output_handle,
            stderr=subprocess.STDOUT
        )
        print("Ganache process started.")

    def extract_credentials(self) -> GanacheCredentials:
        """
        Waits, extracts credentials, and deletes output file.
        Note: Does not terminate the process automatically anymore.
        """
        print(f"Waiting {self.wait_seconds} seconds for Ganache output...")
        time.sleep(self.wait_seconds)

        if self.output_handle:
            self.output_handle.close()

        with open(self.output_file, "r") as f:
            content = f.read()
        print(content)

        account_pattern = re.compile(r"\(\d+\)\s*(0x[a-fA-F0-9]{40})\s*")
        accounts = [acc.strip() for acc in account_pattern.findall(content)]
        accounts.sort(key=lambda x: content.find(x)) # Sort by appearance in content

        privkey_pattern = re.compile(r"\(\d+\)\s(0x[a-fA-F0-9]{64})")
        private_keys = privkey_pattern.findall(content)
        private_keys.sort(key=lambda x: content.find(x)) # Sort by appearance in content

        if not accounts or not private_keys:
            raise ValueError("Could not extract accounts or private keys. Check Ganache output.")

        creds = GanacheCredentials(accounts=accounts, private_keys=private_keys)

        # self.delete_output_file()

        self.credentials = creds
        return creds

    def terminate_process(self):
        """
        Terminates the ganache-cli process if it's running.
        """
        if self.process and self.process.poll() is None:
            print("Terminating ganache-cli process...")
            self.process.terminate()
            self.process.wait()
            print("Ganache process terminated.")
        else:
            print("No running ganache-cli process to terminate.")

    def is_process_alive(self):
        """
        Checks if the ganache-cli process is alive and prints process details.
        """
        if self.process is None:
            print("Ganache process has not been started.")
        elif self.process.poll() is None:
            print(f"Ganache process is running (PID: {self.process.pid}).")
        else:
            print("Ganache process is not running.")

    def delete_output_file(self):
        """
        Deletes the output file.
        """
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
            print(f"Deleted temporary file '{self.output_file}'.")
        else:
            print(f"File '{self.output_file}' not found.")