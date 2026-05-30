import aiohttp
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/stream")
async def proxy(url: str, request: Request):

    async def generator():
        timeout = aiohttp.ClientTimeout(total=None, connect=10, sock_read=300)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Icy-MetaData": "1",
            "Accept": "*/*",
        }

        while True:
            try:
                if await request.is_disconnected():
                    break

                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.get(url, headers=headers) as r:
                        async for chunk in r.content.iter_chunked(8192):
                            if await request.is_disconnected():
                                return
                            if chunk:
                                yield chunk

            except (aiohttp.ClientError, asyncio.TimeoutError):
                await asyncio.sleep(1)
            except GeneratorExit:
                return

    return StreamingResponse(
        generator(),
        media_type="audio/mpeg",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Transfer-Encoding": "chunked",
        },
    )
