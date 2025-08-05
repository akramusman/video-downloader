from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from downloader.yt_dlp_handler import YTDLPHandler
from fastapi.middleware.cors import CORSMiddleware
import os
import time

app = FastAPI()
yt_dlp_handler = YTDLPHandler()

# Add this block after app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process")
async def process(request: Request):
    data = await request.json()
    video_url = data.get("url")
    format_id = data.get("format_id")

    if not video_url:
        raise HTTPException(status_code=400, detail="URL is required")

    if not format_id:
        # Analyze mode
        try:
            metadata = yt_dlp_handler.analyze_video(video_url)
            return JSONResponse(content=metadata)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        # Download mode
        try:
            file_path, file_name = yt_dlp_handler.download_video(video_url, format_id)
            # Wait up to 30 seconds for file to exist and be non-empty
            for _ in range(30):
                if os.path.exists(file_path) and os.path.getsize(file_path) > 1024:
                    break
                time.sleep(1)
            else:
                raise HTTPException(status_code=500, detail="File not ready or download failed")

            def iterfile():
                with open(file_path, "rb") as f:
                    while chunk := f.read(1024 * 1024):
                        yield chunk

            response = StreamingResponse(iterfile(), media_type="application/octet-stream")
            response.headers["Content-Disposition"] = f'attachment; filename="{file_name}"'
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
