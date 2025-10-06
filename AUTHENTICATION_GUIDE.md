<h1 align="center">
  CyberSmart Authentication & Score Tracking System 🔐
</h1>

<p align="center">
  <strong>Comprehensive User Management and Progress Analytics</strong>
</p>

<p align="left">
  This guide details the <strong>authentication system</strong> and <strong>score tracking infrastructure</strong> implemented in CyberSmart. The platform features secure user management, persistent session handling, and comprehensive analytics for tracking cybersecurity learning progress.
</p>

<div align="center">
  
  <a href="#overview">🔍 Overview</a> • <a href="#authentication-system">🔐 Authentication</a> • <a href="#database-schema">🗃️ Database</a>
  <br>
  <a href="#score-tracking">📊 Score Tracking</a> • <a href="#user-interface">🎨 User Interface</a> • <a href="#security-features">🛡️ Security</a>
  <br>

</div>

## Overview

### 🎯 **System Capabilities**
- **Secure Authentication:** PBKDF2 password hashing with salt protection
- **Session Management:** Persistent login sessions across assessments
- **Score Analytics:** Individual and community progress tracking
- **Assessment Types:** Pre-assessment, Post-assessment, and Practice modes
- **Progress Visualization:** Beautiful UI with gradient cards and metrics

### 🏗️ **Architecture Components**
- **SQLite Database:** Local data storage with relational structure
- **Authentication Layer:** Secure login/register with session persistence
- **Score Engine:** Multi-dimensional assessment scoring system
- **Analytics Dashboard:** Real-time progress visualization

## Authentication System

### 🔐 **User Authentication Flow**

```
Welcome Screen → Login/Register → Exam Selection → Assessment → Results & History
```

#### **Authentication Features:**
- **Secure Registration:** Username/password with confirmation validation
- **Login Persistence:** Sessions maintained across browser refreshes
- **Password Security:** PBKDF2 hashing with 100,000 iterations and random salt
- **Session Management:** Unique session IDs for each assessment attempt

#### **Authentication Pages:**
1. **Welcome Screen:** Beautiful gradient UI with login/register options
2. **Login Form:** Existing user authentication
3. **Registration Form:** New user account creation with password confirmation
4. **Dashboard:** User-specific score history and logout functionality

### 🎨 **User Interface Components**

```css
/* Beautiful gradient styling for authentication */
.auth-title {
    color: #1a1a1a;
    font-size: 3rem;
    font-weight: 800;
}

.exam-type-container {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    border-radius: 12px;
    color: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
```

## Database Schema

### 🗃️ **SQLite Database Structure**

#### **Users Table**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

#### **User Scores Table**
```sql
CREATE TABLE user_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_id TEXT NOT NULL,
    exam_type TEXT NOT NULL,  -- 'pre', 'post', 'practice'
    phishing_score REAL,
    password_match_score REAL,
    password_strength_entropy REAL,
    overall_score REAL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

#### **User Sessions Table**
```sql
CREATE TABLE user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_id TEXT UNIQUE NOT NULL,
    exam_type TEXT NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### 📊 **Data Relationships**
- **One-to-Many:** Users → User Scores (one user, multiple assessments)
- **One-to-Many:** Users → User Sessions (one user, multiple sessions)
- **Foreign Keys:** Maintain referential integrity across tables

## Score Tracking

### 📈 **Assessment Types**

#### **Pre-Assessment**
- **Purpose:** Baseline cybersecurity knowledge measurement
- **Scoring:** Initial competency across all security domains
- **Analytics:** Establishes learning starting point

#### **Post-Assessment**  
- **Purpose:** Learning effectiveness measurement
- **Scoring:** Final competency after platform interaction
- **Analytics:** Improvement calculation vs pre-assessment

#### **Practice Mode**
- **Purpose:** Continuous learning without formal evaluation
- **Scoring:** Tracked but not included in improvement metrics
- **Analytics:** Progress monitoring and skill reinforcement

### 🎯 **Scoring Dimensions**

#### **Phishing Awareness (0-200 scale)**
```python
# Sigmoid transformation for balanced scoring
def get_phishing_score(correct_answers: int, total_questions: int) -> float:
    base_score = (correct_answers / total_questions) * 200
    sigmoid = lambda x: 200 / (1 + np.exp(-0.05 * (x - 100)))
    return round(sigmoid(base_score), 2)
```

