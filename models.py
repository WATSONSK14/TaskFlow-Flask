from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin
from datetime import datetime, timezone, timedelta
from extensions import db

def now_with_offset():
    return datetime.now(timezone(timedelta(hours=3)))

class User(db.Model, UserMixin):
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    username : Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email : Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_with_offset)
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    authority: Mapped[int] = mapped_column(Integer,default=0)

    boards = relationship('Board', back_populates='user', cascade='all, delete-orphan', passive_deletes=False)


class Board(db.Model):
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    title : Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_with_offset)

    user_id : Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates='boards')
    lists = relationship('List', back_populates='board', cascade='all, delete-orphan', passive_deletes=False)

class List(db.Model):
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    title : Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_with_offset)
    board_id : Mapped[int] = mapped_column(ForeignKey('board.id', ondelete='CASCADE'), nullable=False)
    board = relationship('Board', back_populates='lists')
    quests = relationship('Quest', back_populates='list', cascade='all, delete-orphan', passive_deletes=False)

class Quest(db.Model):
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    title : Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    is_finished: Mapped[bool] = mapped_column(Boolean, default=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_with_offset)

    list_id : Mapped[int] = mapped_column(ForeignKey('list.id', ondelete='CASCADE'), nullable=False)
    list = relationship('List', back_populates='quests')

