import sqlite3
import requests

"""
Problem Statement 1:
API Data Retrieval and Storage: You are tasked with fetching data from an external REST API, storing it in a local SQLite database, and displaying the retrieved data. The API provides a list of books in JSON format with attributes like title, author, and publication year.

Here, I am using my own hosted json file as an API which provides the list of books with basic details that is mentioned in above problem statement.
"""


# The exact raw API endpoint matching your repository data
API_URL = "https://raw.githubusercontent.com/sanjaykumarm/AccuKnox/refs/heads/main/list-of-books.json"
DB_NAME = "books_database.db"

def init_database():
    """Sets up the local SQLite database and structure."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publication_year INTEGER
        )
    """)
    conn.commit()
    return conn

def fetch_and_store_books(conn):
    """Fetches clean data from the live API and bulk inserts it into SQLite."""
    try:
        print(f"Connecting to API: {API_URL}...")
        response = requests.get(API_URL)
        
        # Throws an exception for 4xx or 5xx network status codes
        response.raise_for_status() 
        books_list = response.json()
        
        # Prepare data tuple mapping for efficient bulk execution
        # .strip() handles any hidden leading spaces present in the source strings
        data_tuples = [
            (
                book.get("id"),
                book.get("title", "").strip(),
                book.get("author", "").strip(),
                book.get("publication_year")
            )
            for book in books_list
        ]
        
        cursor = conn.cursor()
        
        # Batch insert minimizes system overhead and ensures transaction atomicity
        cursor.executemany("""
            INSERT OR REPLACE INTO books (id, title, author, publication_year)
            VALUES (?, ?, ?, ?)
        """, data_tuples)
        
        conn.commit()
        print(f"--> Successfully pulled and updated {len(data_tuples)} records in SQLite.")
        
    except requests.exceptions.RequestException as e:
        print(f"🚨 Network or API Error occurred: {e}")
    except ValueError:
        print("🚨 Error: The response payload was not valid JSON data.")

def display_database_records(conn):
    """Fetches stored records directly from SQLite and displays them cleanly."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, publication_year FROM books ORDER BY id ASC")
    rows = cursor.fetchall()
    
    print("\n" + "="*80)
    print(f"{'ID':<5} | {'BOOK TITLE':<32} | {'AUTHOR':<24} | {'YEAR':<6}")
    print("-"*80)
    
    for row in rows:
        book_id, title, author, year = row
        print(f"{book_id:<5} | {title:<32} | {author:<24} | {year:<6}")
        
    print("="*80 + "\n")

if __name__ == "__main__":
    # Initialize database connection and we will use this same connection throughout the program execution.
    db_connection = init_database()
    
    # Fetch the data from API and Display the record from the Local SQLite database.
    fetch_and_store_books(db_connection)
    display_database_records(db_connection)
    
    # Close or Shut down active database connections to avoid memory leak or resource optimization.
    db_connection.close()
    print("Database connection closed.")