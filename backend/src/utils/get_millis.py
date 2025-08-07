import asyncio
import json
from time import time_ns

def get_millis() -> int:
    """Return a number of milliseconds passed since the epoch"""
    return time_ns() // 1_000_000
