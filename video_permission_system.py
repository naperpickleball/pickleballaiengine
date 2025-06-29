#!/usr/bin/env python3
"""
PickleballAI Video Permission System
Controls coach access to submitted videos with read-only and edit permissions
"""

import json
import os
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

class VideoPermissionSystem:
    def __init__(self):
        self.data_dir = "data"
        self.videos_dir = "videos"
        self.permissions_file = os.path.join(self.data_dir, "video_permissions.json")
        self.videos_file = os.path.join(self.data_dir, "videos.json")
        self.logs_dir = "logs"
        
        # Ensure directories exist
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.videos_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Initialize data files
        self._init_data_files()
        
        # Setup logging
        self._setup_logging()
    
    def _init_data_files(self):
        """Initialize data files if they don't exist"""
        files_to_init = {
            self.permissions_file: {"permissions": []},
            self.videos_file: {"videos": []}
        }
        
        for file_path, default_data in files_to_init.items():
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump(default_data, f, indent=2)
    
    def _setup_logging(self):
        """Setup logging for the permission system"""
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(self.logs_dir, f"video_permissions_{today}.log")
        
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
    
    def upload_video(self, student_email: str, video_filename: str, 
                    original_path: str = None) -> Dict:
        """Upload and register a new video with student ownership"""
        
        # Generate unique video ID
        video_id = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{student_email.split('@')[0]}"
        
        # Create video record
        video = {
            "id": video_id,
            "filename": video_filename,
            "original_filename": video_filename,
            "student_email": student_email,
            "uploaded_at": datetime.now().isoformat(),
            "status": "uploaded",
            "size_bytes": 0,  # Will be updated if file exists
            "duration_seconds": 0,  # Will be updated if video processing is available
            "thumbnail_path": None,
            "analysis_status": "pending"
        }
        
        # If original file exists, copy it to videos directory
        if original_path and os.path.exists(original_path):
            video_path = os.path.join(self.videos_dir, f"{video_id}_{video_filename}")
            try:
                shutil.copy2(original_path, video_path)
                video["size_bytes"] = os.path.getsize(video_path)
                video["local_path"] = video_path
                self.logger.info(f"Video copied: {original_path} -> {video_path}")
            except Exception as e:
                self.logger.error(f"Error copying video: {str(e)}")
                return {"success": False, "error": f"Failed to copy video: {str(e)}"}
        else:
            # Just register the video without copying (for demo purposes)
            video["local_path"] = f"demo_path/{video_filename}"
        
        # Save video record
        data = self._load_data(self.videos_file)
        data.setdefault("videos", []).append(video)
        self._save_data(self.videos_file, data)
        
        # Create initial permissions (student has full access)
        self._create_permissions(video_id, student_email, ["read", "write", "delete"])
        
        self.logger.info(f"Video uploaded: {video_id} by {student_email}")
        return {"success": True, "video_id": video_id, "video": video}
    
    def _create_permissions(self, video_id: str, user_email: str, permissions: List[str]):
        """Create or update permissions for a user on a video"""
        data = self._load_data(self.permissions_file)
        
        # Remove existing permissions for this user on this video
        data["permissions"] = [
            p for p in data.get("permissions", [])
            if not (p["video_id"] == video_id and p["user_email"] == user_email)
        ]
        
        # Add new permissions
        permission = {
            "video_id": video_id,
            "user_email": user_email,
            "permissions": permissions,
            "granted_at": datetime.now().isoformat(),
            "granted_by": "system"
        }
        
        data.setdefault("permissions", []).append(permission)
        self._save_data(self.permissions_file, data)
        
        self.logger.info(f"Permissions created: {user_email} -> {video_id} ({permissions})")
    
    def assign_coach_permissions(self, video_id: str, coach_email: str, 
                               request_id: str) -> Dict:
        """Assign read and edit permissions to coach for a video"""
        
        # Verify video exists
        video = self.get_video(video_id)
        if not video:
            return {"success": False, "error": "Video not found"}
        
        # Coach gets read and edit permissions (no delete)
        permissions = ["read", "edit"]
        
        # Create coach permissions
        self._create_permissions(video_id, coach_email, permissions)
        
        # Log the permission assignment
        self.logger.info(f"Coach permissions assigned: {coach_email} -> {video_id} for request {request_id}")
        
        return {
            "success": True,
            "video_id": video_id,
            "coach_email": coach_email,
            "permissions": permissions,
            "message": f"Coach {coach_email} can now read and edit video {video_id}"
        }
    
    def check_permissions(self, video_id: str, user_email: str, 
                         required_permission: str) -> bool:
        """Check if user has required permission on video"""
        data = self._load_data(self.permissions_file)
        
        for permission in data.get("permissions", []):
            if (permission["video_id"] == video_id and 
                permission["user_email"] == user_email and
                required_permission in permission["permissions"]):
                return True
        
        return False
    
    def get_user_permissions(self, video_id: str, user_email: str) -> List[str]:
        """Get all permissions for a user on a video"""
        data = self._load_data(self.permissions_file)
        
        for permission in data.get("permissions", []):
            if (permission["video_id"] == video_id and 
                permission["user_email"] == user_email):
                return permission["permissions"]
        
        return []
    
    def get_video(self, video_id: str) -> Optional[Dict]:
        """Get video information by ID"""
        data = self._load_data(self.videos_file)
        
        for video in data.get("videos", []):
            if video["id"] == video_id:
                return video
        
        return None
    
    def get_user_videos(self, user_email: str) -> List[Dict]:
        """Get all videos a user has access to"""
        data = self._load_data(self.videos_file)
        user_videos = []
        
        for video in data.get("videos", []):
            if self.check_permissions(video["id"], user_email, "read"):
                # Add permission info to video
                video["user_permissions"] = self.get_user_permissions(video["id"], user_email)
                user_videos.append(video)
        
        return user_videos
    
    def update_video_analysis(self, video_id: str, analysis_data: Dict, 
                            updated_by: str) -> Dict:
        """Update video with analysis data (requires edit permission)"""
        
        if not self.check_permissions(video_id, updated_by, "edit"):
            return {"success": False, "error": "No edit permission on this video"}
        
        data = self._load_data(self.videos_file)
        
        for video in data.get("videos", []):
            if video["id"] == video_id:
                # Update analysis data
                video["analysis_data"] = analysis_data
                video["analysis_updated_at"] = datetime.now().isoformat()
                video["analysis_updated_by"] = updated_by
                video["analysis_status"] = "completed"
                
                self._save_data(self.videos_file, data)
                
                self.logger.info(f"Video analysis updated: {video_id} by {updated_by}")
                return {"success": True, "video_id": video_id}
        
        return {"success": False, "error": "Video not found"}
    
    def add_video_annotations(self, video_id: str, annotations: List[Dict], 
                            added_by: str) -> Dict:
        """Add annotations to video (requires edit permission)"""
        
        if not self.check_permissions(video_id, added_by, "edit"):
            return {"success": False, "error": "No edit permission on this video"}
        
        data = self._load_data(self.videos_file)
        
        for video in data.get("videos", []):
            if video["id"] == video_id:
                # Initialize annotations if not exists
                if "annotations" not in video:
                    video["annotations"] = []
                
                # Add new annotations with metadata
                for annotation in annotations:
                    annotation["added_at"] = datetime.now().isoformat()
                    annotation["added_by"] = added_by
                    annotation["annotation_id"] = f"ann_{len(video['annotations']) + 1}"
                
                video["annotations"].extend(annotations)
                video["last_annotated_at"] = datetime.now().isoformat()
                video["last_annotated_by"] = added_by
                
                self._save_data(self.videos_file, data)
                
                self.logger.info(f"Annotations added: {video_id} by {added_by} ({len(annotations)} annotations)")
                return {"success": True, "video_id": video_id, "annotations_added": len(annotations)}
        
        return {"success": False, "error": "Video not found"}
    
    def get_video_annotations(self, video_id: str, user_email: str) -> Dict:
        """Get video annotations (requires read permission)"""
        
        if not self.check_permissions(video_id, user_email, "read"):
            return {"success": False, "error": "No read permission on this video"}
        
        video = self.get_video(video_id)
        if not video:
            return {"success": False, "error": "Video not found"}
        
        return {
            "success": True,
            "video_id": video_id,
            "annotations": video.get("annotations", []),
            "user_permissions": self.get_user_permissions(video_id, user_email)
        }
    
    def delete_video(self, video_id: str, user_email: str) -> Dict:
        """Delete video (requires delete permission - only student can do this)"""
        
        if not self.check_permissions(video_id, user_email, "delete"):
            return {"success": False, "error": "No delete permission on this video"}
        
        data = self._load_data(self.videos_file)
        
        # Remove video from videos list
        data["videos"] = [v for v in data.get("videos", []) if v["id"] != video_id]
        self._save_data(self.videos_file, data)
        
        # Remove all permissions for this video
        perm_data = self._load_data(self.permissions_file)
        perm_data["permissions"] = [p for p in perm_data.get("permissions", []) if p["video_id"] != video_id]
        self._save_data(self.permissions_file, perm_data)
        
        # Delete actual file if it exists
        video = self.get_video(video_id)
        if video and "local_path" in video and os.path.exists(video["local_path"]):
            try:
                os.remove(video["local_path"])
                self.logger.info(f"Video file deleted: {video['local_path']}")
            except Exception as e:
                self.logger.error(f"Error deleting video file: {str(e)}")
        
        self.logger.info(f"Video deleted: {video_id} by {user_email}")
        return {"success": True, "video_id": video_id, "message": "Video deleted successfully"}
    
    def revoke_coach_permissions(self, video_id: str, coach_email: str, 
                                revoked_by: str) -> Dict:
        """Revoke coach permissions on video (only student can do this)"""
        
        # Check if revoker has delete permission (student)
        if not self.check_permissions(video_id, revoked_by, "delete"):
            return {"success": False, "error": "Only video owner can revoke permissions"}
        
        data = self._load_data(self.permissions_file)
        
        # Remove coach permissions
        original_count = len(data.get("permissions", []))
        data["permissions"] = [
            p for p in data.get("permissions", [])
            if not (p["video_id"] == video_id and p["user_email"] == coach_email)
        ]
        
        if len(data["permissions"]) < original_count:
            self._save_data(self.permissions_file, data)
            self.logger.info(f"Coach permissions revoked: {coach_email} -> {video_id} by {revoked_by}")
            return {"success": True, "message": f"Permissions revoked for {coach_email}"}
        else:
            return {"success": False, "error": "No permissions found to revoke"}

# Example usage
if __name__ == "__main__":
    # Initialize the system
    permission_system = VideoPermissionSystem()
    
    # Example: Upload video and assign coach permissions
    result = permission_system.upload_video(
        student_email="student1@example.com",
        video_filename="serve_analysis.mp4"
    )
    
    if result["success"]:
        video_id = result["video_id"]
        
        # Assign coach permissions
        coach_result = permission_system.assign_coach_permissions(
            video_id=video_id,
            coach_email="coach1@example.com",
            request_id="req_1"
        )
        
        print("Upload Result:", result)
        print("Coach Permissions:", coach_result) 