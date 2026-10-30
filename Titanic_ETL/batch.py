# Import argparse to accept command-line arguments
import argparse

# Import the extraction, transformation, validation and loading functions
from extract import extract
from transform import transform
from validate import validate
from load import load


# Function to execute the ETL pipeline by processing data in smaller batches
def run_batch_pipeline(batch_size=100, table_name="passengers"):

    # Check whether the batch size is valid
    if batch_size < 1:
        raise ValueError("batch_size must be at least 1")

    # Step 1: Extract the complete raw dataset
    raw = extract()

    # Calculate the total number of rows in the dataset
    total_rows = len(raw)

    # Check whether the extracted dataset contains any records
    if total_rows == 0:
        print("No rows found; nothing to load.")
        return

    # Display the total number of records and the selected batch size
    print(f"Starting batch ETL: {total_rows} rows, batch size {batch_size}")

    # Initialize a counter to track the total number of loaded rows
    loaded_rows = 0

    # Step 2: Divide the dataset into smaller batches and process them one by one
    for batch_number, start in enumerate(
        range(0, total_rows, batch_size), start=1
    ):

        # Select the required number of rows for the current batch
        batch = raw.iloc[start:start + batch_size].copy()

        # Display the current batch number and its row range
        print(
            f"\nProcessing batch {batch_number}: "
            f"rows {start + 1}-{start + len(batch)}"
        )

        # Step 3: Clean and transform the current batch
        clean_batch = transform(batch)

        # Step 4: Validate the transformed batch to check data quality
        validate(clean_batch)

        # Step 5: Select the loading mode based on the current batch
        # Replace the table for the first batch to avoid retaining old data
        # Append subsequent batches to the existing table
        mode = "replace" if batch_number == 1 else "append"

        # Load the cleaned and validated batch into the MySQL database
        load(
            clean_batch,
            table_name=table_name,
            if_exists=mode
        )

        # Update the total number of successfully processed rows
        loaded_rows += len(clean_batch)

    # Display the final loading summary after processing all batches
    print(
        f"\nBatch ETL completed. Loaded {loaded_rows} "
        f"rows into '{table_name}'."
    )


# Execute the batch pipeline only when this file is run directly
if __name__ == "__main__":

    # Create an argument parser to accept inputs from the command line
    parser = argparse.ArgumentParser(
        description="Run Titanic ETL with batch processing."
    )

    # Accept the batch size from the user; default value is 100 rows
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Number of rows per batch (default: 100)"
    )

    # Accept the destination MySQL table name; default is passengers
    parser.add_argument(
        "--table",
        default="passengers",
        help="Destination MySQL table (default: passengers)"
    )

    # Read and store the command-line arguments
    args = parser.parse_args()

    # Run the batch ETL pipeline using the provided arguments
    run_batch_pipeline(
        batch_size=args.batch_size,
        table_name=args.table
    )