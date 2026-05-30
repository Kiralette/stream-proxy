import aiohttp
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/stream")
async def proxy(url: str, request: Request):
    async def generator():
        timeout = aiohttp.ClientTimeout(total=None, connect=10, sock_read=None)
        while True:
            try:
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.get(url, headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                        "Referer": "https://www.181fm.com/",
                        "Origin": "https://www.181fm.com",
                        "Icy-MetaData": "1",
                        "Connection": "keep-alive",
                        "Accept": "*/*",
                    }) as r:
                        async for chunk in r.content.iter_chunked(4096):
                            if chunk:
                                yield chunk
                        # Stream ended normally — reconnect immediately
            except Exception:
                # Connection dropped — reconnect
                import asyncio
                await asyncio.sleep(0.5)

    return StreamingResponse(
        generator(),
        media_type="audio/mpeg",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
