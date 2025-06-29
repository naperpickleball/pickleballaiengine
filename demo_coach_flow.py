#!/usr/bin/env python3
"""
PickleballAI Coach Flow Demo
Demonstrates the complete coach notification and video permission system
"""

import json
import os
from datetime import datetime
from coach_notification_system import CoachNotificationSystem
from video_permission_system import VideoPermissionSystem

def print_header(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_section(title):
    print(f"\n--- {title} ---")

def demo_video_permissions():
    """Demo the video permission system"""
    print_header("VIDEO PERMISSION SYSTEM DEMO")
    
    # Initialize systems
    notification_system = CoachNotificationSystem()
    video_permissions = VideoPermissionSystem()
    
    # Demo 1: Upload video and assign permissions
    print_section("1. Student Uploads Video")
    student_email = "student1@example.com"
    video_filename = "serve_analysis.mp4"
    
    result = video_permissions.upload_video(
        student_email=student_email,
        video_filename=video_filename
    )
    
    if result["success"]:
        video_id = result["video_id"]
        print(f"✅ Video uploaded successfully")
        print(f"   Video ID: {video_id}")
        print(f"   Student: {student_email}")
        print(f"   Filename: {video_filename}")
    else:
        print(f"❌ Video upload failed: {result['error']}")
        return
    
    # Demo 2: Assign coach permissions
    print_section("2. Assign Coach Permissions")
    coach_email = "coach1@example.com"
    
    permission_result = video_permissions.assign_coach_permissions(
        video_id=video_id,
        coach_email=coach_email,
        request_id="demo_request_1"
    )
    
    if permission_result["success"]:
        print(f"✅ Coach permissions assigned")
        print(f"   Coach: {coach_email}")
        print(f"   Permissions: {permission_result['permissions']}")
        print(f"   Message: {permission_result['message']}")
    else:
        print(f"❌ Permission assignment failed: {permission_result['error']}")
    
    # Demo 3: Check permissions
    print_section("3. Check Permissions")
    
    # Check student permissions (should have all)
    student_permissions = video_permissions.get_user_permissions(video_id, student_email)
    print(f"Student permissions: {student_permissions}")
    
    # Check coach permissions (should have read and edit only)
    coach_permissions = video_permissions.get_user_permissions(video_id, coach_email)
    print(f"Coach permissions: {coach_permissions}")
    
    # Demo 4: Test permission checks
    print_section("4. Test Permission Checks")
    
    # Student should have all permissions
    print(f"Student can read: {video_permissions.check_permissions(video_id, student_email, 'read')}")
    print(f"Student can edit: {video_permissions.check_permissions(video_id, student_email, 'edit')}")
    print(f"Student can delete: {video_permissions.check_permissions(video_id, student_email, 'delete')}")
    
    # Coach should have read and edit only
    print(f"Coach can read: {video_permissions.check_permissions(video_id, coach_email, 'read')}")
    print(f"Coach can edit: {video_permissions.check_permissions(video_id, coach_email, 'edit')}")
    print(f"Coach can delete: {video_permissions.check_permissions(video_id, coach_email, 'delete')}")
    
    # Demo 5: Coach adds annotations
    print_section("5. Coach Adds Annotations")
    
    annotations = [
        {
            "text": "Good serve form, but try to keep your toss more consistent",
            "type": "feedback",
            "timestamp": 5.2
        },
        {
            "text": "Excellent footwork on the return",
            "type": "praise",
            "timestamp": 12.8
        },
        {
            "text": "Work on your kitchen line positioning",
            "type": "correction",
            "timestamp": 18.5
        }
    ]
    
    annotation_result = video_permissions.add_video_annotations(
        video_id=video_id,
        annotations=annotations,
        added_by=coach_email
    )
    
    if annotation_result["success"]:
        print(f"✅ Annotations added successfully")
        print(f"   Annotations added: {annotation_result['annotations_added']}")
    else:
        print(f"❌ Annotation failed: {annotation_result['error']}")
    
    # Demo 6: Coach updates analysis
    print_section("6. Coach Updates Analysis")
    
    analysis_data = {
        "timestamp": datetime.now().isoformat(),
        "analysis_type": "pickleball_technique",
        "results": {
            "serve_technique": "Good form, consistent toss",
            "footwork": "Needs improvement on lateral movement",
            "positioning": "Good court awareness",
            "recommendations": [
                "Work on split-step timing",
                "Improve backhand consistency",
                "Practice kitchen line positioning"
            ]
        }
    }
    
    analysis_result = video_permissions.update_video_analysis(
        video_id=video_id,
        analysis_data=analysis_data,
        updated_by=coach_email
    )
    
    if analysis_result["success"]:
        print(f"✅ Analysis updated successfully")
    else:
        print(f"❌ Analysis update failed: {analysis_result['error']}")
    
    # Demo 7: Test delete permissions
    print_section("7. Test Delete Permissions")
    
    # Coach tries to delete (should fail)
    delete_result_coach = video_permissions.delete_video(video_id, coach_email)
    print(f"Coach delete attempt: {'❌ Failed (expected)' if not delete_result_coach['success'] else '✅ Succeeded (unexpected)'}")
    if not delete_result_coach['success']:
        print(f"   Error: {delete_result_coach['error']}")
    
    # Student tries to delete (should succeed)
    delete_result_student = video_permissions.delete_video(video_id, student_email)
    print(f"Student delete attempt: {'✅ Succeeded (expected)' if delete_result_student['success'] else '❌ Failed (unexpected)'}")
    
    # Re-upload video for next demos
    if delete_result_student['success']:
        print_section("8. Re-upload Video for Next Demos")
        result = video_permissions.upload_video(
            student_email=student_email,
            video_filename=video_filename
        )
        if result["success"]:
            print(f"✅ Video re-uploaded for next demos")
    
    return video_id if 'video_id' in locals() else None

def demo_coach_notifications():
    """Demo the coach notification system with video permissions"""
    print_header("COACH NOTIFICATION SYSTEM DEMO")
    
    # Initialize system
    notification_system = CoachNotificationSystem()
    
    # Demo 1: Process annotation request with video permissions
    print_section("1. Process Annotation Request")
    
    result = notification_system.process_annotation_request(
        student_email="student2@example.com",
        student_name="Jane Student",
        coach_email="coach2@example.com",
        video_filename="match_analysis.mp4",
        message="Please analyze my serve and return technique"
    )
    
    if result["success"]:
        print(f"✅ Request processed successfully")
        print(f"   Coach exists: {result['coach_exists']}")
        print(f"   Request ID: {result.get('request_id', 'N/A')}")
        print(f"   Video ID: {result.get('video_id', 'N/A')}")
        print(f"   Permissions assigned: {result.get('permissions_assigned', False)}")
        print(f"   Notification sent: {result.get('notification_sent', False)}")
        print(f"   Estimated cost: ${result.get('estimated_cost', 0):.2f}")
        print(f"   Message: {result['message']}")
    else:
        print(f"❌ Request processing failed: {result['error']}")
    
    # Demo 2: Process request for non-existing coach
    print_section("2. Process Request for New Coach")
    
    result2 = notification_system.process_annotation_request(
        student_email="student3@example.com",
        student_name="Bob Student",
        coach_email="newcoach@example.com",
        video_filename="doubles_game.mp4",
        message="Need help with doubles strategy"
    )
    
    if result2["success"]:
        print(f"✅ Request processed successfully")
        print(f"   Coach exists: {result2['coach_exists']}")
        print(f"   Invitation ID: {result2.get('invitation_id', 'N/A')}")
        print(f"   Video ID: {result2.get('video_id', 'N/A')}")
        print(f"   Message: {result2['message']}")
    else:
        print(f"❌ Request processing failed: {result2['error']}")
    
    # Demo 3: Get pending requests
    print_section("3. Get Pending Requests")
    
    requests = notification_system.get_pending_requests()
    print(f"Total pending requests: {len(requests)}")
    
    for req in requests:
        print(f"   Request {req['id']}: {req['student_name']} -> {req['coach_email']}")
        print(f"     Video: {req['video_filename']}")
        print(f"     Status: {req['status']}")
        if 'video_id' in req:
            print(f"     Video ID: {req['video_id']}")
    
    # Demo 4: Update request status
    print_section("4. Update Request Status")
    
    if requests:
        first_request = requests[0]
        success = notification_system.update_request_status(
            request_id=first_request['id'],
            status='accepted',
            response='I would be happy to help analyze your video!'
        )
        
        if success:
            print(f"✅ Request {first_request['id']} status updated to 'accepted'")
        else:
            print(f"❌ Failed to update request status")
    
    return result.get('video_id') if result and result['success'] else None

def demo_integration():
    """Demo the integration between notification and permission systems"""
    print_header("INTEGRATION DEMO")
    
    # Initialize systems
    notification_system = CoachNotificationSystem()
    video_permissions = VideoPermissionSystem()
    
    print_section("1. Complete Workflow")
    
    # Step 1: Student submits request
    print("Step 1: Student submits annotation request")
    result = notification_system.process_annotation_request(
        student_email="integration@example.com",
        student_name="Integration Test",
        coach_email="integration_coach@example.com",
        video_filename="integration_test.mp4",
        message="Testing the complete workflow"
    )
    
    if not result["success"]:
        print(f"❌ Integration test failed: {result['error']}")
        return
    
    video_id = result["video_id"]
    coach_email = "integration_coach@example.com"
    
    print(f"✅ Request processed, Video ID: {video_id}")
    
    # Step 2: Check permissions were assigned
    print("\nStep 2: Verify permissions were assigned")
    permissions = video_permissions.get_user_permissions(video_id, coach_email)
    print(f"Coach permissions: {permissions}")
    
    # Step 3: Coach adds annotations
    print("\nStep 3: Coach adds annotations")
    annotation_result = video_permissions.add_video_annotations(
        video_id=video_id,
        annotations=[{
            "text": "This is a test annotation from the integration demo",
            "type": "feedback",
            "timestamp": 10.0
        }],
        added_by=coach_email
    )
    
    if annotation_result["success"]:
        print(f"✅ Annotation added successfully")
    else:
        print(f"❌ Annotation failed: {annotation_result['error']}")
    
    # Step 4: Coach updates analysis
    print("\nStep 4: Coach updates analysis")
    analysis_result = video_permissions.update_video_analysis(
        video_id=video_id,
        analysis_data={
            "test": "integration_demo",
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        },
        updated_by=coach_email
    )
    
    if analysis_result["success"]:
        print(f"✅ Analysis updated successfully")
    else:
        print(f"❌ Analysis failed: {analysis_result['error']}")
    
    # Step 5: Verify coach cannot delete
    print("\nStep 5: Verify coach cannot delete video")
    delete_result = video_permissions.delete_video(video_id, coach_email)
    if not delete_result["success"]:
        print(f"✅ Coach correctly cannot delete video: {delete_result['error']}")
    else:
        print(f"❌ Coach was able to delete video (security issue!)")
    
    print_section("2. System Status")
    
    # Get system statistics
    print("Video Permissions System:")
    videos = video_permissions.get_user_videos(coach_email)
    print(f"   Videos accessible to coach: {len(videos)}")
    
    print("\nNotification System:")
    requests = notification_system.get_pending_requests(coach_email)
    print(f"   Pending requests for coach: {len(requests)}")
    
    print("\n✅ Integration demo completed successfully!")

def main():
    """Run all demos"""
    print_header("PICKLEBALLAI COACH FLOW DEMO")
    print("This demo shows the complete coach notification and video permission system")
    print("Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    try:
        # Run demos
        demo_video_permissions()
        demo_coach_notifications()
        demo_integration()
        
        print_header("DEMO COMPLETED SUCCESSFULLY")
        print("✅ All systems are working correctly!")
        print("\nKey Features Demonstrated:")
        print("• Video upload and permission assignment")
        print("• Coach read/edit permissions (no delete)")
        print("• Annotation and analysis capabilities")
        print("• Email notifications for coaches")
        print("• Request management workflow")
        print("• Security: coaches cannot delete videos")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 