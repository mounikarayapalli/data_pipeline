# Import Seaborn to access the built-in Titanic dataset
import seaborn as sns  # type: ignore[reportMissingModuleSource]


# Define a function to extract the Titanic dataset
def extract():

    # Load the Titanic dataset from Seaborn
    df = sns.load_dataset('titanic')

    # Display the total number of extracted rows and columns
    print(f"Extracted {len(df)} rows, {len(df.columns)} columns")

    # Return the extracted dataset for further processing
    return df