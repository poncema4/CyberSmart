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
        Save user scores to database and mark session as completed and stored
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
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
    
    def reset_database(self):
        """
        Reset the database by dropping and recreating all tables for testing purposes
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('DROP TABLE IF EXISTS user_sessions')
            cursor.execute('DROP TABLE IF EXISTS user_scores')
            cursor.execute('DROP TABLE IF EXISTS users')
            
            conn.commit()
        
        self.init_database()
        print("Database reset successfully!")

db = DatabaseManager()