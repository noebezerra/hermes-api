def normalize_value(value):
    if isinstance(value, bytes):
        return value.hex()
    return value

def normalize_row(row):
    return {key: normalize_value(value) for key, value in row.items()}
