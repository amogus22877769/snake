import asyncio


def run_async_in_thread(coroutine):
    loop = asyncio.get_running_loop()
    loop.run_until_complete(coroutine)
