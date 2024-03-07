import asyncio
from time import time

import aiohttp


async def fetch(session):
    url = 'http://localhost:8000/sample-async/'
    async with session.get(url) as response:
        result = await response.text()
        print('Result is:', result)
        return result


async def main():
    start = time()
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session) for _ in range(100)])
    print('execution time:', time() - start)


if __name__ == '__main__':
    asyncio.run(main())
