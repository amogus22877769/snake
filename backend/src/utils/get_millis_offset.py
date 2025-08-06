from datetime import datetime
def get_millis_offset() -> int:
    return datetime.now().microsecond // 1000 % 100
