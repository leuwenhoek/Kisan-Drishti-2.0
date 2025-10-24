from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
from myapi import get_plant_diagnosis
from datetime import datetime
import sqlite3
import uuid
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Required for sessions

# Configure upload folder
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Database initialization
DB_PATH = 'history.db'

def init_db():
    """Initialize the database with history table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diagnosis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            query TEXT,
            diagnosis TEXT NOT NULL,
            image_path TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            session_id TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_diagnosis(filename, query, diagnosis, image_path, session_id=None):
    """Save diagnosis to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO diagnosis_history (filename, query, diagnosis, image_path, session_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (filename, query, diagnosis, image_path, session_id))
    conn.commit()
    conn.close()

def get_user_history(session_id=None, limit=50):
    """Get user's diagnosis history"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if session_id:
        cursor.execute('''
            SELECT * FROM diagnosis_history 
            WHERE session_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (session_id, limit))
    else:
        cursor.execute('''
            SELECT * FROM diagnosis_history 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Initialize database on startup
init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/kisan-bot', methods=['GET', 'POST'])
def kisan_bot():
    # Default language
    default_language = 'English'
    
    if request.method == 'POST':
        # Check if file and query are in the request
        if 'crop-image' not in request.files:
            return render_template('kisan_bot.html', diagnosis='Error: No image uploaded.', language=default_language)
        
        file = request.files['crop-image']
        query = request.form.get('query', '')
        language = request.form.get('language', default_language)

        if file.filename == '':
            return render_template('kisan_bot.html', diagnosis='Error: No file selected.', language=language)
        
        if file and allowed_file(file.filename):
            # Get session ID for tracking user history
            session_id = session.get('user_session')
            if not session_id:
                session_id = str(uuid.uuid4())
                session['user_session'] = session_id
            
            # Create unique filename
            file_ext = os.path.splitext(file.filename)[1].lower()
            filename = f"{uuid.uuid4().hex[:8]}{file_ext}"
            
            # Save the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Get AI diagnosis with language
            diagnosis = get_plant_diagnosis(file_path, query, language)
            print(f"Diagnosis: {diagnosis}")  # Log for debugging
            
            image_path = f"uploads/{filename}"
            
            save_diagnosis(filename, query, diagnosis, image_path, session_id)
            
            return render_template('kisan_bot.html', 
                                 diagnosis=diagnosis, 
                                 image_path=image_path,
                                 success=True,
                                 language=language)
        
        return render_template('kisan_bot.html', diagnosis='Error: Invalid file format. Please upload PNG, JPG, or GIF.', language=language)

    # GET request: Render the form
    return render_template('kisan_bot.html', language=default_language)

@app.route('/history')
def history():
    # Get user's session history
    session_id = session.get('user_session')
    history_data = get_user_history(session_id)
    
    return render_template('history.html', history=history_data)

@app.route('/expert-desk')
def expert_desk():
    return render_template('expert.html')

@app.route('/team')
def about():
    return render_template('team.html')

if __name__ == "__main__":
    app.run(debug=True)