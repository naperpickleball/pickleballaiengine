#!/usr/bin/env python3
"""
PickleballAI Coach Dashboard
Web interface for coaches to manage annotation requests and videos
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import secrets

# Import the notification system and video permissions
from coach_notification_system import CoachNotificationSystem
from video_permission_system import VideoPermissionSystem

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

class CoachDashboard:
    def __init__(self):
        self.notification_system = CoachNotificationSystem()
        self.video_permissions = VideoPermissionSystem()
        self.data_dir = "data"
        self.coaches_file = os.path.join(self.data_dir, "coaches.json")
        self.requests_file = os.path.join(self.data_dir, "annotation_requests.json")
        
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
    
    def authenticate_coach(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate coach login"""
        data = self._load_data(self.coaches_file)
        
        for coach in data.get("coaches", []):
            if coach["email"] == email and coach.get("password") == password:
                return coach
        
        return None
    
    def get_coach_requests(self, coach_email: str) -> List[Dict]:
        """Get all requests for a specific coach with video information"""
        requests = self.notification_system.get_pending_requests(coach_email)
        
        # Add video information to each request
        for req in requests:
            if "video_id" in req:
                video = self.video_permissions.get_video(req["video_id"])
                if video:
                    req["video_info"] = video
                    req["user_permissions"] = self.video_permissions.get_user_permissions(
                        req["video_id"], coach_email
                    )
        
        return requests
    
    def get_coach_videos(self, coach_email: str) -> List[Dict]:
        """Get all videos the coach has access to"""
        return self.video_permissions.get_user_videos(coach_email)
    
    def get_coach_stats(self, coach_email: str) -> Dict:
        """Get coach statistics"""
        data = self._load_data(self.requests_file)
        requests = data.get("requests", [])
        
        coach_requests = [req for req in requests if req.get("coach_email") == coach_email]
        coach_videos = self.get_coach_videos(coach_email)
        
        stats = {
            "total_requests": len(coach_requests),
            "pending_requests": len([req for req in coach_requests if req["status"] == "pending"]),
            "accepted_requests": len([req for req in coach_requests if req["status"] == "accepted"]),
            "completed_requests": len([req for req in coach_requests if req["status"] == "completed"]),
            "total_earnings": sum(req.get("estimated_cost", 0) for req in coach_requests if req["status"] in ["accepted", "completed"]),
            "total_videos": len(coach_videos),
            "videos_with_annotations": len([v for v in coach_videos if v.get("annotations")])
        }
        
        return stats

# Initialize the dashboard
dashboard = CoachDashboard()

