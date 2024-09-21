from __future__ import print_function
import os.path
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import psycopg2
import sys
from datetime import datetime
import math
import time
import humanize
from mailparser import mailparser
import html2text
import argparse

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    
    parser = argparse.ArgumentParser(description="Analyze emails for relevance to a query.")
    parser.add_argument('-l', '--limit', type=int, required=True, help='The limit of emails to load')
    args = parser.parse_args()

    total_message_limit = args.limit
    
    print("I am downloading your email to a local database")
    connection = connect_to_db()
    if not connection:
        return
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'config/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Call the Gmail API
    service = build('gmail', 'v1', credentials=creds)


    # latest_cached_timestamp = 
    latest_cached_timestamp = get_latest_cached_email_timestamp(connection)
    earliest_cached_timestamp = get_earliest_cached_email_timestamp(connection)
    # Initial API request
    # START get_emails
    # print(f"Latest timestamp: {latest_cached_timestamp}")
    total_start_time = time.time()

    #TO LOAD ONLY MESSAGES LATER THAN WHATS IN DB (LIKE AN UPDATE)
    #total_messages_found = fetch_emails_between_timestamps(service, connection, latest_cached_timestamp, earliest_cached_timestamp, 0)
    
    #TO LOAD ONLY MESSAGES EARLIER THAN WHATS IN DB (LIKE CATCHING UP ON OLDER DATA)
    total_messages_found = fetch_emails_between_timestamps(service, connection, total_message_limit, 0, earliest_cached_timestamp)
    
    print(f"Total messages retrieved: {total_messages_found}")
    total_end_time = time.time()
    total_elapsed_timespan = total_end_time-total_start_time
    
    # Get the total number of emails from okay I'm just making up the number now
    total_emails = 401425
    total_loaded_in_table = get_total_entries_in_table(connection)
    print(f"Total number of emails in your inbox: {total_emails}. Entries in database: {total_loaded_in_table}. Coverage: {total_loaded_in_table*100/total_emails:.2f}%")
    
    fraction_emails_processed = total_messages_found/total_emails
    all_emails_estimated_time = total_elapsed_timespan/fraction_emails_processed
    
    print(f"Total elapsed time: {format_duration(total_elapsed_timespan)}. If you tried to process all {total_emails} emails, it would take approximately {format_duration(all_emails_estimated_time)}")

def fetch_emails_between_timestamps(service, connection, total_message_limit, minimum_timestamp, maximum_timestamp):
    # Convert the timestamp to RFC 2822 date format used by Gmail API
    queries = []
    query = ""
    if minimum_timestamp != 0:
        queries.append(f"after:{datetime.utcfromtimestamp((minimum_timestamp/1000)-86400).strftime('%Y/%m/%d')}")
    if maximum_timestamp != 0:
        queries.append(f"before:{datetime.utcfromtimestamp((maximum_timestamp/1000)+86400).strftime('%Y/%m/%d')}")
        
    query = " ".join(queries)
    print(f"query: {query}", flush=True)
    total_messages_found = 0
    messages_per_page = 50
    if messages_per_page > total_message_limit:
        messages_per_page = total_message_limit
    
    iteration_limit = (total_message_limit/messages_per_page)
    
    start_time = time.time()
    
    print(f"Starting download & insertion of up to {total_message_limit} messages, with {messages_per_page} messages per page.", flush=True)
    results = service.users().messages().list(userId='me', maxResults=messages_per_page, q=query).execute()
    messages = results.get('messages', [])
    total_messages_found = len(messages)
    time.sleep(1)
    
    
    # Loop to handle pagination
    
    iteration_count = 2
    load_messages_into_database(connection, service, process_messages(service, messages))
    page_one_time = time.time()
    time_delta_one_page = page_one_time-start_time

    
    print(f"Page 1/{iteration_limit:.0f}, Load time: {format_duration(time_delta_one_page)}. Elapsed time: {format_duration(time_delta_one_page)}. Estimated remaining time: {format_duration(time_delta_one_page*iteration_limit)}", flush=True)


    while 'nextPageToken' in results and iteration_count <= iteration_limit:
        page_start_time = time.time()
        page_token = results['nextPageToken']
        
        results = service.users().messages().list(
            userId='me', maxResults=messages_per_page, pageToken=page_token, q=query
        ).execute()
        messages = results.get('messages', [])

        load_messages_into_database(connection, service, process_messages(service, messages))

        total_messages_found = total_messages_found + len(messages)
        time.sleep(1)
        page_end_time = time.time()
        time_delta_this_page = page_end_time-page_start_time
        time_delta_from_start = page_end_time-start_time
        average_time_per_page = time_delta_from_start/iteration_count
        projected_total_time = average_time_per_page*(iteration_limit-iteration_count)
        
        
        
        print(f"Page {iteration_count:.0f}/{iteration_limit:.0f}, Load time: {format_duration(time_delta_this_page)}. Elapsed time: {format_duration(average_time_per_page)}. Estimated remaining time: {format_duration(projected_total_time)}", flush=True)
        iteration_count += 1
    print("Finished downloading emails", flush=True)
    return total_messages_found

