from models import Quest, List, now_with_offset
from helpers.utils import name_router

class QuestService:
    def __init__(self, db):
        self.db = db

    def create_quest(self, title, description, quest_notes, current_list):
        quest_title = title
        quest_description = description
        quest_notes = quest_notes
        exists_title = [qst.title for qst in current_list.quests]
        if quest_title in exists_title:
            quest_title = name_router(db=self.db, model=Quest, field_name="title",base_title=quest_title, list_id=current_list.id)
        new_quest = Quest(title=quest_title, description=quest_description,notes=quest_notes, list_id=current_list.id)
        self.db.session.add(new_quest)
        self.db.session.commit()
        return new_quest

    def update_quest(self, title, quest_id, description, quest_notes):
        quest_title = title
        quest_id = quest_id
        quest_description = description
        quest_notes = quest_notes

        current_quest = self.db.session.execute(self.db.select(Quest).filter_by(id=quest_id)).scalar()
        current_list = self.db.session.execute(self.db.select(List).filter_by(id=current_quest.list_id)).scalar()
        check_quest = self.db.session.execute(self.db.select(Quest).filter_by(title=quest_title, list_id=current_list.id)).scalar_one_or_none()

        if current_quest:
            if check_quest and check_quest.id != current_quest.id:
                quest_title = name_router(self.db, model=Quest, field_name="title",base_title=quest_title, list_id=current_list.id)
            current_quest.title = quest_title
            current_quest.description = quest_description
            current_quest.notes = quest_notes
            self.db.session.commit()
        return current_quest

    def delete_quest(self, quest_id):
        quest_id = quest_id
        current_quest = self.db.session.execute(self.db.select(Quest).filter_by(id=quest_id)).scalar()
        if current_quest:
            self.db.session.delete(current_quest)
            self.db.session.commit()
        return current_quest

    def quest_status(self, current_quest, is_finished):
        if current_quest.list_id:
            current_quest.is_finished = is_finished
            if is_finished:
                current_quest.completed_at = now_with_offset()
            else:
                current_quest.completed_at = None
            self.db.session.commit()