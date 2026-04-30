import os
import json
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
import requests
from functools import lru_cache
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['DATABASE'] = 'portfolio.db'

# ==================== UTILITIES ====================

def mask_email(email):
    """Mask email address for privacy: john.doe@gmail.com -> jo***@gm***.com"""
    if not email or '@' not in email:
        return "***@***.***"
    
    local, domain = email.split('@')
    domain_name, domain_ext = domain.rsplit('.', 1)
    
    # Show first 2 chars, mask rest
    masked_local = local[:2] + '*' * (len(local) - 2) if len(local) > 2 else local
    masked_domain = domain_name[:2] + '*' * (len(domain_name) - 2) if len(domain_name) > 2 else domain_name
    
    return f"{masked_local}@{masked_domain}.{domain_ext}"

def get_db():
    """Get database connection"""
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize database with tables"""
    db = get_db()
    cursor = db.cursor()
    
    # Ratings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            email_masked TEXT NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            review TEXT,
            project_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            image_path TEXT,
            technologies TEXT,
            github_link TEXT,
            live_link TEXT,
            featured BOOLEAN DEFAULT 0,
            order_idx INTEGER DEFAULT 0
        )
    ''')
    
    # Certificates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            organization TEXT,
            date_received TEXT,
            image_path TEXT,
            certificate_url TEXT
        )
    ''')
    
    db.commit()
    db.close()

@lru_cache(maxsize=1)
def get_github_stats(username='klyjj'):
    """Fetch GitHub user stats via API"""
    try:
        # Get user stats
        user_url = f'https://api.github.com/users/{username}'
        user_response = requests.get(user_url, timeout=5)
        
        if user_response.status_code != 200:
            return None
        
        user_data = user_response.json()
        
        # Get repos to calculate stars
        repos_url = f'https://api.github.com/users/{username}/repos'
        repos_response = requests.get(repos_url + '?per_page=100', timeout=5)
        
        total_stars = 0
        if repos_response.status_code == 200:
            repos = repos_response.json()
            total_stars = sum(repo.get('stargazers_count', 0) for repo in repos)
        
        return {
            'followers': user_data.get('followers', 0),
            'public_repos': user_data.get('public_repos', 0),
            'total_stars': total_stars,
            'bio': user_data.get('bio', ''),
            'location': user_data.get('location', ''),
            'avatar_url': user_data.get('avatar_url', '')
        }
    except Exception as e:
        print(f"Error fetching GitHub stats: {e}")
        return None

def load_projects_config():
    """Load projects from JSON config file"""
    config_path = os.path.join('data', 'projects.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'projects': []}

def load_certificates_config():
    """Load certificates from JSON config file"""
    config_path = os.path.join('data', 'certificates.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'certificates': []}

def get_all_ratings():
    """Get all ratings from database"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT name, email_masked, rating, review, created_at FROM ratings ORDER BY created_at DESC')
    ratings = [dict(row) for row in cursor.fetchall()]
    db.close()
    return ratings

def calculate_average_rating():
    """Calculate average rating from all submissions"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT AVG(rating) as avg_rating, COUNT(*) as count FROM ratings')
    result = cursor.fetchone()
    db.close()
    
    return {
        'average': round(result['avg_rating'], 1) if result['avg_rating'] else 0,
        'count': result['count'] if result['count'] else 0
    }

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page with profile and floating ratings"""
    github_stats = get_github_stats()
    ratings = get_all_ratings()
    rating_stats = calculate_average_rating()
    projects_data = load_projects_config()
    
    context = {
        'github_stats': github_stats,
        'ratings': ratings[:10],  # Show latest 10 ratings
        'rating_stats': rating_stats,
        'all_ratings_count': len(ratings),
        'profile_name': 'Klein Ric Abong',
        'profile_aliases': ['klyjj', 'kleia'],
        'profile_image': '/static/images/profile.png',
        'projects': projects_data.get('projects', [])
    }
    
    return render_template('index.html', **context)

@app.route('/projects')
def projects():
    """Projects gallery page"""
    projects_data = load_projects_config()
    github_stats = get_github_stats()
    
    return render_template('projects.html', 
                         projects=projects_data.get('projects', []),
                         github_stats=github_stats)

@app.route('/certificates')
def certificates():
    """Certificates page"""
    certs_data = load_certificates_config()
    
    return render_template('certificates.html',
                          certificates=certs_data.get('certificates', []))

@app.route('/rate')
def rate_page():
    """Render rating submission page with project list"""
    projects_data = load_projects_config()
    return render_template('rate.html', projects=projects_data.get('projects', []))

@app.route('/cv')
def cv():
    """CV view page"""
    projects_data = load_projects_config()
    certs_data = load_certificates_config()
    
    return render_template('cv.html',
                          projects=projects_data.get('projects', []),
                          certificates=certs_data.get('certificates', []))

@app.route('/api/submit-rating', methods=['POST'])
def submit_rating():
    """Submit a new rating (API endpoint)"""
    try:
        data = request.get_json()
        
        # Validate input
        if not all(key in data for key in ['name', 'email', 'rating', 'review']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        name = data['name'].strip()
        email = data['email'].strip()
        rating = int(data['rating'])
        review = data['review'].strip()
        
        if not (1 <= rating <= 5):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        if not name or not email or not review:
            return jsonify({'error': 'All fields are required'}), 400
        
        # Validate email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Mask email
        email_masked = mask_email(email)
        
        # Insert into database
        db = get_db()
        cursor = db.cursor()
        # Resolve optional project title to project_id
        project_title = data.get('project')
        project_id = None
        if project_title:
            proj_cursor = db.cursor()
            proj_cursor.execute('SELECT id FROM projects WHERE title = ?', (project_title,))
            proj_row = proj_cursor.fetchone()
            if proj_row:
                project_id = proj_row[0]
        cursor.execute('''
            INSERT INTO ratings (name, email, email_masked, rating, review, project_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, email, email_masked, rating, review, project_id))
        db.commit()
        db.close()
        
        # Clear cache
        get_github_stats.cache_clear()
        
        return jsonify({
            'success': True,
            'message': 'Rating submitted successfully!',
            'rating': {
                'name': name,
                'email_masked': email_masked,
                'rating': rating,
                'review': review,
                'created_at': datetime.now().isoformat()
            }
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ratings', methods=['GET'])
def get_ratings():
    """Get all ratings (API endpoint)"""
    ratings = get_all_ratings()
    rating_stats = calculate_average_rating()
    
    return jsonify({
        'ratings': ratings,
        'stats': rating_stats
    })

@app.route('/download-cv')
def download_cv():
    """Download CV as PDF"""
    try:
        cv_path = os.path.join('static', 'downloads', 'cv.pdf')
        if os.path.exists(cv_path):
            return send_file(cv_path, as_attachment=True, download_name='Klein_Ric_Abong_CV.pdf')
        else:
            return jsonify({'error': 'CV not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def page_not_found(e):
    """404 error handler"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """500 error handler"""
    return render_template('500.html'), 500

# ==================== INITIALIZATION ====================

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
