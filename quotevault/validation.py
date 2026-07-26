# Pure validation — no framework, no storage. Easiest thing to UNIT test.
def validate_quote(data):
    errors = []
    raw_text = data.get("text") if isinstance(data, dict) else None
    text = raw_text.strip() if isinstance(raw_text, str) else ""

    raw_author = data.get("author") if isinstance(data, dict) else None
    author = raw_author.strip() if isinstance(raw_author, str) and raw_author.strip() else "Anonymous"

    if not text:
        errors.append("text is required")
    if len(text) > 280:
        errors.append("text must be <= 280 characters")

    return (len(errors) == 0, errors, {"text": text, "author": author})
