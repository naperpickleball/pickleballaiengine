#!/usr/bin/env python3
"""
PickleballAI Coach Notification System
Handles email notifications for coach annotation requests
"""

import smtplib
import json
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional
import logging

class CoachNotificationSystem:
    def __init__(self):
        self.data_dir = "data"
        self.coaches_file = os.path.join(self.data_dir, "coaches.json")
        self.requests_file = os.path.join(self.data_dir, "annotation_requests.json")
        self.logs_dir = "logs"
        
        # Ensure directories exist
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Initialize data files
        self._init_data_files()
        
        # Email configuration (in production, use environment variables)
        self.smtp_config = {
            'server': 'smtp.gmail.com',
            'port': 587,
            'username': 'your-email@gmail.com',  # Replace with actual email
            'password': 'your-app-password',     # Replace with app password
            'from_name': 'PickleballAI Platform'
        }
        
        # Setup logging
        self._setup_logging()
    
    def _init_data_files(self):
        """Initialize data files if they don't exist"""
        files_to_init = {
            self.coaches_file: {"coaches": []},
            self.requests_file: {"requests": []}
        }
        
        for file_path, default_data in files_to_init.items():
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump(default_data, f, indent=2)
    
    def _setup_logging(self):
        """Setup logging for the notification system"""
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(self.logs_dir, f"coach_notifications_{today}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
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
    
    def check_coach_exists(self, email: str) -> bool:
        """Check if a coach exists in the system"""
        data = self._load_data(self.coaches_file)
        return any(coach["email"] == email for coach in data.get("coaches", []))
    
    def get_coach_by_email(self, email: str) -> Optional[Dict]:
        """Get coach information by email"""
        data = self._load_data(self.coaches_file)
        for coach in data.get("coaches", []):
            if coach["email"] == email:
                return coach
        return None
    
    def create_coach_request(self, student_email: str, student_name: str, 
                           coach_email: str, coach_name: str, 
                           video_filename: str, message: str = "") -> Dict:
        """Create a new annotation request"""
        data = self._load_data(self.requests_file)
        
        request = {
            "id": f"req_{len(data.get('requests', [])) + 1}",
            "student_email": student_email,
            "student_name": student_name,
            "coach_email": coach_email,
            "coach_name": coach_name,
            "video_filename": video_filename,
            "message": message,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "notified_at": None,
            "responded_at": None,
            "estimated_cost": self._calculate_cost(coach_email),
            "priority": "normal"
        }
        
        data.setdefault("requests", []).append(request)
        self._save_data(self.requests_file, data)
        
        self.logger.info(f"Created annotation request: {request['id']} from {student_email} to {coach_email}")
        return request
    
    def _calculate_cost(self, coach_email: str) -> float:
        """Calculate estimated cost based on coach's hourly rate"""
        coach = self.get_coach_by_email(coach_email)
        if coach:
            # Estimate 30 minutes for annotation
            return coach.get("hourly_rate", 50) * 0.5
        return 25.0  # Default cost
    
    def send_coach_notification(self, request_id: str) -> bool:
        """Send email notification to coach about annotation request"""
        data = self._load_data(self.requests_file)
        
        # Find the request
        request = None
        for req in data.get("requests", []):
            if req["id"] == request_id:
                request = req
                break
        
        if not request:
            self.logger.error(f"Request {request_id} not found")
            return False
        
        # Update request status
        request["notified_at"] = datetime.now().isoformat()
        self._save_data(self.requests_file, data)
        
        # Send email
        try:
            success = self._send_email(
                to_email=request["coach_email"],
                to_name=request["coach_name"],
                subject="New Pickleball Video Annotation Request",
                template="coach_notification",
                context={
                    "coach_name": request["coach_name"],
                    "student_name": request["student_name"],
                    "student_email": request["student_email"],
                    "video_filename": request["video_filename"],
                    "message": request["message"],
                    "estimated_cost": request["estimated_cost"],
                    "request_id": request["id"],
                    "login_url": "http://localhost:5000/coach/login"
                }
            )
            
            if success:
                self.logger.info(f"Notification sent to {request['coach_email']} for request {request_id}")
            else:
                self.logger.error(f"Failed to send notification to {request['coach_email']}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error sending notification: {str(e)}")
            return False
    
    def _send_email(self, to_email: str, to_name: str, subject: str, 
                   template: str, context: Dict) -> bool:
        """Send email using SMTP"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.smtp_config['from_name']} <{self.smtp_config['username']}>"
            msg['To'] = f"{to_name} <{to_email}>"
            
            # Create HTML content
            html_content = self._get_email_template(template, context)
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port']) as server:
                server.starttls()
                server.login(self.smtp_config['username'], self.smtp_config['password'])
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Email sending failed: {str(e)}")
            return False
    
    def _get_email_template(self, template: str, context: Dict) -> str:
        """Get email template with context"""
        if template == "coach_notification":
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 20px; border-radius: 0 0 10px 10px; }}
                    .button {{ background: #667eea; color: white; padding: 12px 24px; 
                              text-decoration: none; border-radius: 5px; display: inline-block; }}
                    .highlight {{ background: #fff3cd; padding: 10px; border-radius: 5px; margin: 10px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🏓 PickleballAI</h1>
                        <p>New Video Annotation Request</p>
                    </div>
                    <div class="content">
                        <h2>Hello {context['coach_name']},</h2>
                        
                        <p>You have received a new video annotation request from <strong>{context['student_name']}</strong>.</p>
                        
                        <div class="highlight">
                            <strong>Request Details:</strong><br>
                            • Student: {context['student_name']} ({context['student_email']})<br>
                            • Video: {context['video_filename']}<br>
                            • Estimated Cost: ${context['estimated_cost']:.2f}<br>
                            • Request ID: {context['request_id']}
                        </div>
                        
                        {f"<p><strong>Student Message:</strong><br>{context['message']}</p>" if context['message'] else ""}
                        
                        <p>To review and respond to this request, please log into your coach dashboard:</p>
                        
                        <p style="text-align: center;">
                            <a href="{context['login_url']}" class="button">Login to Coach Dashboard</a>
                        </p>
                        
                        <p><small>This is an automated notification from the PickleballAI platform.</small></p>
                    </div>
                </div>
            </body>
            </html>
            """
        
        return "Email template not found"
    
    def process_annotation_request(self, student_email: str, student_name: str,
                                 coach_email: str, video_filename: str, 
                                 message: str = "") -> Dict:
        """Main function to process an annotation request"""
        
        # Check if coach exists
        coach_exists = self.check_coach_exists(coach_email)
        
        if coach_exists:
            # Get coach information
            coach = self.get_coach_by_email(coach_email)
            coach_name = coach["name"]
            
            # Create request
            request = self.create_coach_request(
                student_email=student_email,
                student_name=student_name,
                coach_email=coach_email,
                coach_name=coach_name,
                video_filename=video_filename,
                message=message
            )
            
            # Send notification
            notification_sent = self.send_coach_notification(request["id"])
            
            return {
                "success": True,
                "coach_exists": True,
                "request_id": request["id"],
                "notification_sent": notification_sent,
                "estimated_cost": request["estimated_cost"],
                "message": f"Request sent to {coach_name}. Email notification {'sent' if notification_sent else 'failed'}."
            }
        
        else:
            # Coach doesn't exist - create invitation
            invitation = self._create_coach_invitation(
                student_email=student_email,
                student_name=student_name,
                coach_email=coach_email,
                video_filename=video_filename,
                message=message
            )
            
            return {
                "success": True,
                "coach_exists": False,
                "invitation_id": invitation["id"],
                "message": f"Coach invitation sent to {coach_email}. They will be notified to join the platform."
            }
    
    def _create_coach_invitation(self, student_email: str, student_name: str,
                                coach_email: str, video_filename: str, 
                                message: str = "") -> Dict:
        """Create a coach invitation for non-existing coaches"""
        data = self._load_data(self.requests_file)
        
        invitation = {
            "id": f"inv_{len(data.get('requests', [])) + 1}",
            "type": "coach_invitation",
            "student_email": student_email,
            "student_name": student_name,
            "coach_email": coach_email,
            "video_filename": video_filename,
            "message": message,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "invitation_sent_at": None,
            "coach_joined_at": None
        }
        
        data.setdefault("requests", []).append(invitation)
        self._save_data(self.requests_file, data)
        
        # Send invitation email
        self._send_coach_invitation(invitation)
        
        self.logger.info(f"Created coach invitation: {invitation['id']} for {coach_email}")
        return invitation
    
    def _send_coach_invitation(self, invitation: Dict) -> bool:
        """Send invitation email to potential coach"""
        try:
            success = self._send_email(
                to_email=invitation["coach_email"],
                to_name="Coach",
                subject="Join PickleballAI as a Coach",
                template="coach_invitation",
                context={
                    "student_name": invitation["student_name"],
                    "student_email": invitation["student_email"],
                    "video_filename": invitation["video_filename"],
                    "message": invitation["message"],
                    "invitation_id": invitation["id"],
                    "signup_url": "http://localhost:5000/coach/signup"
                }
            )
            
            if success:
                # Update invitation status
                data = self._load_data(self.requests_file)
                for req in data.get("requests", []):
                    if req["id"] == invitation["id"]:
                        req["invitation_sent_at"] = datetime.now().isoformat()
                        break
                self._save_data(self.requests_file, data)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error sending coach invitation: {str(e)}")
            return False
    
    def get_pending_requests(self, coach_email: str = None) -> List[Dict]:
        """Get pending requests, optionally filtered by coach"""
        data = self._load_data(self.requests_file)
        requests = data.get("requests", [])
        
        if coach_email:
            return [req for req in requests if req.get("coach_email") == coach_email and req["status"] == "pending"]
        
        return [req for req in requests if req["status"] == "pending"]
    
    def update_request_status(self, request_id: str, status: str, response: str = "") -> bool:
        """Update request status (accepted, declined, completed)"""
        data = self._load_data(self.requests_file)
        
        for request in data.get("requests", []):
            if request["id"] == request_id:
                request["status"] = status
                request["response"] = response
                request["responded_at"] = datetime.now().isoformat()
                
                self._save_data(self.requests_file, data)
                self.logger.info(f"Request {request_id} status updated to {status}")
                return True
        
        return False

# Example usage
if __name__ == "__main__":
    # Initialize the system
    notification_system = CoachNotificationSystem()
    
    # Example: Process an annotation request
    result = notification_system.process_annotation_request(
        student_email="student@example.com",
        student_name="John Student",
        coach_email="coach@example.com",
        video_filename="match_video.mp4",
        message="Please analyze my serve technique and provide feedback."
    )
    
    print("Request Result:", result) 