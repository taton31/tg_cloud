from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine 

from urllib.parse import quote

from app.models import Base

from dotenv import load_dotenv
load_dotenv('.env')

from app.Progress import Progress
progress = Progress()

from config import DATABASE_URL


app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

from app.models.crud_search import search_files_form, search_folders_form
from app.models.crud_file import get_files, create_file_with_id, rename_file, move_file, remove_file, get_file_id
from app.models.crud_folder import get_folders, rename_folder, move_folder, remove_folder, create_folder_but




from app.routers import file_sl, navigate, search