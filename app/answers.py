import asyncio
from database import GET_KEYS

async def fetch_keys():
    keys = await GET_KEYS()
    return keys