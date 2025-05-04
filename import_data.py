import pymongo
import json
from datetime import datetime
from bson import ObjectId

import config

# Connect to MongoDB
client = pymongo.MongoClient(config.MONGO_CONNECTION_STRING)
db = client[config.MONGO_DB_NAME]
collection = db[config.MONGO_COLLECTION_NAME]

# Convert the data format for MongoDB
def parse_date(date_str):
    try:
        if isinstance(date_str, dict) and "$date" in date_str:
            date_str = date_str["$date"]
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except:
        return None

def parse_long(long_val):
    try:
        if isinstance(long_val, dict) and "$numberLong" in long_val:
            return int(long_val["$numberLong"])
        return long_val
    except:
        return long_val

# Sample data (from your provided MongoDB document)
data = {
    "_id": ObjectId("67fd83487398620d8c99d614"),
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
        "EMPLOYER_ADDRESS2": None,
        "EMPLOYER_CITY": "Lorain",
        "EMPLOYER_STATE": "OH",
        "EMPLOYER_POSTAL_CODE": "44053",
        "EMPLOYER_COUNTRY": "UNITED STATES OF AMERICA",
        "EMPLOYER_PHONE": parse_long({"$numberLong": "14409604000"}),
        "EMPLOYER_FEIN": "27-0995585",
        "EMPLOYER_POC_LAST_NAME": "Burk",
        "EMPLOYER_POC_FIRST_NAME": "Kelsey",
        "EMPLOYER_POC_JOB_TITLE": "Senior Paralegal - Immigration",
        "EMPLOYER_POC_ADDRESS1": "1701 Mercy Health Place",
        "EMPLOYER_POC_ADDRESS2": None,
        "EMPLOYER_POC_CITY": "Cincinnati",
        "EMPLOYER_POC_STATE": "OH",
        "EMPLOYER_POC_POSTAL_CODE": "45237",
        "EMPLOYER_POC_COUNTRY": "UNITED STATES OF AMERICA",
        "EMPLOYER_POC_PHONE": parse_long({"$numberLong": "17067687124"}),
        "EMPLOYER_POC_EMAIL": "KBurk@mercy.com"
    },
    "employer_poc_details": {
        "EMPLOYER_POC_LAST_NAME": "Burk",
        "EMPLOYER_POC_FIRST_NAME": "Kelsey",
        "EMPLOYER_POC_JOB_TITLE": "Senior Paralegal - Immigration",
        "EMPLOYER_POC_ADDRESS1": "1701 Mercy Health Place",
        "EMPLOYER_POC_ADDRESS2": None,
        "EMPLOYER_POC_CITY": "Cincinnati",
        "EMPLOYER_POC_STATE": "OH",
        "EMPLOYER_POC_POSTAL_CODE": "45237",
        "EMPLOYER_POC_COUNTRY": "UNITED STATES OF AMERICA",
        "EMPLOYER_POC_PHONE": parse_long({"$numberLong": "17067687124"}),
        "EMPLOYER_POC_EMAIL": "KBurk@mercy.com"
    },
    "agent_details": {
        "AGENT_REPRESENTING_EMPLOYER": "Yes",
        "AGENT_ATTORNEY_LAST_NAME": "Jenkins",
        "AGENT_ATTORNEY_FIRST_NAME": "Staci",
        "AGENT_ATTORNEY_MIDDLE_NAME": "Marie",
        "AGENT_ATTORNEY_ADDRESS1": "425 Walnut Street",
        "AGENT_ATTORNEY_ADDRESS2": "Suite 1800",
        "AGENT_ATTORNEY_CITY": "Cincinnati",
        "AGENT_ATTORNEY_STATE": "OH",
        "AGENT_ATTORNEY_POSTAL_CODE": "45202",
        "AGENT_ATTORNEY_COUNTRY": "UNITED STATES OF AMERICA",
        "AGENT_ATTORNEY_PHONE": 15133578767,
        "AGENT_ATTORNEY_EMAIL_ADDRESS": "SMJenkins@taftlaw.com",
        "LAWFIRM_NAME_BUSINESS_NAME": "Taft Stettinius & Hollister LLP",
        "STATE_OF_HIGHEST_COURT": "OH",
        "NAME_OF_HIGHEST_STATE_COURT": "Supreme Court of Ohio"
    },
    "worksite_details": {
        "WORKSITE_WORKERS": 1,
        "WORKSITE_ADDRESS1": "5940 Oak Point Rd.",
        "WORKSITE_CITY": "Lorain",
        "WORKSITE_COUNTY": "LORAIN",
        "WORKSITE_STATE": "OH",
        "WORKSITE_POSTAL_CODE": "44053",
        "TOTAL_WORKSITE_LOCATIONS": 1,
        "SECONDARY_ENTITY": "No"
    },
    "wage_details": {
        "WAGE_RATE_OF_PAY_FROM": 64147,
        "WAGE_RATE_OF_PAY_TO": 295000,
        "WAGE_UNIT_OF_PAY": "Year",
        "PREVAILING_WAGE": 64147,
        "PW_WAGE_LEVEL": "I"
    },
    "pw_columns": {
        "PW_UNIT_OF_PAY": "Year",
        "PW_WAGE_LEVEL": "I",
        "PW_OES_YEAR": "7/1/2024 - 6/30/2025",
        "PREVAILING_WAGE": 64147
    },
    "preparer": {
        "PREPARER_LAST_NAME": "Saoudi",
        "PREPARER_FIRST_NAME": "Kendra",
        "PREPARER_BUSINESS_NAME": "Taft Stettinius & Hollister LLP",
        "PREPARER_EMAIL": "ksaoudi@taftlaw.com"
    },
    "CASE_NUMBER": "I-200-24365-576456",
    "CASE_STATUS": "Denied",
    "RECEIVED_DATE": parse_date({"$date": "2024-12-30T00:00:00.000Z"}),
    "DECISION_DATE": parse_date({"$date": "2024-12-31T00:00:00.000Z"}),
    "VISA_CLASS": "H-1B",
    "JOB_TITLE": "Family Medicine Physician",
    "SOC_CODE": "29-1215.00",
    "SOC_TITLE": "Family Medicine Physicians",
    "FULL_TIME_POSITION": "Y",
    "BEGIN_DATE": parse_date({"$date": "2025-06-29T00:00:00.000Z"}),
    "END_DATE": parse_date({"$date": "2028-06-28T00:00:00.000Z"}),
    "CHANGE_EMPLOYER": 1,
    "AGREE_TO_LC_STATEMENT": "Yes",
    "WILLFUL_VIOLATOR": "No",
    "PUBLIC_DISCLOSURE": "Disclose Business",
    "year": 2025,
    "quarter": "Q1"
}

