import os
import re

def extract_member_ids(directory_path):
    pattern = re.compile(r'(\d+[A-Za-z]?)\.xml')

    member_ids = []

    for filename in os.listdir(directory_path):
        match = pattern.match(filename)
        if match:
            member_id = match.group(1)
            member_ids.append(member_id)

    return member_ids


directory_path = os.path.join(os.getcwd(), 'Input_file')  

member_ids = extract_member_ids(directory_path)

for member_id in member_ids:
    print(member_id)
