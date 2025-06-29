#!/usr/bin/env python3
"""
PickleballAI Coach Flow Demo
Demonstrates the complete flow from student request to coach notification
"""

import json
import os
from datetime import datetime
from coach_notification_system import CoachNotificationSystem

def create_sample_data():
    """Create sample coaches and users for testing"""
    notification_system = CoachNotificationSystem()
    
    # Create sample coaches
    coaches_data = {
        "coaches": [
            {
                "id": "coach_1",
                "email": "coach1@example.com",
                "name": "Sarah Johnson",
                "password": "password123",
                "specialization": "Advanced Techniques",
                "hourly_rate": 75.0,
                "status": "active",
                "created_at": datetime.now().isoformat(),
                "total_earnings": 0.0,
                "total_sessions": 0
            },
            {
                "id": "coach_2", 
                "email": "coach2@example.com",
                "name": "Mike Chen",
                "password": "password123",
                "specialization": "Strategy & Tactics",
                "hourly_rate": 60.0,
                "status": "active",
                "created_at": datetime.now().isoformat(),
                "total_earnings": 0.0,
                "total_sessions": 0
            },
            {
                "id": "coach_3",
                "email": "newcoach@example.com",
                "name": "New Coach",
                "password": "password123", 
                "specialization": "Beginner Training",
                "hourly_rate": 45.0,
                "status": "active",
                "created_at": datetime.now().isoformat(),
                "total_earnings": 0.0,
                "total_sessions": 0
            }
        ]
    }
    
    # Create sample users
    users_data = {
        "users": [
            {
                "id": "user_1",
                "email": "student1@example.com",
                "name": "John Student",
                "password": "password123",
                "role": "student",
                "status": "active",
                "created_at": datetime.now().isoformat(),
                "total_spent": 0.0,
                "total_sessions": 0
            },
            {
                "id": "user_2",
                "email": "student2@example.com", 
                "name": "Jane Player",
                "password": "password123",
                "role": "student",
                "status": "active",
                "created_at": datetime.now().isoformat(),
                "total_spent": 0.0,
                "total_sessions": 0
            }
        ]
    }
    
    # Save sample data
    with open("data/coaches.json", "w") as f:
        json.dump(coaches_data, f, indent=2)
    
    with open("data/users.json", "w") as f:
        json.dump(users_data, f, indent=2)
    
    print("✅ Sample data created successfully!")

def demo_existing_coach_flow():
    """Demo flow with existing coach"""
    print("\n" + "="*60)
    print("🏓 DEMO: Existing Coach Flow")
    print("="*60)
    
    notification_system = CoachNotificationSystem()
    
    # Test 1: Student submits request to existing coach
    print("\n1️⃣ Student submits request to existing coach...")
    result = notification_system.process_annotation_request(
        student_email="student1@example.com",
        student_name="John Student",
        coach_email="coach1@example.com",  # Existing coach
        video_filename="john_serve_analysis.mp4",
        message="Please analyze my serve technique and provide feedback on my form."
    )
    
    print(f"   Result: {result['message']}")
    print(f"   Coach exists: {result['coach_exists']}")
    print(f"   Notification sent: {result.get('notification_sent', False)}")
    print(f"   Estimated cost: ${result.get('estimated_cost', 0):.2f}")
    
    # Test 2: Check coach's pending requests
    print("\n2️⃣ Checking coach's pending requests...")
    pending_requests = notification_system.get_pending_requests("coach1@example.com")
    print(f"   Pending requests: {len(pending_requests)}")
    
    for req in pending_requests:
        print(f"   - Request {req['id']}: {req['student_name']} -> {req['video_filename']}")
    
    # Test 3: Coach responds to request
    print("\n3️⃣ Coach responds to request...")
    if pending_requests:
        request_id = pending_requests[0]['id']
        success = notification_system.update_request_status(
            request_id, 
            'accepted', 
            'I\'ll analyze your serve technique and provide detailed feedback within 24 hours.'
        )
        print(f"   Request {request_id} accepted: {success}")
    
    return result

