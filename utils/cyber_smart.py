import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import math
import re

class CyberSmart:
    def __init__(self) -> None:
        """
        Initialize the CyberSmart password scoring system
        """
        self.scaler = StandardScaler()
        self.mlp = MLPRegressor(
            hidden_layer_sizes=(64, 32, 16),
            activation='relu',
            solver='adam',
            max_iter=1000,
            random_state=42
        )
        self._initialize_models()

    def _initialize_models(self) -> None:
        """
        Initialize and train the neural network with the baseline data

        Format:
        [entropy, length, char_diversity, pattern_strength, common_patterns]

        Structure:
        Row 1: Very Weak password example
        Row 2: Weak password example
        Row 3: Moderate password example
        Row 4: Strong password example
        Row 5: Very strong password example
        """
        base_x = np.array([
            [20, 6, 1, 0.2, 0.9],
            [40, 8, 2, 0.4, 0.7],
            [60, 10, 3, 0.6, 0.5],
            [80, 12, 4, 0.8, 0.3],
            [100, 16, 4, 1.0, 0.1]
        ])
        
        """
        Corresponding scores for the baseline passwords

        Range:
        0.2 - Very Weak
        0.4 - Weak
        0.6 - Moderate
        0.8 - Strong
        1.0 - Very Strong
        """
        base_y = np.array([0.2, 0.4, 0.6, 0.8, 1.0])
        
        base_x_scale = self.scaler.fit_transform(base_x)
        
        self.mlp.fit(base_x_scale, base_y)

    def calculate_char_diversity(self, password: str) -> int:
        """
        Calculate the character diversity score

        Scale:
        1 - Only one type of character (e.g, all lowercase)
        2 - Two types of characters (e.g., lowercase and numbers)
        3 - Three types of characters (e.g., lowercase, uppercase, numbers)
        4 - All four types of characters (lowercase, uppercase, numbers, special characters)
        """
        char_types = sum([
            bool(re.search(r'[a-z]', password)),
            bool(re.search(r'[A-Z]', password)),
            bool(re.search(r'[0-9]', password)),
            bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        ])
        return char_types

    def calculate_pattern_strength(self, password: str) -> float:
        """
        Calculate pattern-based strength score
        
        Initialize the strength to 1.0 and deduct points for each detected weak pattern

        Scale:
        1.0: No weak patterns detected
        0.7 - 0.9: Minor issues detected
        0.4 - 0.6: Multiple weaknessess detected
        0.1: Very weak, repeated characters or several common patterns detected
        """
        patterns = {
            r'123|234|345|456|567|678|789': 0.2,
            r'abc|bcd|cde|def|efg': 0.2,
            r'password|admin|user': 0.1,
            r'([a-zA-Z0-9])\1\1+': 0.3
        }
        
        strength = 1.0

        for pattern, penalty in patterns.items():
            if re.search(pattern, password.lower()):
                strength -= penalty

        return max(0.1, strength)

    def check_common_patterns(self, password: str) -> float:
        """
        Check for common password patterns
        
        Initialize the strength to 1.0 and deduct points for each detected weak pattern

        Scale:
        1.0 - No weak patterns detected
        0.8 - Minor issues detected
        0.6 - Very weak, repeated characters or several common patterns detected
        """
        common_patterns = [
            r'\d{4}$',
            r'^[A-Z][a-z]+\d+$'
        ]
        
        pattern_matches = sum(bool(re.search(p, password)) for p in common_patterns)
        return 1.0 - (pattern_matches * 0.2)
    
    def calculate_entropy(self, password: str) -> float:
        """
        Calculate password entropy
        
        Entropy scale depends on:
        - Password length
        - Character set diversity (lowercase, uppercase, numbers, special characters)

        Formula: 
        Entropy = Length * log2(char_set_size)

        The entropy is capped at 100 for normalization
        """
        char_set_size = 0
        if re.search(r'[a-z]', password): char_set_size += 26
        if re.search(r'[A-Z]', password): char_set_size += 26
        if re.search(r'[0-9]', password): char_set_size += 10
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): char_set_size += 32
        
        if char_set_size == 0:
            return 0
            
        entropy = len(password) * math.log2(char_set_size)

        return min(100, entropy)

    def calculate_password_score(self, password: str) -> float:
        """
        Calculate comprehensive password score through neural network

        Features:
        - Entropy: Unpredictability of characters
        - Lenght: Number of characters
        - Character diversity: Presence of lowercase, uppercase, numbers, and special characters
        - Pattern strength: Penalizes sequences, repeated characters, and common words
        - Common patterns: Penalizes predictable patterns like years or capitalized words followed by numbers

        Scale:
        160 - 200: Very strong
        120 - 159: Strong
        80 - 119: Moderate
        40 - 79: Weak
        0 - 39: Very weak
        """
        if not password:
            return 0.0

        entropy = self.calculate_entropy(password)
        length = len(password)
        char_diversity = self.calculate_char_diversity(password)
        pattern_strength = self.calculate_pattern_strength(password)
        common_patterns = self.check_common_patterns(password)

        features = np.array([[
            entropy,
            length,
            char_diversity,
            pattern_strength,
            common_patterns
        ]])

        features_scaled = self.scaler.transform(features)

        score = self.mlp.predict(features_scaled)[0]

        return score * 200

