import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse

# Function to scrape table data from the given URL
def scrape_table_data(url):
    # Send a GET request to the URL with SSL certificate verification disabled
    response = requests.get(url, verify=False)
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find the table element
    table = soup.find_all('table')
    table = table[2]  # Assuming the desired table is the third table in the page
    # Initialize lists to store table data
    data = []
    # Extract table headers
    headers = [header.text.strip() for header in table.find_all('th')]
    # Extract table rows
    for row in table.find_all('tr'):
        row_data = [cell.text.strip() for cell in row.find_all('td')]
        if row_data:
            data.append(row_data)
    # Create a DataFrame
    df = pd.DataFrame(data, columns=headers)
    return df

# Streamlit App
def main():
    st.title("Website Table Scraper")
    url = st.text_input("Enter the Website URL:")
    
    if st.button("Scrape Table"):
        if url:
            try:
                df = scrape_table_data(url)
                parsed_url = urlparse(url)
                path = parsed_url.path
                # Extracting the hospital type from the path
                hospital_type = path.split('/')[-1].split('.')[0]
                csv_filename = f"{hospital_type}.csv"
                # Save DataFrame to CSV
                df.to_csv(csv_filename, index=False)  # Save DataFrame to CSV
                st.dataframe(df)
                # Download button for CSV file
                st.markdown(f"Download the scraped data as CSV: [**{csv_filename}**](./{csv_filename})")
            except Exception as e:
                st.error(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
