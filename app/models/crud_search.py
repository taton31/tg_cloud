from app import db as db_session

from . import File, Folder


def search_files_form(folder: str, filename: str, extension: str, uploaded_after, uploaded_before, size_from: int, size_to: int):

    query = db_session.query(File)
    if folder is not None:
        query = query.filter(File.path.ilike(f"%{folder}%"))
    if filename is not None:
        query = query.filter(File.name.ilike(f"%{filename}%"))
    if extension is not None:
        query = query.filter(File.extension == extension)
    if uploaded_after is not None:
        query = query.filter(File.datetime > uploaded_after)
    if uploaded_before is not None:
        query = query.filter(File.datetime < uploaded_before)
    if size_from is not None:
        query = query.filter(File.size >= size_from)
    if size_to is not None:
        query = query.filter(File.size <= size_to)
    
    files = query.all()
    return files



def search_folders_form(folder_in_folder: str, subfolder_name: str):
    query = db_session.query(Folder)
    if folder_in_folder is not None:
        query = query.filter(Folder.path_to.ilike(f"%{folder_in_folder}%"))
    if subfolder_name is not None:
        query = query.filter(Folder.name.ilike(f"%{subfolder_name}%"))
    
    folders = query.all()
    return folders