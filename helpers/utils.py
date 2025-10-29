from flask import request, redirect, url_for, flash

def name_router(db, model, field_name, base_title, **filters):
    i = 1
    while True:
        new_title = f"{base_title}({i})"
        exists = db.session.execute(
            db.select(model).filter_by(**{field_name: new_title}, **filters)
        ).scalar_one_or_none()
        if not exists:
            return new_title
        i += 1

def handle_redirect(message, category="warning", endpoint='board', **kwargs):
    flash(message, category)
    return redirect(request.referrer or url_for("board"))