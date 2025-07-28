from celery import shared_task
from app.ai.tagging import tag_file_content
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_file_task(file_path: str):
    """Celery task for processing files"""
    return process_file_sync(file_path)

def process_file_sync(file_path: str):
    """Synchronous function for processing files (can be called directly)"""
    try:
        print(f"🚀 Processing file at {file_path}")
        tags = tag_file_content(file_path)
        if tags:
            print(f"🏷️ AI Tags: {', '.join(tags)}")
            logger.info(f"File processed successfully: {file_path} - Tags: {tags}")
            return {"status": "success", "tags": tags}
        else:
            print("🤷 No tags found")
            logger.info(f"File processed but no tags found: {file_path}")
            return {"status": "success", "tags": []}
    except Exception as e:
        error_msg = f"Error processing file {file_path}: {str(e)}"
        print(f"❌ {error_msg}")
        logger.error(error_msg)
        return {"status": "error", "error": str(e)}
