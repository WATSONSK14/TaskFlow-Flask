from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, timedelta
from extensions import db, login_manager
from forms import RegisterForm, LoginForm
from models import User, Board, List, Quest
from services import *
from helpers import *
from config import DevConfig, ProdConfig
import os
from dotenv import load_dotenv

load_dotenv(override=False)
app = Flask(__name__)

if os.getenv('FLASK_ENV') == "production":
    app.config.from_object(ProdConfig)
else:
    app.config.from_object(DevConfig)

db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'
login_manager.login_message = 'Giriş Yapmalısınız'
login_manager.login_message_category = 'info'
login_manager.session_protection = 'strong'

board_service = BoardService(db, current_user)
list_service = ListService(db)
quest_service = QuestService(db)

ACTIONS = {
    "create_board": board_service.create_board,
    "update_board" : board_service.update_board,
    "delete_board" : board_service.delete_board,
    "create_list": list_service.create_list,
    "update_list" : list_service.update_list,
    "delete_list": list_service.delete_list,
    "create_quest": quest_service.create_quest,
    "update_quest": quest_service.update_quest,
    "delete_quest": quest_service.delete_quest,
    "toggle_quest_status": quest_service.quest_status,
}

@login_manager.user_loader
def load_user(id):
    return db.session.get(User, id)

with app.app_context():
    db.create_all()

@app.route('/')
def first_page():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template("first.html")


@app.route('/home', methods=['GET','POST'])
@login_required
def home():
    context = {'boards':current_user.boards}
    return render_template("home.html", context=context)

@app.route('/boards', methods=['GET','POST'])
@login_required
def board():
    if request.method == "POST":
        action = request.form.get('action')
        handler = ACTIONS.get(action)
        if handler:
            if action == "create_board":
                title = request.form.get('board_title')
                if not title:
                    return handle_redirect("Lütfen Bir Pano Adı Giriniz...", "danger", 'board')
                new_board = handler(title=title)
                return handle_redirect("Pano Başarıyla Oluşturuldu", "success", "board")
            if action == "update_board":
                board_id = request.form.get('board_id')
                board_title = request.form.get('board_title')
                if not board_title:
                    return handle_redirect("Lütfen Bir Pano Adı Giriniz...", "danger", 'board')
                current_board = handler(title=board_title, board_id=board_id)
                if not current_board:
                    return handle_redirect("Yetkisiz Erişim", "warning", "board")
                else:
                    return handle_redirect("Pano İsmi Güncellendi", "success", "board")
            if action == "delete_board":
                board_id = request.form.get('board_id')
                current_board = handler(board_id=board_id)
                if not current_board:
                    return handle_redirect("Yetkisiz Erişim", "warning", "board")
                else:
                    return handle_redirect("Pano Başarıyla Silindi", "success", "board")

    boards = current_user.boards
    return render_template("boards.html", boards=boards)

@app.route('/boards/<int:board_id>', methods=['GET','POST'])
@login_required
def board_detail(board_id):
    current_board = db.session.execute(db.select(Board).filter_by(id=board_id, user_id = current_user.id)).scalar_one_or_none()
    if current_board is None:
        return handle_redirect("Yetkisiz Erişim", "warning")

        
        action = request.form.get('action')
        handler = ACTIONS.get(action)
        if handler:
            # Pano Detayları (Listeler)
            if action == 'create_list':
                title = request.form.get('list_title')
                if not title:
                    return handle_redirect("Başlık Boş Olamaz", "warning", 'board_detail', board_id=board_id)
                new_list = handler(title=title, board_id=board_id, current_board=current_board)
                return handle_redirect("Liste Başarıyla Oluşturuldu", "success","board_detail", board_id=board_id)

            if action == 'update_list':
                title = request.form.get('list_title')
                if not title:
                    return handle_redirect("Başlık Boş Olamaz", "warning", 'board_detail', board_id=board_id)
                list_id = request.form.get('list_id')
                current_list = handler(title=title, list_id=list_id, current_board=current_board)
                if not current_list:
                    return handle_redirect("Yetkisiz Erişim", "warning" , 'board_detail', board_id=board_id)
                else:
                    return handle_redirect("Liste Başarıyla Güncellendi", "success" , 'board_detail', board_id=board_id)
            if action == 'delete_list':
                list_id = request.form.get('list_id')
                current_list = handler(list_id=list_id, current_board=current_board)
                if not current_list:
                    return handle_redirect("Yetkisiz Erişim", "warning" , 'board_detail', board_id=board_id)
                else:
                    return handle_redirect("Liste Başarıyla Silindi", "success", 'board_detail', board_id=board_id)


            # Liste Detayları (Listeye Görev Ekleme)
            elif action == 'create_quest':
                list_id = request.form.get('list_id')
                current_list = db.session.execute(
                    db.select(List).filter_by(id=list_id, board_id=board_id)).scalar_one_or_none()
                if not current_list:
                    return handle_redirect("Yetkisiz Erişim", "warning")
                title = request.form.get('quest_title')
                if not title:
                    return handle_redirect("Başlık Boş Olamaz", "warning", 'board_detail', board_id=board_id)

                description = request.form.get('quest_description')
                quest_notes = request.form.get('quest_notes')
                new_quest = handler(title=title, description=description, quest_notes=quest_notes, current_list=current_list)
                return handle_redirect("Görev Başarıyla Oluşturuldu", "success", "board_detail", board_id=board_id)

            elif action == 'update_quest':
                quest_title = request.form.get('quest_title')
                if not quest_title:
                    return handle_redirect("Lütfen Bir Görev Başlığı Giriniz...", "warning", 'board_detail', board_id=board_id)
                quest_description = request.form.get('quest_description')
                quest_notes = request.form.get('quest_notes')
                quest_id = request.form.get('quest_id')
                current_quest = handler(title=quest_title, quest_id=quest_id, description=quest_description, quest_notes=quest_notes)
                if not current_quest:
                    return handle_redirect("Yetkisiz Erişim", "warning", 'board_detail', board_id=board_id)
                else:
                    return handle_redirect("Görev İsmi Başarıyla Değiştirildi", "success", "board_detail", board_id=board_id)

            elif action == 'delete_quest':
                quest_id = request.form.get('quest_id')
                current_quest = handler(quest_id=quest_id)
                if not current_quest:
                    return handle_redirect("Yetkisiz Erişim", "warning", 'board_detail', board_id=board_id)
                else:
                    return handle_redirect("Görev Başarıyla Silindi", "success", 'board_detail', board_id=board_id)

            # Görev Detayları (Görev Durum Güncelleme)
            elif action == 'toggle_quest_status':
                quest_id = request.form.get('quest_id')
                is_finished = 'is_finished' in request.form
                current_quest = db.session.execute(db.select(Quest).filter_by(id=quest_id)).scalar()

                if not current_quest:
                    return handle_redirect("Yetkisiz Erişim", "warning")

                quest_status = handler(current_quest, is_finished)
                return handle_redirect("Görev Durumu Güncellendi", "success","board_detail", board_id=board_id)

    return render_template("board_detail.html", board=current_board)



