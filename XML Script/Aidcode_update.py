import os
import shutil
import re
import pandas as pd

# Define the paths
source_folder = 'C:/Users/kvelinedi/OneDrive - Gold Coast Health Plan/Documents/GoldCoast Onsite Task/Member Aid Code Changes/EnrollmentSparse_July5'
reinstate_folder = os.path.join(source_folder, 'Reinstate_July-5')
change_folder = os.path.join(source_folder, 'Change_July-5')
create_folder = os.path.join(source_folder, 'Create_July-5')
others_folder = os.path.join(source_folder, 'Others_July-5')

# Create subfolders if they don't exist
os.makedirs(reinstate_folder, exist_ok=True)
os.makedirs(change_folder, exist_ok=True)
os.makedirs(create_folder, exist_ok=True)
os.makedirs(others_folder, exist_ok=True)

# List to store maintenanceTypeCode and hccIdentifier
data = []

# Function to extract relevant data using regex
def process_xml_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        
    # Regex patterns to find maintenanceTypeCode and hccIdentifier
    maintenance_type_code_match = re.search(r'<maintenanceTypeCode>(.*?)</maintenanceTypeCode>', content)
    hcc_identifier_match = re.search(r'<hccIdentifier>(.*?)</hccIdentifier>', content)
    
    maintenance_type_code = maintenance_type_code_match.group(1) if maintenance_type_code_match else "not found"
    hcc_identifier = hcc_identifier_match.group(1) if hcc_identifier_match else "not found"
    
    data.append({'fileName': os.path.basename(file_path), 'maintenanceTypeCode': maintenance_type_code, 'hccIdentifier': hcc_identifier})
    
    # Move file to respective folder
    if maintenance_type_code == 'REINSTATEMENT':
        shutil.move(file_path, reinstate_folder)
    elif maintenance_type_code == 'CHANGE':
        shutil.move(file_path, change_folder)
    elif maintenance_type_code == 'CREATE':
        shutil.move(file_path, create_folder)
    else:
        shutil.move(file_path, others_folder)

# Process all XML files in the source folder
for filename in os.listdir(source_folder):
    if filename.endswith('.xml'):
        file_path = os.path.join(source_folder, filename)
        process_xml_file(file_path)

# Create a DataFrame and save to Excel
df = pd.DataFrame(data)
df.to_excel('maintenance_codes_july-5.xlsx', index=False)

print("Process completed successfully!")
