import seaborn as sns  # type: ignore[reportMissingModuleSource]
# Seaborn is used to access the built-in Titanic dataset.


def extract():
    # Load the Titanic dataset from Seaborn
    df = sns.load_dataset("titanic")

    # Display the total number of rows and columns extracted
    print(f"Extracted {len(df)} rows and {len(df.columns)} columns")

    # Display the names of all columns in the original dataset
    print("Original columns:", df.columns.tolist())

    # Return the extracted dataset
    return df


# Execute the extraction function only when this file is run directly
if __name__ == "__main__":
    # Store the extracted dataset in raw_data
    raw_data = extract()

    # Display the first five rows of the extracted dataset
    print(raw_data.head())