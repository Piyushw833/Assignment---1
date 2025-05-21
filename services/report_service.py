from datetime import datetime
from typing import Dict, List
import pandas as pd
from .data_service import DataService

class ReportService:
    def __init__(self, data_service: DataService):
        self.data_service = data_service

    def generate_monthly_claims_report(self) -> Dict:
        """Generate report of total claims per month"""
        claims = self.data_service.get_all_claims()
        if not claims:
            return {}

        # Convert claims to DataFrame
        df = pd.DataFrame(claims)
        df['date_of_claim'] = pd.to_datetime(df['date_of_claim'])
        df['month'] = df['date_of_claim'].dt.strftime('%Y-%m')

        monthly_claims = df.groupby('month').agg({
            'claim_id': 'count',
            'claim_amount': ['sum', 'mean']
        }).reset_index()

        monthly_claims.columns = ['month', 'total_claims', 'total_amount', 'average_amount']
        
        return monthly_claims.to_dict(orient='records')

    def calculate_average_claim_by_policy(self) -> Dict:
        """Calculate average claim amount by policy type"""
        claims = self.data_service.get_all_claims()
        policyholders = self.data_service.get_all_policyholders()
        
        if not claims or not policyholders:
            return {}

        # Create DataFrames
        claims_df = pd.DataFrame(claims)
        policyholders_df = pd.DataFrame(policyholders)

        # Merge claims with policyholders
        merged_df = claims_df.merge(
            policyholders_df[['policyholder_id', 'policy_type']],
            on='policyholder_id'
        )

        # Calculate averages by policy type
        policy_averages = merged_df.groupby('policy_type').agg({
            'claim_amount': ['mean', 'sum', 'count']
        }).round(2)

        policy_averages.columns = ['average_amount', 'total_amount', 'claim_count']
        
        return policy_averages.to_dict(orient='index')

    def get_highest_claim(self) -> Dict:
        """Get details of the highest claim filed"""
        claims = self.data_service.get_all_claims()
        if not claims:
            return {}

        highest_claim = max(claims, key=lambda x: float(x['claim_amount']))
        policyholder = self.data_service.get_policyholder(highest_claim['policyholder_id'])

        return {
            'claim_id': highest_claim['claim_id'],
            'policyholder_id': highest_claim['policyholder_id'],
            'policyholder_name': policyholder['name'],
            'claim_amount': highest_claim['claim_amount'],
            'date_of_claim': highest_claim['date_of_claim'],
            'policy_type': policyholder['policy_type'],
            'status': highest_claim['status']
        }

    def get_pending_claims_report(self) -> List[Dict]:
        """Get list of policyholders with pending claims"""
        claims = self.data_service.get_all_claims()
        pending_claims = []

        for claim in claims:
            if claim['status'] == 'Pending':
                policyholder = self.data_service.get_policyholder(claim['policyholder_id'])
                pending_claims.append({
                    'claim_id': claim['claim_id'],
                    'policyholder_id': claim['policyholder_id'],
                    'policyholder_name': policyholder['name'],
                    'claim_amount': claim['claim_amount'],
                    'date_of_claim': claim['date_of_claim'],
                    'policy_type': policyholder['policy_type'],
                    'reason': claim['reason']
                })

        return sorted(pending_claims, key=lambda x: x['date_of_claim'], reverse=True) 