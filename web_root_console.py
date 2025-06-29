#!/usr/bin/env python3
"""
PickleballAI Web Root Console
Web interface for managing the PickleballAI platform
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

class WebRootConsole:
    def __init__(self):
        self.data_dir = "data"
        self.coaches_file = os.path.join(self.data_dir, "coaches.json")
        self.users_file = os.path.join(self.data_dir, "users.json")
        self.storage_file = os.path.join(self.data_dir, "storage.json")
        self.transactions_file = os.path.join(self.data_dir, "transactions.json")
        self.logs_dir = "logs"
        
        # Ensure directories exist
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        os.makedirs("templates", exist_ok=True)
        os.makedirs("static", exist_ok=True)
        
        # Initialize data files
        self._init_data_files()
    
    def _init_data_files(self):
        """Initialize data files with empty structures if they don't exist"""
        files_to_init = {
            self.coaches_file: {"coaches": []},
            self.users_file: {"users": []},
            self.storage_file: {"buckets": []},
            self.transactions_file: {"transactions": []}
        }
        
        for file_path, default_data in files_to_init.items():
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump(default_data, f, indent=2)
    
    def _log_action(self, action: str, details: str):
        """Log an action to the daily log file"""
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(self.logs_dir, f"root_actions_{today}.log")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {action}: {details}\n"
        
        with open(log_file, 'a') as f:
            f.write(log_entry)
    
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
    
    def create_coach(self, email: str, name: str, specialization: str, hourly_rate: float):
        """Create a new coach account"""
        data = self._load_data(self.coaches_file)
        
        # Check if coach already exists
        for coach in data.get("coaches", []):
            if coach["email"] == email:
                return {"success": False, "message": f"Coach with email {email} already exists"}
        
        coach = {
            "id": f"coach_{len(data.get('coaches', [])) + 1}",
            "email": email,
            "name": name,
            "specialization": specialization,
            "hourly_rate": hourly_rate,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "total_earnings": 0.0,
            "total_sessions": 0
        }
        
        data.setdefault("coaches", []).append(coach)
        self._save_data(self.coaches_file, data)
        
        self._log_action("CREATE_COACH", f"Created coach: {email} ({name})")
        return {"success": True, "message": f"Coach {name} created successfully", "coach": coach}
    
    def block_coach(self, email: str):
        """Block a coach's access"""
        data = self._load_data(self.coaches_file)
        
        for coach in data.get("coaches", []):
            if coach["email"] == email:
                coach["status"] = "blocked"
                self._save_data(self.coaches_file, data)
                
                self._log_action("BLOCK_COACH", f"Blocked coach: {email}")
                return {"success": True, "message": f"Coach {email} has been blocked"}
        
        return {"success": False, "message": f"Coach with email {email} not found"}
    
    def unblock_coach(self, email: str):
        """Unblock a coach's access"""
        data = self._load_data(self.coaches_file)
        
        for coach in data.get("coaches", []):
            if coach["email"] == email:
                coach["status"] = "active"
                self._save_data(self.coaches_file, data)
                
                self._log_action("UNBLOCK_COACH", f"Unblocked coach: {email}")
                return {"success": True, "message": f"Coach {email} has been unblocked"}
        
        return {"success": False, "message": f"Coach with email {email} not found"}
    
    def create_user(self, email: str, name: str, role: str = "student"):
        """Create a new user account"""
        data = self._load_data(self.users_file)
        
        # Check if user already exists
        for user in data.get("users", []):
            if user["email"] == email:
                return {"success": False, "message": f"User with email {email} already exists"}
        
        user = {
            "id": f"user_{len(data.get('users', [])) + 1}",
            "email": email,
            "name": name,
            "role": role,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "total_spent": 0.0,
            "total_sessions": 0
        }
        
        data.setdefault("users", []).append(user)
        self._save_data(self.users_file, data)
        
        self._log_action("CREATE_USER", f"Created user: {email} ({name}) - Role: {role}")
        return {"success": True, "message": f"User {name} created successfully", "user": user}
    
    def create_storage_bucket(self, bucket_name: str, purpose: str, size_gb: int):
        """Create a new storage bucket"""
        data = self._load_data(self.storage_file)
        
        # Check if bucket already exists
        for bucket in data.get("buckets", []):
            if bucket["name"] == bucket_name:
                return {"success": False, "message": f"Bucket with name {bucket_name} already exists"}
        
        bucket = {
            "id": f"bucket_{len(data.get('buckets', [])) + 1}",
            "name": bucket_name,
            "purpose": purpose,
            "size_gb": size_gb,
            "used_gb": 0,
            "status": "active",
            "created_at": datetime.now().isoformat()
        }
        
        data.setdefault("buckets", []).append(bucket)
        self._save_data(self.storage_file, data)
        
        self._log_action("CREATE_BUCKET", f"Created bucket: {bucket_name} ({size_gb}GB)")
        return {"success": True, "message": f"Storage bucket '{bucket_name}' created successfully", "bucket": bucket}
    
    def get_logs(self, days: int = 1):
        """Get logs for the specified number of days"""
        logs = []
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            log_file = os.path.join(self.logs_dir, f"root_actions_{date}.log")
            
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    content = f.read()
                    if content.strip():
                        logs.append({"date": date, "content": content})
        
        return logs
    
    def get_daily_report(self, date: str = None):
        """Get daily activity report"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Load all data
        coaches_data = self._load_data(self.coaches_file)
        users_data = self._load_data(self.users_file)
        transactions_data = self._load_data(self.transactions_file)
        
        # Count active coaches and users
        active_coaches = len([c for c in coaches_data.get("coaches", []) if c["status"] == "active"])
        active_users = len([u for u in users_data.get("users", []) if u["status"] == "active"])
        
        # Calculate today's transactions
        today_transactions = [
            t for t in transactions_data.get("transactions", [])
            if t.get("date", "").startswith(date)
        ]
        
        total_revenue = sum(t.get("amount", 0) for t in today_transactions)
        total_sessions = len(today_transactions)
        
        return {
            "date": date,
            "active_coaches": active_coaches,
            "active_users": active_users,
            "total_sessions": total_sessions,
            "total_revenue": total_revenue,
            "recent_transactions": today_transactions[-5:]  # Last 5 transactions
        }
    
    def get_coaches(self):
        """Get all coaches"""
        data = self._load_data(self.coaches_file)
        return data.get("coaches", [])
    
    def get_users(self):
        """Get all users"""
        data = self._load_data(self.users_file)
        return data.get("users", [])
    
    def get_storage(self):
        """Get all storage buckets"""
        data = self._load_data(self.storage_file)
        return data.get("buckets", [])

# Initialize the console
console = WebRootConsole()

# Routes
@app.route('/')
def index():
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple authentication (in production, use proper auth)
        if username == 'admin' and password == 'admin123':
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

# API Routes
@app.route('/api/coaches', methods=['GET', 'POST'])
def api_coaches():
    if request.method == 'GET':
        coaches = console.get_coaches()
        return jsonify({"success": True, "coaches": coaches})
    
    elif request.method == 'POST':
        data = request.json
        result = console.create_coach(
            data['email'],
            data['name'],
            data['specialization'],
            float(data['hourly_rate'])
        )
        return jsonify(result)

@app.route('/api/coaches/<action>', methods=['POST'])
def api_coach_action(action):
    data = request.json
    email = data['email']
    
    if action == 'block':
        result = console.block_coach(email)
    elif action == 'unblock':
        result = console.unblock_coach(email)
    else:
        result = {"success": False, "message": "Invalid action"}
    
    return jsonify(result)

@app.route('/api/users', methods=['GET', 'POST'])
def api_users():
    if request.method == 'GET':
        users = console.get_users()
        return jsonify({"success": True, "users": users})
    
    elif request.method == 'POST':
        data = request.json
        result = console.create_user(
            data['email'],
            data['name'],
            data.get('role', 'student')
        )
        return jsonify(result)

@app.route('/api/storage', methods=['GET', 'POST'])
def api_storage():
    if request.method == 'GET':
        buckets = console.get_storage()
        return jsonify({"success": True, "buckets": buckets})
    
    elif request.method == 'POST':
        data = request.json
        result = console.create_storage_bucket(
            data['name'],
            data['purpose'],
            int(data['size_gb'])
        )
        return jsonify(result)

@app.route('/api/logs')
def api_logs():
    days = request.args.get('days', 1, type=int)
    logs = console.get_logs(days)
    return jsonify({"success": True, "logs": logs})

@app.route('/api/report')
def api_report():
    date = request.args.get('date')
    report = console.get_daily_report(date)
    return jsonify({"success": True, "report": report})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 