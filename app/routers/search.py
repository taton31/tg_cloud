from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sse_starlette.sse import EventSourceResponse
from app import app, templates, search_files_form

from typing import Optional




@app.get("/search", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})


@app.post("/search/file", response_class=HTMLResponse)
async def search_files(
    request: Request,
    folder: Optional[str] = Form(None),
    filename: Optional[str] = Form(None),
    extension: Optional[str] = Form(None),
    uploaded_after: Optional[str] = Form(None),
    uploaded_before: Optional[str] = Form(None),
    size_from: Optional[int] = Form(None),
    size_to: Optional[int] = Form(None)
    # folder_in_folder: Optional[str] = Form(None),
    # subfolder_name: Optional[str] = Form(None)
):
    
    return templates.TemplateResponse("search.html", {"request": request, "folders": [], "files": search_files_form(folder, filename, extension, uploaded_after, uploaded_before, size_from, size_to)})