def demo_new_coach_flow():
    """Demo flow with new coach"""
    print("\n" + "="*60)
    print("🏓 DEMO: New Coach Flow")
    print("="*60)
    
    notification_system = CoachNotificationSystem()
    
    # Test: Student submits request to non-existing coach
    print("\n1️⃣ Student submits request to new coach...")
    result = notification_system.process_annotation_request(
        student_email="student2@example.com",
        student_name="Jane Player", 
        coach_email="newcoach@example.com",  # New coach
        video_filename="jane_doubles_match.mp4",
        message="I need help with my doubles strategy and positioning."
    )
    
    print(f"   Result: {result['message']}")
    print(f"   Coach exists: {result['coach_exists']}")
    print(f"   Invitation sent: {result.get('invitation_id', 'N/A')}")
    
    return result

def demo_multiple_requests():
    """Demo multiple requests to different coaches"""
    print("\n" + "="*60)
    print("🏓 DEMO: Multiple Requests")
    print("="*60)
    
    notification_system = CoachNotificationSystem()
    
    # Submit multiple requests
    requests = [
        {
            "student": ("student1@example.com", "John Student"),
            "coach": "coach2@example.com",
            "video": "john_net_play.mp4",
            "message": "Analyze my net play and volley technique."
        },
        {
            "student": ("student2@example.com", "Jane Player"),
            "coach": "coach1@example.com", 
            "video": "jane_serve_return.mp4",
            "message": "Help me improve my serve return positioning."
        },
        {
            "student": ("student1@example.com", "John Student"),
            "coach": "coach3@example.com",
            "video": "john_beginner_skills.mp4", 
            "message": "I'm a beginner, please focus on basic fundamentals."
        }
    ]
    
    for i, req in enumerate(requests, 1):
        print(f"\n{i}️⃣ Submitting request {i}...")
        result = notification_system.process_annotation_request(
            student_email=req["student"][0],
            student_name=req["student"][1],
            coach_email=req["coach"],
            video_filename=req["video"],
            message=req["message"]
        )
        print(f"   Status: {result['message']}")

def show_system_status():
    """Show current system status"""
    print("\n" + "="*60)
    print("📊 SYSTEM STATUS")
    print("="*60)
    
    notification_system = CoachNotificationSystem()
    
    # Load data
    with open("data/coaches.json", "r") as f:
        coaches_data = json.load(f)
    
    with open("data/users.json", "r") as f:
        users_data = json.load(f)
    
    with open("data/annotation_requests.json", "r") as f:
        requests_data = json.load(f)
    
    print(f"\n👨‍🏫 Coaches: {len(coaches_data['coaches'])}")
    for coach in coaches_data['coaches']:
        print(f"   - {coach['name']} ({coach['email']}) - ${coach['hourly_rate']}/hr")
    
    print(f"\n👤 Users: {len(users_data['users'])}")
    for user in users_data['users']:
        print(f"   - {user['name']} ({user['email']})")
    
    print(f"\n📝 Requests: {len(requests_data.get('requests', []))}")
    for req in requests_data.get('requests', []):
        status_color = {
            'pending': '🟡',
            'accepted': '🟢', 
            'completed': '🔵',
            'declined': '🔴'
        }.get(req['status'], '⚪')
        
        print(f"   {status_color} {req['id']}: {req['student_name']} -> {req['coach_email']} ({req['status']})")

def main():
    """Run the complete demo"""
    print("🏓 PickleballAI Coach Flow Demo")
    print("="*60)
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Create sample data
    create_sample_data()
    
    # Run demos
    demo_existing_coach_flow()
    demo_new_coach_flow() 
    demo_multiple_requests()
    
    # Show final status
    show_system_status()
    
    print("\n" + "="*60)
    print("✅ Demo completed successfully!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run coach dashboard: python coach_dashboard.py")
    print("2. Run student system: python student_request_system.py")
    print("3. Access coach dashboard: http://localhost:5001")
    print("4. Access student system: http://localhost:5002")
    print("\nTest credentials:")
    print("Coach: coach1@example.com / password123")
    print("Student: student1@example.com / password123")

if __name__ == "__main__":
    main() 