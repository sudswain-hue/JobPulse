# JobPulse - Labor Market Insights

A Streamlit web application that provides job seekers with up-to-date labor market insights from MongoDB data.

## Features

- Real-time job market data visualization
- Filter jobs by visa class, job title, and location
- Analyze salary trends and employer statistics
- View case status distribution and approval rates
- Explore top employers and occupations

## Setup Instructions

### 1. Install Required Dependencies

```bash
pip install streamlit pymongo pandas plotly
```

### 2. MongoDB Setup

1. Make sure MongoDB is installed and running on your system
2. Create a database named `jobpulse`
3. Create a collection named `job_listings`
4. Import your job data into the collection

Here's a sample script to import your data into MongoDB:

```python
import pymongo
import json

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["jobpulse"]
collection = db["job_listings"]

# Sample data (your existing MongoDB document)
data = {
    "employment_details": {
        "NEW_EMPLOYMENT": 0,
        "CONTINUED_EMPLOYMENT": 0,
        "CHANGE_PREVIOUS_EMPLOYMENT": 0,
        "NEW_CONCURRENT_EMPLOYMENT": 0,
        "AMENDED_PETITION": 0,
        "TOTAL_WORKER_POSITIONS": 1,
        "NAICS_CODE": 62111
    },
    "employer_details": {
        "EMPLOYER_NAME": "Mercy Health Physicians Lorain, LLC",
        "EMPLOYER_ADDRESS1": "3700 Kolbe Rd.",
        "EMPLOYER_CITY": "Lorain",
        "EMPLOYER_STATE": "OH",
        "EMPLOYER_POSTAL_CODE": "44053",
        "EMPLOYER_COUNTRY": "UNITED STATES OF AMERICA",
        "EMPLOYER_PHONE": 14409604000,
        "EMPLOYER_FEIN": "27-0995585",
        # ... rest of employer details
    },
    # ... rest of your document structure
    "CASE_NUMBER": "I-200-24365-576456",
    "CASE_STATUS": "Denied",
    "RECEIVED_DATE": "2024-12-30T00:00:00.000Z",
    "DECISION_DATE": "2024-12-31T00:00:00.000Z",
    "VISA_CLASS": "H-1B",
    "JOB_TITLE": "Family Medicine Physician",
    "SOC_CODE": "29-1215.00",
    "SOC_TITLE": "Family Medicine Physicians",
    "FULL_TIME_POSITION": "Y",
    "BEGIN_DATE": "2025-06-29T00:00:00.000Z",
    "END_DATE": "2028-06-28T00:00:00.000Z",
    "CHANGE_EMPLOYER": 1,
    "year": 2025,
    "quarter": "Q1"
}

# Insert the data
collection.insert_one(data)
print("Data imported successfully!")
```

### 3. Run the Streamlit App

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## Customization

You can modify the application by:

1. Adding more filters in the sidebar
2. Creating additional visualizations based on your data
3. Updating the MongoDB connection parameters if your database is hosted elsewhere
4. Adding user authentication if needed

## Project Structure

- `app.py`: Main Streamlit application
- `README.md`: Project documentation
- Additional files can be added as your project grows

## Future Work 
