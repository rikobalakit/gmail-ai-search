import psycopg2
from psycopg2 import sql
from sentence_transformers import CrossEncoder
import argparse
from datetime import datetime
import math
import time

def main():
    parser = argparse.ArgumentParser(description="Analyze emails for relevance to a query.")
    parser.add_argument('-q', '--query', type=str, required=True, help='The query string to evaluate against emails.')
    parser.add_argument('-l', '--limit', type=int, default=50, help='The limit of emails to return (default: 50)')

    args = parser.parse_args()

    query = args.query
    return_list_limit = args.limit
    
    try:
        # Connect to PostgreSQL
        connection = psycopg2.connect(
            dbname="gmail_db",
            user="postgres",
            password="postgres",
            host="db"
        )
        cursor = connection.cursor()

        model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2')

        # Test the connection
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        #print(f"Connected to PostgreSQL DB: {db_version[0]}")
        
        # Define your query and email body
        
        
        
        scored_emails = []
        
        found_emails = get_emails(cursor)
        number_of_emails = len(found_emails)
        print(f"Searching {number_of_emails} emails for a best match for the query: '{query}'", flush=True)
        
        slice_size = number_of_emails/10
        current_slice_to_pass = slice_size
        progress_counter = 0
        slice_counter = 0
        
        analyze_start_time = time.time()
        
        for idx, (email_id, subject, bodyclean) in enumerate(found_emails, start=1):
            email_id = email_id if email_id is not None else "N/A"
            subject = subject if subject is not None else "No Subject"
            bodyclean = strip_line_breaks(bodyclean if bodyclean is not None else "No Body")
            
            score = get_relevance_score(model, query, bodyclean)
            
            #print(f"{idx}. ID: {email_id} | Subject: {subject[:40]:50} | Score: {score} | Body: {bodyclean[:50]}")
            scored_emails.append({
                'id': email_id,
                'subject': subject,
                'score': score,
                'bodyclean': bodyclean
            })
            
            progress_counter = progress_counter + 1
            if progress_counter > current_slice_to_pass:
                current_progress = progress_counter/number_of_emails
                current_slice_to_pass = current_slice_to_pass + slice_size
                slice_counter = slice_counter + 10
                elapsed_time = time.time()-analyze_start_time
                time_per_analysis = elapsed_time/progress_counter
                total_time_estimate = time_per_analysis * number_of_emails
                remaining_time_estimate = total_time_estimate - elapsed_time
                print(f"{slice_counter}% complete. Elapsed time: {format_duration(elapsed_time)}. Estimated remaining time: {format_duration(remaining_time_estimate)}", flush=True)
                
            
            
            
        sorted_emails = sorted(scored_emails, key=lambda x: x['score'], reverse=True)    
        top_emails = sorted_emails[:return_list_limit]
        # Print the sorted emails
        print(f"\nTop {return_list_limit} Emails Sorted by Relevance Score (Descending):",flush=True)
        print("==============================================")
        for idx, email in enumerate(top_emails, start=1):
            # Truncate 'subject' to first 40 characters and 'bodyclean' to first 50 characters
            truncated_subject = email['subject'][:40] + ('...' if len(email['subject']) > 40 else '')
            truncated_body = email['bodyclean'][:50] + ('...' if len(email['bodyclean']) > 50 else '')
            
            print(f"{idx}. ID: {email['id']} | Subject: {truncated_subject:40} | Score: {email['score']:.4f} | Body: {truncated_body:50}")

        total_emails = 401425
        total_elapsed_time = time.time()-analyze_start_time
        print(f"Total time to analyze {number_of_emails} emails: {format_duration(time.time()-analyze_start_time)}")
        total_emails_time_estimate = total_elapsed_time/(number_of_emails/total_emails)
        print(f"If you wanted to analyze all {total_emails}, it would take {format_duration(total_emails_time_estimate)}")
        #query = "job application acceptance or rejection"
        #email_body = "Thank you for applying, we are happy to move you to the next stage..."
        #score = get_relevance_score(model, query, email_body)
        #print(f"Relevance Score: {score}")

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error connecting to the database: {e}")

def get_relevance_score(model, query, email_body):
    # Initialize the CrossEncoder model
    
    
    # Prepare the input as a list of [query, email_body] pairs
    inputs = [[query, email_body]]
    
    # Get the relevance score
    scores = model.predict(inputs)
    
    # Since we have only one pair, return the first score
    return scores[0]    

def get_emails(cursor):
    # Define the SQL query to fetch id, subject, sender
    query = sql.SQL("""
        SELECT id, subject, bodyclean
        FROM emails
        ORDER BY timestamp DESC;
    """)

    # Execute the query
    cursor.execute(query)

    # Fetch all results
    emails = cursor.fetchall()

    return emails

def strip_line_breaks(s):
    if s:
        return s.replace('\n', ' ').replace('\r', ' ').strip()
    return s

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
    
if __name__ == "__main__":
    main()
    
