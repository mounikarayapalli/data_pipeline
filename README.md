<<<<<<< HEAD
# Titanic Data Engineering Project – ETL & ELT Pipelines

A practical data engineering project that implements and compares **ETL (Extract, Transform, Load)** and **ELT (Extract, Load, Transform)** workflows using Python, MySQL, and SQL.

## 📌 About the Project

This project focuses on understanding how data moves through a data pipeline, starting from extraction and ending with cleaned, validated, and analysis-ready data.

Using the Titanic dataset, I implemented two separate pipelines to explore how data can be processed using Python and SQL.

The project includes:

- **ETL Pipeline:** Data is extracted, cleaned, validated, and then stored in MySQL.
- **ELT Pipeline:** Raw data is first stored in MySQL, and the transformations are performed later using SQL.

The goal is to gain hands-on experience with different data engineering approaches, database operations, pipeline automation, and data quality validation.

## 📁 Repository Structure

```text
data_pipeline/
│
├── Titanic_ETL/
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   ├── load.py
│   ├── pipeline.py
│   ├── batch.py
│   └── ETL.ipynb
│
├── Titanic_ELT/
│   ├── extract.py
│   ├── load.py
│   ├── config.py
│   ├── run_elt.py
│   │
│   └── sql/
│       ├── create_staging.sql
│       ├── transform_data.sql
│       ├── create_analytics.sql
│       └── data_quality.sql
│
├── requirements.txt
├── .gitignore
├── ELT.txt
└── README.md
```

## 🧰 Tools and Technologies

| Technology | Usage in the Project |
|---|---|
| Python | Building and running data pipelines |
| Pandas | Data manipulation and preprocessing |
| Seaborn | Accessing the Titanic dataset |
| MySQL | Storing raw and processed data |
| SQL | Data transformation and analysis |
| SQLAlchemy | Database connection and data loading |
| MySQL Connector | Connecting Python with MySQL |
| MySQL Workbench | Database administration and query execution |
| Git & GitHub | Source code management |
| VS Code | Development environment |

---

## 1. ETL Implementation

**ETL – Extract, Transform, Load**

In the ETL approach, the data is processed and cleaned using Python before it is stored in the target MySQL database.

### Pipeline Flow

```text
        Titanic Dataset
               |
               v
           Extraction
               |
               v
          Transformation
               |
               v
           Validation
               |
               v
              Loading
               |
               v
          MySQL Database
```

### What happens in this pipeline?

| Stage | Implementation |
|---|---|
| Extract | Fetch the Titanic dataset using Seaborn. |
| Transform | Handle missing values and clean the dataset using Python. |
| Validate | Check data quality and verify the transformed records. |
| Load | Insert the cleaned data into MySQL. |

### Python Modules

- `extract.py` – Retrieves the original Titanic dataset.
- `transform.py` – Handles data cleaning and preprocessing.
- `validate.py` – Performs validation checks on the transformed data.
- `load.py` – Stores the processed records in MySQL.
- `pipeline.py` – Runs the complete ETL process.
- `batch.py` – Processes and loads data in smaller batches.

---

## 2. ELT Implementation

**ELT – Extract, Load, Transform**

Unlike ETL, this approach stores the original data in MySQL first. The cleaning, transformation, and analytical operations are then performed directly inside the database using SQL.

### Pipeline Flow

```text
        Titanic Dataset
               |
               v
           Extraction
               |
               v
              Loading
               |
               v
          raw_titanic
               |
               v
          stg_titanic
               |
               v
        clean_passengers
               |
               v
          Analytics Views
               |
               v
        Data Quality Checks
```

### Implementation Details

**Step 1 – Data Extraction**

- Retrieved the Titanic dataset using Seaborn.
- Extracted 891 records containing 15 original columns.

**Step 2 – Raw Data Loading**

- Loaded the original dataset into the `raw_titanic` table.
- Added three metadata columns:
  - `source_row_id` – Identifies individual source records.
  - `load_timestamp` – Records when the data was loaded.
  - `batch_id` – Identifies the current data loading batch.
- Kept the original source values unchanged during the Python loading process.

**Step 3 – SQL Transformations**

Performed the following operations inside MySQL:

- Handled missing age values using passenger-class and sex-based averages.
- Replaced missing embarkation values with the most frequently occurring value.
- Converted sex values into numerical format (male = 0, female = 1).
- Created age categories: Child, Teen, Adult, and Senior.
- Calculated passenger family size.
- Identified passengers travelling alone.
- Classified fares into Low, Medium, High, and Premium categories using quartiles.

