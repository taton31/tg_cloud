from app import app, create_file_with_id, get_file_id

from fastapi import Request, UploadFile
from fastapi.responses import StreamingResponse

from sse_starlette.sse import EventSourceResponse

import asyncio

from urllib.parse import quote


from app.Progress import Progress
progress = Progress()

from bot import download_file, send_file_cor

from config import CHANK


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, path: str, task_id: int, size: int):
    i = 0
    ids = []

    while chunk := await file.read(CHANK):
        ids.append( await send_file_cor(chunk, task_id, i, size))
        i += 1
        print(f'SEND file: {round(i*CHANK/size*100,2)}')

    create_file_with_id(file.filename, round(size/1024/1024, 3), path, file.filename.split('.')[-1], str(ids))

    return {"status": 200}



@app.get("/downloadfile")
async def create_upload_file(type: str, id: str, task_id: int):
    
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
