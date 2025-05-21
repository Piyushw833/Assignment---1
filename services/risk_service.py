from datetime import datetime, timedelta
from typing import List, Dict
import pandas as pd
from .data_service import DataService

class RiskService:
    def __init__(self, data_service: DataService):
        self.data_service = data_service

    def calculate_claim_frequency(self, policyholder_id: str) -> Dict:
        """Calculate claim frequency for a policyholder"""
        claims = self.data_service.get_policyholder_claims(policyholder_id)
        total_claims = len(claims)
        
        if total_claims == 0:
            return {
                "policyholder_id": policyholder_id,
                "total_claims": 0,
                "claims_last_year": 0,
                "claim_frequency": 0
            }

        # Calculate claims in the last year
        one_year_ago = datetime.now() - timedelta(days=365)
        claims_last_year = len([
            claim for claim in claims
            if datetime.fromisoformat(claim["date_of_claim"].split(".")[0]) > one_year_ago
        ])

        return {
            "policyholder_id": policyholder_id,
            "total_claims": total_claims,
            "claims_last_year": claims_last_year,
            "claim_frequency": claims_last_year / 12  # Average claims per month
        }

    def identify_high_risk_policyholders(self) -> List[Dict]:
        """Identify high-risk policyholders based on claims"""
        high_risk_policyholders = []
        
        for policyholder_id in self.data_service.policyholders:
            policyholder = self.data_service.get_policyholder(policyholder_id)
            claims = self.data_service.get_policyholder_claims(policyholder_id)
            
            if not claims:
                continue

            # Calculate total claim amount
            total_claim_amount = sum(claim["claim_amount"] for claim in claims)
            claim_ratio = total_claim_amount / float(policyholder["sum_insured"])
            
            # Check last year's claims
            one_year_ago = datetime.now() - timedelta(days=365)
            recent_claims = len([
                claim for claim in claims
                if datetime.fromisoformat(claim["date_of_claim"].split(".")[0]) > one_year_ago
            ])

            if recent_claims > 3 or claim_ratio > 0.8:
                high_risk_policyholders.append({
                    "policyholder_id": policyholder_id,
                    "name": policyholder["name"],
                    "recent_claims": recent_claims,
                    "claim_ratio": claim_ratio,
                    "total_claim_amount": total_claim_amount
                })

        return high_risk_policyholders

    def analyze_claims_by_policy_type(self) -> Dict:
        """Analyze claims aggregated by policy type"""
        claims_df = pd.DataFrame(self.data_service.get_all_claims())
        policyholders_df = pd.DataFrame(self.data_service.get_all_policyholders())
        
        if claims_df.empty or policyholders_df.empty:
            return {}

        # Merge claims with policyholders to get policy types
        merged_df = claims_df.merge(
            policyholders_df[["policyholder_id", "policy_type"]],
            on="policyholder_id"
        )

        analysis = {}
        for policy_type in merged_df["policy_type"].unique():
            policy_claims = merged_df[merged_df["policy_type"] == policy_type]
            
            analysis[policy_type] = {
                "total_claims": len(policy_claims),
                "total_amount": float(policy_claims["claim_amount"].sum()),
                "average_amount": float(policy_claims["claim_amount"].mean()),
                "max_amount": float(policy_claims["claim_amount"].max()),
                "pending_claims": len(policy_claims[policy_claims["status"] == "Pending"])
            }

        return analysis 