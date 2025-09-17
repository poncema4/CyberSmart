import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import math
import re

class CyberSecurityScorer:
    def __init__(self):
        self.scaler = StandardScaler()
        # Neural network for comprehensive scoring
        self.mlp = MLPRegressor(
            hidden_layer_sizes=(64, 32, 16),
            activation='relu',
            solver='adam',
            max_iter=1000,
            random_state=42
        )
        self._initialize_models()

    def _initialize_models(self):
        # Initialize with some expert-defined baseline data
        # Format: [entropy, length, char_diversity, pattern_strength, common_patterns]
        X_train = np.array([
            [20, 6, 1, 0.2, 0.9],   # Weak password example
            [40, 8, 2, 0.4, 0.7],   # Moderate password example
            [60, 10, 3, 0.6, 0.5],  # Good password example
            [80, 12, 4, 0.8, 0.3],  # Strong password example
            [100, 16, 4, 1.0, 0.1]  # Very strong password example
        ])
        
        # Corresponding strength scores (0-1)
        y_train = np.array([0.2, 0.4, 0.6, 0.8, 1.0])
        
        # Fit the scaler and transform training data
        X_scaled = self.scaler.fit_transform(X_train)
        
        # Train the neural network
        self.mlp.fit(X_scaled, y_train)

    def _calculate_char_diversity(self, password):
        """Calculate character diversity score"""
        char_types = sum([
            bool(re.search(r'[a-z]', password)),
            bool(re.search(r'[A-Z]', password)),
            bool(re.search(r'[0-9]', password)),
            bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        ])
        return char_types

    def _calculate_pattern_strength(self, password):
        """Calculate pattern-based strength score"""
        patterns = {
            r'123|234|345|456|567|678|789': 0.2,  # Sequential numbers
            r'abc|bcd|cde|def|efg': 0.2,          # Sequential letters
            r'password|admin|user': 0.1,          # Common words
            r'([a-zA-Z0-9])\1\1+': 0.3           # Repeated characters
        }
        
        strength = 1.0
        for pattern, penalty in patterns.items():
            if re.search(pattern, password.lower()):
                strength -= penalty
        return max(0.1, strength)

    def _check_common_patterns(self, password):
        """Check for common password patterns"""
        common_patterns = [
            r'\d{4}$',          # Ending with 4 digits (like year)
            r'^[A-Z][a-z]+\d+$' # Capitalized word followed by numbers
        ]
        
        pattern_matches = sum(bool(re.search(p, password)) for p in common_patterns)
        return 1.0 - (pattern_matches * 0.2)

    def calculate_password_score(self, password):
        """Calculate comprehensive password score using neural network"""
        if not password:
            return 0.0

        # Calculate feature vector
        entropy = self._calculate_entropy(password)
        length = len(password)
        char_diversity = self._calculate_char_diversity(password)
        pattern_strength = self._calculate_pattern_strength(password)
        common_patterns = self._check_common_patterns(password)

        # Prepare features for neural network
        features = np.array([[
            entropy,
            length,
            char_diversity,
            pattern_strength,
            common_patterns
        ]])

        # Scale features
        features_scaled = self.scaler.transform(features)

        # Get neural network prediction
        score = self.mlp.predict(features_scaled)[0]

        return score * 200  # Scale to 0-200 range

    def _calculate_entropy(self, password):
        """Calculate password entropy"""
        char_set_size = 0
        if re.search(r'[a-z]', password): char_set_size += 26
        if re.search(r'[A-Z]', password): char_set_size += 26
        if re.search(r'[0-9]', password): char_set_size += 10
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): char_set_size += 32
        
        if char_set_size == 0:
            return 0
            
        entropy = len(password) * math.log2(char_set_size)
        return min(100, entropy)  # Cap at 100 for normalization

# Global scorer instance
scorer = CyberSecurityScorer()

def get_password_score(password):
    """Get a comprehensive password score"""
    return scorer.calculate_password_score(password)

def get_phishing_score(correct_answers, total_questions):
    """Calculate phishing awareness score using weighted scoring"""
    base_score = (correct_answers / total_questions) * 200
    
    # Apply sigmoid transformation for more nuanced scoring
    sigmoid = lambda x: 200 / (1 + np.exp(-0.05 * (x - 100)))
    return round(sigmoid(base_score), 2)

def get_match_score(correct_matches, total_matches):
    """Calculate password matching score using weighted scoring"""
    base_score = (correct_matches / total_matches) * 200
    
    # Apply exponential weighting for more critical evaluation
    weighted_score = 200 * (1 - np.exp(-0.02 * base_score))
    return round(weighted_score, 2)
