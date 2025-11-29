def parseRange(range: str) -> int:
    """Parses a range string formatted as '7d', '30d', '6m', '1y' into days."""
    if not range or len(range) < 2:
        raise ValueError("Invalid range string")

    unit = range[-1]
    try:
        value = int(range[:-1])
    except ValueError:
        raise ValueError("Invalid range value")

    if unit == "d":
        return value
    elif unit == "m":
        return value * 30
    elif unit == "y":
        return value * 365
    else:
        raise ValueError("Invalid range unit")
