import psycopg2

def main():
    try:
        # Connect to PostgreSQL
        connection = psycopg2.connect(
            dbname="gmail_db",
            user="postgres",
            password="postgres",
            host="db"
        )
        cursor = connection.cursor()

        # Test the connection
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"Connected to PostgreSQL DB: {db_version[0]}")

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error connecting to the database: {e}")
    
if __name__ == "__main__":
    main()