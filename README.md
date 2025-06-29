# 🎾 PickleballAI Platform

**AI-Powered Personalized Pickleball Coaching Platform**

## 🎯 **Project Overview**

A comprehensive AI coaching platform that combines:
- **Roboflow pre-trained models** for video analysis
- **Coach expertise** for personalized training
- **Edge computing** for real-time coaching anywhere
- **Multi-interface delivery** (goggles, watch, phone, earplugs)
- **Monetization model** with revenue sharing

## 🏗️ **Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                    PICKLEBALLAI PLATFORM                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │
│  │   Video Input   │    │ Roboflow Base   │    │ Coach Input  │ │
│  │   (User Video)  │───▶│   Model         │───▶│ (Annotations)│ │
│  └─────────────────┘    └─────────────────┘    └──────────────┘ │
│           │                       │                       │     │
│           ▼                       ▼                       ▼     │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │
│  │ Edge Computing  │    │ Personalized    │    │ Multi-       │ │
│  │ (Jetson Nano)   │    │ User Model      │    │ Interface    │ │
│  └─────────────────┘    └─────────────────┘    │ Delivery     │ │
│           │                       │            └──────────────┘ │
│           ▼                       ▼                             │
│  ┌─────────────────┐    ┌─────────────────┐                    │
│  │ Real-time       │    │ Monetization    │                    │
│  │ Coaching        │    │ (Revenue Share) │                    │ │
│  └─────────────────┘    └─────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
```

## 📋 **Plan of Action**

### **Phase 1: Hardcoded Prototype (2-3 weeks)**
**Goal**: Create a working prototype with mock data to demonstrate the concept

#### **Week 1: Core Prototype**
- [ ] Set up project structure
- [ ] Create mock video analysis system
- [ ] Build basic coaching feedback engine
- [ ] Develop simple web interface

#### **Week 2: Multi-Interface Prototype**
- [ ] Implement voice output simulation
- [ ] Create video annotation overlay
- [ ] Build text-based coaching interface
- [ ] Add haptic feedback simulation

#### **Week 3: Monetization Prototype**
- [ ] Create subscription tiers
- [ ] Implement revenue sharing logic
- [ ] Build coach management system
- [ ] Add payment simulation

### **Phase 2: Minimal Real Data Integration (4-6 weeks)**
**Goal**: Replace mock data with real Roboflow integration and basic AI

#### **Week 4-5: Roboflow Integration**
- [ ] Integrate Roboflow API
- [ ] Implement real video analysis
- [ ] Create basic object detection
- [ ] Build data collection pipeline

#### **Week 6-7: Coach Annotation System**
- [ ] Build coach annotation interface
- [ ] Implement correction system
- [ ] Create training dataset generation
- [ ] Add coach profile management

#### **Week 8-9: Personalized Models**
- [ ] Implement model fine-tuning
- [ ] Create user-specific models
- [ ] Build model versioning system
- [ ] Add performance tracking

### **Phase 3: Edge Computing Implementation (6-8 weeks)**
**Goal**: Deploy system to Jetson Nano or equivalent edge devices

#### **Week 10-11: Edge System Setup**
- [ ] Set up Jetson Nano development environment
- [ ] Optimize models for edge deployment
- [ ] Implement local inference
- [ ] Create edge-cloud sync

#### **Week 12-13: Multi-Interface Delivery**
- [ ] Implement voice output system
- [ ] Create AR overlay for goggles
- [ ] Build smartwatch interface
- [ ] Add earplug audio system

#### **Week 14-15: Real-time Processing**
- [ ] Optimize for low latency
- [ ] Implement real-time coaching
- [ ] Add performance monitoring
- [ ] Create offline capabilities

### **Phase 4: Monetization & Scaling (4-6 weeks)**
**Goal**: Implement full monetization and prepare for production

#### **Week 16-17: Payment Integration**
- [ ] Integrate payment processors
- [ ] Implement subscription management
- [ ] Create revenue tracking
- [ ] Add coach payout system

#### **Week 18-19: Production Deployment**
- [ ] Set up production infrastructure
- [ ] Implement monitoring and logging
- [ ] Create backup and recovery
- [ ] Add security measures

#### **Week 20-21: Scaling & Optimization**
- [ ] Optimize performance
- [ ] Implement caching strategies
- [ ] Add load balancing
- [ ] Create scaling policies

## 📁 **Project Structure**

```
PickleballAI_Platform/
├── prototype/           # Phase 1: Hardcoded prototype
│   ├── mock_data/      # Mock video data and results
│   ├── web_interface/  # Basic web UI
│   ├── voice_system/   # Voice output simulation
│   └── payment_sim/    # Payment simulation
├── backend/            # Phase 2: Real backend
│   ├── api/           # REST API endpoints
│   ├── ai_engine/     # AI analysis engine
│   ├── coach_system/  # Coach management
│   └── payment/       # Payment processing
├── frontend/           # User interfaces
│   ├── web_app/       # Web application
│   ├── mobile_app/    # Mobile app
│   └── coach_portal/  # Coach dashboard
├── edge_system/        # Phase 3: Edge computing
│   ├── jetson_code/   # Jetson Nano code
│   ├── interfaces/    # Multi-interface delivery
│   └── optimization/  # Performance optimization
├── models/            # AI models and training
│   ├── base_models/   # Roboflow base models
│   ├── personalized/  # User-specific models
│   └── training/      # Training scripts
├── data/              # Data management
│   ├── videos/        # User video uploads
│   ├── annotations/   # Coach annotations
│   └── analytics/     # Performance analytics
├── deployment/        # Production deployment
│   ├── docker/        # Docker configurations
│   ├── kubernetes/    # K8s deployment
│   └── monitoring/    # Monitoring setup
└── docs/              # Documentation
    ├── api/           # API documentation
    ├── deployment/    # Deployment guides
    └── user_guides/   # User documentation
