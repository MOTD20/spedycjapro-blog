#!/bin/bash

# Initialize database
echo "🔧 Initializing database..."
python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('✅ Database tables created')
"

# Create admin user
echo "👤 Creating admin user..."
python3 -c "
from app import app, User
with app.app_context():
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
        from app import db
        db.session.add(admin_user)
        db.session.commit()
        print('✅ Admin user created: admin / admin123')
    else:
        print('✅ Admin user already exists')
"

# Start the application
echo "🚀 Starting application..."
python3 app.py 