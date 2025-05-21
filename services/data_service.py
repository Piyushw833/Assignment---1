import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import os

class DataService:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.policyholders: Dict[str, dict] = {}
        self.claims: Dict[str, dict] = {}
        self._ensure_data_dir()
        self._load_data()

    def _ensure_data_dir(self):
        """Ensure the data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _load_data(self):
        """Load data from JSON files"""
        try:
            if os.path.exists(f"{self.data_dir}/policyholders.json"):
                with open(f"{self.data_dir}/policyholders.json", "r") as f:
                    self.policyholders = json.load(f)
            if os.path.exists(f"{self.data_dir}/claims.json"):
                with open(f"{self.data_dir}/claims.json", "r") as f:
                    self.claims = json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")

    def _save_data(self):
        """Save data to JSON files"""
        try:
            with open(f"{self.data_dir}/policyholders.json", "w") as f:
                json.dump(self.policyholders, f, default=str)
            with open(f"{self.data_dir}/claims.json", "w") as f:
                json.dump(self.claims, f, default=str)
        except Exception as e:
            print(f"Error saving data: {e}")

    def add_policyholder(self, policyholder_data: dict) -> str:
        """Add a new policyholder"""
        policyholder_id = policyholder_data["policyholder_id"]
        self.policyholders[policyholder_id] = policyholder_data
        self._save_data()
        return policyholder_id

    def get_policyholder(self, policyholder_id: str) -> Optional[dict]:
        """Get policyholder by ID"""
        return self.policyholders.get(policyholder_id)

    def get_all_policyholders(self) -> List[dict]:
        """Get all policyholders"""
        return list(self.policyholders.values())

    def add_claim(self, claim_data: dict) -> str:
        """Add a new claim"""
        claim_id = claim_data["claim_id"]
        self.claims[claim_id] = claim_data
        self._save_data()
        return claim_id

    def get_claim(self, claim_id: str) -> Optional[dict]:
        """Get claim by ID"""
        return self.claims.get(claim_id)

    def get_all_claims(self) -> List[dict]:
        """Get all claims"""
        return list(self.claims.values())

    def update_claim_status(self, claim_id: str, status: str) -> bool:
        """Update claim status"""
        if claim_id in self.claims:
            self.claims[claim_id]["status"] = status
            self._save_data()
            return True
        return False

    def get_policyholder_claims(self, policyholder_id: str) -> List[dict]:
        """Get all claims for a policyholder"""
        return [
            claim for claim in self.claims.values()
            if claim["policyholder_id"] == policyholder_id
        ] 