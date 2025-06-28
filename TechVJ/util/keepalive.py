import asyncio
import logging
import aiohttp
import traceback
from info import *

async def ping_server():
    sleep_time = int(PING_INTERVAL) if PING_INTERVAL else 300  # Default to 5 minutes

    while True:
        await asyncio.sleep(sleep_time)
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(STREAM_URL) as resp:
                    logging.info("Pinged server with response: {}".format(resp.status))
        except aiohttp.ClientError as e:
            logging.warning(f"Couldn't connect to the site URL..! Reason: {e}")
        except Exception as e:
            logging.error("Unexpected error during ping:")
            traceback.print_exc()
