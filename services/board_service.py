from models import Board, List
from helpers.utils import name_router


class BoardService:
    def __init__(self, db, current_user):
        self.db = db
        self.current_user = current_user


    def create_board(self, title):
        board_title = title
        check_title = self.db.session.execute(
            self.db.select(Board).filter_by(title=board_title, user_id=self.current_user.id)).scalar_one_or_none()
        if check_title:
            new_title = name_router(db=self.db,model=Board, field_name="title", base_title=board_title, user_id=self.current_user.id)
        else:
            new_title = board_title
        board = Board(title=new_title, user_id=self.current_user.id)
        self.db.session.add(board)
        self.db.session.commit()
        return board

    def update_board(self, title, board_id):
        board_title = title
        board_id = int(board_id)
        current_board = self.db.session.execute(self.db.select(Board).filter_by(id=board_id, user_id=self.current_user.id)).scalar_one_or_none()
        check_title = self.db.session.execute(self.db.select(Board).filter_by(title=board_title, user_id=self.current_user.id)).scalar_one_or_none()
        if current_board:
            if check_title and check_title.id != current_board.id:
                board_title = name_router(self.db, Board, "title", base_title=board_title, id=board_id)
            current_board.title = board_title
            self.db.session.commit()
        return current_board

    def delete_board(self, board_id):
        board_id = int(board_id)
        current_board = self.db.session.execute(self.db.select(Board).filter_by(id=board_id)).scalar()
        if current_board:
            self.db.session.delete(current_board)
            self.db.session.commit()
        return current_board