def load_messages_into_database(connection, service, messages):
    for message in messages:
            msg = service.users().messages().get(userId = 'me', id=message['id']).execute()
            msg_raw = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
            message_details = get_message_details(msg, msg_raw)
            #print(f"ID: {message_details['id']} | Sender: {message_details['sender']} | Subject: {message_details['subject']} | Snippet: {message_details['snippet']}")
            insert_email_data(connection, message_details)
            
def process_messages(service, messages):
    all_messages = []
    for message in messages:
            # Retrieve the message details (including timestamp)
            message_details = service.users().messages().get(userId='me', id=message['id']).execute()
            
            # Gmail API's internalDate is in milliseconds, so we divide by 1000 to get seconds
            #email_timestamp = int(message_details['internalDate']) / 1000

            # Apply the time check after retrieving the messages
            #if email_timestamp <= minimum_timestamp:
            #    return all_messages

            # Otherwise, add the message to the new messages list
            all_messages.append(message)
    return all_messages
            
def get_total_entries_in_table(connection):
    cursor = connection.cursor()

    # Query to get the maximum timestamp
    query = "SELECT COUNT(*) FROM emails;"
    cursor.execute(query)
    row_count = cursor.fetchone()[0]

    cursor.close()
    return row_count
            
def get_latest_cached_email_timestamp(connection):
    cursor = connection.cursor()

    # Query to get the maximum timestamp
    query = "SELECT MAX(timestamp) FROM emails;"
    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()

    # Return the result (the maximum timestamp)
    if result[0]:
        return result[0]
    else:
        return 0  # If there are no emails in the table
    
def get_earliest_cached_email_timestamp(connection):
    cursor = connection.cursor()

    # Query to get the maximum timestamp
    query = "SELECT MIN(timestamp) FROM emails;"
    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()

    # Return the result (the minimum timestamp)
    if result[0]:
        return result[0]
    else:
        return time.time()*1000  # If there are no emails in the table
    
def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname="gmail_db",
            user="postgres",
            password="postgres",
            host="db",  # Connect to the 'db' service in Docker
            port="5432"
        )
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def get_message_details(message, message_raw):
    message_id = message['id']
    snippet = message.get('snippet', 'No snippet available')
    
    # Headers (subject, from, date)
    headers = message['payload']['headers']
    subject = None
    sender = None
    for header in headers:
        if header['name'] == 'Subject':
            subject = header['value']
        if header['name'] == 'From':
            sender = header['value']
    bodyraw = ""
    
    
    raw_email = base64.urlsafe_b64decode(message_raw.get('raw'))   
    parsed_mail = mailparser.parse_from_bytes(raw_email)     
    plaintext_body = parsed_mail.text_plain[0] if parsed_mail.text_plain else None
    html_body = parsed_mail.text_html[0] if parsed_mail.text_html else None
    bodyraw = (plaintext_body or "") + " " + (html_body or "")
    bodyclean = strip_html(bodyraw)
    
    # Timestamp
    timestamp = int(message['internalDate'])  # Convert to human-readable date
    
    return {
        'id': message_id,
        'subject': subject,
        'sender': sender,
        'snippet': snippet,
        'bodyraw': bodyraw,
        'bodyclean': bodyclean,
        'timestamp': timestamp
    }
    
def strip_html(raw_email_text_body):
    return html2text.html2text(raw_email_text_body).lstrip().rstrip()

def insert_email_data(connection, message_details):
    try:
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO emails (id, subject, sender, snippet, bodyraw, bodyclean, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """
        cursor.execute(insert_query, (
            message_details['id'],
            message_details['subject'],
            message_details['sender'],
            message_details['snippet'],
            message_details['bodyraw'],
            message_details['bodyclean'],
            message_details['timestamp']
        ))
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.rollback()  # Rollback any changes made before the error
        sys.exit(1)  # Exit the script with a non-zero exit code
        
def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    result = []

    if hours > 0:
        result.append(f"{hours:.0f} hour" + ("s" if hours > 1 else ""))
    if minutes > 0:
        result.append(f"{minutes:.0f} minute" + ("s" if minutes > 1 else ""))
    if secs > 0 or (hours == 0 and minutes == 0):
        result.append(f"{secs:.0f} second" + ("s" if secs != 1 else ""))

    return " ".join(result)

if __name__ == '__main__':
    main()