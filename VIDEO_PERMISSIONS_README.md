# Video Permission System - PickleballAI

## Overview

The Video Permission System ensures that once a student submits a video for coach annotation, the coach receives **read-only and edit permissions only**. The coach **cannot delete** the video - only the student (video owner) has delete permissions.

## Key Features

### 🔐 Permission Levels

1. **Student (Video Owner)**: `read`, `write`, `delete`
2. **Coach**: `read`, `edit` (no delete)
3. **System**: Enforces permissions at API level

### 🛡️ Security Model

- **Student Control**: Only students can delete their own videos
- **Coach Access**: Coaches can view, analyze, and annotate videos
- **No Escalation**: Coaches cannot gain delete permissions
- **Audit Trail**: All permission changes are logged

## Implementation Details

### Core Components

#### 1. VideoPermissionSystem (`video_permission_system.py`)

```python
class VideoPermissionSystem:
    def upload_video(self, student_email, video_filename)
    def assign_coach_permissions(self, video_id, coach_email, request_id)
    def check_permissions(self, video_id, user_email, required_permission)
    def add_video_annotations(self, video_id, annotations, added_by)
    def update_video_analysis(self, video_id, analysis_data, updated_by)
    def delete_video(self, video_id, user_email)  # Only students can delete
```

#### 2. CoachNotificationSystem Integration (`coach_notification_system.py`)

```python
def process_annotation_request(self, student_email, student_name, 
                             coach_email, video_filename, message):
    # 1. Upload video
    video_result = self.video_permissions.upload_video(...)
    
    # 2. Assign coach permissions (read + edit only)
    permission_result = self.video_permissions.assign_coach_permissions(...)
    
    # 3. Send notification
    notification_sent = self.send_coach_notification(...)
```

#### 3. Coach Dashboard Integration (`coach_dashboard.py`)

```python
@app.route('/video/<video_id>')
def video_detail(video_id):
    # Check if coach has access to this video
    if not dashboard.video_permissions.check_permissions(video_id, coach_email, "read"):
        return render_template('error.html', error="Access denied to this video")
    
    # Get video info and permissions
    video = dashboard.video_permissions.get_video(video_id)
    permissions = dashboard.video_permissions.get_user_permissions(video_id, coach_email)
```

## Permission Flow

### 1. Video Upload
```
Student uploads video → VideoPermissionSystem.upload_video()
→ Student gets: read, write, delete permissions
→ Video registered in system
```

### 2. Coach Assignment
```
Student requests coach annotation → CoachNotificationSystem.process_annotation_request()
→ VideoPermissionSystem.assign_coach_permissions()
→ Coach gets: read, edit permissions (no delete)
→ Email notification sent to coach
```

### 3. Coach Actions
```
Coach can:
✅ View video details
✅ Add annotations
✅ Update analysis data
✅ Export annotations
❌ Delete video (blocked by permission check)
```

### 4. Student Actions
```
Student can:
✅ View video details
✅ Delete video (only student has delete permission)
✅ Revoke coach permissions
✅ Manage all aspects of their video
```

## API Endpoints

### Video Management
- `GET /api/videos` - List coach's accessible videos
- `GET /api/videos/<video_id>` - Get video details (requires read permission)
- `POST /api/videos/<video_id>/annotations` - Add annotations (requires edit permission)
- `POST /api/videos/<video_id>/analysis` - Update analysis (requires edit permission)

### Permission Enforcement
All endpoints check permissions before allowing actions:

```python
@app.route('/api/videos/<video_id>/annotations', methods=['POST'])
def api_video_annotations(video_id):
    if 'coach_email' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    coach_email = session['coach_email']
    
    # Permission check happens in add_video_annotations()
    result = dashboard.video_permissions.add_video_annotations(
        video_id=video_id,
        annotations=annotations,
        added_by=coach_email
    )
```

## User Interface

### Coach Dashboard
- **Video List**: Shows all accessible videos with permission badges
- **Permission Indicators**: Clear visual indicators for read/edit permissions
- **No Delete Options**: Delete buttons are not shown to coaches
- **Annotation Tools**: Full annotation and analysis capabilities

### Video Detail Page
- **Permission Section**: Clear display of coach's permissions
- **Action Buttons**: Only shows actions the coach can perform
- **Security Messages**: Explains that only students can delete videos

## Data Storage

### Permissions Data (`data/video_permissions.json`)
```json
{
  "permissions": [
    {
      "video_id": "video_20250629_004855_student",
      "user_email": "coach@example.com",
      "permissions": ["read", "edit"],
      "granted_at": "2025-06-29T00:48:55.127Z",
      "granted_by": "system"
    }
  ]
}
```

### Videos Data (`data/videos.json`)
```json
{
  "videos": [
    {
      "id": "video_20250629_004855_student",
      "filename": "serve_analysis.mp4",
      "student_email": "student@example.com",
      "uploaded_at": "2025-06-29T00:48:55.126Z",
      "status": "uploaded",
      "analysis_status": "pending",
      "annotations": [],
      "analysis_data": null
    }
  ]
}
```

## Testing

### Test Script (`test_video_permissions.py`)
```bash
python3 test_video_permissions.py
```

**Test Results:**
- ✅ Video upload works
- ✅ Coach permissions assigned correctly (read + edit only)
- ✅ Coach cannot delete video (security enforced)
- ✅ Student can delete video (owner rights preserved)

## Security Features

### 1. Permission Validation
- All video operations check permissions before execution
- No way to bypass permission system
- Clear error messages for unauthorized actions

### 2. Session Management
- Coach authentication required for all video operations
- Session validation on every request
- Automatic logout on session expiry

### 3. Audit Logging
- All permission changes logged with timestamps
- User actions tracked for security monitoring
- Daily log files for review

### 4. Data Integrity
- Video ownership clearly defined
- No orphaned videos or permissions
- Cleanup on video deletion

## Benefits

### For Students
- **Control**: Maintain full control over their videos
- **Security**: Videos cannot be deleted by coaches
- **Transparency**: Clear visibility of who has access

### For Coaches
- **Access**: Can view and annotate videos as needed
- **Tools**: Full annotation and analysis capabilities
- **Clarity**: Clear understanding of their permissions

### For Platform
- **Security**: Robust permission system prevents abuse
- **Scalability**: Permission system can handle multiple coaches per video
- **Compliance**: Clear audit trail for data protection

## Future Enhancements

1. **Temporary Permissions**: Time-limited access for coaches
2. **Permission Levels**: Different coach tiers with varying access
3. **Bulk Operations**: Manage permissions for multiple videos
4. **Advanced Logging**: Detailed activity tracking
5. **API Rate Limiting**: Prevent abuse of video operations

## Conclusion

The Video Permission System successfully implements the requirement that coaches can only read and edit videos but cannot delete them. The system is secure, scalable, and provides a clear separation of responsibilities between students and coaches while maintaining full functionality for video analysis and annotation. 