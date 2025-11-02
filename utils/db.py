import sqlite3
import hashlib
from datetime import datetime
from typing import Optional, Dict, List, Tuple
import os

class DatabaseManager:
    def __init__(self, db_path: str = "data/cybersmart.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """
        Initialize the database with the required tables
        """
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_scores (
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
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_id TEXT UNIQUE NOT NULL,
                    exam_type TEXT NOT NULL,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_id TEXT NOT NULL,
                    exam_type TEXT NOT NULL,
                    game_type TEXT NOT NULL,  -- 'phishing' or 'password_match'
                    question_id TEXT NOT NULL,
                    is_correct BOOLEAN NOT NULL,
                    response_time REAL NOT NULL,  -- time in seconds
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_badges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    badge_id TEXT NOT NULL,
                    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, badge_id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
    
    def hash_password(self, password: str) -> str:
        """
        Hash password using SHA-256 with salt
        """
        salt = os.urandom(32)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt.hex() + password_hash.hex()
    
    def verify_password(self, password: str, stored_hash: str) -> bool:
        """
        Verify password with the stored hash
        """
        if len(stored_hash) < 64:
            return False
        
        salt = bytes.fromhex(stored_hash[:64])
        stored_password_hash = stored_hash[64:]
        
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return password_hash.hex() == stored_password_hash
    
    def register_user(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Register a new user and check if they can register upon all 
        valid edge cases that are checked
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
                if cursor.fetchone():
                    return False, "Username already exists, choose another one"
                
                password_hash = self.hash_password(password)
                cursor.execute('''
                    INSERT INTO users (username, password_hash)
                    VALUES (?, ?)
                ''', (username, password_hash))
                
                conn.commit()
                return True, "User registered successfully"
        
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    
    def login_user(self, username: str, password: str) -> Tuple[bool, Optional[Dict], str]:
        """
        Login user and return user info upon all valid edge cases
        that are checked passed
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT id, username, password_hash
                    FROM users WHERE username = ?
                ''', (username,))
                
                user = cursor.fetchone()
                if not user:
                    return False, None, "Username does not exist"
                
                user_id, username, password_hash = user
                
                if not self.verify_password(password, password_hash):
                    return False, None, "Incorrect password"
                
                cursor.execute('''
                    UPDATE users SET last_login = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (user_id,))
                
                conn.commit()
                
                user_info = {
                    'id': user_id,
                    'username': username
                }
                
                return True, user_info, "User logged in successfully"
        
        except sqlite3.Error as e:
            return False, None, f"Database error: {str(e)}"
    
    def create_session(self, user_id: int, exam_type: str) -> str:
        """
        Create a new user session
        """
        session_id = hashlib.md5(f"{user_id}_{datetime.now()}_{exam_type}".encode()).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_sessions (user_id, session_id, exam_type)
                VALUES (?, ?, ?)
            ''', (user_id, session_id, exam_type))
            conn.commit()
        
        return session_id
    
    def save_user_scores(self, user_id: int, session_id: str, exam_type: str, 
                        phishing_score: float, password_match_score: float, 
                        password_strength_entropy: float, overall_score: float):
        """
        Save user scores to database and CSV file, keeping both synchronized
        """
        import csv
        from datetime import datetime
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
            username_row = cursor.fetchone()
            username = username_row[0] if username_row else f"user_{user_id}"
            
            cursor.execute('''
                INSERT INTO user_scores 
                (user_id, session_id, exam_type, phishing_score, password_match_score, 
                 password_strength_entropy, overall_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, session_id, exam_type, phishing_score, 
                  password_match_score, password_strength_entropy, overall_score))
            
            cursor.execute('''
                UPDATE user_sessions 
                SET completed_at = CURRENT_TIMESTAMP, is_active = 0
                WHERE session_id = ?
            ''', (session_id,))
            
            conn.commit()
        
        csv_file = "reports/user_scores.csv"
        file_exists = os.path.isfile(csv_file)
        
        with open(csv_file, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            
            if not file_exists:
                writer.writerow([
                    "Timestamp", "Username", "User ID", "Session ID", "Exam Type",
                    "Phishing Score", "Password Match Score", "Password Strength Entropy", "Overall Score"
                ])
            
            timestamp = datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([
                timestamp, username, user_id, session_id, exam_type,
                phishing_score, password_match_score, password_strength_entropy, overall_score
            ])
    
    def get_user_scores(self, user_id: int) -> List[Dict]:
        """
        Get all scores for a user that is stored in the database
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DISTINCT session_id, exam_type, phishing_score, password_match_score,
                       password_strength_entropy, overall_score, completed_at
                FROM user_scores 
                WHERE user_id = ?
                ORDER BY completed_at DESC
            ''', (user_id,))
            
            rows = cursor.fetchall()
            scores = []
            for row in rows:
                scores.append({
                    'session_id': row[0],
                    'exam_type': row[1],
                    'phishing_score': row[2],
                    'password_match_score': row[3],
                    'password_strength_entropy': row[4],
                    'overall_score': row[5],
                    'completed_at': row[6]
                })
            return scores
    
    def get_user_improvement(self, user_id: int) -> Dict:
        """
        Calculate user improvement from pre to post exam
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT phishing_score, password_match_score, password_strength_entropy, overall_score
                FROM user_scores 
                WHERE user_id = ? AND exam_type = 'pre'
                ORDER BY completed_at DESC LIMIT 1
            ''', (user_id,))
            pre_result = cursor.fetchone()
            
            cursor.execute('''
                SELECT phishing_score, password_match_score, password_strength_entropy, overall_score
                FROM user_scores 
                WHERE user_id = ? AND exam_type = 'post'
                ORDER BY completed_at DESC LIMIT 1
            ''', (user_id,))
            post_result = cursor.fetchone()
            
            if not pre_result or not post_result:
                return {
                    'has_both': False,
                    'message': 'Complete both pre and post assessments to see improvement'
                }
            
            pre_scores = {'phishing': pre_result[0], 'password_match': pre_result[1], 
                         'password_strength': pre_result[2], 'overall': pre_result[3]}
            post_scores = {'phishing': post_result[0], 'password_match': post_result[1], 
                          'password_strength': post_result[2], 'overall': post_result[3]}
            
            improvements = {
                'phishing': post_scores['phishing'] - pre_scores['phishing'],
                'password_match': post_scores['password_match'] - pre_scores['password_match'],
                'password_strength': post_scores['password_strength'] - pre_scores['password_strength'],
                'overall': post_scores['overall'] - pre_scores['overall']
            }
            
            return {
                'has_both': True,
                'pre_scores': pre_scores,
                'post_scores': post_scores,
                'improvements': improvements
            }
    
    def get_global_averages(self) -> Dict:
        """
        Get global average scores for pre and post exams
        which is unique for each user to avoid skewed results
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT AVG(phishing_score), AVG(password_match_score), 
                       AVG(password_strength_entropy), AVG(overall_score), COUNT(DISTINCT user_id)
                FROM user_scores WHERE exam_type = 'pre'
            ''')
            pre_result = cursor.fetchone()
            
            cursor.execute('''
                SELECT AVG(phishing_score), AVG(password_match_score), 
                       AVG(password_strength_entropy), AVG(overall_score), COUNT(DISTINCT user_id)
                FROM user_scores WHERE exam_type = 'post'
            ''')
            post_result = cursor.fetchone()
            
            global_improvement = None
            if pre_result[0] and post_result[0]:
                global_improvement = {
                    'phishing': (post_result[0] or 0) - (pre_result[0] or 0),
                    'password_match': (post_result[1] or 0) - (pre_result[1] or 0),
                    'password_strength': (post_result[2] or 0) - (pre_result[2] or 0),
                    'overall': (post_result[3] or 0) - (pre_result[3] or 0)
                }
            
            return {
                'pre_averages': {
                    'phishing': round(pre_result[0], 1) if pre_result[0] else 0,
                    'password_match': round(pre_result[1], 1) if pre_result[1] else 0,
                    'password_strength': round(pre_result[2], 1) if pre_result[2] else 0,
                    'overall': round(pre_result[3], 1) if pre_result[3] else 0,
                    'count': pre_result[4]
                },
                'post_averages': {
                    'phishing': round(post_result[0], 1) if post_result[0] else 0,
                    'password_match': round(post_result[1], 1) if post_result[1] else 0,
                    'password_strength': round(post_result[2], 1) if post_result[2] else 0,
                    'overall': round(post_result[3], 1) if post_result[3] else 0,
                    'count': post_result[4]
                },
                'global_improvement': global_improvement
            }
    
    def save_performance_metric(self, user_id: int, session_id: str, exam_type: str,
                                game_type: str, question_id: str, is_correct: bool, 
                                response_time: float):
        """Save individual question performance metrics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO performance_analytics 
                (user_id, session_id, exam_type, game_type, question_id, is_correct, response_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, session_id, exam_type, game_type, question_id, is_correct, response_time))
            conn.commit()
    
    def get_user_weak_areas(self, user_id: int) -> Dict:
        """
        Analyze user's performance to identify weak areas and slow response times
        Returns categories where user struggles and takes longer to answer
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT 
                    AVG(CASE WHEN is_correct THEN 1.0 ELSE 0.0 END) as accuracy,
                    AVG(response_time) as avg_time,
                    COUNT(*) as total_attempts
                FROM performance_analytics
                WHERE user_id = ? AND game_type = 'phishing' AND exam_type = 'pre'
            ''', (user_id,))
            phishing_stats = cursor.fetchone()

            cursor.execute('''
                SELECT 
                    AVG(CASE WHEN is_correct THEN 1.0 ELSE 0.0 END) as accuracy,
                    AVG(response_time) as avg_time,
                    COUNT(*) as total_attempts
                FROM performance_analytics
                WHERE user_id = ? AND game_type = 'password_match' AND exam_type = 'pre'
            ''', (user_id,))
            password_stats = cursor.fetchone()

            cursor.execute('''
                SELECT AVG(response_time) as overall_avg_time
                FROM performance_analytics
                WHERE user_id = ? AND exam_type = 'pre'
            ''', (user_id,))
            overall_avg = cursor.fetchone()
            
            result = {
                'phishing': {
                    'accuracy': phishing_stats[0] if phishing_stats[0] else 0,
                    'avg_time': phishing_stats[1] if phishing_stats[1] else 0,
                    'total_attempts': phishing_stats[2] if phishing_stats[2] else 0,
                    'is_weak': (phishing_stats[0] or 0) < 0.6,
                    'is_slow': (phishing_stats[1] or 0) > (overall_avg[0] or 0) * 1.2 if overall_avg[0] else False
                },
                'password_match': {
                    'accuracy': password_stats[0] if password_stats[0] else 0,
                    'avg_time': password_stats[1] if password_stats[1] else 0,
                    'total_attempts': password_stats[2] if password_stats[2] else 0,
                    'is_weak': (password_stats[0] or 0) < 0.6,
                    'is_slow': (password_stats[1] or 0) > (overall_avg[0] or 0) * 1.2 if overall_avg[0] else False
                },
                'overall_avg_time': overall_avg[0] if overall_avg[0] else 0
            }
            
            return result
    
    def reset_database(self):
        """
        Reset the database by dropping and recreating all tables for testing purposes
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('DROP TABLE IF EXISTS user_badges')
            cursor.execute('DROP TABLE IF EXISTS performance_analytics')
            cursor.execute('DROP TABLE IF EXISTS user_sessions')
            cursor.execute('DROP TABLE IF EXISTS user_scores')
            cursor.execute('DROP TABLE IF EXISTS users')
            
            conn.commit()
        
        self.init_database()
        print("Database reset successfully!")
    
    def award_badge(self, user_id: int, badge_id: str) -> bool:
        """
        Award a badge to a user if they don't already have it
        Returns True if badge was newly awarded, False if already owned
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute('''
                    SELECT id FROM user_badges 
                    WHERE user_id = ? AND badge_id = ?
                ''', (user_id, badge_id))
                
                if cursor.fetchone():
                    return False

                cursor.execute('''
                    INSERT INTO user_badges (user_id, badge_id)
                    VALUES (?, ?)
                ''', (user_id, badge_id))
                
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            print(f"Error awarding badge: {e}")
            return False
    
    def get_user_badges(self, user_id: int) -> List[str]:
        """
        Get list of badge IDs that a user has earned
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT badge_id, earned_at 
                FROM user_badges 
                WHERE user_id = ?
                ORDER BY earned_at DESC
            ''', (user_id,))
            
            return [row[0] for row in cursor.fetchall()]
    
    def check_and_award_badges(self, user_id: int) -> List[str]:
        """
        Check user's performance and award appropriate badges
        Returns list of newly awarded badge IDs
        """
        newly_awarded = []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT phishing_score, exam_type 
                FROM user_scores 
                WHERE user_id = ?
                ORDER BY completed_at DESC
            ''', (user_id,))
            phishing_scores = cursor.fetchall()

            cursor.execute('''
                SELECT password_match_score, exam_type 
                FROM user_scores 
                WHERE user_id = ?
                ORDER BY completed_at DESC
            ''', (user_id,))
            password_scores = cursor.fetchall()

            cursor.execute('''
                SELECT overall_score, exam_type 
                FROM user_scores 
                WHERE user_id = ?
                ORDER BY completed_at DESC
            ''', (user_id,))
            overall_scores = cursor.fetchall()
        
        # Badge 1: Phish Hunter - Score 80%+ on phishing (160+ on 0-200 scale)
        if phishing_scores and any(score[0] >= 160 for score in phishing_scores):
            if self.award_badge(user_id, 'phish_hunter'):
                newly_awarded.append('phish_hunter')
        
        # Badge 2: Password Pro - Score 80%+ on password match (160+ on 0-200 scale)
        if password_scores and any(score[0] >= 160 for score in password_scores):
            if self.award_badge(user_id, 'password_pro'):
                newly_awarded.append('password_pro')
        
        # Badge 3: Cyber Defender - Score 80%+ overall (160+ on 0-200 scale)
        if overall_scores and any(score[0] >= 160 for score in overall_scores):
            if self.award_badge(user_id, 'cyber_defender'):
                newly_awarded.append('cyber_defender')
        
        # Badge 4: Quick Learner - Improve score by 20+ points between attempts
        if len(overall_scores) >= 2:
            for i in range(len(overall_scores) - 1):
                if overall_scores[i][0] - overall_scores[i + 1][0] >= 20:
                    if self.award_badge(user_id, 'quick_learner'):
                        newly_awarded.append('quick_learner')
                    break
        
        # Badge 5: Perfect Score - Get 100% (200/200) on any assessment
        if overall_scores and any(score[0] >= 200 for score in overall_scores):
            if self.award_badge(user_id, 'perfect_score'):
                newly_awarded.append('perfect_score')
        
        # Badge 6: Dedicated Student - Complete all three exam types (pre, practice, post)
        exam_types = set(score[1] for score in overall_scores)
        if len(exam_types) >= 3:
            if self.award_badge(user_id, 'dedicated_student'):
                newly_awarded.append('dedicated_student')
        
        return newly_awarded

db = DatabaseManager()