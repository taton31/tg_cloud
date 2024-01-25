from app import app, create_file_with_id, get_file_id

from fastapi import Request, UploadFile, BackgroundTasks
from fastapi.responses import StreamingResponse

from sse_starlette.sse import EventSourceResponse

import asyncio
import os

from urllib.parse import quote


from app.Progress import Progress
progress = Progress()

from bot import send_file, download_file 

from config import TMP_FILE_FOLDER, CHANK


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, path: str, task_id: int, background_tasks: BackgroundTasks):
    file_path = f'{TMP_FILE_FOLDER}/{task_id}'

    with open(file_path, "wb") as f:
        while chunk := await file.read(CHANK):
            f.write(chunk)

    tg_id = await send_file(task_id)
    create_file_with_id(file.filename, round(file.size/1024/1024, 3), path, file.filename.split('.')[-1], tg_id)

    background_tasks.add_task(os.remove, file_path)

    return {"status": 200}



@app.get("/downloadfile")
async def create_upload_file(type: str, id: str, task_id: int, background_tasks: BackgroundTasks):
    tg_id, name = get_file_id(id)
    total_size = await download_file(tg_id, task_id)

    file_path = f'{TMP_FILE_FOLDER}/{task_id}'
    
    def generate_file_chunks(file_path, chunk_size=CHANK):
            with open(f'{file_path}', 'rb') as f:
                while chunk := f.read(chunk_size):
                    yield chunk

    name = quote(name, safe='')

    background_tasks.add_task(os.remove, file_path)

    return StreamingResponse(generate_file_chunks(file_path), media_type="application/octet-stream", headers={"Content-Disposition": f"attachment;filename=\"{name}\"", "content-length": f"{total_size}"})
   


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
