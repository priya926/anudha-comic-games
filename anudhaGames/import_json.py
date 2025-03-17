import json
from firebase_config import db

# Load JSON file
with open("data.json", "r") as file:
    data = json.load(file)

# Iterate through each story in the JSON file and upload it to Firestore
for story_id, story_data in data.items():
    db.collection("stories").document(story_id).set(story_data)
    print(f"Uploaded: {story_id}")

print("JSON data successfully imported into Firestore!")