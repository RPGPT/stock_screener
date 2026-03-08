def format_number(value: float) -> str:
    num = round(float(value), 2)
    for unit in ['', 'K', 'M', 'B', 'T']:
        if abs(num) < 1000:
            result = f"{num:.2f}".rstrip('0').rstrip('.')
            return f"{result}{unit}"
        num /= 1000
    result = f"{num:.2f}".rstrip('0').rstrip('.')
    return f"{result}P"