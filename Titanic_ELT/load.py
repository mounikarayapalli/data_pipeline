# Import datetime to record the date and time of data loading
from datetime import datetime

# Import uuid4 to generate a unique batch ID for each data load
from uuid import uuid4

# Import SQLAlchemy functions to create a database connection
from sqlalchemy import URL, create_engine

# Import MySQL database configuration from config.py
from config import DB_CONFIG


# Function to load the extracted dataset into the MySQL database
def load(df, table_name="raw_titanic"):

    # Check whether the MySQL password is provided
    if not DB_CONFIG["password"]:
        raise ValueError(
            "MYSQL_PASSWORD is not set. Set it in your VS Code terminal."
        )

    # Create the database connection URL using the configuration details
    connection_url = URL.create(
        "mysql+mysqlconnector",              # MySQL connector dialect
        username=DB_CONFIG["user"],          # MySQL username
        password=DB_CONFIG["password"],      # MySQL password
        host=DB_CONFIG["host"],              # MySQL server address
        port=DB_CONFIG["port"],              # MySQL port number
        database=DB_CONFIG["database"]       # Target database name
    )

    # Create the SQLAlchemy engine to communicate with MySQL
    engine = create_engine(connection_url)

    try:
        # Verify whether the MySQL database connection is successful
        with engine.connect():
            print("MySQL connection successful")

        # Create a copy of the original dataset to preserve raw data
        raw_data = df.copy()

        # Add a unique row number to identify each source record
        raw_data.insert(0, "source_row_id", range(1, len(raw_data) + 1))

        # Add the current date and time to track when data was loaded
        raw_data["load_timestamp"] = datetime.now()

        # Generate a unique batch ID to identify this particular data load
        raw_data["batch_id"] = str(uuid4())

        # Load the dataset into MySQL
        # if_exists="replace" replaces the existing table with the new dataset
        # index=False prevents the DataFrame index from being stored as a column
        raw_data.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False
        )

        # Display the total number of records successfully loaded
        print(
            f"Loaded {len(raw_data)} rows into '{table_name}' table"
        )

        # Display the timestamp associated with the current data load
        print("Load timestamp:", raw_data["load_timestamp"].iloc[0])

        # Display the unique batch ID associated with the current data load
        print("Batch ID:", raw_data["batch_id"].iloc[0])

    finally:
        # Close the database engine and release its resources
        engine.dispose()