#### **Password Matching (0-200 scale)**
```python
# Exponential weighting for accuracy emphasis
def get_match_score(correct_matches: int, total_matches: int) -> float:
    base_score = (correct_matches / total_matches) * 200
    weighted_score = 200 * (1 - np.exp(-0.02 * base_score))
    return round(weighted_score, 2)
```

#### **Password Strength (Entropy-based)**
- **Calculation:** Mathematical entropy using character set diversity
- **Scale:** Normalized to 0-200 range for consistency
- **Factors:** Length, complexity, pattern analysis

### 📊 **Analytics Dashboard**

#### **Personal Metrics**
- **Individual Progress:** Pre vs post assessment comparison
- **Score History:** Complete assessment timeline
- **Improvement Tracking:** Quantified learning gains
- **Performance Breakdown:** Domain-specific strengths/weaknesses

#### **Global Metrics**
- **Community Averages:** Aggregate performance statistics
- **Improvement Trends:** Platform effectiveness measurement
- **Participant Counts:** Unique user engagement metrics
- **Comparative Analysis:** Individual vs community performance

## User Interface

### 🎨 **Design Philosophy**

#### **Modern Streamlit Styling**
```css
.score-history-container {
    background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    border-radius: 12px;
    padding: 1.5rem;
    color: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.score-card {
    background: rgba(255,255,255,0.1);
    border-radius: 8px;
    padding: 1rem;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
}
```

#### **Responsive Components**
- **Gradient Cards:** Beautiful score display with visual hierarchy
- **Sidebar Integration:** Persistent score history with logout option
- **Conditional Display:** Assessment history only shown when relevant
- **Progress Indicators:** Visual representation of improvement metrics

### 🔄 **User Experience Flow**

1. **Authentication** → Secure login with beautiful gradient UI
2. **Exam Selection** → Choose assessment type with clear descriptions  
3. **Assessment Flow** → Maintained existing 4-step game progression
4. **Results Display** → Comprehensive scoring with historical context
5. **Dashboard Access** → Sidebar navigation with logout functionality

## Security Features

### 🛡️ **Password Security**
- **Hashing Algorithm:** PBKDF2 with SHA-256
- **Salt Generation:** 32-byte random salt per password
- **Iteration Count:** 100,000 iterations for computational resistance
- **Storage Format:** Salt + hash concatenation for verification

### 🔒 **Session Security**
- **Unique Session IDs:** MD5 hash of user ID, timestamp, and exam type
- **Session Persistence:** Maintains login state across page refreshes
- **Automatic Cleanup:** Sessions marked inactive upon completion
- **Secure Storage:** Server-side session management

### 🛡️ **Data Protection**
- **SQL Injection Prevention:** Parameterized queries throughout
- **Input Validation:** Sanitization of all user inputs
- **Error Handling:** Graceful failure with informative messages
- **Data Isolation:** User-specific data access controls

### 🔐 **Authentication Validation**
```python
def verify_password(self, password: str, stored_hash: str) -> bool:
    """Secure password verification with salt extraction"""
    if len(stored_hash) < 64:
        return False
    
    salt = bytes.fromhex(stored_hash[:64])
    stored_password_hash = stored_hash[64:]
    
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return password_hash.hex() == stored_password_hash
```

## Implementation Details

### 🏗️ **Database Operations**

#### **User Registration**
```python
def register_user(self, username: str, password: str) -> Tuple[bool, str]:
    """Secure user registration with duplicate checking"""
    # 1. Check username availability
    # 2. Hash password with salt
    # 3. Insert user record
    # 4. Return success status
```

#### **Score Persistence**
```python
def save_user_scores(self, user_id: int, session_id: str, exam_type: str, 
                    scores...):
    """Save assessment scores and mark session complete"""
    # 1. Insert score record
    # 2. Update session completion
    # 3. Maintain data integrity
```

#### **Analytics Calculation**
```python
def get_global_averages(self) -> Dict:
    """Calculate community statistics with unique user counting"""
    # 1. Aggregate pre-assessment averages
    # 2. Aggregate post-assessment averages  
    # 3. Calculate improvement metrics
    # 4. Count unique participants
```

### 🎯 **Key Benefits**

- **Educational Effectiveness:** Pre/post assessment comparison shows learning impact
- **User Engagement:** Beautiful UI encourages continued platform usage  
- **Data Privacy:** Local SQLite storage keeps user data secure
- **Scalable Analytics:** System supports unlimited users and assessments
- **Security Best Practices:** Industry-standard authentication and data protection

---

<p align="center">
  <strong>🔐 Secure • 📊 Comprehensive • 🎨 Beautiful</strong>
</p>