**Step 4 – Analytical Views**

Created three SQL views to understand passenger survival patterns and fare distribution.

| View Name | Description |
|---|---|
| `vw_survival_by_class_sex` | Compares survival rates across passenger classes and sexes. |
| `vw_survival_by_age_group` | Examines survival patterns across different age groups. |
| `vw_top3_fares_per_class` | Finds the three highest fares within each passenger class. |

**Step 5 – Data Quality Validation**

Implemented five SQL-based checks to verify the transformed dataset.

| No. | Validation Check | Expected Condition |
|---|---|---|
| 1 | Age validation | Age values must be between 0 and 100. |
| 2 | Source ID validation | Source row IDs must be unique and non-NULL. |
| 3 | Missing value validation | Age and embarked columns must not contain NULL values. |
| 4 | Row count validation | Raw and clean tables must have matching row counts. |
| 5 | Sex encoding validation | Sex values must contain only 0 and 1. |

---

## ⚙️ Running the ELT Pipeline

The `run_elt.py` module acts as the main execution file for the ELT workflow.

It automates the following tasks:

1. Extracts the Titanic dataset.
2. Loads the original records into MySQL.
3. Executes the SQL scripts in the required sequence.
4. Creates staging and transformed tables.
5. Generates analytical views.
6. Executes the data quality checks.
7. Displays individual PASS/FAIL results and the overall status.

**Run the pipeline using:**

```bash
python run_elt.py
```

### Expected Execution Results

- 891 records extracted from the Titanic dataset.
- 891 records loaded into `raw_titanic`.
- Staging and clean tables created.
- Three analytical views generated.
- Five data quality checks executed.

**Latest successful run:** All five data quality checks returned PASS.

---

## 🚀 Getting Started

Follow these steps to set up and execute the project locally.

### Prerequisites

Make sure you have installed:

- Python 3.x
- MySQL Server
- MySQL Workbench
- Visual Studio Code
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/mounikarayapalli/data_pipeline.git
```

### 2. Open the Project Directory

```bash
cd data_pipeline
```

### 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 4. Create the MySQL Database

Open MySQL Workbench and execute:

```sql
CREATE DATABASE IF NOT EXISTS titanic_db;
```

### 5. Configure Database Credentials

Set your MySQL password as an environment variable.

**For Windows PowerShell:**

```powershell
$env:MYSQL_PASSWORD = "YOUR_MYSQL_PASSWORD"
```

Make sure the database configuration in `Titanic_ELT/config.py` and the ETL configuration matches your local MySQL setup.

### 6. Execute the ELT Pipeline

```bash
cd Titanic_ELT
python run_elt.py
```

The script will automatically execute extraction, raw data loading, SQL transformations, analytics creation, and data quality validation.

---

## 🔍 ETL vs ELT – What I Observed

Both approaches perform similar data engineering tasks, but they differ in where and when transformations take place.

| Comparison | ETL | ELT |
|---|---|---|
| Full Form | Extract, Transform, Load | Extract, Load, Transform |
| Transformation Stage | Before loading | After loading |
| Main Processing Tool | Python | SQL |
| Raw Data Storage | Depends on implementation | Preserved in the raw table |
| Database Responsibility | Stores processed data | Stores and transforms data |
| Key Advantage | Data is cleaned before storage | Uses database processing capabilities |

## 📚 What I Learned

Working on this project helped me understand and practise several data engineering concepts:

- Difference between ETL and ELT architectures.
- Extracting datasets using Python and Seaborn.
- Data manipulation and preprocessing with Pandas.
- Connecting Python applications to MySQL.
- Writing SQL queries for data transformation.
- Handling missing values and categorical encoding.
- Creating analytical views for reporting.
- Implementing data quality validation checks.
- Automating pipeline execution using Python.
- Processing records using batch-based ETL.
- Managing project files using Git and GitHub.

## 👩‍💻 Author

**Mounika Rayapalli**

B.Tech – Computer Science and Engineering

GitHub: [mounikarayapalli](https://github.com/mounikarayapalli)

Project Repository: [data_pipeline](https://github.com/mounikarayapalli/data_pipeline)

---

⭐ *A hands-on project exploring how Python and SQL can work together to build, automate, and validate data pipelines using ETL and ELT approaches.*
=======
# data_pipeline
>>>>>>> 46045c7fa673a85a1992436b2a4094a254e62e68
