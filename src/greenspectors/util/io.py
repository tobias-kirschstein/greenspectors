import requests


def download_file(url: str, store_location: str):
    r = requests.get(url)
    open(store_location, 'wb').write(r.content)


def parse_size_to_mb(size_str: str) -> float:
    size_str = size_str.replace(',', '')
    if size_str == '-':
        return 0

    size = float(size_str[:-1])
    unit = size_str[-1]
    if unit == 'B':
        multiplier = 1 / (1000 * 1000)
    elif unit == 'K':
        multiplier = 1 / 1000
    elif unit == 'M':
        multiplier = 1
    elif unit == 'G':
        multiplier = 1000
    else:
        raise ValueError(f"Unknown unit: {unit}")

    return size * multiplier
