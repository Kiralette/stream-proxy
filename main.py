import aiohttp
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/stream")
async def proxy(url: str):
    async def generator():
        timeout = aiohttp.ClientTimeout(total=None, connect=10, sock_read=None)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers={
                "User-Agent": "Mozilla/5.0",
                "Icy-MetaData": "1",
            }) as r:
                async for chunk in r.content.iter_chunked(4096):
                    if chunk:
                        yield chunk

    return StreamingResponse(
        generator(),
        media_type="audio/mpeg",
        headers={"Access-Control-Allow-Origin": "*", "Cache-Control": "no-cache"},
    )
