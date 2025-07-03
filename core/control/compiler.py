import subprocess
import json
from pathlib import Path
from typing import Optional, List
from pydantic import BaseModel


class ContractArtifact(BaseModel):
    abi: List[dict]
    bytecode: str


class ContractCompiler:
    def __init__(
        self,
        contract_path: str,
        contract_name: str,
        abi_output: Optional[str] = None,
        bin_output: Optional[str] = None,
    ):
        self.contract_path = contract_path
        self.contract_name = contract_name

        # Set default output paths if not provided
        abi_default = f"{self.contract_name}.abi.json"
        bin_default = f"{self.contract_name}.bin"

        self.abi_output = str(Path(abi_output or abi_default).resolve())
        self.bin_output = str(Path(bin_output or bin_default).resolve())

    def compile(self) -> ContractArtifact:
        """
        Compiles the Solidity contract using solc and returns a ContractArtifact.
        """
        # Ensure contract file exists
        if not Path(self.contract_path).is_file():
            raise FileNotFoundError(f"Contract file not found: {self.contract_path}")

        print(f"✅ Compiling {self.contract_path} using solc...")

        # Run solc to output ABI and bytecode into the same directory
        result = subprocess.run(
            [
                "solc",
                "--abi",
                "--bin",
                self.contract_path,
                "--overwrite",
                "-o",
                str(Path(self.abi_output).parent),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(f"solc compilation failed:\n{result.stderr}")

        print("✅ Compilation complete.")

        abi_file = Path(self.abi_output).parent / f"{self.contract_name}.abi"
        bin_file = Path(self.bin_output).parent / f"{self.contract_name}.bin"

        if not abi_file.exists() or not bin_file.exists():
            raise FileNotFoundError(
                "Compiled ABI or bytecode not found. Check solc output."
            )

        with abi_file.open("r") as f:
            abi_raw = f.read()
        abi = json.loads(abi_raw)

        with bin_file.open("r") as f:
            bytecode = f.read().strip()

        with Path(self.abi_output).open("w") as f:
            json.dump(abi, f, indent=2)
        with Path(self.bin_output).open("w") as f:
            f.write(bytecode)

        print(f"✅ ABI saved to {self.abi_output}")
        print(f"✅ Bytecode saved to {self.bin_output}")

        return ContractArtifact(abi=abi, bytecode=bytecode)
