from database.connection import get_sql_connection
from datetime import datetime

# Function to insert or update data in SQL Server
def insert_or_update_data_to_sql(data):
    conn = get_sql_connection()
    cursor = conn.cursor()
    newly_inserted_data = []
    updated_data = []

    for record in data:
        try:
            bid_submission_closing_date = datetime.strptime(record[0], '%d-%b-%Y %I:%M %p')
            e_published_date = datetime.strptime(record[4], '%d-%b-%Y %I:%M %p')
            tender_title = record[1]
            reference_number = record[2]
            tender_id = record[3]

            cursor.execute("SELECT BidSubmissionClosingDate, EPublishedDate FROM Tenders WHERE TenderID = ?", tender_id)
            existing_record = cursor.fetchone()

            if existing_record:
                existing_bid_date = existing_record[0]
                existing_epublish_date = existing_record[1]

                if existing_bid_date is None or bid_submission_closing_date > existing_bid_date:
                    cursor.execute("""
                        UPDATE Tenders
                        SET BidSubmissionClosingDate = ?, EPublishedDate = ?, TenderTitle = ?, ReferenceNumber = ?
                        WHERE TenderID = ?
                    """, bid_submission_closing_date, e_published_date, tender_title, reference_number, tender_id)
                    print(f"Tender {tender_id} updated with new BidSubmissionClosingDate.")
                    updated_data.append([bid_submission_closing_date, tender_title, reference_number, tender_id, e_published_date])

                elif existing_epublish_date is None or (bid_submission_closing_date == existing_bid_date and e_published_date > existing_epublish_date):
                    cursor.execute("""
                        UPDATE Tenders
                        SET EPublishedDate = ?, TenderTitle = ?, ReferenceNumber = ?
                        WHERE TenderID = ?
                    """, e_published_date, tender_title, reference_number, tender_id)
                    print(f"Tender {tender_id} updated with new EPublishedDate.")
                    updated_data.append([bid_submission_closing_date, tender_title, reference_number, tender_id, e_published_date])

                else:
                    print(f"Tender {tender_id} already exists and is up-to-date. Skipping insertion.")
            else:
                cursor.execute("""
                    INSERT INTO Tenders (BidSubmissionClosingDate, TenderTitle, ReferenceNumber, TenderID, EPublishedDate)
                    VALUES (?, ?, ?, ?, ?)
                """, bid_submission_closing_date, tender_title, reference_number, tender_id, e_published_date)
                print(f"Inserted new tender: {tender_id}")
                newly_inserted_data.append([bid_submission_closing_date, tender_title, reference_number, tender_id, e_published_date])
        except Exception as e:
            print(f"Error processing record {record[3]}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    return newly_inserted_data, updated_data

def fetch_all_data_from_sql():
    conn = get_sql_connection()
    cursor = conn.cursor()
    query = "SELECT BidSubmissionClosingDate, TenderTitle, ReferenceNumber, TenderID, EPublishedDate FROM dbo.Tenders"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return [list(row) for row in data]