```

## 🚀 **Getting Started**

### **Prerequisites**
- Python 3.8+
- Node.js 16+
- Docker
- Jetson Nano (for Phase 3)
- Roboflow API key

### **Quick Start**
```bash
# Clone the repository
git clone <repository-url>
cd PickleballAI_Platform

# Set up development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start prototype
cd prototype
python app.py
```

## 💰 **Monetization Model**

### **Revenue Streams**
1. **Live Coaching**: $29.99-$79.99/month (30% platform, 70% coach)
2. **Voice Commentary**: $9.99-$29.99/video (25% platform, 75% coach)
3. **Digital Twin**: $39.99-$99.99/month (20% platform, 80% coach)

### **Target Market**
- **Individual Players**: Personal coaching
- **Training Facilities**: Professional coaching system
- **Tournaments**: Event coaching services
- **Coaches**: Revenue sharing platform

## 🎯 **Success Metrics**

### **Phase 1 Success**
- [ ] Working prototype with mock data
- [ ] Multi-interface demonstration
- [ ] Payment simulation working
- [ ] User feedback collected

### **Phase 2 Success**
- [ ] Real Roboflow integration
- [ ] Coach annotation system working
- [ ] Personalized models created
- [ ] Basic monetization implemented

### **Phase 3 Success**
- [ ] Edge computing deployment
- [ ] Real-time coaching working
- [ ] Multi-interface delivery
- [ ] Performance targets met

### **Phase 4 Success**
- [ ] Full monetization system
- [ ] Production deployment
- [ ] Revenue targets achieved
- [ ] Scalable infrastructure

## 🤝 **Contributing**

This project is in active development. Please refer to the documentation for contribution guidelines.

## 📄 **License**

[License information to be added]

---

**Next Steps**: Start with Phase 1 - Hardcoded Prototype 

# PickleballAI Root Console

A comprehensive administration system for the PickleballAI platform, providing both command-line and web interfaces for managing coaches, users, storage, and monitoring system activity.

## Features

### 🔐 Authentication
- Secure login system for root administrators
- Session-based authentication
- Role-based access control

### 👨‍🏫 Coach Management
- Create new coach accounts
- Block/unblock coach access
- View coach statistics and earnings
- Manage coach specializations and hourly rates

### 👥 User Management
- Create new user accounts (students, coaches, admins)
- View user activity and spending
- Manage user roles and status

### 🗄️ Storage Management
- Create and manage storage buckets
- Monitor storage usage
- Track bucket purposes and allocations

### 📊 Monitoring & Analytics
- Real-time dashboard with key metrics
- Daily activity reports
- Comprehensive logging system
- Transaction tracking

### 📝 Logging System
- Daily log files with timestamps
- Action tracking for all administrative operations
- Configurable log retention

## Installation

1. Clone the repository:
```bash
git clone https://github.com/naperpickleball/pickleballaiengine.git
cd PickleballAIEngine
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:

### Command Line Interface
```bash
python root_console.py
```

### Web Interface
```bash
python web_root_console.py
```

Then open your browser to `http://localhost:5000`

## Usage

### Web Interface Login
- **Username:** admin
- **Password:** admin123

### Key Features

#### Dashboard
- Overview of active coaches, users, and storage
- Today's revenue and session statistics
- Recent activity feed

#### Coach Management
- Add new coaches with specialization and hourly rates
- Block/unblock coach access
- View coach performance metrics

#### User Management
- Create users with different roles (student, coach, admin)
- Monitor user activity and spending
- Manage user status

#### Storage Management
- Create storage buckets for different purposes
- Monitor storage usage and capacity
- Track bucket status and performance

#### Logs & Reports
- View daily activity logs
- Generate custom date reports
- Monitor system activity and transactions

## File Structure

```
PickleballAIEngine/
├── root_console.py          # CLI version
├── web_root_console.py      # Web version
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── data/                   # Data storage
│   ├── coaches.json
│   ├── users.json
│   ├── storage.json
│   └── transactions.json
├── logs/                   # Log files
│   └── root_actions_YYYY-MM-DD.log
├── templates/              # HTML templates
│   ├── login.html
│   └── dashboard.html
└── static/                 # Static assets
    └── js/
        └── dashboard.js
```

## API Endpoints

### Authentication
- `POST /login` - User login
- `GET /logout` - User logout

### Coaches
- `GET /api/coaches` - List all coaches
- `POST /api/coaches` - Create new coach
- `POST /api/coaches/block` - Block coach
- `POST /api/coaches/unblock` - Unblock coach

### Users
- `GET /api/users` - List all users
- `POST /api/users` - Create new user

### Storage
- `GET /api/storage` - List all buckets
- `POST /api/storage` - Create new bucket

### Monitoring
- `GET /api/logs` - Get system logs
- `GET /api/report` - Get daily report

## Security Features

- Session-based authentication
- Input validation and sanitization
- Secure password handling
- Action logging for audit trails
- Role-based access control

## Development

### Adding New Features
1. Update the `WebRootConsole` class in `web_root_console.py`
2. Add corresponding API endpoints
3. Update the frontend JavaScript in `static/js/dashboard.js`
4. Add UI elements in `templates/dashboard.html`

### Data Storage
All data is stored in JSON files in the `data/` directory:
- `coaches.json` - Coach information and statistics
- `users.json` - User accounts and activity
- `storage.json` - Storage bucket configurations
- `transactions.json` - Financial transactions

### Logging
All administrative actions are logged to daily files in the `logs/` directory with timestamps and detailed information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the PickleballAI platform and is proprietary software.

## Support

For support and questions, please contact the development team or create an issue in the repository. 