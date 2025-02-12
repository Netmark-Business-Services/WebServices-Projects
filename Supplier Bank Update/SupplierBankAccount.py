import os
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import time


os.makedirs('logs', exist_ok=True)


vendor_update_file = 'Input_File' 
df_vendor_update = pd.read_excel(vendor_update_file, dtype=str)

vendor_info_file = 'Information_File' 
df_vendor_info = pd.read_excel(vendor_info_file, dtype=str)

df_vendor_update['VendorNumber'] = df_vendor_update['VendorNumber'].str.strip()
df_vendor_update['Supplier Name'] = df_vendor_update['Supplier Name'].str.strip()

df_vendor_info['VendorNumber'] = df_vendor_info['VendorNumber'].str.strip()
df_vendor_info['VendorName'] = df_vendor_info['VendorName'].str.strip()

df_matched = pd.merge(df_vendor_update, df_vendor_info, on='VendorNumber', how='left')

df_matched['Name_Match'] = df_matched.apply(lambda row: row['Supplier Name'] == row['VendorName'], axis=1)

df_name_mismatch = df_matched[df_matched['Name_Match'] == False]  
df_name_match = df_matched[df_matched['Name_Match'] == True] 

print("Mismatched rows between Supplier Name and VendorName:")
print(df_name_mismatch[['VendorNumber', 'Supplier Name', 'VendorName']])

print(f"Number of rows with correct VendorNumber and Name match: {len(df_name_match)}")
print(df_name_match.head())

environments = {
    "UAT": {
        "url": "https://gchp-con-ut01.gchp.local:9193/connector/services/v5/PayeeBankAccount",
        "log_file": "response.txt"
    },
    "PreProd": {
        "url": "https://gchp-lb-pp01.gchp.local:9193/connector/services/v5/PayeeBankAccount",
        "log_file": "response.txt"
    },
    "Prod": {
        "url": "https://gchp-lb-pr01.gchp.local:5559/connector/services/v5/PayeeBankAccount",
        "log_file": "response.txt"
    }
}

username = "username"
password = "password"

current_env = os.getenv('ENV', 'env')

if current_env not in environments:
    raise ValueError(f"Unknown environment: {current_env}")

config = environments[current_env]
url = config["url"]
log_file = config["log_file"]


with open(log_file, 'w') as response_file:
   
    for index, row in df_name_match.iterrows():
        VendorNumber = row['VendorNumber']
        VendorName = row['VendorName']
        NPI = row['NPI_x'] 
        MethodOfPayment = row['MethodOfPayment']
        AccountNumber = row['AccountNumber']
        RoutingNumber = row['RoutingNumber']
        BankName = row['BankName']
        AccountName = row['AccountName']
        
       
        AccountName = AccountName.strip().replace("&", "")

        
        soap_body = f"""<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pay="http://www.healthedge.com/connector/schema/payeebankaccounts">
           <soapenv:Header/>
           <soapenv:Body>
              <pay:payeeBankAccounts>
              <bankAccountId>{VendorNumber}-1</bankAccountId>
                 <payee>            
                    <payeeSupplierHccId>{VendorNumber}</payeeSupplierHccId>
                 </payee>
                 <payeeBankAccountDateRange>
                    <startDate>1800-01-01</startDate>
                    <endDate>3000-01-01</endDate>
                    <routingNumber>{RoutingNumber}</routingNumber>
                    <accountNumber>{AccountNumber}</accountNumber>                          
                        <countryCode>
                            <countryCode>US</countryCode>
                        </countryCode>
                    <accountOwner>{AccountName}</accountOwner>
                    <bankAccountType>
                       <codeSetName>BankAccountType</codeSetName>
                       <codeEntry>C</codeEntry>                                  
                    </bankAccountType>
                 </payeeBankAccountDateRange>
                 <maintenanceComment>Updated Bank Info</maintenanceComment>
                 <maintenanceReasonCode>
                    <codeSetName>PayeeBankAccountsCreateReason</codeSetName>
                    <codeEntry>1</codeEntry>            
                 </maintenanceReasonCode>
              </pay:payeeBankAccounts>
           </soapenv:Body>
        </soapenv:Envelope>
        """
       
        soap_body = soap_body.strip().encode('utf-8')
       
        headers = {'Content-Type': 'text/xml; charset=utf-8'}
        response = requests.post(url, data=soap_body, headers=headers, auth=HTTPBasicAuth(username, password), verify=False)
       
        response_file.write(f"Response for Vendor {VendorName}-{VendorNumber}:\n")
        response_file.write(response.text + "\n\n")
       
        print(f"Response for Vendor {VendorName}-{VendorNumber}:")
        print(response.text)
        
        time.sleep(2)

print(f"All requests for {current_env} have been sent and responses have been written to '{log_file}'.")
