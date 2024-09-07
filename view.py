import json
import pandas as pd
import streamlit as st
from streamlit_tags import st_tags
import app
import app.scrape
from data import config, model

st.set_page_config(page_title="Grabby", layout="wide")

form_data = model.FormData(model="", fields=[], url="", query="")

with open("styles.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Before we go tell me some stuff")

# Divide the page into two columns, aligned symmetrically
col1, col2 = st.columns(2, gap="large")

with col1:
    st.header("Model Selection")
    form_data.model = st.selectbox(
        "Select AI model",
        options=["gpt-4o-mini", "gpt-4o-2024-08-06"],
        index=0,
        help="Choose the AI model you want to use for scraping."
    )

    st.header("URL To Scrape")
    form_data.url = st.text_input(
        "Put the web URL here",
        placeholder="https://example.com",
        help="Enter the URL of the website you want to scrape."
    )

with col2:
    st.header("Fields to Extract")
    tags = st_tags(
        label='Enter Fields to Extract:',
        text='Press enter to add a tag',
        value=[],  # Default values if any
        suggestions=["title", "meta", "content"],  # Added sample suggestions
        maxtags=-1,  # Unlimited tags
        key='tags_input'
    )
    form_data.fields = tags
    further_prompt = st.text_input("Is there additional things I should consider?")
    form_data.query = further_prompt

# Logic here
if 'perform_scrape' not in st.session_state:
    st.session_state['perform_scrape'] = False

if st.button("Start Scraping", help="Click to start the scraping process."):
    with st.spinner('Please wait... Data is being scraped.'):
        try:
            st.session_state['results'] = app.scrape.perform_scrape(form_data)
            print(st.session_state['results'])
            st.session_state['perform_scrape'] = True
        except Exception as e:
            st.session_state["perform_scrape"] = False

if st.session_state.get('perform_scrape'):
    result = st.session_state['results']

    # Display the DataFrame and other data
    st.write("Scraped Data:", result.df)
    
    # Create columns for download buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        # Convert DataFrame to JSON
        json_data = result.df.to_json(orient='records', lines=True)
        st.download_button("Download JSON", data=json_data, file_name=f"{result.timestamp}_data.json")
    
    with col2:
        # Convert DataFrame to CSV
        csv_data = result.df.to_csv(index=False)
        st.download_button("Download CSV", data=csv_data, file_name=f"{result.timestamp}_data.csv")
    
    # with col3:
    #     # Convert DataFrame to XLSX
    #     xlsx_data = result.df.to_excel(index=False, engine='openpyxl')
    #     st.download_button("Download XLSX", data=xlsx_data, file_name=f"{result.timestamp}_data.xlsx")

    # Optional: Download Markdown if needed
    if result.markdown:
        st.download_button("Download Markdown", data=result.markdown, file_name=f"{result.timestamp}_data.md")

st.markdown("<p style='text-align: center; font-size: 14px;'>© 2024 AI Scraper. All rights reserved.</p>", unsafe_allow_html=True)
