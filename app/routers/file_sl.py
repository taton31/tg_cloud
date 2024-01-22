from app import app, create_file_with_id, get_file_id

from fastapi import Request, UploadFile
from fastapi.responses import StreamingResponse

from sse_starlette.sse import EventSourceResponse

import asyncio


from urllib.parse import quote
from io import BytesIO

from app.Progress import Progress
progress = Progress()

from bot import send_file, download_file 


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, path: str, task_id: int):
    # print({"filename": file.filename, "text": path})
    # set_progress(task_id, 0)
    file_data = await file.read()
    # Отправка файла через телеграм-бота
    bio = BytesIO(file_data)
    bio.name = file.filename
    tg_id = await send_file(bio, task_id)
    create_file_with_id(file.filename, round(file.size/1024/1024, 3), path, file.filename.split('.')[-1], tg_id)
    return {"filename": file.filename, "text": path}


# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile, path: str, task_id: int):
#     # print({"filename": file.filename, "text": path})
#     set_progress(task_id, 0)
#     file_data = await file.read()
#     # Отправка файла через телеграм-бота
#     bio = BytesIO(file_data)
#     bio.name = file.filename
#     tg_id = await send_file(bio, task_id)
#     create_file_with_id(db, file.filename, round(file.size/1024/1024, 3), path, file.filename.split('.')[-1], tg_id)
#     return {"filename": file.filename, "text": path}


@app.get("/downloadfile")
async def create_upload_file(type: str, id: str, task_id: int):
    # set_progress(task_id, 0)
    tg_id, name = get_file_id(id)
    blob = await download_file(tg_id, task_id)
    blob = BytesIO(blob)
    name = quote(name, safe='')
    return StreamingResponse(blob, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment;filename=\"{name}\"", "content-length": f"{blob.getbuffer().nbytes}"})
   


# @app.get("/downloadfile")
# async def create_upload_file(type: str, id: str, task_id: int):
#     set_progress(task_id, 0)
#     tg_id, name = get_file_id(db, id)
#     blob = await download_file(tg_id, task_id)
#     name = quote(name, safe='')
#     return StreamingResponse(BytesIO(blob), media_type="application/octet-stream", headers={"Content-Disposition": f"attachment;filename=\"{name}\""})
   



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