@app.route('/user/detail', methods=['GET', 'POST'])
@login_required
def user_detail():
    username_form = request.form.get('username')
    action = request.form.get('action')
    if action == 'kayit':
        username_check = db.session.execute(db.select(User).filter_by(username=username_form)).scalar()
        if username_check:
            flash("Bu Kullanıcı Adı Zaten Kullanılıyor")
            return redirect(url_for('user_detail'))
        if len(username_form) < 6 or len(username_form) > 25:
            flash("Kullanıcı Adı Minimum 6 Maximum 25 Karakter Olmalıdır")
            return redirect(url_for('user_detail'))
        current_user.username = username_form
        db.session.commit()
        flash("Kullanıcı Adınız Başarıyla Değiştirildi")
        return redirect(url_for('user_detail'))
    return render_template("user_detail.html")

@app.route('/quest_detail/<int:quest_id>', methods=['GET', 'POST'])
@login_required
def quest_detail(quest_id):
    current_quest = db.session.execute(db.select(Quest).filter_by(id=quest_id)).scalar_one_or_none()
    current_list = db.session.execute(db.select(List).filter_by(id=current_quest.list_id)).scalar_one_or_none()
    if not current_quest:
        return handle_redirect("Yetkisiz Erişim", "warning", 'quest_detail', quest_id=quest_id)
    if current_quest:
        if current_list.board.user_id != current_user.id:
            return handle_redirect("Yetkisiz Erişim", "warning", 'quest_detail', quest_id=quest_id)

    return render_template("quest_detail.html", quest=current_quest, list=current_list)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("Yeniden Kayıt Olmak İçin Mevcut Hesaptan Çıkış Yapmalısın","warning")
        return redirect(url_for('first_page'))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password)
        email_check = db.session.execute(db.select(User).filter_by(email=email)).scalar()
        if email_check:
            flash('email already registered',"warning")
            return redirect(url_for('register'))
        username = email.split('@')[0]
        username_check = db.session.execute(db.select(User).filter_by(username=username)).scalar()
        if username_check:
            i = 1
            while True:
                new_username = f"{username}-{i}"
                exists = db.session.execute(db.select(User).filter_by(username=new_username)).scalar()
                if not exists:
                    username = new_username
                    break
                i += 1

        new_user = User(
            email=email,
            username=username,
            password=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Başarıyla Kayıt Oldunuz","success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("Zaten Giriş Yaptınız","warning")
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Username or password is incorrect", "warning")
            return redirect(url_for('login'))
        if not check_password_hash(user.password, password):
            flash("Username or password is incorrect", "warning")
            return redirect(url_for('login'))

        login_user(user)
        utc_plus_3 = timezone(timedelta(hours=3))
        user.last_login = datetime.now(utc_plus_3)
        db.session.commit()
        flash("Logged in Successfully", "success")
        return redirect(url_for('home'))

    return render_template("login.html",form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Logged out Successfully", "success")
    return redirect(url_for('first_page'))

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=(os.getenv('APP_ENV', 'development').lower() != 'production')
    )

