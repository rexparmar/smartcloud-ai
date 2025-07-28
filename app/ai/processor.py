def tag_file_content(file_path: str) -> list[str]:
    # For now, just simulate AI tagging
    # In real life, you'd use transformers, LLMs, etc.
    with open(file_path, 'r', errors='ignore') as f:
        content = f.read().lower()

    tags = []
    if "invoice" in content:
        tags.append("Finance")
    if "report" in content:
        tags.append("Work")
    if "love" in content:
        tags.append("Personal")

    return tags
