from datetime import datetime


def convert_timestamp(ts: int) -> str:
    """Convert Unix timestamp to UTC datetime string."""
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def format_timestamp(ts: int) -> str:
    """Convert Unix timestamp to local datetime string."""
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
