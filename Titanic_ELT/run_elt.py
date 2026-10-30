# Import Path to work with file and folder paths
from pathlib import Path

# Import MySQL connector to connect and execute SQL commands
import mysql.connector

# Import database configuration from config.py
from config import DB_CONFIG

# Import the extraction function from extract.py
from extract import extract

# Import the loading function from load.py
from load import load


# Get the directory path where the current Python file is located
BASE_DIR = Path(__file__).resolve().parent


# List of SQL files to execute in the correct pipeline order
SQL_FILES = [
    "create_staging.sql",       # Create the staging table
    "transform_data.sql",       # Transform the raw data
    "create_analytics.sql",     # Create analytics tables
    "data_quality.sql",         # Perform data quality checks
]


# Function to read and execute SQL statements from a file
def run_sql_file(cursor, file_name):
    """Execute all SQL statements in one file."""

    # Construct the complete path of the SQL file
    file_path = BASE_DIR / "sql" / file_name

    # Check whether the SQL file exists
    if not file_path.exists():
        raise FileNotFoundError(f"SQL file not found: {file_path}")

    # Read the SQL file content using UTF-8 encoding
    sql_text = file_path.read_text(encoding="utf-8")

    # Remove standalone SQL comment lines to avoid executing them
    lines = [
        line for line in sql_text.splitlines()
        if not line.strip().startswith("--")
    ]

    # Join the remaining lines and separate SQL statements using semicolons
    statements = "\n".join(lines).split(";")

    # Execute each SQL statement one by one
    for statement in statements:
        statement = statement.strip()

        # Execute only non-empty SQL statements
        if statement:
            cursor.execute(statement)

            # Fetch and clear results if the SQL statement returns rows
            if cursor.with_rows:
                cursor.fetchall()

    # Display a success message after executing the SQL file
    print(f"PASS: {file_name} executed successfully")


# Function to display the results of all data quality checks
def print_quality_results(cursor):
    """Print PASS or FAIL for every data quality check."""

    # Retrieve the check names and their execution status
    cursor.execute("""
        SELECT check_name, status
        FROM dq_results
        ORDER BY check_name
    """)

    # Store all data quality results
    results = cursor.fetchall()

    # Check whether any data quality results are available
    if not results:
        print("FAIL: No data quality results found.")
        return False

    # Assume all checks passed initially
    all_passed = True

    # Display the data quality report heading
    print("\n--- DATA QUALITY RESULTS ---")

    # Display each check name along with its PASS or FAIL status
    for check_name, status in results:
        print(f"{status}: {check_name}")

        # Mark the overall result as failed if any check fails
        if status != "PASS":
            all_passed = False

    # Display the final data quality status
    print("----------------------------")
    print("Overall:", "PASS" if all_passed else "FAIL")

    # Return the overall data quality result
    return all_passed


# Main function to execute the complete ELT pipeline
def run_elt():

    # Initialize database connection and cursor variables
    connection = None
    cursor = None

    try:
        # Display the pipeline starting message
        print("Starting Titanic ELT pipeline...\n")

        # Step 1: Extract the Titanic dataset from the source
        raw_data = extract()

        # Step 2: Load the extracted raw data into the MySQL database
        load(raw_data)

        # Display a success message after extraction and loading
        print("\nPASS: Extraction and loading completed")

        # Step 3: Establish a connection with the MySQL database
        connection = mysql.connector.connect(**DB_CONFIG)

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # Step 4: Execute all SQL files in the specified order
        for file_name in SQL_FILES:
            run_sql_file(cursor, file_name)

        # Step 5: Display the results of the five data quality checks
        print_quality_results(cursor)

        # Display the pipeline completion message
        print("\nELT pipeline finished.")

    except Exception as error:

        # Display an error message if any pipeline step fails
        print(f"\nFAIL: ELT pipeline stopped: {error}")

        # Raise the exception again to make the failure visible
        raise

    finally:

        # Close the database cursor if it was created
        if cursor is not None:
            cursor.close()

        # Close the database connection if it is still active
        if connection is not None and connection.is_connected():
            connection.close()


# Execute the ELT pipeline only when this file is run directly
if __name__ == "__main__":
    run_elt()