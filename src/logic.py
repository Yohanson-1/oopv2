def format_hhmmss(seconds: int) -> str:
    """Convert elapsed seconds into HH:MM:SS string."""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"
