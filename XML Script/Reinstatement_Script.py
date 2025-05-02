import os
import pandas as pd
from datetime import datetime
from xml.etree import ElementTree as ET


def parse_xml_file(file_path):
    reinstatement_members = []
    
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    for member in root.iter('member'):
        maintenance_type_code = member.find('maintenanceTypeCode').text
        if maintenance_type_code == 'REINSTATEMENT':
            member_id = member.find('.//id').text
            for plan_selection in member.iter('planSelection'):
                start_date = plan_selection.find('startDate').text
                start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
                if start_date_dt < datetime(2024, 7, 1):
                    reinstatement_members.append((member_id, start_date))
    
    return reinstatement_members


def create_excel(reinstatement_members, output_path):
    reinstatement_df = pd.DataFrame(reinstatement_members, columns=['Member ID', 'Start Date'])

    with pd.ExcelWriter(output_path) as writer:
        reinstatement_df.to_excel(writer, sheet_name='Reinstatement Members', index=False)


input_directory = 'Input_file'
output_file_path = 'output_file'


xml_files = [f for f in os.listdir(input_directory) if f.endswith('.xml')]

reinstatement_members = []


for xml_file in xml_files:
    file_path = os.path.join(input_directory, xml_file)
    print(f"Processing file: {file_path}")  
    members = parse_xml_file(file_path)
    if members:
        print(f"Found members in {xml_file}: {members}")  
    reinstatement_members.extend(members)


if reinstatement_members:
    create_excel(reinstatement_members, output_file_path)
    print("Excel file created at:", output_file_path)
else:
    print("No reinstatement members found.")
