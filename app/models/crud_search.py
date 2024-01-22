from sqlalchemy.orm import Session
from app import db as db_session

from . import File, Folder


def search_files_form(folder: str, filename: str, extension: str, uploaded_after, uploaded_before, size_from: int, size_to: int):
    # fil= 
    print(uploaded_after)
    # file = db_session.query(File).filter((File.path == folder) & () & () & () & () & () & () & () & ()).all()
    return []