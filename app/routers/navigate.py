from fastapi import Request
from fastapi.responses import HTMLResponse, FileResponse

from app import app, templates
from app import get_folders, rename_folder, remove_folder, move_folder, create_folder_but
from app import get_files, remove_file, rename_file, move_file



@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, path: str = '/'):
    return templates.TemplateResponse("index.html", {"request": request, "folders": get_folders(path), "files": get_files(path), 'path':path})


@app.get("/rename")
async def rename(type: str, id: int, new_name: str):
    if type == 'folder':
        rename_folder(id, new_name)
    elif type == 'file':
        rename_file(id, new_name)


@app.get("/move")
async def move(type: str, id: int, new_path: str):
    if type == 'folder':
        move_folder(id, new_path)
    elif type == 'file':
        move_file(id, new_path)


@app.get("/remove")
async def move(type: str, id: int):
    if type == 'folder':
        remove_folder(id)
    elif type == 'file':
        remove_file(id)


@app.get("/create")
async def create(name: str, path: str):
    create_folder_but(name, path)



@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('app/static/favicon.ico')
