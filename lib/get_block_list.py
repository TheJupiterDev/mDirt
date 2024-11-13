import requests as rs
import json

# Get the latest version
latest_unparsed = rs.get("https://raw.githubusercontent.com/PrismarineJS/minecraft-data/refs/heads/master/data/pc/latest/proto.yml")
content = latest_unparsed.text

# Extract version
for line in content.splitlines():
    if line.startswith('!version:'):
        version = line.split('!version: ')[1].strip()
        print(version)
        break

# Get the items data in JSON format and parse it into a dictionary
items_response = rs.get(f'https://raw.githubusercontent.com/PrismarineJS/minecraft-data/refs/heads/master/data/pc/{version}/items.json')
items = json.loads(items_response.text)  # Convert string to dictionary

# Initialize the list to store item names
items_parsed = []

# Iterate over the parsed dictionary and extract item names
for item in items:
    if item["name"] != 'air':
        items_parsed.append(item["name"])

# Write the parsed items list to a JSON file
with open('./src/item_list.json', 'w') as f:
    json.dump({"items": items_parsed}, f, indent=4)  # Directly dump the dictionary with items
