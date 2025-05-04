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
      "employment_details": {
        "TOTAL_WORKER_POSITIONS": 1,
        "NAICS_CODE": 54151
      },
      "employer_details": {
        "EMPLOYER_NAME": "IBM Corporation",
        "EMPLOYER_ADDRESS1": "3039 Cornwallis Road, PO Box 12195",
        "EMPLOYER_ADDRESS2": None,
        "EMPLOYER_CITY": "Durham",
        "EMPLOYER_STATE": "NC",
        "EMPLOYER_POSTAL_CODE": "27709",
        "EMPLOYER_COUNTRY": "UNITED STATES OF AMERICA",
        "EMPLOYER_PHONE": { "$numberLong": "19192541493"},
        "EMPLOYER_FEIN": "13-0871985",
        "EMPLOYER_POC_LAST_NAME": "Lammonds",
        "EMPLOYER_POC_FIRST_NAME": "Andrea",
        "EMPLOYER_POC_JOB_TITLE": "US Immigration Team Lead",
        "EMPLOYER_POC_ADDRESS1": "3039 Cornwallis Road, PO Box 12195",
        "EMPLOYER_POC_ADDRESS2": None,
        "EMPLOYER_POC_CITY": "Durham",
        "EMPLOYER_POC_STATE": "NC",
        "EMPLOYER_POC_POSTAL_CODE": "27709",
        "EMPLOYER_POC_COUNTRY": "UNITED STATES OF AMERICA",
        "EMPLOYER_POC_PHONE": {"$numberLong": "19192541493"},
        "EMPLOYER_POC_EMAIL": "Andrea.Lammonds1@ibm.com"
      },
      "worksite_details": {
        "WORKSITE_WORKERS": 1,
        "WORKSITE_ADDRESS1": "150 Venable Lane",
        "WORKSITE_CITY": "Monroe",
        "WORKSITE_COUNTY": "OUACHITA",
        "WORKSITE_STATE": "LA",
        "WORKSITE_POSTAL_CODE": "71203",
        "TOTAL_WORKSITE_LOCATIONS": 1
      },
      "wage_details": {
        "WAGE_RATE_OF_PAY_FROM": 87027,
        "WAGE_RATE_OF_PAY_TO": 104907,
        "WAGE_UNIT_OF_PAY": "Year",
        "PREVAILING_WAGE": 87027
      },
      "pw_columns": {
        "PREVAILING_WAGE": 87027,
        "PW_UNIT_OF_PAY": "Year"
      },
      "CASE_NUMBER": "I-200-24358-566689",
      "CASE_STATUS": "Certified",
      "RECEIVED_DATE": {"$date": "2024-12-22T00:00:00.000Z"},
      "DECISION_DATE": {"$date": "2024-12-31T00:00:00.000Z"},
      "VISA_CLASS": "H-1B",
      "JOB_TITLE": "Technical Lead",
      "SOC_CODE": "15-1211.00",
      "SOC_TITLE": "Computer Systems Analysts",
      "FULL_TIME_POSITION": "Y",
      "BEGIN_DATE": {"$date": "2025-05-18T00:00:00.000Z"},
      "END_DATE": {"$date": "2028-05-17T00:00:00.000Z"},
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