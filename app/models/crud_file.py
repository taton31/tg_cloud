from app import db as db_session

from . import File, Folder

def get_files(file_path: str):
    files = db_session.query(File).filter((File.path == file_path) & (File.is_del == False)).all()
    return files


def create_file_with_id(name: str, size: str, path: str, extension: str, tg_id: int):
    file = File(name=name, size=size, path=path, extension=extension, tg_id=tg_id)
    db_session.add(file)
    db_session.commit()
    db_session.refresh(file)
    return file


def rename_file(id: int, new_name: str):
    file = db_session.query(File).filter((File.id == id) & (File.is_del == False)).first()
    file.name = new_name
    db_session.commit() 
    return file


def get_file_id(id: int):
    file = db_session.query(File).filter((File.id == id) & (File.is_del == False)).first()
    return file.tg_id, file.name



def move_file(id: int, new_path: str):
    folder = db_session.query(Folder).filter((Folder.path_to == new_path) & (Folder.is_del == False)).first()
   
    if folder or new_path == '/':
        file = db_session.query(File).filter((File.id == id) & (File.is_del == False)).first()
        file.path = new_path
        db_session.commit()  
        return file
    

def remove_file(id: int):
    file = db_session.query(File).filter(File.id == id).first()
    file.is_del = True
    db_session.commit() 
    return file


def get_not_backuped_file():
    files = db_session.query(File).filter((File.tg_id_backup == None) & (File.is_del == False)).all()
    return files

def add_backup_id(id, id_backup):
    file = db_session.query(File).filter((File.id == id)).first()
    file.tg_id_backup = id_backup
    db_session.commit() 
    return file