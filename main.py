import aiohttp
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/stream")
async def proxy(url: str):
    async def generator():
        timeout = aiohttp.ClientTimeout(total=None, connect=10, sock_read=None)
        connector = aiohttp.TCPConnector(force_close=False, enable_cleanup_closed=True)
        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            async with session.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Icy-MetaData": "1",
                "Connection": "keep-alive",
                "Keep-Alive": "timeout=300",
            }) as r:
                async for chunk in r.content.iter_chunked(4096):
                    if chunk:
                        yield chunk

    return StreamingResponse(
        generator(),
        media_type="audio/mpeg",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