score = CyberSmart()

def get_password_score(password: str) -> float:
    """
    Get a comprehensive password score based on the various metrics
    """
    return score.calculate_password_score(password)

def get_phishing_score(correct_answers: int, total_questions: int) -> float:
    """
    Calculate phishing awareness score using weighted scoring

    Scale:
    0 - 39: Very Low
    40 - 79: Low
    80 - 119: Moderate
    120 - 159: High
    160 - 200: Very High

    Algorithm: Sigmoid Transformation for balanced scoring
    1. Compute base score (correct_answers / total_questions) * 200
    2. Apply sigmoid transformation to smooth scoring curve

    Logic: 
    - Linear base score (percentage scaled to 200)
    - Sigmoid transformation to avoid extreme scores for small changes in answers
        ~ Maps any score into a smooth 0 - 200 range
        ~ Flattens at extremes: Avoids someone scoring 0 or 200 too easily
        ~ Emphasizes differences in the middle range (80 - 120)
    
    Formula:
    - 200 --> max score scaling
    - k = 0.05 --> controls the steepness
    - midpoint = 100 --> neutral point
    """
    base_score = (correct_answers / total_questions) * 200
    
    sigmoid = lambda x: 200 / (1 + np.exp(-0.05 * (x - 100)))
    return round(sigmoid(base_score), 2)

def get_match_score(correct_matches: int, total_matches: int) -> float:
    """
    Calculate password matching score using weighted scoring
    
    Scale:
    0 - 39: Very Low
    40 - 79: Low
    80 - 119: Moderate
    120 - 159: High
    160 - 200: Very High

    Algorithm: Exponentially weighted scoring for accuracy
    1. At low accuracy, the exponential curve grows slowly, so small correct matches barely increase the score
    2. At high accuracy, the exponential curve grows rapidly, so near-perfect performance quickly approaches 200

    Logic:
    - Linear base score (percentage scaled to 200)
    - Makes the scoring curve non-linear
    - Strongly penalizes low accuracy (0 - 50% match)
    - Strongly rewards high accuracy (90 - 100% match)
    - Ensures small mistakes matte more when accuracy is low, but improvement near perfection is rewarded more sharply

    Formula:
    - weight_score = 200 * (1 - exp(-k * base_score))
    - 200 --> max score scaling
    - k = 0.02 --> rate of exponential growth
    """
    base_score = (correct_matches / total_matches) * 200
    
    weighted_score = 200 * (1 - np.exp(-0.02 * base_score))
    return round(weighted_score, 2)