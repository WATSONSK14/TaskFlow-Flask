from models import List
from helpers.utils import name_router

class ListService:
    def __init__(self, db):
        self.db = db

    def create_list(self, title, board_id, current_board):
        list_title = title
        existing_titles = {lst.title for lst in current_board.lists}
        if list_title in existing_titles:
            list_title = name_router(db=self.db, model=List, field_name="title", base_title=list_title, board_id=board_id)
        new_list = List(title=list_title, board_id=board_id)
        self.db.session.add(new_list)
        self.db.session.commit()
        return new_list

    def update_list(self, title, list_id, current_board):
        list_title = title
        list_id = int(list_id)
        current_list = self.db.session.execute(self.db.select(List).filter_by(id=list_id, board_id=current_board.id)).scalar_one_or_none()
        list_check = self.db.session.execute(self.db.select(List).filter_by(title=list_title, board_id=current_board.id)).scalar_one_or_none()
        if current_list:
            if list_check and list_check.id != current_list.id:
                list_title = name_router(db=self.db, model=List, field_name="title", base_title=list_title, board_id=current_list.board_id)
            current_list.title = list_title
            self.db.session.commit()
        return current_list

    def delete_list(self, list_id, current_board):
        list_id = int(list_id)
        current_list = self.db.session.execute(self.db.select(List).filter_by(id=list_id, board_id=current_board.id)).scalar_one_or_none()
        if current_list:
            self.db.session.delete(current_list)
            self.db.session.commit()
        return current_list