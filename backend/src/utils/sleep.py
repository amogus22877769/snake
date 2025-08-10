from time import sleep as time_sleep
from asyncio import get_running_loop

async def sleep(sleep_for: float) -> None:
    """An asyncio sleep.

    On Windows this achieves a better granularity than asyncio.sleep

    Args:
        sleep_for (float): Seconds to sleep for.
    """
    await get_running_loop().run_in_executor(None, time_sleep, sleep_for)