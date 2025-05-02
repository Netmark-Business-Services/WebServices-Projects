import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# File paths
file1 = ''  # Contains supplier NPI, location name, address, and ContractTypeName
file2 = ''  # Contains supplier NPI, location name, address, and HCC ID
output_file = ''

# Check if files exist
if not os.path.exists(file1):
    raise FileNotFoundError(f"File not found: {file1}")
if not os.path.exists(file2):
    raise FileNotFoundError(f"File not found: {file2}")

# Load Excel files
logging.info("Loading Excel files...")
df1 = pd.read_excel(file1, header=0)  # Assume headers exist
df2 = pd.read_excel(file2, header=0)  # Assume headers exist

# Define column indices for file1
FILE1_SUPPLIER_NPI = 0
FILE1_SUPPLIER_LOCATION_NAME = 1
FILE1_SUPPLIER_ADDRESS = 2
FILE1_CONTRACT_TYPE = 3

# Define column indices for file2
FILE2_SUPPLIER_NPI = 0
FILE2_SUPPLIER_LOCATION_NAME = 1
FILE2_SUPPLIER_ADDRESS = 2
FILE2_SUPPLIER_HCC_ID = 3

# Prepare output data
output_data = []

# Filter file1 rows where ContractTypeName is 'PrimaryCareProvider'
df1_filtered = df1[df1.iloc[:, FILE1_CONTRACT_TYPE] == 'PrimaryCareProvider']

# Create a complete address for file1
df1_filtered['complete_address'] = df1_filtered.iloc[:, FILE1_SUPPLIER_LOCATION_NAME] + '-' + df1_filtered.iloc[:, FILE1_SUPPLIER_ADDRESS]

# Create a complete address for file2
df2['complete_address'] = df2.iloc[:, FILE2_SUPPLIER_LOCATION_NAME] + '-' + df2.iloc[:, FILE2_SUPPLIER_ADDRESS]

# Process each row in file2
logger.info("Starting row-by-row comparison...")
for index2, row2 in df2.iterrows():
    supplier_hcc_id = row2.iloc[FILE2_SUPPLIER_HCC_ID]
    supplier_npi = row2.iloc[FILE2_SUPPLIER_NPI]
    complete_address2 = row2['complete_address']

    # Initialize status as 'Not a Match'
    status = 'Not a Match'

    # Compare with each row in filtered file1
    for index1, row1 in df1_filtered.iterrows():
        supplier_npi1 = row1.iloc[FILE1_SUPPLIER_NPI]
        complete_address1 = row1['complete_address']

        # Log the comparison
        logger.info(
            f"Comparing File2 Row {index2} (NPI: {supplier_npi}, Address: {complete_address2}) "
            f"with File1 Row {index1} (NPI: {supplier_npi1}, Address: {complete_address1})"
        )

        # Check for match
        if supplier_npi == supplier_npi1 and complete_address2 == complete_address1:
            status = 'Matched'
            logger.info(f"Match found for HCC ID {supplier_hcc_id} (NPI: {supplier_npi}, Address: {complete_address2})")
            break  # No need to check further once a match is found

    # Append result to output_data
    output_data.append([supplier_hcc_id, supplier_npi, complete_address2, status])

# Convert output data to DataFrame
output_df = pd.DataFrame(output_data)

# Save the results to an Excel file
logger.info(f"Saving comparison results to {output_file}...")
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    output_df.to_excel(writer, index=False, sheet_name='Comparison Results')

logger.info(f"Comparison completed. Results saved to {output_file}.")