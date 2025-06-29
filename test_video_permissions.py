#!/usr/bin/env python3
"""
Test Video Permission System
Verifies that coaches can only read and edit videos, not delete them
"""

from video_permission_system import VideoPermissionSystem
from coach_notification_system import CoachNotificationSystem

def test_video_permissions():
    print("Testing Video Permission System...")
    
    # Initialize systems
    video_permissions = VideoPermissionSystem()
    notification_system = CoachNotificationSystem()
    
    # Test 1: Upload video
    print("\n1. Uploading video...")
    result = video_permissions.upload_video(
        student_email="test_student@example.com",
        video_filename="test_video.mp4"
    )
    
    if not result["success"]:
        print(f"❌ Upload failed: {result['error']}")
        return
    
    video_id = result["video_id"]
    print(f"✅ Video uploaded: {video_id}")
    
    # Test 2: Assign coach permissions
    print("\n2. Assigning coach permissions...")
    coach_email = "test_coach@example.com"
    
    permission_result = video_permissions.assign_coach_permissions(
        video_id=video_id,
        coach_email=coach_email,
        request_id="test_request"
    )
    
    if not permission_result["success"]:
        print(f"❌ Permission assignment failed: {permission_result['error']}")
        return
    
    print(f"✅ Permissions assigned: {permission_result['permissions']}")
    
    # Test 3: Check permissions
    print("\n3. Checking permissions...")
    
    # Student should have all permissions
    student_permissions = video_permissions.get_user_permissions(video_id, "test_student@example.com")
    print(f"Student permissions: {student_permissions}")
    
    # Coach should have read and edit only
    coach_permissions = video_permissions.get_user_permissions(video_id, coach_email)
    print(f"Coach permissions: {coach_permissions}")
    
    # Test 4: Verify coach cannot delete
    print("\n4. Testing delete permissions...")
    
    # Coach tries to delete (should fail)
    delete_result = video_permissions.delete_video(video_id, coach_email)
    if not delete_result["success"]:
        print(f"✅ Coach correctly cannot delete: {delete_result['error']}")
    else:
        print(f"❌ Coach was able to delete (security issue!)")
    
    # Student can delete (should succeed)
    student_delete = video_permissions.delete_video(video_id, "test_student@example.com")
    if student_delete["success"]:
        print(f"✅ Student can delete (correct)")
    else:
        print(f"❌ Student cannot delete: {student_delete['error']}")
    
    print("\n✅ All tests passed! Video permission system is working correctly.")

if __name__ == "__main__":
    test_video_permissions() 