# Routes
@app.route('/')
def index():
    if 'coach_email' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        coach = dashboard.authenticate_coach(email, password)
        
        if coach:
            session['coach_email'] = email
            session['coach_name'] = coach['name']
            return redirect(url_for('dashboard'))
        else:
            return render_template('coach_login.html', error='Invalid credentials')
    
    return render_template('coach_login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        specialization = request.form.get('specialization')
        hourly_rate = float(request.form.get('hourly_rate', 50))
        
        # Check if coach already exists
        if dashboard.notification_system.check_coach_exists(email):
            return render_template('coach_signup.html', error='Coach with this email already exists')
        
        # Create new coach
        data = dashboard._load_data(dashboard.coaches_file)
        
        coach = {
            "id": f"coach_{len(data.get('coaches', [])) + 1}",
            "email": email,
            "name": name,
            "password": password,  # In production, hash the password
            "specialization": specialization,
            "hourly_rate": hourly_rate,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "total_earnings": 0.0,
            "total_sessions": 0
        }
        
        data.setdefault("coaches", []).append(coach)
        dashboard._save_data(dashboard.coaches_file, data)
        
        # Auto-login
        session['coach_email'] = email
        session['coach_name'] = name
        
        return redirect(url_for('dashboard'))
    
    return render_template('coach_signup.html')

@app.route('/dashboard')
def dashboard_page():
    if 'coach_email' not in session:
        return redirect(url_for('login'))
    
    coach_email = session['coach_email']
    coach_name = session['coach_name']
    
    # Get coach data
    coach = dashboard.notification_system.get_coach_by_email(coach_email)
    stats = dashboard.get_coach_stats(coach_email)
    requests = dashboard.get_coach_requests(coach_email)
    videos = dashboard.get_coach_videos(coach_email)
    
    return render_template('coach_dashboard.html', 
                         coach=coach, 
                         stats=stats, 
                         requests=requests,
                         videos=videos)

@app.route('/videos')
def videos_page():
    if 'coach_email' not in session:
        return redirect(url_for('login'))
    
    coach_email = session['coach_email']
    videos = dashboard.get_coach_videos(coach_email)
    
    return render_template('coach_videos.html', videos=videos)

@app.route('/video/<video_id>')
def video_detail(video_id):
    if 'coach_email' not in session:
        return redirect(url_for('login'))
    
    coach_email = session['coach_email']
    
    # Check if coach has access to this video
    if not dashboard.video_permissions.check_permissions(video_id, coach_email, "read"):
        return render_template('error.html', error="Access denied to this video")
    
    video = dashboard.video_permissions.get_video(video_id)
    permissions = dashboard.video_permissions.get_user_permissions(video_id, coach_email)
    annotations = dashboard.video_permissions.get_video_annotations(video_id, coach_email)
    
    return render_template('video_detail.html', 
                         video=video, 
                         permissions=permissions,
                         annotations=annotations)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# API Routes
@app.route('/api/requests', methods=['GET'])
def api_requests():
    if 'coach_email' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    coach_email = session['coach_email']
    requests = dashboard.get_coach_requests(coach_email)
    
    return jsonify({"success": True, "requests": requests})

@app.route('/api/requests/<request_id>/<action>', methods=['POST'])
def api_request_action(request_id, action):
    if 'coach_email' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    response = data.get('response', '')
    
    if action == 'accept':
        success = dashboard.notification_system.update_request_status(request_id, 'accepted', response)
    elif action == 'decline':
        success = dashboard.notification_system.update_request_status(request_id, 'declined', response)
    elif action == 'complete':
        success = dashboard.notification_system.update_request_status(request_id, 'completed', response)
    else:
        return jsonify({"error": "Invalid action"}), 400
    
    if success:
        return jsonify({"success": True, "message": f"Request {action}ed successfully"})
    else:
        return jsonify({"error": "Request not found"}), 404

@app.route('/api/videos', methods=['GET'])
def api_videos():
    if 'coach_email' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    coach_email = session['coach_email']
    videos = dashboard.get_coach_videos(coach_email)
    
    return jsonify({"success": True, "videos": videos})

@app.route('/api/videos/<video_id>/annotations', methods=['GET', 'POST'])
def api_video_annotations(video_id):
    if 'coach_email' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    coach_email = session['coach_email']
    
    if request.method == 'GET':
        result = dashboard.video_permissions.get_video_annotations(video_id, coach_email)
        return jsonify(result)
    
    elif request.method == 'POST':
        data = request.json
        annotations = data.get('annotations', [])
        
        result = dashboard.video_permissions.add_video_annotations(
            video_id=video_id,
            annotations=annotations,
            added_by=coach_email
        )
        
        return jsonify(result)

@app.route('/api/videos/<video_id>/analysis', methods=['POST'])
def api_video_analysis(video_id):
    if 'coach_email' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    coach_email = session['coach_email']
    data = request.json
    
    result = dashboard.video_permissions.update_video_analysis(
        video_id=video_id,
        analysis_data=data,
        updated_by=coach_email
    )
    
    return jsonify(result)

@app.route('/api/stats')
def api_stats():
    if 'coach_email' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    coach_email = session['coach_email']
    stats = dashboard.get_coach_stats(coach_email)
    
    return jsonify({"success": True, "stats": stats})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 