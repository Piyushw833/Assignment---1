# Insurance Management System

A comprehensive web-based insurance claim management and risk analysis application built with Python and Streamlit.

## Features

- **Policyholder Management**
  - Register new policyholders
  - View policyholder details
  - Track policy information

- **Claim Management**
  - Submit new claims
  - Track claim status
  - Update claim status
  - View claim history

- **Risk Analysis**
  - Identify high-risk policyholders
  - Analyze claim frequency
  - Track claim ratios
  - Policy type analysis

- **Reports**
  - Monthly claims summary
  - Average claim by policy type
  - Highest claim details
  - Pending claims report

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd insurance-management-system
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit application:
```bash
streamlit run main.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Use the sidebar navigation to access different modules:
   - Dashboard: Overview of key metrics
   - Policyholder Management: Add and view policyholders
   - Claim Management: Submit and manage claims
   - Risk Analysis: View risk metrics and analysis
   - Reports: Generate and view various reports

## Data Storage

The application uses JSON files for data persistence, stored in the `data` directory:
- `policyholders.json`: Stores policyholder information
- `claims.json`: Stores claim information

## Project Structure

```
insurance_system/
├── data/
│   ├── policyholders.json
│   └── claims.json
├── models/
│   ├── policyholder.py
│   └── claim.py
├── services/
│   ├── data_service.py
│   ├── risk_service.py
│   └── report_service.py
├── main.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.x
- Streamlit
- Pandas
- Plotly
- Pydantic

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 