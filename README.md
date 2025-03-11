# Automated Data Cleaning Pipeline - User-Friendly Guide

This Python project offers an easy-to-use automated data cleaning pipeline powered by Pandas. It's designed to simplify and standardize your data preprocessing, saving you time and effort.

## Features

-   **Flexible Data Loading:**
    -      Supports various file formats including CSV, Excel, JSON, and Parquet.
    -      Handles common loading issues and standardizes column names.
-   **Data Validation:**
    -      Applies customizable validation rules to identify data quality issues.
    -      Checks for missing values, numeric ranges, and date formats.
-   **Modular Cleaning Pipeline:**
    -      A customizable pipeline to add and execute cleaning steps in a defined order.
    -      Includes functions for removing duplicates, standardizing dates, and cleaning text columns.
    -   Provides detailed logging of each pipeline step.
-   **Quality Metrics Generation:**
    -      Generates comprehensive data quality metrics, including row counts, missing values, unique values, and data types.
    -      Allows comparison with baseline metrics to track data changes.
-   **Standardized Text Cleaning:**
    -   Clean text columns by trimming, lowercasing, removing multiple spaces, and special characters.

## What This Tool Does

* **Reads Your Data Easily:** Handles common file types like CSV, Excel, JSON, and Parquet.
* **Checks Your Data for Errors:** Validates your data based on rules you can customize.
* **Cleans Your Data Automatically:** Removes duplicates, fixes date formats, and cleans up messy text.
* **Gives You a Data Health Report:** Provides insights into your data's quality, like missing values and data types.

## Getting Started

1.  **Download the Files:**
    * Click the "Code" button on the repository and select "Download ZIP".
    * Extract the ZIP file to a folder on your computer.
2.  **Install the Necessary Tools:**
    * You'll need Python installed. If you don't have it, download it from [python.org](https://www.python.org/downloads/).
    * Open your computer's terminal or command prompt.
    * Navigate to the folder where you extracted the files using the `cd` command (e.g., `cd path/to/your/folder`).
    * Install the required Python packages by running: `pip install pandas openpyxl pyarrow`
3.  **Put Your Data in the Right Place:**
    * Create a folder named `data` inside the project folder.
    * Place your data files (CSV, Excel, JSON, or Parquet) into the `data` folder.
4.  **Run the Cleaning Script:**
    * Open your terminal or command prompt and make sure you are still in the project folder.
    * Run the script using Python: `python your_script_name.py` (replace `your_script_name.py` with the actual name of your python file).
    * Example: If your python file is called `clean_data.py`, you would run `python clean_data.py`
5.  **See the Results:**
    * The script will print out validation results, cleaning pipeline details, and data quality metrics in your terminal.
    * You can modify the script to save the cleaned data to a new file, if you wish.

## Customizing the Cleaning Process

* **Change Validation Rules:**
    * Open the Python script in a text editor.
    * Look for the `validate_dataset` function.
    * Modify the `validation_rules` dictionary to set your own validation criteria (e.g., specific date ranges or numeric limits).
* **Add or Remove Cleaning Steps:**
    * Find the `DataCleaningPipeline` section in the script.
    * Use the `pipeline.add_step()` function to add new cleaning steps or comment out existing steps to remove them. You can add your own custom cleaning functions as well.
* **Specify Your Data File:**
    * In the `if __name__ == "__main__":` section, change the `file_path` variable to the name of your data file inside the `data` folder. For example, `file_path = "data/my_data.csv"`.

## Example (Simplified)

Let's say you have a file called `sales.csv` in the `data` folder:

1.  **Place `sales.csv` in the `data` folder.**
2.  **Run the script:** `python your_script_name.py`
3.  **The script will:**
    * Load `sales.csv`.
    * Check it for errors (according to the default or your custom rules).
    * Clean it (remove duplicates, fix dates, clean text).
    * Show you a report.

## Important Notes

* Make sure you have Python and the required packages installed.
* If you encounter any errors, double-check your file paths and installation steps.
* You can customize the script to fit your specific data cleaning needs.

## Need Help?

If you have any questions or encounter any issues, feel free to open an issue on the repository.
