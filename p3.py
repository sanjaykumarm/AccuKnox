import csv
import sqlite3
import os

"""
This program is a part of below assignment:

CSV Data Import to a Database: Write a Python script that reads data from a CSV file containing user information (e.g., name, email) and inserts it into a SQLite database.
"""
DB_NAME = "user_info_database.db"
CSV_NAME = "user_information.csv"

def init_database():
    """Creates the SQLite database and the users table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            sr_no INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            mobile_number TEXT
        )
    """)
    conn.commit()
    return conn

def import_csv_to_db(conn):
    """Reads data from the CSV file and inserts it efficiently into the database."""
    if not os.path.exists(CSV_NAME):
        print(f"Error: The file '{CSV_NAME}' was not found in the current directory.")
        print("Please ensure the CSV file is placed next to this script.")
        return

    cursor = conn.cursor()
    
    with open(CSV_NAME, mode="r", encoding="utf-8") as f:
        # Detect delimiter automatically (comma or tab)
        sample = f.read(2048)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=[',', '\t'])
            reader = csv.reader(f, dialect)
        except csv.Error:
            # Fallback to standard reader if sniffing fails
            reader = csv.reader(f)

        # Skip the header row (sr.no., name, email, mobile_number)
        header = next(reader, None)
        
        user_tuples = []
        for row in reader:
            if not row:
                continue  # Skip blank rows
                
            # Map row columns safely
            try:
                sr_no = int(row[0].strip())
                name = row[1].strip()
                email = row[2].strip()
                mobile = row[3].strip() if len(row) > 3 else None
                
                user_tuples.append((sr_no, name, email, mobile))
            except (ValueError, IndexError) as e:
                print(f"тЪая╕П Skipping malformed row {row}: {e}")

        if user_tuples:
            # Bulk batch insert for optimal processing speed
            cursor.executemany("""
                INSERT OR REPLACE INTO users (sr_no, name, email, mobile_number)
                VALUES (?, ?, ?, ?)
            """, user_tuples)
            conn.commit()
            print(f"--> Successfully imported {len(user_tuples)} user records into '{DB_NAME}'.")
        else:
            print("No valid records found in the CSV file.")

def display_imported_users(conn):
    """Fetches and displays the stored database entries cleanly."""
    cursor = conn.cursor()
    cursor.execute("SELECT sr_no, name, email, mobile_number FROM users ORDER BY sr_no ASC")
    rows = cursor.fetchall()
    
    print("\n" + "="*85)
    print(f"{'SR.NO.':<8} | {'NAME':<24} | {'EMAIL':<30} | {'MOBILE NUMBER':<15}")
    print("-"*85)
    for row in rows:
        sr_no, name, email, mobile = row
        print(f"{sr_no:<8} | {name:<24} | {email:<30} | {str(mobile):<15}")
    print("="*85 + "\n")

if __name__ == '__main__':
    # Initialize connection
    db_connection = init_database()
    
    # Import data from CSV to Database and display it to confirm database contains exactly same records
    import_csv_to_db(db_connection)
    display_imported_users(db_connection)
    
    # Close the connection to avoid memory leak and resource optimization.
    db_connection.close()

