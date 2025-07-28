# app/ai/tagging.py
def tag_file_content(file_path: str) -> list[str]:
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read().lower()

    tags = []
    if "invoice" in content:
        tags.append("Finance")
    if "report" in content:
        tags.append("Work")
    if "love" in content:
        tags.append("Personal")
    return tags