# Generate more sample data for demonstration
def generate_sample_data():
    samples = [data]  # Start with the original data
    
    # Create variations with different job titles, employers, and salaries
    job_variations = [
        {"JOB_TITLE": "Software Engineer", "SOC_CODE": "15-1252.00", "SOC_TITLE": "Software Developers", 
         "wage_details": {"WAGE_RATE_OF_PAY_FROM": 110000, "WAGE_RATE_OF_PAY_TO": 150000, "WAGE_UNIT_OF_PAY": "Year", "PREVAILING_WAGE": 105000}, 
         "CASE_STATUS": "Certified"},
        
        {"JOB_TITLE": "Data Scientist", "SOC_CODE": "15-2051.00", "SOC_TITLE": "Data Scientists", 
         "wage_details": {"WAGE_RATE_OF_PAY_FROM": 120000, "WAGE_RATE_OF_PAY_TO": 165000, "WAGE_UNIT_OF_PAY": "Year", "PREVAILING_WAGE": 115000}, 
         "CASE_STATUS": "Certified"},
        
        {"JOB_TITLE": "Product Manager", "SOC_CODE": "15-2051.00", "SOC_TITLE": "Product Managers", 
         "wage_details": {"WAGE_RATE_OF_PAY_FROM": 125000, "WAGE_RATE_OF_PAY_TO": 170000, "WAGE_UNIT_OF_PAY": "Year", "PREVAILING_WAGE": 120000}, 
         "CASE_STATUS": "Withdrawn"},
        
        {"JOB_TITLE": "UX Designer", "SOC_CODE": "27-1024.00", "SOC_TITLE": "User Experience Designers", 
         "wage_details": {"WAGE_RATE_OF_PAY_FROM": 95000, "WAGE_RATE_OF_PAY_TO": 130000, "WAGE_UNIT_OF_PAY": "Year", "PREVAILING_WAGE": 90000}, 
         "CASE_STATUS": "Certified"},
        
        {"JOB_TITLE": "Network Engineer", "SOC_CODE": "15-1241.00", "SOC_TITLE": "Network and Computer Systems Administrators", 
         "wage_details": {"WAGE_RATE_OF_PAY_FROM": 88000, "WAGE_RATE_OF_PAY_TO": 120000, "WAGE_UNIT_OF_PAY": "Year", "PREVAILING_WAGE": 85000}, 
         "CASE_STATUS": "Denied"}
    ]
    
    employer_variations = [
        {"employer_details": {"EMPLOYER_NAME": "Google LLC", "EMPLOYER_CITY": "Mountain View", "EMPLOYER_STATE": "CA"}},
        {"employer_details": {"EMPLOYER_NAME": "Microsoft Corporation", "EMPLOYER_CITY": "Redmond", "EMPLOYER_STATE": "WA"}},
        {"employer_details": {"EMPLOYER_NAME": "Amazon Web Services", "EMPLOYER_CITY": "Seattle", "EMPLOYER_STATE": "WA"}},
        {"employer_details": {"EMPLOYER_NAME": "Apple Inc.", "EMPLOYER_CITY": "Cupertino", "EMPLOYER_STATE": "CA"}},
        {"employer_details": {"EMPLOYER_NAME": "Meta Platforms Inc.", "EMPLOYER_CITY": "Menlo Park", "EMPLOYER_STATE": "CA"}}
    ]
    
    location_variations = [
        {"worksite_details": {"WORKSITE_CITY": "San Francisco", "WORKSITE_STATE": "CA", "WORKSITE_POSTAL_CODE": "94105"}},
        {"worksite_details": {"WORKSITE_CITY": "New York", "WORKSITE_STATE": "NY", "WORKSITE_POSTAL_CODE": "10001"}},
        {"worksite_details": {"WORKSITE_CITY": "Austin", "WORKSITE_STATE": "TX", "WORKSITE_POSTAL_CODE": "78701"}},
        {"worksite_details": {"WORKSITE_CITY": "Chicago", "WORKSITE_STATE": "IL", "WORKSITE_POSTAL_CODE": "60601"}},
        {"worksite_details": {"WORKSITE_CITY": "Boston", "WORKSITE_STATE": "MA", "WORKSITE_POSTAL_CODE": "02110"}}
    ]
    
    # Generate combinations
    for i in range(len(job_variations)):
        for j in range(len(employer_variations)):
            new_sample = data.copy()
            
            # Update with new job details
            new_sample["JOB_TITLE"] = job_variations[i]["JOB_TITLE"]
            new_sample["SOC_CODE"] = job_variations[i]["SOC_CODE"]
            new_sample["SOC_TITLE"] = job_variations[i]["SOC_TITLE"]
            new_sample["wage_details"] = job_variations[i]["wage_details"].copy()
            new_sample["CASE_STATUS"] = job_variations[i]["CASE_STATUS"]
            
            # Update employer details
            for key, value in employer_variations[j]["employer_details"].items():
                new_sample["employer_details"][key] = value
            
            # Update location with a random variation
            loc_idx = (i + j) % len(location_variations)
            for key, value in location_variations[loc_idx]["worksite_details"].items():
                new_sample["worksite_details"][key] = value
            
            # Generate a new ObjectId
            new_sample["_id"] = ObjectId()
            
            # Add to samples
            samples.append(new_sample)
    
    return samples

# Drop existing collection if it exists
collection.drop()

# Insert the generated data
samples = generate_sample_data()
collection.insert_many(samples)

print(f"Successfully imported {len(samples)} job listings into MongoDB!")