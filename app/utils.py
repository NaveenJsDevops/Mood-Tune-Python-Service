def normalize_text(value: str) -> str:
    """
    Normalize input text by trimming and converting to lowercase.

    Args:
        value (str): Input string.

    Returns:
        str: Normalized string.
    """
    return value.strip().lower()
