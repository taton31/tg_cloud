from fastapi import Request, Form, Depends
from fastapi.responses import HTMLResponse

from app import app, templates, search_files_form, search_folders_form

from typing import Optional, Annotated

from app.routers.auth import get_current_username


@app.get("/search", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})


@app.post("/search/file", response_class=HTMLResponse)
async def search_files(
    username: Annotated[str, Depends(get_current_username)], 
    request: Request,
    folder: Optional[str] = Form(None),
    filename: Optional[str] = Form(None),
    extension: Optional[str] = Form(None),
    uploaded_after: Optional[str] = Form(None),
    uploaded_before: Optional[str] = Form(None),
    size_from: Optional[int] = Form(None),
    size_to: Optional[int] = Form(None)
):
    
    return templates.TemplateResponse("search.html", {"request": request, "folders": [], "files": search_files_form(folder, filename, extension, uploaded_after, uploaded_before, size_from, size_to)})



@app.post("/search/folder", response_class=HTMLResponse)
async def search_files(
    username: Annotated[str, Depends(get_current_username)], 
    request: Request,
    folder_in_folder: Optional[str] = Form(None),
    subfolder_name: Optional[str] = Form(None)
):
    
    return templates.TemplateResponse("search.html", {"request": request, "folders": search_folders_form(folder_in_folder, subfolder_name), "files": []})

