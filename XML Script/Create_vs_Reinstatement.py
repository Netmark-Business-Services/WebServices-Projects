import os
import xml.etree.ElementTree as ET

def extract_member_info(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    member_id_element = root.find('.//hccIdentifier')
    maintenance_code_element = root.find('.//maintenanceTypeCode')

    
    member_id = member_id_element.text if member_id_element is not None else 'Not found'
    maintenance_code = maintenance_code_element.text if maintenance_code_element is not None else 'Not found'

    return member_id, maintenance_code

def process_all_xml_files(folder_path):
    member_info_list = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xml'):
            xml_file = os.path.join(folder_path, file_name)
            member_id, maintenance_code = extract_member_info(xml_file)
            member_info_list.append((member_id, maintenance_code))

    return member_info_list

if __name__ == "__main__":
    folder_path = "Input_file"
    member_info = process_all_xml_files(folder_path)

    for info in member_info:
        print(f'Member ID: {info[0]}, Maintenance Type Code: {info[1]}')
