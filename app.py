import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import job_search
import config

# Set page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.DEFAULT_LAYOUT
)

# MongoDB connection
@st.cache_resource
def init_connection():
    try:
        # Add connection options to improve reliability
        _client = pymongo.MongoClient(
            config.MONGO_CONNECTION_STRING,
            serverSelectionTimeoutMS=10000,  # 10 seconds timeout
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            maxPoolSize=50
        )
        # Force a connection check
        _client.admin.command('ping')
        return _client
    except Exception as e:
        st.error(f"MongoDB Connection Error: {e}")
        if config.DEBUG:
            st.exception(e)
        return None

# Function to fetch data from MongoDB
@st.cache_data(ttl=config.CACHE_TTL)
def get_data(_client):
    if _client is None:
        return []
    
    try:
        db = _client[config.MONGO_DB_NAME]
        items = db[config.MONGO_COLLECTION_NAME].find()
        items = list(items)  # Convert cursor to list
        return items
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        if config.DEBUG:
            st.exception(e)
        return []

# Initialize connection
_client = init_connection()

# Check if connection succeeded
if _client:
    #st.success("Connected to MongoDB")
    data = get_data(_client)
    if data:
        #df = pd.DataFrame(data)
        # Flatten nested dictionaries (1 level deep)
        df = pd.json_normalize(data)
    else:
        st.warning("No data available in the MongoDB collection. Please check your database content.")
        df = pd.DataFrame()
else:
    st.error("Failed to connect to MongoDB. Please check your connection string and network connectivity.")
    # Create an empty dataframe if connection fails
    df = pd.DataFrame()
    
    # Provide troubleshooting information in debug mode
    if config.DEBUG:
        st.info("""
        ## Troubleshooting tips:
        1. Check if your MongoDB Atlas credentials are correct
        2. Make sure your MongoDB Atlas cluster is running
        3. Verify that your IP address is whitelisted in MongoDB Atlas
        4. Ensure your network allows outbound connections to MongoDB Atlas
        """)

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Job Search", "Market Trends", "About"])

if page == "Dashboard":
    # Header & App Description
    st.title("JobPulse - Labor Market Insights")
    st.markdown("""
        Gain valuable insights into the current job market to make informed career decisions.
        Explore trending skills, wage expectations, and companies with the most opportunities.
    """)

