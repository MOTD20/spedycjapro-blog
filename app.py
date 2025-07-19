from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-super-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spedycjapro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Blog Post Model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(300))
    image_url = db.Column(db.String(500))
    category = db.Column(db.String(50), default='Ogólne')
    tags = db.Column(db.String(200))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    
    author = db.relationship('User', backref=db.backref('posts', lazy=True))
    
    def __repr__(self):
        return f'<Post {self.title}>'

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Musisz się zalogować, aby uzyskać dostęp do tej strony.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Musisz się zalogować, aby uzyskać dostęp do tej strony.', 'warning')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('Nie masz uprawnień administratora.', 'error')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/artykuly')
def artykuly():
    return render_template('artykuly.html')

@app.route('/porady')
def porady():
    return render_template('porady.html')

@app.route('/kontakt')
def kontakt():
    return render_template('kontakt.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        # Validation
        if not all([username, email, password, confirm_password, first_name, last_name]):
            flash('Wszystkie pola są wymagane.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Hasła nie są identyczne.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Hasło musi mieć co najmniej 6 znaków.', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Nazwa użytkownika już istnieje.', 'error')
            return render_template('register.html')
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Adres email już istnieje.', 'error')
            return render_template('register.html')
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Konto zostało utworzone pomyślnie! Możesz się teraz zalogować.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Wystąpił błąd podczas tworzenia konta. Spróbuj ponownie.', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        if not username or not password:
            flash('Wprowadź nazwę użytkownika i hasło.', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            session['is_admin'] = user.is_admin
            
            if remember:
                session.permanent = True
            
            flash(f'Witaj z powrotem, {user.first_name}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Nieprawidłowa nazwa użytkownika lub hasło.', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Zostałeś wylogowany.', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/api/check-auth')
def check_auth():
    if 'user_id' in session:
        return jsonify({
            'authenticated': True,
            'user': {
                'username': session['username'],
                'first_name': session['first_name'],
                'last_name': session['last_name']
            }
        })
    return jsonify({'authenticated': False})

# Blog Routes
@app.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(is_published=True).order_by(Post.created_at.desc()).paginate(
        page=page, per_page=6, error_out=False)
    return render_template('blog.html', posts=posts)

@app.route('/blog/<slug>')
def post_detail(slug):
    post = Post.query.filter_by(slug=slug, is_published=True).first_or_404()
    post.views += 1
    db.session.commit()
    return render_template('post_detail.html', post=post)

# Admin Routes
@app.route('/admin')
@admin_required
def admin_dashboard():
    total_posts = Post.query.count()
    published_posts = Post.query.filter_by(is_published=True).count()
    total_users = User.query.count()
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_posts=total_posts,
                         published_posts=published_posts,
                         total_users=total_users,
                         recent_posts=recent_posts)

@app.route('/admin/posts')
@admin_required
def admin_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin/posts.html', posts=posts)

@app.route('/admin/posts/new', methods=['GET', 'POST'])
@admin_required
def admin_new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        excerpt = request.form.get('excerpt')
        category = request.form.get('category')
        tags = request.form.get('tags')
        image_url = request.form.get('image_url')
        is_published = 'is_published' in request.form
        
        # Generate slug from title
        slug = title.lower().replace(' ', '-').replace('ą', 'a').replace('ć', 'c').replace('ę', 'e').replace('ł', 'l').replace('ń', 'n').replace('ó', 'o').replace('ś', 's').replace('ź', 'z').replace('ż', 'z')
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        
        new_post = Post(
            title=title,
            slug=slug,
            content=content,
            excerpt=excerpt,
            category=category,
            tags=tags,
            image_url=image_url,
            author_id=session['user_id'],
            is_published=is_published
        )
        
        db.session.add(new_post)
        db.session.commit()
        
        flash('Post został utworzony pomyślnie!', 'success')
        return redirect(url_for('admin_posts'))
    
    return render_template('admin/new_post.html')

@app.route('/admin/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.excerpt = request.form.get('excerpt')
        post.category = request.form.get('category')
        post.tags = request.form.get('tags')
        post.image_url = request.form.get('image_url')
        post.is_published = 'is_published' in request.form
        
        # Update slug if title changed
        new_slug = post.title.lower().replace(' ', '-').replace('ą', 'a').replace('ć', 'c').replace('ę', 'e').replace('ł', 'l').replace('ń', 'n').replace('ó', 'o').replace('ś', 's').replace('ź', 'z').replace('ż', 'z')
        new_slug = ''.join(c for c in new_slug if c.isalnum() or c == '-')
        post.slug = new_slug
        
        db.session.commit()
        
        flash('Post został zaktualizowany pomyślnie!', 'success')
        return redirect(url_for('admin_posts'))
    
    return render_template('admin/edit_post.html', post=post)

@app.route('/admin/posts/<int:post_id>/delete', methods=['POST'])
@admin_required
def admin_delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    
    flash('Post został usunięty pomyślnie!', 'success')
    return redirect(url_for('admin_posts'))

@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/<int:user_id>/toggle-admin', methods=['POST'])
@admin_required
def admin_toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    
    status = 'administratorem' if user.is_admin else 'użytkownikiem'
    flash(f'Użytkownik {user.username} jest teraz {status}!', 'success')
    return redirect(url_for('admin_users'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@spedycjapro.pl',
                first_name='Administrator',
                last_name='Systemu',
                is_admin=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Admin user created: admin / admin123")
        
        # Create sample posts if none exist
        if Post.query.count() == 0:
            sample_posts = [
                {
                    'title': 'Optymalizacja tras transportowych w 2025 roku',
                    'content': '''
                    <h2>Wprowadzenie</h2>
                    <p>W dobie rosnącej konkurencji i zmieniających się przepisów, optymalizacja tras jest kluczowa dla efektywności firm logistycznych.</p>
                    
                    <h2>Nowe technologie</h2>
                    <p>Sztuczna inteligencja i machine learning rewolucjonizują sposób planowania tras. Algorytmy mogą teraz uwzględniać:</p>
                    <ul>
                        <li>Ruch drogowy w czasie rzeczywistym</li>
                        <li>Warunki pogodowe</li>
                        <li>Ograniczenia czasowe</li>
                        <li>Koszty paliwa</li>
                    </ul>
                    
                    <h2>Korzyści</h2>
                    <p>Implementacja nowoczesnych rozwiązań może przynieść:</p>
                    <ul>
                        <li>Redukcję kosztów o 15-25%</li>
                        <li>Skrócenie czasu dostawy o 20%</li>
                        <li>Zmniejszenie emisji CO2</li>
                        <li>Zwiększenie satysfakcji klientów</li>
                    </ul>
                    ''',
                    'excerpt': 'W dobie rosnącej konkurencji i zmieniających się przepisów, optymalizacja tras jest kluczowa dla efektywności firm logistycznych.',
                    'category': 'Optymalizacja',
                    'tags': 'transport, optymalizacja, AI, logistyka',
                    'image_url': 'https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?auto=format&fit=crop&w=600&q=80',
                    'is_published': True
                },
                {
                    'title': 'Jak bezpiecznie przewozić ładunki niebezpieczne?',
                    'content': '''
                    <h2>Klasyfikacja ładunków niebezpiecznych</h2>
                    <p>Ładunki niebezpieczne są klasyfikowane według 9 głównych klas zgodnie z przepisami ADR.</p>
                    
                    <h2>Wymagania prawne</h2>
                    <p>Transport ładunków niebezpiecznych wymaga:</p>
                    <ul>
                        <li>Specjalnych uprawnień kierowcy</li>
                        <li>Odpowiedniego oznakowania pojazdu</li>
                        <li>Dokumentacji transportowej</li>
                        <li>Ubezpieczenia odpowiedzialności cywilnej</li>
                    </ul>
                    
                    <h2>Bezpieczeństwo</h2>
                    <p>Kluczowe aspekty bezpieczeństwa:</p>
                    <ul>
                        <li>Prawidłowe pakowanie i oznakowanie</li>
                        <li>Kontrola temperatury</li>
                        <li>Monitoring GPS</li>
                        <li>Plan awaryjny</li>
                    </ul>
                    ''',
                    'excerpt': 'Transport ładunków niebezpiecznych wymaga przestrzegania surowych zasad oraz odpowiedniego przygotowania.',
                    'category': 'Bezpieczeństwo',
                    'tags': 'bezpieczeństwo, ADR, ładunki niebezpieczne',
                    'image_url': 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=600&q=80',
                    'is_published': True
                }
            ]
            
            for post_data in sample_posts:
                post = Post(
                    title=post_data['title'],
                    slug=post_data['title'].lower().replace(' ', '-').replace('ą', 'a').replace('ć', 'c').replace('ę', 'e').replace('ł', 'l').replace('ń', 'n').replace('ó', 'o').replace('ś', 's').replace('ź', 'z').replace('ż', 'z'),
                    content=post_data['content'],
                    excerpt=post_data['excerpt'],
                    category=post_data['category'],
                    tags=post_data['tags'],
                    image_url=post_data['image_url'],
                    author_id=admin_user.id,
                    is_published=post_data['is_published']
                )
                db.session.add(post)
            
            db.session.commit()
            print("✅ Sample posts created")
    
    # Development
    if app.debug:
        app.run(debug=True, host='0.0.0.0', port=8000)
    else:
        # Production
        import os
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 