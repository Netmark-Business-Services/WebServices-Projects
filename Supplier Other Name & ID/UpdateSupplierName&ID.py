import os
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import time
from datetime import datetime

os.makedirs('logs', exist_ok=True)

supplier_data_file = 'Input_File'
df_supplier_data = pd.read_excel(supplier_data_file, dtype=str)

df_supplier_data['Supplier ID'] = df_supplier_data['Supplier ID'].str.strip()
df_supplier_data['Organization Name'] = df_supplier_data['Organization Name'].str.strip()
df_supplier_data['Identification Number'] = df_supplier_data['Identification Number'].str.strip()
df_supplier_data['Payment Type'] = df_supplier_data['Payment Type'].str.strip()
df_supplier_data['NPI'] = df_supplier_data['NPI'].str.strip()
df_supplier_data['Date'] = df_supplier_data['Date'].str.strip()

environments = {
    "UAT": {
        "url": "https://gchp-con-ut01.gchp.local:9193/connector/services/classic/ProviderMaintenanceServiceStronglyTyped",
        "username": "username",
        "password": "password",
        "log_file": "Responses.txt",
    },
    "Prod": {
        "url": "https://gchp-con-pr01.gchp.local:5559/connector/services/classic/ProviderMaintenanceServiceStronglyTyped",
        "username": "username",
        "password": "password",
        "log_file": "Responses.txt",
    },
}

current_env = os.getenv('ENV', 'env')

if current_env not in environments:
    raise ValueError(f"Unknown environment: {current_env}")

config = environments[current_env]
url = config["url"]
username = config["username"]
password = config["password"]
log_file = config["log_file"]

log_directory = os.path.dirname(log_file)
os.makedirs(log_directory, exist_ok=True)

with open(log_file, 'w') as response_file:
    for index, row in df_supplier_data.iterrows():
        supplier_id = row['Supplier ID']
        organization_name = row['Organization Name']
        identification_number = row['Identification Number']
        npi = row['NPI']
        payment_type = row['Payment Type']
        
        raw_date = row['Date']
        as_of_date = pd.to_datetime(row['Date']).strftime('%Y-%m-%d')  
        
        soap_body = f"""<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:heall="http://healthedge.com">
           <soapenv:Header/>
           <soapenv:Body>
              <ns0:createSupplier xmlns:ns0="http://healthedge.com">
                 <supplier>
                    <assignHccIdentifier>{supplier_id}</assignHccIdentifier>
                    <organization operation="merge">
                       <otherNames>
                          <otherOrganizationNameUsed>
                             <organizationName>{organization_name}</organizationName>
                             <otherNameType>
                                <id>Trading Partner</id>
                                <type>OrganizationOtherNameType</type>
                             </otherNameType>
                          </otherOrganizationNameUsed>
                       </otherNames>
                    </organization>
                    <otherIdList operation="merge">
                       <otherIdEntry>
                          <identificationNumber>{identification_number}</identificationNumber>
                          <identificationType>
                             <id>Electronic Transmitter ID</id>
                             <type>IdentificationType</type>
                          </identificationType>
                       </otherIdEntry>
                    </otherIdList>
                    <remittanceType operation="merge">
                       <id>{payment_type}</id>
                       <type>RemittanceType</type>
                    </remittanceType>
                    <npi>{npi}</npi>
                 </supplier>
                 <asOfDate>{as_of_date}</asOfDate>
              </ns0:createSupplier>
           </soapenv:Body>
        </soapenv:Envelope>
        """

        soap_body = soap_body.strip().encode('utf-8')

        headers = {'Content-Type': 'text/xml; charset=utf-8'}
        response = requests.post(url, data=soap_body, headers=headers, auth=HTTPBasicAuth(username, password), verify=False)

        response_file.write(f"Response for Supplier {organization_name} ({supplier_id}):\n")
        response_file.write(response.text + "\n\n")

        print(f"Response for Supplier {organization_name} ({supplier_id}):")
        print(response.text)

        time.sleep(2)

print(f"All requests for {current_env} have been sent and responses have been written to '{log_file}'.")
