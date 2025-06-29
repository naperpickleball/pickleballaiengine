# PickleballAI Coach Flow System

A comprehensive system for managing coach-student interactions, from annotation requests to email notifications and dashboard management.

## 🏓 Overview

The Coach Flow System handles the complete lifecycle of annotation requests:

1. **Student submits request** → Coach receives notification
2. **Coach exists** → Immediate email notification + dashboard update
3. **Coach doesn't exist** → Invitation email sent to join platform
4. **Coach responds** → Request status updated, student notified

## 🏗️ Architecture

### Core Components

```
PickleballAI Coach Flow/
├── coach_notification_system.py    # Email notifications & request processing
├── coach_dashboard.py              # Coach web interface (port 5001)
├── student_request_system.py       # Student web interface (port 5002)
├── demo_coach_flow.py              # Demo script for testing
├── data/                           # JSON data storage
│   ├── coaches.json               # Coach profiles
│   ├── users.json                 # Student profiles  
│   └── annotation_requests.json   # Request tracking
├── logs/                          # System logs
└── templates/                     # HTML templates
```

### Data Flow

```
Student Request → Notification System → Email + Dashboard → Coach Response
     ↓                    ↓                    ↓                ↓
  Web Form           Check Coach         Send Email        Update Status
     ↓                    ↓                    ↓                ↓
  Validation         Create Request      Log Action        Notify Student
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Demo
```bash
python demo_coach_flow.py
```

### 3. Start Services
```bash
# Terminal 1: Coach Dashboard
python coach_dashboard.py

# Terminal 2: Student System  
python student_request_system.py

# Terminal 3: Root Console (optional)
python web_root_console.py
```

### 4. Access Interfaces
- **Coach Dashboard**: http://localhost:5001
- **Student System**: http://localhost:5002  
- **Root Console**: http://localhost:5000

## 👥 User Roles & Flows

### Student Flow
1. **Register/Login** → Student dashboard
2. **Select Coach** → Choose from available coaches
3. **Submit Request** → Upload video + message
4. **Track Status** → Monitor request progress
5. **Receive Analysis** → Get coach feedback

### Coach Flow
1. **Register/Login** → Coach dashboard
2. **Receive Notifications** → Email + dashboard alerts
3. **Review Requests** → View pending requests
4. **Accept/Decline** → Respond to requests
5. **Provide Analysis** → Submit feedback
6. **Track Earnings** → Monitor revenue

### Root Flow
1. **Manage Coaches** → Create, block, unblock coaches
2. **Monitor System** → View logs and reports
3. **Manage Storage** → Create storage buckets
4. **Track Revenue** → Monitor platform earnings

## 📧 Email Notification System

### Coach Notification Email
- **Subject**: "New Pickleball Video Annotation Request"
- **Content**: Request details, student info, estimated cost
- **Action**: Direct link to coach dashboard

### Coach Invitation Email  
- **Subject**: "Join PickleballAI as a Coach"
- **Content**: Platform introduction, signup link
- **Action**: Coach registration form

### Email Configuration
```python
smtp_config = {
    'server': 'smtp.gmail.com',
    'port': 587,
    'username': 'your-email@gmail.com',
    'password': 'your-app-password',
    'from_name': 'PickleballAI Platform'
}
```

## 🔧 Configuration

### Environment Variables (Production)
```bash
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Database Configuration
DATABASE_URL=postgresql://user:pass@localhost/pickleballai

# Security
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
```

### Data Storage
All data is stored in JSON files for simplicity:
- `coaches.json` - Coach profiles and credentials
- `users.json` - Student profiles and credentials  
- `annotation_requests.json` - Request tracking and status

## 📊 API Endpoints

### Coach Dashboard (Port 5001)
```
GET  /                    # Dashboard home
GET  /login              # Login page
POST /login              # Authenticate coach
GET  /signup             # Coach registration
POST /signup             # Create coach account
GET  /dashboard          # Main dashboard
GET  /logout             # Logout

# API Endpoints
GET  /api/requests       # Get coach's requests
POST /api/requests/<id>/<action>  # Accept/decline/complete
GET  /api/stats          # Get coach statistics
```

### Student System (Port 5002)
```
GET  /                    # Student home
GET  /login              # Login page
POST /login              # Authenticate student
GET  /signup             # Student registration
POST /signup             # Create student account
GET  /dashboard          # Student dashboard
GET  /submit-request     # Request form
POST /submit-request     # Submit annotation request
GET  /logout             # Logout

# API Endpoints
GET  /api/coaches        # Get available coaches
GET  /api/requests       # Get student's requests
POST /api/submit-request # Submit new request
```

## 🧪 Testing

### Demo Script
```bash
python demo_coach_flow.py
```

### Test Scenarios
1. **Existing Coach Flow**
   - Student submits request to existing coach
   - Coach receives email notification
   - Coach responds via dashboard

2. **New Coach Flow**  
   - Student submits request to new coach
   - Coach receives invitation email
   - Coach registers and responds

3. **Multiple Requests**
   - Multiple students submit requests
   - Different coaches receive notifications
   - System tracks all requests

### Test Credentials
```
Coach: coach1@example.com / password123
Student: student1@example.com / password123
Root: admin / admin123
```

## 📈 Monitoring & Logging

### Log Files
- `logs/coach_notifications_YYYY-MM-DD.log` - Email notifications
- `logs/root_actions_YYYY-MM-DD.log` - Administrative actions

### Dashboard Metrics
- **Coaches**: Active coaches, total earnings, session count
- **Students**: Active users, total spent, request count  
- **Requests**: Pending, accepted, completed, declined
- **Revenue**: Daily, weekly, monthly earnings

## 🔒 Security Features

### Authentication
- Session-based authentication
- Password protection (hash in production)
- Role-based access control

### Data Protection
- Input validation and sanitization
- SQL injection prevention (JSON storage)
- XSS protection

### Email Security
- SMTP with TLS encryption
- App passwords for Gmail
- Rate limiting (implement in production)

## 🚀 Production Deployment

### Recommended Stack
- **Backend**: Flask + Gunicorn
- **Database**: PostgreSQL
- **Email**: AWS SES or SendGrid
- **Hosting**: AWS EC2 or Heroku
- **SSL**: Let's Encrypt

### Environment Setup
```bash
# Install production dependencies
pip install gunicorn psycopg2-binary

# Set environment variables
export FLASK_ENV=production
export DATABASE_URL=postgresql://...

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 coach_dashboard:app
gunicorn -w 4 -b 0.0.0.0:5002 student_request_system:app
```

## 🔄 Future Enhancements

### Phase 2 Features
- [ ] Real-time notifications (WebSocket)
- [ ] Video upload and storage
- [ ] Payment processing (Stripe)
- [ ] Mobile app (React Native)
- [ ] AI-powered analysis integration
- [ ] Coach rating system

### Phase 3 Features  
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] Coach marketplace
- [ ] Subscription plans
- [ ] API for third-party integrations

## 📞 Support

For questions or issues:
1. Check the logs in `logs/` directory
2. Review the demo script output
3. Verify email configuration
4. Test with provided credentials

## 📄 License

This project is part of the PickleballAI platform and is proprietary software. 