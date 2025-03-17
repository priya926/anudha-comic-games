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
        if story_data.get("required_points", 0) <= user_points:
            stories.append({
                "id": story.id,
                "name": story_data.get("story_name", "Unnamed Story"),
                "required_points": story_data.get("required_points", 0)
            })
    return stories

def get_user_points(user_id):
    user_ref = db.collection("User").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        return user_doc.to_dict().get("points", 0)
    else:
        user_ref.set({"points": 0})
        return 0

def update_user_points(user_id, points):
    user_ref = db.collection("User").document(user_id)
    user_ref.update({"points": points})