from app import app, create_file_with_id, get_file_id

from fastapi import Request, UploadFile, Depends
from fastapi.responses import StreamingResponse

from sse_starlette.sse import EventSourceResponse

import asyncio

from urllib.parse import quote


from app.Progress import Progress
progress = Progress()

from bot import download_file, send_file_cor

from typing import List, Annotated


from app.routers.auth import get_current_username


@app.post("/uploadfile/")
async def create_upload_file(file: List[UploadFile], path: str, task_id: int, size: int, caption = None):
    for f in file:
        ids = await send_file_cor(f, task_id, f.size, caption)

        create_file_with_id(f.filename, round(f.size/1024/1024, 3), path, f.filename.split('.')[-1], ids)

    return {"status": 200}



@app.get("/downloadfile")
async def create_upload_file(username: Annotated[str, Depends(get_current_username)], type: str, id: str, task_id: int):
    if type == 'folder': 
        return {"status": 400}
    tg_id, name = get_file_id(id)

    name = quote(name, safe='')

    return StreamingResponse(download_file(tg_id, task_id), media_type="application/octet-stream", headers={"Content-Disposition": f"attachment;filename=\"{name}\""})
   


@app.get("/load_progress")
async def events(request: Request, task_id: int):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break

            if progress.get_progress(task_id) == 0:
                await asyncio.sleep(0.5)
                continue

            if progress.get_progress(task_id) > 99:
                progress.progress_dict.pop(task_id)
                yield 100
                break

            yield progress.get_progress(task_id)

            await asyncio.sleep(0.5)

    return EventSourceResponse(event_generator(), media_type="text/event-stream")
