from firebase_config import db

def get_story_node(story_id, node_id):
    doc_ref = db.collection("stories").document(story_id)
    doc = doc_ref.get()
    if doc.exists:
        story_data = doc.to_dict()
        return story_data["nodes"].get(node_id, None), story_data.get("required_points", 0)
    return None, 0

def get_all_stories(user_points):
    stories_ref = db.collection("stories").stream()
    stories = []
    for story in stories_ref:
        story_data = story.to_dict()
        stories.append({
            "id": story.id,
            "name": story_data.get("story_name", "Unnamed Story"),
            "required_points": story_data.get("required_points", 0)
        })
    return stories

def get_user_total_points(user_id):
    user_ref = db.collection("User").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        return user_doc.to_dict().get("userpoints", 0)
    return 0

def get_user_current_points(story_id, node_id):
    user_ref = db.collection("stories").document(story_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        story_content = user_doc.to_dict()
        nodes = story_content.get("nodes", {})
        current_node = nodes[node_id]
        return current_node.get("points", 0)
    return 0

def get_user_story_points(user_id, story_id):
    ref = db.collection("User").document(user_id).collection("stories").document(story_id)
    doc = ref.get()
    return doc.to_dict().get("points", 0) if doc.exists else 0

def update_user_points(user_id, story_id, earned_points):
    user_ref = db.collection("User").document(user_id)
    story_ref = user_ref.collection("stories").document(story_id)

    # Get existing totals
    user_total = get_user_total_points(user_id)
    story_total = get_user_story_points(user_id, story_id)

    # Update
    user_ref.update({"userpoints": user_total + earned_points})
    # story_ref.set({"points": story_total + earned_points}, merge=True)
    user_ref = db.collection("User").document(user_id)
    user_ref.update({"points": earned_points})

def get_all_choices_from_story(story_id):
    story_ref = db.collection("stories").document(story_id)
    story_data = story_ref.get().to_dict()
    all_choices = []
    for node in story_data.get("nodes", {}).values():
        for choice_key, choice_val in node.get("choices", {}).items():
            if choice_val.get("points") > 0:  # Only include choices with points
                all_choices.append(choice_key)
    return all_choices    