import re
import pandas as pd

claim_ids = []
member_ids = []
statuses = []
messages = []

claim_id_pattern = re.compile(r"<claimId>(\d+)</claimId>")
member_id_pattern = re.compile(r"Member ID (\w+)")
status_pattern = re.compile(r"<status>(\w+)</status>")
message_pattern = re.compile(r"<message>(.*?)</message>")


with open('Input_file', 'r') as file:
    content = file.read()


responses = content.split('Response for Claim ID')


for response in responses:
    if response.strip():
        claim_id_match = claim_id_pattern.search(response)
        member_id_match = member_id_pattern.search(response)
        status_match = status_pattern.search(response)
        message_match = message_pattern.search(response)

        claim_id = claim_id_match.group(1) if claim_id_match else None
        member_id = member_id_match.group(1) if member_id_match else None
        status = status_match.group(1) if status_match else None
        message = message_match.group(1) if message_match and status == 'ERROR' else 'Successfully Processed'

        claim_ids.append(claim_id)
        member_ids.append(member_id)
        statuses.append(status)
        messages.append(message)


df = pd.DataFrame({
    'Claim ID': claim_ids,
    'Member ID': member_ids,
    'Status': statuses,
    'Message': messages
})


df.to_excel("FILE", index=False)

print(f"Data has been successfully written")
