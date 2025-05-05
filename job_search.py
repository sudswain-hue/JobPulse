import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px
import config
from datetime import datetime

def render_job_search(_client):
    """
    Renders the advanced job search component
    """
    st.title("Advanced Job Search")
    st.write("Find your perfect job opportunity by exploring our database of positions")
    
    # Get data from MongoDB
    db = _client[config.MONGO_DB_NAME]
    items = list(db[config.MONGO_COLLECTION_NAME].find())
    if not items:
        st.warning("No job listings found in the database.")
        return
    
    df = pd.json_normalize(items)
    
    # Create multiple search filters in columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Job title search (text input for more flexibility)
        job_title_search = st.text_input("Job Title Keywords", "")
        company_name_search = st.text_input("Company Name", "")
        
        # Salary range slider
        #if 'wage_details.WAGE_RATE_OF_PAY_FROM' in df.columns:
        #    min_salary = int(df['wage_details.WAGE_RATE_OF_PAY_FROM'].min())
        #    max_salary = int(df['wage_details.WAGE_RATE_OF_PAY_FROM'].max())
        #    salary_range = st.slider(
        #        "Salary Range",
        #        min_value=min_salary,
        #        max_value=max_salary,
        #        value=(min_salary, max_salary),
        #        step=5000
        #    )
    
    with col2:
        # Location filter (state)
        if 'worksite_details.WORKSITE_STATE' in df.columns:
            state_options = ['All'] + sorted(df['worksite_details.WORKSITE_STATE'].unique().tolist())
            selected_state = st.selectbox('State', state_options)
            
            # City filter (only show cities from selected state)
            city_options = ['All']
            if selected_state != 'All':
                city_options += sorted(df[df['worksite_details.WORKSITE_STATE'] == selected_state]['worksite_details.WORKSITE_CITY'].unique().tolist())
            selected_city = st.selectbox('City', city_options)
        
        # Visa class filter
        #if 'VISA_CLASS' in df.columns:
        #    visa_options = ['All'] + sorted(df['VISA_CLASS'].unique().tolist())
        #    selected_visa = st.selectbox('Visa Class', visa_options)
    
    # Apply filters
    filtered_df = df.copy()
    
    # Job title filter (partial match)
    if job_title_search:
        filtered_df = filtered_df[filtered_df['JOB_TITLE'].str.contains(job_title_search, case=False, na=False)]
    if company_name_search:
        filtered_df = filtered_df[filtered_df['employer_details.EMPLOYER_NAME'].str.contains(company_name_search, case=False, na=False)]

    # Salary filter
    #if 'wage_details.WAGE_RATE_OF_PAY_FROM' in df.columns:
    #    filtered_df = filtered_df[
    #        (filtered_df['wage_details.WAGE_RATE_OF_PAY_FROM'] >= salary_range[0]) & 
    #        (filtered_df['wage_details.WAGE_RATE_OF_PAY_FROM'] <= salary_range[1])
    #    ]
    
    # State filter
    if selected_state != 'All' and 'worksite_details.WORKSITE_STATE' in df.columns:
        filtered_df = filtered_df[filtered_df['worksite_details.WORKSITE_STATE'] == selected_state]
    
    # City filter
    if selected_city != 'All' and 'worksite_details.WORKSITE_CITY' in df.columns:
        filtered_df = filtered_df[filtered_df['worksite_details.WORKSITE_CITY'] == selected_city]
    
    # Visa class filter
    #if selected_visa != 'All' and 'VISA_CLASS' in df.columns:
    #    filtered_df = filtered_df[filtered_df['VISA_CLASS'] == selected_visa]
    
    # Display search results
    st.subheader(f"Search Results ({len(filtered_df)} jobs found)")
    
    if filtered_df.empty:
        st.info("No jobs match your search criteria. Try adjusting your filters.")
    else:
        # Show job cards
        for i, row in filtered_df.iterrows():
            with st.expander(f"{row['JOB_TITLE']} at {row['employer_details.EMPLOYER_NAME']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Job Title:** {row['JOB_TITLE']}")
                    st.markdown(f"**Employer:** {row['employer_details.EMPLOYER_NAME']}")
                    st.markdown(f"**Employer Location:** {row['employer_details.EMPLOYER_CITY']}, {row['employer_details.EMPLOYER_STATE']}")
                    st.markdown(f"**Location:** {row['worksite_details.WORKSITE_CITY']}, {row['worksite_details.WORKSITE_STATE']}")
                    st.markdown(f"**Occupation:** {row['SOC_TITLE']}")
                    
                    # Format dates for display
                    begin_date = row.get('BEGIN_DATE')
                    end_date = row.get('END_DATE')
                    
                    if begin_date and isinstance(begin_date, pd.Timestamp):
                        begin_date_str = begin_date.strftime('%Y-%m-%d')
                        st.markdown(f"**Start Date:** {begin_date_str}")
                    
                    if end_date and isinstance(end_date, pd.Timestamp):
                        end_date_str = end_date.strftime('%Y-%m-%d')
                        st.markdown(f"**End Date:** {end_date_str}")
                
                with col2:
                    # Display salary information
                    if 'wage_details' in row and isinstance(row['wage_details'], dict):
                        wage_from = row['wage_details'].get('WAGE_RATE_OF_PAY_FROM')
                        wage_to = row['wage_details'].get('WAGE_RATE_OF_PAY_TO')
                        wage_unit = row['wage_details'].get('WAGE_UNIT_OF_PAY')
                        
                        if wage_from:
                            st.markdown(f"**Salary Range:**")
                            st.markdown(f"${wage_from:,.2f} - ${wage_to:,.2f} per {wage_unit.lower() if wage_unit else 'year'}")
                    
                    # Case status with color coding
                    case_status = row.get('CASE_STATUS')
                    if case_status:
                        status_color = {
                            'Certified': 'green',
                            'Denied': 'red',
                            'Withdrawn': 'orange',
                            'In Process': 'blue'
                        }.get(case_status, 'gray')
                        
                        st.markdown(f"**Status:** <span style='color:{status_color};font-weight:bold'>{case_status}</span>", unsafe_allow_html=True)
        
        # Pagination (if there are many results)
        if len(filtered_df) > 10:
            st.write("---")
            page_col1, page_col2, page_col3 = st.columns([1, 3, 1])
            with page_col2:
                st.write("Showing the first 10 results. Refine your search for more specific results.")

    # Show some analytics on search results
    if not filtered_df.empty and len(filtered_df) > 1:
        st.write("---")
        st.subheader("Insights from Your Search Results")
        
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            # Salary distribution for this search
            if 'wage_details.WAGE_RATE_OF_PAY_FROM' in filtered_df.columns:
                fig = px.box(
                    filtered_df, 
                    y='wage_details.WAGE_RATE_OF_PAY_FROM',
                    title="Salary Distribution",
                    labels={'wage_details.WAGE_RATE_OF_PAY_FROM': 'Salary Range'},
                    color_discrete_sequence=['#3366CC']
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with insight_col2:
            # Employer distribution
            if 'employer_details.EMPLOYER_NAME' in filtered_df.columns:
                top_employers = filtered_df['employer_details.EMPLOYER_NAME'].value_counts().head(5)
                fig = px.pie(
                    values=top_employers.values,
                    names=top_employers.index,
                    title="Top Employers",
                    hole=0.4
                )
                st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    # This allows the file to be imported into the main app
    st.write("This is a component file. Run the main app.py file.")