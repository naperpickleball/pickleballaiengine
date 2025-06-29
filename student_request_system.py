#!/usr/bin/env python3
"""
PickleballAI Student Request System
Handles student requests for coach annotations
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import secrets

# Import the notification system
from coach_notification_system import CoachNotificationSystem

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

class StudentRequestSystem:
    def __init__(self):
        self.notification_system = CoachNotificationSystem()
        self.data_dir = "data"
        self.users_file = os.path.join(self.data_dir, "users.json")
        self.coaches_file = os.path.join(self.data_dir, "coaches.json")
        
        # Ensure directories exist
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs("templates", exist_ok=True)
        os.makedirs("static", exist_ok=True)
    
    def _load_data(self, file_path: str) -> Dict:
        """Load data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _save_data(self, file_path: str, data: Dict):
        """Save data to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user login"""
        data = self._load_data(self.users_file)
        
        for user in data.get("users", []):
            if user["email"] == email and user.get("password") == password:
                return user
        
        return None
    
    def get_available_coaches(self) -> List[Dict]:
        """Get list of available coaches"""
        data = self._load_data(self.coaches_file)
        return [coach for coach in data.get("coaches", []) if coach["status"] == "active"]
    
    def get_user_requests(self, user_email: str) -> List[Dict]:
        """Get all requests for a specific user"""
        data = self._load_data(self.notification_system.requests_file)
        requests = data.get("requests", [])
        return [req for req in requests if req.get("student_email") == user_email]
    
    def submit_annotation_request(self, student_email: str, student_name: str,
                                coach_email: str, video_filename: str, 
                                message: str = "") -> Dict:
        """Submit a new annotation request"""
        return self.notification_system.process_annotation_request(
            student_email=student_email,
            student_name=student_name,
            coach_email=coach_email,
            video_filename=video_filename,
            message=message
        )

# Initialize the system
system = StudentRequestSystem()

# Routes
@app.route('/')
def index():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = system.authenticate_user(email, password)
        
        if user:
            session['user_email'] = email
            session['user_name'] = user['name']
            return redirect(url_for('dashboard'))
        else:
            return render_template('student_login.html', error='Invalid credentials')
    
    return render_template('student_login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        
        # Check if user already exists
        data = system._load_data(system.users_file)
        for user in data.get("users", []):
            if user["email"] == email:
                return render_template('student_signup.html', error='User with this email already exists')
        
        # Create new user
        user = {
            "id": f"user_{len(data.get('users', [])) + 1}",
            "email": email,
            "name": name,
            "password": password,  # In production, hash the password
            "role": "student",
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "total_spent": 0.0,
            "total_sessions": 0
        }
        
        data.setdefault("users", []).append(user)
        system._save_data(system.users_file, data)
        
        # Auto-login
        session['user_email'] = email
        session['user_name'] = name
        
        return redirect(url_for('dashboard'))
    
    return render_template('student_signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    user_email = session['user_email']
    user_name = session['user_name']
    
    # Get user data
    requests = system.get_user_requests(user_email)
    coaches = system.get_available_coaches()
    
    return render_template('student_dashboard.html', 
                         user_name=user_name,
                         requests=requests, 
                         coaches=coaches)

@app.route('/submit-request', methods=['GET', 'POST'])
def submit_request():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        coach_email = request.form.get('coach_email')
        video_filename = request.form.get('video_filename')
        message = request.form.get('message', '')
        
        result = system.submit_annotation_request(
            student_email=session['user_email'],
            student_name=session['user_name'],
            coach_email=coach_email,
            video_filename=video_filename,
            message=message
        )
        
        if result['success']:
            return render_template('request_success.html', result=result)
        else:
            return render_template('submit_request.html', 
                                 coaches=system.get_available_coaches(),
                                 error=result.get('message', 'Unknown error'))
    
    return render_template('submit_request.html', 
                         coaches=system.get_available_coaches())

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# API Routes
@app.route('/api/coaches')
def api_coaches():
    coaches = system.get_available_coaches()
    return jsonify({"success": True, "coaches": coaches})

@app.route('/api/requests')
def api_requests():
    if 'user_email' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    user_email = session['user_email']
    requests = system.get_user_requests(user_email)
    
    return jsonify({"success": True, "requests": requests})

@app.route('/api/submit-request', methods=['POST'])
def api_submit_request():
    if 'user_email' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    
    result = system.submit_annotation_request(
        student_email=session['user_email'],
        student_name=session['user_name'],
        coach_email=data['coach_email'],
        video_filename=data['video_filename'],
        message=data.get('message', '')
    )
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002) 