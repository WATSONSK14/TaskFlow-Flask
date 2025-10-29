### 📋 Proje: Pano/List/Görev Yönetimi (Flask)

Modern, basit ve hızlı bir Pano → Liste → Görev yönetim uygulaması. Kullanıcılar panolar oluşturur, her panoda listeler, her listede görevler tutar. Görevlere açıklama ve not eklenebilir, görev durumu (tamamlandı/devam ediyor) yönetilir. Görsel olarak sade, responsive ve Jinja2 tabanlı bir arayüz sunar.

### 🧰 Teknolojiler
- 🐍 Flask, Flask-Login
- 🗄️ SQLAlchemy (ORM) + SQLite (varsayılan)
- 🧩 Jinja2 (template)
- 🔐 python-dotenv (.env ile konfig)
- 🎨 Vanilla JS + CSS

### ✨ Özellikler
- 🗂️ Pano CRUD: oluştur/düzenle/sil
- 🧱 Liste CRUD: oluştur/düzenle/sil
- ✅ Görev CRUD: oluştur/düzenle/sil
- 🔁 Görev durumu: tamamla/geri al (toggle)
- 📝 Görev açıklaması ve notları
- 🔎 Görev detayı sayfası (link ile)
- 🪟 Modal formlar (ekleme/düzenleme)
- 🔔 Flash mesajları (başarı/uyarı)
- 📱 Responsive düzen ve uzun metin kısaltma (line clamp)
- 🔒 Yetki kontrolü: Kullanıcıya ait olmayan kaynaklara erişim engeli

### 🖼️ Ekranlar
- Panolar: `templates/boards.html`
- Pano Detayı: `templates/board_detail.html`
- Görev Detayı: `templates/quest_detail.html`
- Giriş/Kayıt/Kullanıcı: `templates/login.html`, `templates/register.html`, `templates/user_detail.html`

### 🚀 Canlı Demo
- Demo: https://taskflow-flask-asp7.onrender.com/

### Dizinyapısı (Özet)
```
.
├─ main.py
├─ models.py
├─ extensions.py
├─ services/
│  ├─ board_service.py
│  ├─ list_service.py
│  └─ quest_service.py
├─ helpers/
│  └─ utils.py
├─ templates/
│  ├─ base.html
│  ├─ boards.html
│  ├─ board_detail.html
│  ├─ quest_detail.html
│  ├─ includes/sidebar.html
│  └─ ...
├─ static/
│  ├─ css/
│  │  ├─ base.css
│  │  ├─ dashboard.css
│  │  ├─ board_detail.css
│  │  └─ quest_detail.css
│  └─ js/
│     └─ flash-messages.js
└─ instance/
   └─ test.db (lokal sqlite)
```

### 🧪 Kurulum (Lokal Geliştirme)
1) Ortamı hazırla
- Python 3.10+ önerilir
- Sanal ortam (Windows PowerShell):
  - `python -m venv .venv`
  - `.venv\Scripts\Activate.ps1`
- Gerekli paketler:
  - `pip install -r requirements.txt` (yoksa hızlı başlangıç: `pip install flask flask-login sqlalchemy python-dotenv`)

2) .env oluştur
- Proje köküne `.env` dosyası ekleyin:
```
FLASK_SECRET_KEY=uzun-ve-rastgele-bir-anahtar
DATABASE_URL=sqlite:///instance/test.db
APP_ENV=development
SESSION_COOKIE_SAMESITE=Lax
SESSION_COOKIE_SECURE=False
REMEMBER_COOKIE_SECURE=False
```
Not:
- Geliştirmede `*_SECURE=False` mantıklıdır (HTTPS yok).
- Üretimde `*_SECURE=True` yapın.

3) ▶️ Çalıştır
- `python main.py`
- Varsayılan: `http://127.0.0.1:5000/`

### ⚙️ Konfigürasyon
- `main.py` içinde `.env`’den yüklenir:
  - `FLASK_SECRET_KEY` → `app.config['SECRET_KEY']`
  - `DATABASE_URL` → `app.config['SQLALCHEMY_DATABASE_URI']`
- Prod’da Postgres kullanacaksanız URL formatı `postgresql://` olmalı.

### 👤 Giriş/Kullanıcı
- Kayıt sayfasında e-posta/şifre ile kullanıcı oluşturulur.
- Giriş sonrası panolara erişim sağlanır.
- Kullanıcı adı ve bazı alanlar `Kullanıcı Detayları` sayfasında yönetilir.
- Oturum ve yetki akışı `Flask-Login` ile sağlanır.

### 🧱 Veri Modeli (Özet)
- User → Board (1-N)
- Board → List (1-N)
- List → Quest (1-N)
- Quest: `title`, `description`, `notes`, `is_finished`, zaman damgaları

### 🛣️ Önemli Rotalar
- `/` → İlk sayfa / yönlendirme
- `/login`, `/register`, `/logout`
- `/boards` → Panolar listesi + Pano oluşturma/düzenleme/silme (POST ile action)
- `/boards/<int:board_id>` → Pano detayı (listeler/görevler)
- `/quest_detail/<int:quest_id>` → Görev detay sayfası

POST istekleri action bazlıdır (örnekler):
- `action=create_board`, `update_board`, `delete_board`
- `action=create_list`, `update_list`, `delete_list`
- `action=create_quest`, `update_quest`, `delete_quest`, `toggle_quest_status`

### 🎯 Stil & UX
- Uzun başlıklar/açıklamalar taşmayı engellemek için 2–6 satır arası kısaltılır (CSS line clamp).
- Liste başlıklarının altında aksiyon butonları (ekle/düzenle/sil).
- Görev başlığı tıklanabilir → Görev detayı sayfası.

### 🔐 Güvenlik Notları
- Prod’da:
  - `SESSION_COOKIE_SECURE=True`
  - `REMEMBER_COOKIE_SECURE=True`
  - `SESSION_COOKIE_SAMESITE='Lax'` (ihtiyaca göre `Strict/None`)
- `FLASK_SECRET_KEY` mutlaka güçlü ve gizli olmalı (platform env var).

### ☁️ Dağıtım (Özet)
- Env değişkenlerini platform panelinden girin (`DATABASE_URL`, `FLASK_SECRET_KEY`…)
- Dosya sistemi yazma gereksinimi yok (SQLite kullanılacaksa `instance/` yazılabilir olmalı).
- Uygulama `python main.py` ile çalışır; prod’da WSGI sunucusu (gunicorn) önerilir.

### 🛠️ Geliştirme İpuçları
- Uzun metin taşmalarında CSS’te `-webkit-line-clamp` + `word-break/overflow-wrap` kullanıldı.
- Modal içerikleri `templates/board_detail.html` altındaki `<script>` fonksiyonları ile yönetiliyor (göster/gizle, input focus).
- CRUD sonrası `handle_redirect` ile flash + redirect akışı.

### 🗺️ Yol Haritası (İsteğe bağlı)
- Arama/filtreleme
- Pano paylaşımları / ekip üyeleri
- Dosya ekleri / etiket sistemi
- Görevler arası sürükle-bırak (kolaylaştırılmış ve backend uyumlu)

### 🤝 Katkı
- PR’lar memnuniyetle karşılanır. Kod okunabilirliği ve basitliği korunmalı.

---

Made with ❤️ by `watsonsk14`


