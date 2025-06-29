#!/usr/bin/env python3
"""
PickleballAI Root Console
Command-line interface for managing the PickleballAI platform
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class RootConsole:
    def __init__(self):
        self.data_dir = "data"
        self.coaches_file = os.path.join(self.data_dir, "coaches.json")
        self.users_file = os.path.join(self.data_dir, "users.json")
        self.storage_file = os.path.join(self.data_dir, "storage.json")
        self.transactions_file = os.path.join(self.data_dir, "transactions.json")
        self.logs_dir = "logs"
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Initialize data files if they don't exist
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
                print(f"❌ Coach with email {email} already exists")
                return
        
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
        print(f"✅ Coach {name} ({email}) created successfully")
        print(f"   ID: {coach['id']}")
        print(f"   Specialization: {specialization}")
        print(f"   Hourly Rate: ${hourly_rate}")
    
    def block_coach(self, email: str):
        """Block a coach's access"""
        data = self._load_data(self.coaches_file)
        
        for coach in data.get("coaches", []):
            if coach["email"] == email:
                coach["status"] = "blocked"
                self._save_data(self.coaches_file, data)
                
                self._log_action("BLOCK_COACH", f"Blocked coach: {email}")
                print(f"✅ Coach {email} has been blocked")
                return
        
        print(f"❌ Coach with email {email} not found")
    
    def unblock_coach(self, email: str):
        """Unblock a coach's access"""
        data = self._load_data(self.coaches_file)
        
        for coach in data.get("coaches", []):
            if coach["email"] == email:
                coach["status"] = "active"
                self._save_data(self.coaches_file, data)
                
                self._log_action("UNBLOCK_COACH", f"Unblocked coach: {email}")
                print(f"✅ Coach {email} has been unblocked")
                return
        
        print(f"❌ Coach with email {email} not found")
    
    def create_user(self, email: str, name: str, role: str = "student"):
        """Create a new user account"""
        data = self._load_data(self.users_file)
        
        # Check if user already exists
        for user in data.get("users", []):
            if user["email"] == email:
                print(f"❌ User with email {email} already exists")
                return
        
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
        print(f"✅ User {name} ({email}) created successfully")
        print(f"   ID: {user['id']}")
        print(f"   Role: {role}")
    
    def create_storage_bucket(self, bucket_name: str, purpose: str, size_gb: int):
        """Create a new storage bucket"""
        data = self._load_data(self.storage_file)
        
        # Check if bucket already exists
        for bucket in data.get("buckets", []):
            if bucket["name"] == bucket_name:
                print(f"❌ Bucket with name {bucket_name} already exists")
                return
        
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
        print(f"✅ Storage bucket '{bucket_name}' created successfully")
        print(f"   ID: {bucket['id']}")
        print(f"   Purpose: {purpose}")
        print(f"   Size: {size_gb}GB")
    
    def view_logs(self, days: int = 1):
        """View logs for the specified number of days"""
        print(f"\n📋 Viewing logs for the last {days} day(s):")
        print("=" * 60)
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            log_file = os.path.join(self.logs_dir, f"root_actions_{date}.log")
            
            if os.path.exists(log_file):
                print(f"\n📅 {date}:")
                print("-" * 40)
                with open(log_file, 'r') as f:
                    content = f.read()
                    if content.strip():
                        print(content)
                    else:
                        print("No actions logged")
            else:
                print(f"\n📅 {date}: No log file found")
    
    def view_daily_report(self, date: str = None):
        """View daily activity report"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        print(f"\n📊 Daily Report for {date}")
        print("=" * 50)
        
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
        
        print(f"Active Coaches: {active_coaches}")
        print(f"Active Users: {active_users}")
        print(f"Today's Sessions: {total_sessions}")
        print(f"Today's Revenue: ${total_revenue:.2f}")
        
        if today_transactions:
            print(f"\nRecent Transactions:")
            for transaction in today_transactions[-5:]:  # Show last 5
                print(f"  {transaction.get('time', '')} - {transaction.get('description', '')} - ${transaction.get('amount', 0):.2f}")
    
    def list_coaches(self):
        """List all coaches"""
        data = self._load_data(self.coaches_file)
        
        print("\n👨‍🏫 Coaches:")
        print("=" * 80)
        print(f"{'ID':<10} {'Name':<20} {'Email':<25} {'Status':<10} {'Rate':<10} {'Earnings':<12}")
        print("-" * 80)
        
        for coach in data.get("coaches", []):
            print(f"{coach['id']:<10} {coach['name']:<20} {coach['email']:<25} {coach['status']:<10} ${coach['hourly_rate']:<9} ${coach['total_earnings']:<11}")
    
    def list_users(self):
        """List all users"""
        data = self._load_data(self.users_file)
        
        print("\n👤 Users:")
        print("=" * 70)
        print(f"{'ID':<10} {'Name':<20} {'Email':<25} {'Role':<10} {'Status':<10}")
        print("-" * 70)
        
        for user in data.get("users", []):
            print(f"{user['id']:<10} {user['name']:<20} {user['email']:<25} {user['role']:<10} {user['status']:<10}")
    
    def list_storage(self):
        """List all storage buckets"""
        data = self._load_data(self.storage_file)
        
        print("\n🗄️ Storage Buckets:")
        print("=" * 70)
        print(f"{'ID':<10} {'Name':<20} {'Purpose':<20} {'Used/Total':<15} {'Status':<10}")
        print("-" * 70)
        
        for bucket in data.get("buckets", []):
            usage = f"{bucket['used_gb']}/{bucket['size_gb']}GB"
            print(f"{bucket['id']:<10} {bucket['name']:<20} {bucket['purpose']:<20} {usage:<15} {bucket['status']:<10}")
    
    def show_menu(self):
        """Show the main menu"""
        print("\n" + "=" * 60)
        print("🏓 PickleballAI Root Console")
        print("=" * 60)
        print("1. Create Coach")
        print("2. Block/Unblock Coach")
        print("3. Create User")
        print("4. Create Storage Bucket")
        print("5. View Logs")
        print("6. View Daily Report")
        print("7. List Coaches")
        print("8. List Users")
        print("9. List Storage")
        print("0. Exit")
        print("=" * 60)
    
    def run(self):
        """Run the root console"""
        while True:
            self.show_menu()
            choice = input("\nEnter your choice (0-9): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            
            elif choice == "1":
                print("\n📝 Create New Coach:")
                email = input("Email: ").strip()
                name = input("Name: ").strip()
                specialization = input("Specialization: ").strip()
                try:
                    hourly_rate = float(input("Hourly Rate ($): ").strip())
                    self.create_coach(email, name, specialization, hourly_rate)
                except ValueError:
                    print("❌ Invalid hourly rate")
            
            elif choice == "2":
                print("\n🚫 Block/Unblock Coach:")
                email = input("Coach Email: ").strip()
                action = input("Action (block/unblock): ").strip().lower()
                if action == "block":
                    self.block_coach(email)
                elif action == "unblock":
                    self.unblock_coach(email)
                else:
                    print("❌ Invalid action. Use 'block' or 'unblock'")
            
            elif choice == "3":
                print("\n📝 Create New User:")
                email = input("Email: ").strip()
                name = input("Name: ").strip()
                role = input("Role (student/coach/admin): ").strip() or "student"
                self.create_user(email, name, role)
            
            elif choice == "4":
                print("\n📦 Create Storage Bucket:")
                bucket_name = input("Bucket Name: ").strip()
                purpose = input("Purpose: ").strip()
                try:
                    size_gb = int(input("Size (GB): ").strip())
                    self.create_storage_bucket(bucket_name, purpose, size_gb)
                except ValueError:
                    print("❌ Invalid size")
            
            elif choice == "5":
                try:
                    days = int(input("Number of days to view (default 1): ").strip() or "1")
                    self.view_logs(days)
                except ValueError:
                    print("❌ Invalid number of days")
            
            elif choice == "6":
                date = input("Date (YYYY-MM-DD, default today): ").strip() or None
                self.view_daily_report(date)
            
            elif choice == "7":
                self.list_coaches()
            
            elif choice == "8":
                self.list_users()
            
            elif choice == "9":
                self.list_storage()
            
            else:
                print("❌ Invalid choice. Please enter 0-9.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    console = RootConsole()
    console.run() 