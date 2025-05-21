import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from models.policyholder import Policyholder, PolicyType
from models.claim import Claim, ClaimStatus
from services.data_service import DataService
from services.risk_service import RiskService
from services.report_service import ReportService

# Initialize services
data_service = DataService()
risk_service = RiskService(data_service)
report_service = ReportService(data_service)

# Set page config
st.set_page_config(
    page_title="Insurance Management System",
    page_icon="🏥",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a page",
    ["Dashboard", "Policyholder Management", "Claim Management", "Risk Analysis", "Reports"]
)

def format_currency(amount):
    return f"${amount:,.2f}"

# Dashboard
if page == "Dashboard":
    st.title("Insurance Management Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_policyholders = len(data_service.get_all_policyholders())
    total_claims = len(data_service.get_all_claims())
    pending_claims = len([c for c in data_service.get_all_claims() if c['status'] == 'Pending'])
    high_risk = len(risk_service.identify_high_risk_policyholders())
    
    col1.metric("Total Policyholders", total_policyholders)
    col2.metric("Total Claims", total_claims)
    col3.metric("Pending Claims", pending_claims)
    col4.metric("High Risk Policyholders", high_risk)
    
    # Claims by Policy Type
    st.subheader("Claims by Policy Type")
    policy_analysis = risk_service.analyze_claims_by_policy_type()
    if policy_analysis:
        fig = px.pie(
            values=[data['total_claims'] for data in policy_analysis.values()],
            names=list(policy_analysis.keys()),
            title="Distribution of Claims by Policy Type"
        )
        st.plotly_chart(fig)
    
    # Monthly Claims Trend
    st.subheader("Monthly Claims Trend")
    monthly_claims = report_service.generate_monthly_claims_report()
    if monthly_claims:
        df = pd.DataFrame(monthly_claims)
        fig = px.line(
            df,
            x='month',
            y=['total_claims', 'average_amount'],
            title="Monthly Claims Trend"
        )
        st.plotly_chart(fig)

# Policyholder Management
elif page == "Policyholder Management":
    st.title("Policyholder Management")
    
    tab1, tab2 = st.tabs(["Add Policyholder", "View Policyholders"])
    
    with tab1:
        st.subheader("Add New Policyholder")
        with st.form("add_policyholder"):
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=18, max_value=100)
            policy_type = st.selectbox("Policy Type", [t.value for t in PolicyType])
            sum_insured = st.number_input("Sum Insured", min_value=0.0)
            
            if st.form_submit_button("Add Policyholder"):
                try:
                    policyholder_id = f"PH{len(data_service.policyholders) + 1:03d}"
                    policyholder = Policyholder(
                        policyholder_id=policyholder_id,
                        name=name,
                        age=age,
                        policy_type=policy_type,
                        sum_insured=sum_insured
                    )
                    data_service.add_policyholder(policyholder.dict())
                    st.success(f"Policyholder added successfully! ID: {policyholder_id}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab2:
        st.subheader("View Policyholders")
        policyholders = data_service.get_all_policyholders()
        if policyholders:
            df = pd.DataFrame(policyholders)
            df['sum_insured'] = df['sum_insured'].apply(format_currency)
            st.dataframe(df)
        else:
            st.info("No policyholders found")

# Claim Management
elif page == "Claim Management":
    st.title("Claim Management")
    
    tab1, tab2 = st.tabs(["Submit Claim", "View Claims"])
    
    with tab1:
        st.subheader("Submit New Claim")
        with st.form("submit_claim"):
            policyholder_id = st.selectbox(
                "Policyholder ID",
                options=[p['policyholder_id'] for p in data_service.get_all_policyholders()]
            )
            claim_amount = st.number_input("Claim Amount", min_value=0.0)
            reason = st.text_area("Reason")
            
            if st.form_submit_button("Submit Claim"):
                try:
                    claim_id = f"CL{len(data_service.claims) + 1:03d}"
                    claim = Claim(
                        claim_id=claim_id,
                        policyholder_id=policyholder_id,
                        claim_amount=claim_amount,
                        reason=reason
                    )
                    data_service.add_claim(claim.dict())
                    st.success(f"Claim submitted successfully! ID: {claim_id}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab2:
        st.subheader("View Claims")
        claims = data_service.get_all_claims()
        if claims:
            df = pd.DataFrame(claims)
            df['claim_amount'] = df['claim_amount'].apply(format_currency)
            st.dataframe(df)
            
            # Claim Status Update
            st.subheader("Update Claim Status")
            col1, col2 = st.columns(2)
            with col1:
                selected_claim = st.selectbox("Select Claim ID", options=[c['claim_id'] for c in claims])
            with col2:
                new_status = st.selectbox("New Status", options=[s.value for s in ClaimStatus])
            
            if st.button("Update Status"):
                if data_service.update_claim_status(selected_claim, new_status):
                    st.success("Claim status updated successfully!")
                else:
                    st.error("Failed to update claim status")
        else:
            st.info("No claims found")

# Risk Analysis
elif page == "Risk Analysis":
    st.title("Risk Analysis")
    
    # High Risk Policyholders
    st.subheader("High Risk Policyholders")
    high_risk = risk_service.identify_high_risk_policyholders()
    if high_risk:
        df = pd.DataFrame(high_risk)
        df['claim_ratio'] = df['claim_ratio'].apply(lambda x: f"{x:.2%}")
        df['total_claim_amount'] = df['total_claim_amount'].apply(format_currency)
        st.dataframe(df)
    else:
        st.info("No high-risk policyholders found")
    
    # Claims by Policy Type
    st.subheader("Claims Analysis by Policy Type")
    policy_analysis = risk_service.analyze_claims_by_policy_type()
    if policy_analysis:
        df = pd.DataFrame(policy_analysis).T
        df['average_amount'] = df['average_amount'].apply(format_currency)
        df['total_amount'] = df['total_amount'].apply(format_currency)
        st.dataframe(df)
        
        # Visualization
        fig = go.Figure(data=[
            go.Bar(name='Total Claims', x=list(policy_analysis.keys()), y=[d['total_claims'] for d in policy_analysis.values()]),
            go.Bar(name='Pending Claims', x=list(policy_analysis.keys()), y=[d['pending_claims'] for d in policy_analysis.values()])
        ])
        fig.update_layout(title="Claims Distribution by Policy Type", barmode='group')
        st.plotly_chart(fig)
    else:
        st.info("No policy analysis data available")

# Reports
else:
    st.title("Reports")
    
    # Monthly Claims Report
    st.subheader("Monthly Claims Report")
    monthly_claims = report_service.generate_monthly_claims_report()
    if monthly_claims:
        df = pd.DataFrame(monthly_claims)
        df['total_amount'] = df['total_amount'].apply(format_currency)
        df['average_amount'] = df['average_amount'].apply(format_currency)
        st.dataframe(df)
        
        fig = px.line(
            df,
            x='month',
            y='total_claims',
            title="Monthly Claims Trend"
        )
        st.plotly_chart(fig)
    else:
        st.info("No monthly claims data available")
    
    # Average Claim by Policy Type
    st.subheader("Average Claim by Policy Type")
    policy_averages = report_service.calculate_average_claim_by_policy()
    if policy_averages:
        df = pd.DataFrame(policy_averages).T
        df['average_amount'] = df['average_amount'].apply(format_currency)
        df['total_amount'] = df['total_amount'].apply(format_currency)
        st.dataframe(df)
    else:
        st.info("No policy averages data available")
    
    # Highest Claim
    st.subheader("Highest Claim")
    highest_claim = report_service.get_highest_claim()
    if highest_claim:
        col1, col2 = st.columns(2)
        with col1:
            st.write("Claim ID:", highest_claim['claim_id'])
            st.write("Policyholder:", highest_claim['policyholder_name'])
            st.write("Amount:", format_currency(highest_claim['claim_amount']))
        with col2:
            st.write("Date:", highest_claim['date_of_claim'])
            st.write("Policy Type:", highest_claim['policy_type'])
            st.write("Status:", highest_claim['status'])
    else:
        st.info("No claims data available")
    
    # Pending Claims
    st.subheader("Pending Claims")
    pending_claims = report_service.get_pending_claims_report()
    if pending_claims:
        df = pd.DataFrame(pending_claims)
        df['claim_amount'] = df['claim_amount'].apply(format_currency)
        st.dataframe(df)
    else:
        st.info("No pending claims") 