# Main dashboard layout
if not df.empty and page == "Dashboard":
    # Sidebar for filters
    st.sidebar.header("Dashboard Filters")
    
    # Filter by visa class
    if 'VISA_CLASS' in df.columns:
        visa_options = ['All'] + sorted(df['VISA_CLASS'].dropna().unique().tolist())
        selected_visa = st.sidebar.selectbox('Visa Class', visa_options)
    
    # Filter by job title
    if 'JOB_TITLE' in df.columns:
        job_options = ['All'] + sorted(df['JOB_TITLE'].unique().tolist())
        selected_job = st.sidebar.selectbox('Job Title', job_options)
    
    # Filter by state
    selected_state = 'All' # Default Fallback
    if 'employer_details.EMPLOYER_STATE' in df.columns:
        state_options = ['All'] + sorted(df['employer_details.EMPLOYER_STATE'].dropna().unique().tolist())
        selected_state = st.sidebar.selectbox('Select State', state_options)
    
    # Apply filters
    filtered_df = df.copy()
    if selected_visa != 'All':
        filtered_df = filtered_df[filtered_df['VISA_CLASS'] == selected_visa]
    if selected_job != 'All':
        filtered_df = filtered_df[filtered_df['JOB_TITLE'] == selected_job]
    if selected_state != 'All':
        filtered_df = filtered_df[filtered_df['employer_details.EMPLOYER_STATE'] == selected_state]
    
    # Dashboard content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Case Status Distribution")
        if 'CASE_STATUS' in df.columns:
            status_counts = filtered_df['CASE_STATUS'].value_counts()
            fig = px.pie(
                names=status_counts.index,
                values=status_counts.values,
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Salary Range Analysis")
        if 'wage_details.WAGE_RATE_OF_PAY_FROM' in filtered_df.columns:
            fig = px.histogram(
                filtered_df,
                x='wage_details.WAGE_RATE_OF_PAY_FROM',
                nbins=20,
                title="Starting Salary Distribution",
                color_discrete_sequence=['#3366CC']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # More detailed insights
    st.subheader("Job Market Trends")
    col3, col4, col5 = st.columns(3)
    
    # Key metrics
    with col3:
        if 'CASE_STATUS' in filtered_df.columns:
            approval_rate = (filtered_df['CASE_STATUS'] == 'Certified').mean() * 100
            st.metric("Approval Rate", f"{approval_rate:.1f}%")
    
    with col4:
        if 'wage_details.WAGE_RATE_OF_PAY_FROM' in filtered_df.columns:
            avg_salary = filtered_df['wage_details.WAGE_RATE_OF_PAY_FROM'].mean()
            st.metric("Average Starting Salary", f"${avg_salary:,.2f}")
    
    with col5:
        if 'SOC_TITLE' in filtered_df.columns:
            top_occupation = filtered_df['SOC_TITLE'].value_counts().index[0]
            st.metric("Top Occupation", top_occupation)
    
    # Company insights
    st.subheader("Top Employers")
    if 'employer_details.EMPLOYER_NAME' in filtered_df.columns:
        top_employers = filtered_df['employer_details.EMPLOYER_NAME'].value_counts().head(10)
        fig = px.bar(
            x=top_employers.index,
            y=top_employers.values,
            labels={'x': 'Employer', 'y': 'Number of Jobs'},
            color_discrete_sequence=['#38bcb2']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed job listings
    st.subheader("Recent Job Listings")
    if not filtered_df.empty:
        # Format the dataframe for display
        display_df = filtered_df[['JOB_TITLE', 'SOC_TITLE', 'employer_details.EMPLOYER_NAME', 
                                 'worksite_details.WORKSITE_CITY', 'worksite_details.WORKSITE_STATE', 
                                 'wage_details.WAGE_RATE_OF_PAY_FROM', 'CASE_STATUS']].copy()
        
        # Rename columns for better readability
        display_df.columns = ['Job Title', 'Occupation', 'Employer', 'City', 'State', 'Starting Salary', 'Status']
        
        # Format salary values
        display_df['Starting Salary'] = display_df['Starting Salary'].apply(lambda x: f"${x:,.2f}")
        
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No job listings match your filter criteria.")
else:
    st.warning("No data available. Please check your MongoDB connection and database content.")

# Handle page routing
if page == "Job Search":
    # Render the job search component
    job_search.render_job_search(_client)

if page == "Market Trends":
    st.title("Labor Market Trends")
    st.write("Analyze the latest trends in the job market to make informed career decisions.")
    
    if not df.empty:
        # Timeline of job postings
        st.subheader("Job Posting Timeline")
        if 'RECEIVED_DATE' in df.columns:
            df['RECEIVED_MONTH'] = pd.to_datetime(df['RECEIVED_DATE']).dt.strftime('%Y-%m')
            timeline_data = df.groupby('RECEIVED_MONTH').size().reset_index(name='count')
            fig = px.line(
                timeline_data, 
                x='RECEIVED_MONTH', 
                y='count',
                title='Job Postings Over Time',
                labels={'RECEIVED_MONTH': 'Month', 'count': 'Number of Job Postings'},
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Top jobs by salary
        st.subheader("Top Paying Jobs")
        if 'JOB_TITLE' in df.columns and 'wage_details.WAGE_RATE_OF_PAY_FROM' in df.columns:
            job_salary = df.groupby('JOB_TITLE')['wage_details.WAGE_RATE_OF_PAY_FROM'].mean().sort_values(ascending=False).head(10)
            fig = px.bar(
                x=job_salary.index,
                y=job_salary.values,
                labels={'x': 'Job Title', 'y': 'Average Starting Salary ($)'},
                title='Top 10 Highest Paying Jobs',
                color_discrete_sequence=['#38bcb2']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Geographic distribution
        st.subheader("Geographic Distribution of Jobs")
        if 'worksite_details.WORKSITE_STATE' in df.columns:
            state_counts = df['worksite_details.WORKSITE_STATE'].value_counts().head(10)
            fig = px.bar(
                x=state_counts.index,
                y=state_counts.values,
                labels={'x': 'State', 'y': 'Number of Jobs'},
                title='Top 10 States by Job Openings',
                color_discrete_sequence=['#3366CC']
            )
            st.plotly_chart(fig, use_container_width=True)
        
#        # Case status by occupation
#        st.subheader("Approval Rates by Occupation")
#        if 'SOC_TITLE' in df.columns and 'CASE_STATUS' in df.columns:
#            # Calculate approval rates by occupation
#            occupation_approval = df.groupby('SOC_TITLE')['CASE_STATUS'].apply(
#                lambda x: (x == 'Certified').mean() * 100
#            ).sort_values(ascending=False).head(10)
#            
#            fig = px.bar(
#                x=occupation_approval.index,
#                y=occupation_approval.values,
#                labels={'x': 'Occupation', 'y': 'Approval Rate (%)'},
#                title='Top 10 Occupations by Approval Rate',
#                color_discrete_sequence=['#4CAF50']
#            )
#            st.plotly_chart(fig, use_container_width=True)

if page == "About":
    st.title("About JobPulse")
    st.write("""
    ## Our Mission
    
    JobPulse seeks to provide job seekers with up-to-date labor market insights so they can make wise career decisions. 
    Since the skill requirements for technical sectors are always changing, our platform assists users in finding 
    organizations that offer the most prospects for their career goals, as well as trending skills and wage expectations.
    
    ## Features
    
    - **Real-time Data**: Access to the latest job market trends and opportunities
    - **Salary Insights**: Compare compensation across different roles and locations
    - **Company Analysis**: Discover which employers are hiring the most in your field
    - **Geographic Analysis**: Find where the best opportunities are located
    - **Visa Status Tracking**: Monitor H-1B visa approval rates and trends
    
    ## Data Sources
    
    Our data is sourced from government databases, company filings, and public job listings to provide the most 
    comprehensive and accurate picture of the current job market.
    
    """)

# Footer
st.markdown("---")
st.markdown("© 2025 JobPulse - Real-time Labor Market Insights")