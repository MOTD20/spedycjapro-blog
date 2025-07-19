# 🚛 SpedycjaPro Blog

Profesjonalny system blogowy dla firm spedycyjnych i logistycznych z panelem administracyjnym.

## ✨ Funkcje

- 📝 **System blogowy** z rich text editor
- 👨‍💼 **Panel administracyjny** z dashboard
- 👥 **Zarządzanie użytkownikami** i uprawnieniami
- 🏷️ **Kategorie i tagi** dla artykułów
- 🔍 **Wyszukiwanie i filtrowanie**
- 📱 **Responsywny design**
- 🔐 **System autoryzacji**
- 📊 **Statystyki i analityka**

## 🚀 Szybki start

### Wymagania
- Python 3.9+
- pip

### Instalacja lokalna

1. **Klonuj repozytorium:**
```bash
git clone <your-repo-url>
cd blog
```

2. **Zainstaluj zależności:**
```bash
pip install -r requirements.txt
```

3. **Uruchom aplikację:**
```bash
python app.py
```

4. **Otwórz w przeglądarce:**
```
http://localhost:8000
```

### Dane logowania admina
- **Login:** admin
- **Hasło:** admin123

## 🌐 Deployment

### Render.com (Darmowy)

1. **Utwórz konto na [render.com](https://render.com)**
2. **Połącz z GitHub**
3. **Utwórz nowy Web Service**
4. **Wybierz repozytorium**
5. **Ustaw:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. **Deploy!**

### Heroku

1. **Zainstaluj Heroku CLI:**
```bash
# macOS
brew install heroku/brew/heroku

# Windows
# Pobierz z heroku.com
```

2. **Zaloguj się:**
```bash
heroku login
```

3. **Utwórz aplikację:**
```bash
heroku create twoj-blog-nazwa
```

4. **Deploy:**
```bash
git add .
git commit -m "Initial commit"
git push heroku main
```

5. **Otwórz aplikację:**
```bash
heroku open
```

### Railway.app (Darmowy)

1. **Utwórz konto na [railway.app](https://railway.app)**
2. **Połącz z GitHub**
3. **Wybierz repozytorium**
4. **Automatyczny deploy!**

### VPS (DigitalOcean, AWS, etc.)

1. **Połącz się z serwerem:**
```bash
ssh root@twoj-serwer.com
```

2. **Zainstaluj Python i nginx:**
```bash
apt update
apt install python3 python3-pip nginx
```

3. **Klonuj aplikację:**
```bash
git clone <your-repo-url>
cd blog
```

4. **Zainstaluj zależności:**
```bash
pip3 install -r requirements.txt
```

5. **Skonfiguruj systemd service:**
```bash
sudo nano /etc/systemd/system/blog.service
```

```ini
[Unit]
Description=SpedycjaPro Blog
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/blog
Environment="PATH=/var/www/blog/venv/bin"
ExecStart=/var/www/blog/venv/bin/gunicorn app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

6. **Uruchom service:**
```bash
sudo systemctl start blog
sudo systemctl enable blog
```

7. **Skonfiguruj nginx:**
```bash
sudo nano /etc/nginx/sites-available/blog
```

```nginx
server {
    listen 80;
    server_name twoja-domena.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

8. **Aktywuj konfigurację:**
```bash
sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔧 Konfiguracja

### Zmienne środowiskowe

Utwórz plik `.env`:

```env
FLASK_ENV=production
SECRET_KEY=twoj-tajny-klucz
DATABASE_URL=sqlite:///blog.db
```

### Baza danych

Aplikacja używa SQLite domyślnie. Dla produkcji zalecamy PostgreSQL:

```bash
# Zainstaluj PostgreSQL
pip install psycopg2-binary

# Zaktualizuj DATABASE_URL
DATABASE_URL=postgresql://user:password@localhost/blog
```

## 📁 Struktura projektu

```
blog/
├── app.py                 # Główna aplikacja Flask
├── requirements.txt       # Zależności Python
├── Procfile              # Konfiguracja dla Heroku/Render
├── runtime.txt           # Wersja Python
├── .gitignore           # Pliki do ignorowania
├── README.md            # Dokumentacja
├── static/              # Pliki statyczne
│   ├── styles.css
│   └── script.js
└── templates/           # Szablony HTML
    ├── admin/
    │   ├── dashboard.html
    │   ├── posts.html
    │   ├── users.html
    │   ├── new_post.html
    │   └── edit_post.html
    ├── blog.html
    ├── post_detail.html
    └── index.html
```

## 🛠️ Rozwój

### Dodawanie nowych funkcji

1. **Nowe modele** - dodaj w `app.py`
2. **Nowe szablony** - dodaj w `templates/`
3. **Nowe style** - dodaj w `static/styles.css`
4. **Nowe skrypty** - dodaj w `static/script.js`

### Testowanie

```bash
# Uruchom w trybie debug
export FLASK_ENV=development
python app.py
```

## 📞 Wsparcie

- **Email:** support@spedycjapro.pl
- **GitHub Issues:** [Zgłoś problem](https://github.com/twoj-repo/issues)

## 📄 Licencja

MIT License - zobacz plik LICENSE dla szczegółów.

---

**SpedycjaPro Blog** - Profesjonalne rozwiązanie dla firm logistycznych 🚛 