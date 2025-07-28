from celery import shared_task
from app.ai.tagging import tag_file_content

@shared_task
def process_file_task(file_path: str):
    print(f"🚀 Processing file at {file_path}")
    tags = tag_file_content(file_path)
    if tags:
        print(f"🏷️ AI Tags: {', '.join(tags)}")
    else:
        print("🤷 No tags found")
