import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string
from database.crud_operations import insert_or_update_data_to_sql, fetch_all_data_from_sql
import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv

# Function to generate random CAPTCHA values
def generate_random_captcha(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Define a reusable function to display data and create download buttons
def display_and_download_data(data, title, file_name):
    if data:
        df = pd.DataFrame(data, columns=["BID SUBMISSION CLOSING DATE", "TENDER TITLE", "REFERENCE NUMBER", "TENDER ID", "E-PUBLISHED DATE"])
        st.subheader(title)
        st.write(df)

        st.download_button(
            label=f"Download {title} as CSV",
            data=df.to_csv(index=False),
            file_name=file_name,
            mime='text/csv'
        )

# Load .env file
load_dotenv()

# ChromeDriver Path
chromedriver_path = os.getenv("CHROMEDRIVER_PATH")
url = os.getenv("BHEL_URL")

def start_scraping():
    # Streamlit UI
    st.title("BHEL Tender Scraper")

    if st.button("Start Scraping"):
        with st.spinner("Scraping in progress..."):
            service = Service(chromedriver_path)
            driver = webdriver.Chrome(service=service)

            driver.get(url)

            try:
                while True:
                    captcha_value = generate_random_captcha()
                    captcha_input = driver.find_element(By.ID, "captchaText")
                    captcha_input.clear()
                    captcha_input.send_keys(captcha_value)

                    driver.find_element(By.ID, "Submit").click()
                    time.sleep(1)
                    driver.refresh()
                    time.sleep(1)
                    st.warning("Please confirm the alert box manually (if it appears). Waiting for 10 seconds...")
                    time.sleep(1)
                    break

                data = []
                unique_entries = set()
                while True:
                    try:
                        WebDriverWait(driver, 60).until(
                            EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'list_table')]"))
                        )
                        rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'list_table')]/tbody/tr")
                        for row in rows[1:]:
                            columns = row.find_elements(By.TAG_NAME, 'td')
                            if len(columns) >= 5:
                                bid_submission_closing_date = columns[2].text.strip()
                                e_published_date = columns[1].text.strip()
                                column_4_content = columns[4].text.strip()
                                split_values = re.findall(r'\[(.*?)\]', column_4_content)
                                if len(split_values) == 3:
                                    tender_title = split_values[0].strip()
                                    reference_number = split_values[1].strip()
                                    tender_id = split_values[2].strip()
                                else:
                                    tender_title = column_4_content
                                    reference_number = "N/A"
                                    tender_id = "N/A"

                                if tender_id in unique_entries:
                                    continue

                                unique_entries.add(tender_id)
                                data.append([bid_submission_closing_date, tender_title, reference_number, tender_id, e_published_date])

                        try:
                            next_button = WebDriverWait(driver, 1).until(
                                EC.element_to_be_clickable((By.XPATH, "//*[@id='loadNext']"))
                            )
                            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                            next_button.click()
                        except Exception:
                            st.warning("No more pages to load.")
                            break

                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        break

                # if data:
                #     newly_inserted_data, updated_data = insert_or_update_data_to_sql(data)

                #     if newly_inserted_data:
                #         new_df = pd.DataFrame(newly_inserted_data, columns=["BID SUBMISSION CLOSING DATE", "TENDER TITLE", "REFERENCE NUMBER", "TENDER ID"])
                #         st.subheader("Newly Inserted Tenders")
                #         st.write(new_df)

                #         st.download_button(
                #             label="Download Newly Inserted Data as CSV",
                #             data=new_df.to_csv(index=False),
                #             file_name='new_tender_data.csv',
                #             mime='text/csv'
                #         )

                #     if updated_data:
                #         updated_df = pd.DataFrame(updated_data, columns=["BID SUBMISSION CLOSING DATE", "TENDER TITLE", "REFERENCE NUMBER", "TENDER ID"])
                #         st.subheader("Updated Tenders")
                #         st.write(updated_df)

                #         st.download_button(
                #             label="Download Updated Data as CSV",
                #             data=updated_df.to_csv(index=False),
                #             file_name='updated_tender_data.csv',
                #             mime='text/csv'
                #         )

                #     all_tender_data = fetch_all_data_from_sql()
                #     if all_tender_data:
                #         all_df = pd.DataFrame(
                #             all_tender_data,
                #             columns=["BID SUBMISSION CLOSING DATE", "TENDER TITLE", "REFERENCE NUMBER", "TENDER ID", "E-PUBLISHED DATE"]
                #         )

                #         all_df["BID SUBMISSION CLOSING DATE"] = pd.to_datetime(
                #             all_df["BID SUBMISSION CLOSING DATE"], errors='coerce'
                #         ).dt.strftime('%d-%b-%Y %I:%M %p')

                #         st.subheader("All Tenders (Sorted by Closing Date)")
                #         st.write(all_df)

                #         st.download_button(
                #             label="Download All Tender Data as CSV",
                #             data=all_df.to_csv(index=False),
                #             file_name='all_tender_data.csv',
                #             mime='text/csv'
                #         )
                # else:
                #     st.warning("No valid tender data found.")
                
                if data:
                    newly_inserted_data, updated_data = insert_or_update_data_to_sql(data)

                    # Handle newly inserted tenders
                    if newly_inserted_data:
                        display_and_download_data(newly_inserted_data, "Newly Inserted Tenders", "new_tender_data.csv")

                    # Handle updated tenders
                    if updated_data:
                        display_and_download_data(updated_data, "Updated Tenders", "updated_tender_data.csv")

                    # Handle all tenders
                    all_tender_data = fetch_all_data_from_sql()
                    if all_tender_data:
                        all_df = pd.DataFrame(
                            all_tender_data,
                            columns=["BID SUBMISSION CLOSING DATE", "TENDER TITLE", "REFERENCE NUMBER", "TENDER ID", "E-PUBLISHED DATE"]
                        )

                        all_df["BID SUBMISSION CLOSING DATE"] = pd.to_datetime(
                            all_df["BID SUBMISSION CLOSING DATE"], errors='coerce'
                        ).dt.strftime('%d-%b-%Y %I:%M %p')

                        display_and_download_data(all_tender_data, "All Tenders (Sorted by Closing Date)", "all_tender_data.csv")

                else:
                    st.warning("No valid tender data found.")

            finally:
                driver.quit()