import os
import re
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import logging
from datetime import datetime
import xml.etree.ElementTree as ET

# Define environment configurations
# Define environment configurations
environments = {
    "PROD": {
        "url": "https://gchp-lb-pr01.gchp.local:5559/connector/services/classic/PayableServiceStronglyTyped",
        "username": "username",
        "password": "password"
        }
    }

# Determine the base directory of the script
base_dir = os.path.dirname(__file__)

# Ensure the logs directory exists
os.makedirs(os.path.join(base_dir, 'logs'), exist_ok=True)

# Set up logging
log_filename = os.path.join(base_dir, 'logs', f'supplier_payable_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# SOAP Client for Supplier Payable
class SupplierPayableClient:
    def __init__(self, environment="PROD"):
        # Load configuration for the specified environment
        self.config = environments[environment]
        self.url = self.config["url"]
        self.username = self.config["username"]
        self.password = self.config["password"]

        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(self.username, self.password)
        self.session.verify = False
        self.headers = {
            'Content-Type': 'text/xml;charset=UTF-8',
            'SOAPAction': ''
        }
    def create_supplier_payable(self, supplier_hcc_id, amount, release_date, payable_type, payment_cycle_id, bank_account_name, reason_code):
        try:
            # Construct the SOAP request body
            soap_body = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:heal="http://healthedge.com">
   <soapenv:Header/>
   <soapenv:Body>
      <heal:createSupplierPayable>
         <supplierPayable>
            <payableAmount>{amount}</payableAmount>
            <releaseDate>{release_date}</releaseDate>
            <payableType>{payable_type}</payableType>
            <paymentCycleID>{payment_cycle_id}</paymentCycleID>
            <supplierHccID>{supplier_hcc_id}</supplierHccID>
            <bankAccountName>{bank_account_name}</bankAccountName>
            <reasonCode>{reason_code}</reasonCode>
         </supplierPayable>
      </heal:createSupplierPayable>
   </soapenv:Body>
</soapenv:Envelope>"""

            # Write the request to the request log file
            with open(os.path.join(base_dir, 'logs', 'request_log.txt'), 'a', encoding='utf-8') as req_log:
                req_log.write(f"\nRequest for Supplier HCC ID {supplier_hcc_id}:\n{soap_body}\n")

            # Send the SOAP request
            logger.info(f"Sending request for Supplier HCC ID: {supplier_hcc_id}")
            response = self.session.post(self.url, data=soap_body.encode('utf-8'), headers=self.headers)

            # Write the response to the response log file
            with open(os.path.join(base_dir, 'logs', 'response_log.txt'), 'a', encoding='utf-8') as res_log:
                res_log.write(f"\nResponse for Supplier HCC ID {supplier_hcc_id}:\n{response.text}\n")

            # Parse the response for payableIdentifier
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                ns = {'ns2': 'http://healthedge.com'}
                payable_identifier = root.find('.//ns2:payableIdentifier', ns)
                if payable_identifier is not None:
                    return supplier_hcc_id, payable_identifier.text

            return supplier_hcc_id, None

        except Exception as e:
            logger.error(f"Error processing Supplier HCC ID {supplier_hcc_id}: {str(e)}")
            return supplier_hcc_id, None

# Function to parse responses and segregate into success and error
def parse_responses(response_file):
    success_data = []
    error_data = []

    with open(response_file, 'r', encoding='utf-8') as file:
        response_lines = file.read().split('Response for Supplier HCC ID')

        for block in response_lines[1:]:  # Skip the first split (empty before the first response)
            try:
                supplier_id_line, response_body = block.strip().split(':', 1)
                supplier_hcc_id = supplier_id_line.strip()

                # Check for the payableIdentifier tag
                if '<payableIdentifier>' in response_body:
                    payable_identifier = re.search(r'<payableIdentifier>(.*?)</payableIdentifier>', response_body)
                    if payable_identifier:
                        success_data.append({
                            'Supplier HCC ID': supplier_hcc_id,
                            'Payable Identifier': payable_identifier.group(1)
                        })
                else:
                    # Extract faultstring for errors
                    fault_string_match = re.search(r'<faultstring>\{(.*?)\}</faultstring>', response_body, re.DOTALL)
                    fault_string = fault_string_match.group(1) if fault_string_match else 'Unknown error'
                    error_data.append({
                        'Supplier HCC ID': supplier_hcc_id,
                        'Error': fault_string
                    })
            except Exception as e:
                logger.error(f"Failed to parse block: {block[:100]}\nError: {str(e)}")

    return success_data, error_data

# Main execution function
def main():
    try:
        # Set the environment (default to UAT)
        current_env = os.getenv('ENV', 'PROD')

        # Log the chosen environment
        logger.info(f"Starting Supplier Payable Client in {current_env} environment")

        # Initialize the SOAP client with the selected environment
        client = SupplierPayableClient(environment=current_env)

        # Correctly construct the file paths for input files
        supplier_data_file = os.path.join(base_dir, 'TRI Payable Entry PROD - 12-24.xlsx')
        reason_code_file = os.path.join(base_dir, 'TRI Payable Entry PROD - 12-24.xlsx')

        # Read supplier data from Excel file
        logger.info(f"Reading supplier data from {supplier_data_file}")
        df_supplier_data = pd.read_excel(supplier_data_file, sheet_name='Sheet1', dtype=str)

        # Read reason code mapping from another sheet
        logger.info(f"Reading reason code mapping from {reason_code_file}")
        df_reason_mapping = pd.read_excel(reason_code_file, sheet_name='Sheet2', dtype=str)

        # Create a mapping dictionary for faster lookup
        reason_mapping = dict(zip(df_reason_mapping['ADJUSTMENT_PAYABLE_REASON_CODE'], df_reason_mapping['ADJUSTMENT_PAYABLE_REASON']))

        # Strip whitespaces from column names
        df_supplier_data.columns = df_supplier_data.columns.str.strip()

        # Log the column names for debugging
        logger.info(f"Columns in the file: {list(df_supplier_data.columns)}")

        # Prepare lists to store responses
        for _, row in df_supplier_data.iterrows():
            supplier_hcc_id = row['Supplier HCC ID']
            amount = round(float(row['Amount']), 2)  # Round to two decimal places
            release_date = pd.to_datetime(row['Release Date']).strftime('%Y-%m-%d')  # Format date
            payable_type = row['Payable Type']
            payment_cycle_id = row['Payment Cycle ID']
            bank_account_name = row['Bank Account Name']

            # Map reason code
            reason_description = row['Reason Code']
            reason_code = reason_mapping.get(reason_description, 'Unknown')  # Default to 'Unknown' if not found

            #description = "This is Early Payment"

            client.create_supplier_payable(
                supplier_hcc_id, amount, release_date, payable_type, payment_cycle_id, bank_account_name, reason_code#, description
            )

        # Process the responses from the response log
        response_file = os.path.join(base_dir, 'logs', 'response_log.txt')
        logger.info(f"Reading response data from {response_file}")

        successful_responses, error_responses = parse_responses(response_file)

        # Write successful responses to an Excel file
        success_output_file = os.path.join(base_dir, 'logs', 'successful_payables.xlsx')
        pd.DataFrame(successful_responses).to_excel(success_output_file, index=False)
        logger.info(f"Successful payables written to {success_output_file}")

        # Write error responses to an Excel file
        error_output_file = os.path.join(base_dir, 'logs', 'error_payables.xlsx')
        pd.DataFrame(error_responses).to_excel(error_output_file, index=False)
        logger.info(f"Error payables written to {error_output_file}")

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise
if __name__ == "__main__":
    main()
