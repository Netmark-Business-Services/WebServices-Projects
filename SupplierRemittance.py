import os
import requests
import logging
import pandas as pd
from openpyxl import load_workbook
from requests.auth import HTTPBasicAuth
from datetime import datetime


log_file = os.getenv('LOG_FILE')
logging.basicConfig(filename=log_file, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def convert_date_format(date_str):
    if not date_str:
        return None  
    try:
        return datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
    except ValueError:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
        except ValueError:
            logging.error(f"Unknown date format: {date_str}")
            return None  


current_env = os.getenv('ENV', 'UAT')  


environments = {
    "UAT": {
        "url": "https://gchp-con-ut01.gchp.local:9193/connector/services/classic/ProviderMaintenanceServiceStronglyTyped",
        "username": os.getenv('UAT_USERNAME'),
        "password": os.getenv('UAT_PASSWORD'),
        "log_file": "YOUR_LOG_PATH",
        "summary_file": "YOUR_SUMMARY_FILE"
    }
    
}

if current_env not in environments:
    logging.error(f"Invalid environment selected: {current_env}")
    raise ValueError(f"Invalid environment: {current_env}")

env_config = environments[current_env]

def send_request(payload):
    try:
        response = requests.post(
            env_config["url"],
            json=payload,
            auth=HTTPBasicAuth(env_config["username"], env_config["password"]),
            verify=False,  
            timeout=30
        )
        response.raise_for_status()
        logging.info(f"Request successful: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None


def process_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        
        if 'DateColumn' in df.columns:
            df['DateColumn'] = df['DateColumn'].apply(convert_date_format)
        
        for index, row in df.iterrows():
            payload = {
                "supplier_id": row.get("SupplierID", ""),
                "remittance_amount": row.get("Amount", 0),
                "date": row.get("DateColumn", "")
            }
            response = send_request(payload)
            
            with open(env_config["log_file"], "a") as log_f:
                log_f.write(f"{datetime.now()} - Request: {payload} - Response: {response}\n")
        
        logging.info("Excel processing completed.")
    except Exception as e:
        logging.error(f"Error processing Excel file: {e}")

file_path = "INPUT_FILE"
process_excel(file_path)
