from app import db as db_session

from . import File, Folder

def get_folders(folder_path: str):
    folders = db_session.query(Folder).filter((Folder.path == folder_path) & (Folder.is_del == False)).all()
    return folders



def create_folder_but(name: str, path: str):
    folder = Folder(name=name, path=path, path_to=f'{path}/{name}' if path != '/' else f'/{name}')
    db_session.add(folder)
    db_session.commit()
    db_session.refresh(folder)
    return folder



def create_folder(name: str, path: str, path_to: str):
    folder = Folder(name=name, path=path, path_to=path_to)
    db_session.add(folder)
    db_session.commit()
    db_session.refresh(folder)
    return folder



def rename_folder(id: int, new_name: str):
    folder = db_session.query(Folder).filter((Folder.id == id) & (Folder.is_del == False)).first()
    folder.name = new_name
    db_session.commit()  
    return folder



def move_folder(id: int, new_path: str):

    def req_move(path: str, mew_path: str):
        
        folders = db_session.query(Folder).filter(Folder.path == path).all()
        files = db_session.query(File).filter(File.path == path).all()
        for fl in files:
            fl.path = mew_path

        if not folders:
            return
        
        for f in folders:
            old_path_to = f.path_to 
            f.path = mew_path 
            to = f.path_to[f.path_to.rfind('/'):] 
            f.path_to = f'{mew_path}{to}' if mew_path != '/' else to
            new_path_to = f.path_to 
            req_move(old_path_to, new_path_to)

    folder = db_session.query(Folder).filter((Folder.path_to == new_path) & (Folder.is_del == False)).first()

    if folder or new_path == '/':
        folder = db_session.query(Folder).filter((Folder.id == id) & (Folder.is_del == False)).first()
        old_path_to = folder.path_to 
        folder.path = new_path 
        to = folder.path_to[folder.path_to.rfind('/'):]
        folder.path_to = f'{new_path}{to}' if new_path != '/' else to 
        new_path_to = folder.path_to 
        req_move(old_path_to, new_path_to)

        db_session.commit()  
        return folder



def remove_folder(id: int):
    folder = db_session.query(Folder).filter((Folder.id == id) & (Folder.is_del == False)).first()

    def req_remove(path_to: str):
        folders = db_session.query(Folder).filter((Folder.path == path_to) & (Folder.is_del == False)).all()
        files = db_session.query(File).filter((File.path == path_to) & (File.is_del == False)).all()
        for fl in files:
            fl.is_del = True

        if not folders:
            return
        
        for f in folders:
            f.is_del = True
            req_remove(f.path_to)

    folder.is_del = True
    req_remove(folder.path_to)
    db_session.commit()  
    return folder