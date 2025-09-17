# CyberSmart

CyberSmart is an interactive cybersecurity education platform that uses machine learning algorithms to provide personalized learning experiences in password security and phishing awareness. The platform employs neural networks and advanced scoring algorithms to evaluate user performance and provide tailored recommendations.

## Tech Stack

### Frontend:
- Streamlit - Interactive web application framework
- Matplotlib - Data visualization for performance metrics
- Custom CSS - Enhanced UI styling

### Backend:
- Python 3.x - Core programming language
- scikit-learn - Machine learning implementations
- NumPy - Numerical computations and array operations
- Pandas - Data manipulation and analysis

### Machine Learning Components:
- Neural Networks (MLPClassifier)
- Feature Engineering
- Pattern Recognition
- Entropy Calculation
- Sigmoid Transformation

### Storage:
- File-based logging
- GitHub integration for data persistence

## ML Algorithms and Scoring System

### 1. Neural Network Architecture
The platform uses a Multi-Layer Perceptron (MLP) with the following structure:
- Input Layer: 5 neurons (entropy, length, character diversity, pattern strength, common patterns)
- Hidden Layers: (64, 32, 16) neurons with ReLU activation
- Output Layer: 1 neuron (final score)
- Optimizer: Adam
- Loss Function: Mean Squared Error

```python
MLPClassifier(
    hidden_layer_sizes=(64, 32, 16),
    activation='relu',
    solver='adam',
    max_iter=1000
)
```

### 2. Password Strength Evaluation
Features analyzed:
- Character diversity (lowercase, uppercase, numbers, symbols)
- Pattern detection using regex
- Entropy calculation
- Length analysis
- Common password pattern detection

Mathematical formulation:
```
Entropy = L * log2(R)
where:
L = password length
R = character set size (26 lowercase + 26 uppercase + 10 digits + 32 special chars)
```

### 3. Phishing Detection Scoring
Uses a sigmoid transformation for nuanced scoring:
```
score = 200 / (1 + e^(-0.05 * (base_score - 100)))
```

### 4. Password Matching Score
Employs exponential weighting:
```
score = 200 * (1 - e^(-0.02 * base_score))
```

## Features

1. Interactive Cybersecurity Games:
   - Phishing Email Detection
   - Password Strength Analysis
   - Password Pattern Matching
   - Secure Password Generation

2. ML-Powered Scoring System:
   - Neural network evaluation
   - Pattern recognition
   - Entropy-based analysis
   - Comprehensive scoring metrics

3. Personalized Recommendations:
   - Adaptive feedback
   - Tailored security suggestions
   - Progress tracking

## Running Locally

1. Clone the repository:
```bash
git clone https://github.com/poncema4/CyberSmart.git
cd CyberSmart
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export GITHUB_TOKEN=your_github_token
```

4. Run the application:
```bash
streamlit run app.py
```

## Architecture Highlights

### ML Pipeline
1. Data Collection:
   - User interactions
   - Password patterns
   - Performance metrics

2. Feature Engineering:
   - Character set analysis
   - Pattern detection
   - Entropy calculation
   - Length normalization

3. Scoring System:
   - Neural network evaluation
   - Sigmoid transformation
   - Exponential weighting
   - Normalized scoring (0-200 scale)

### Performance Metrics
- Password Strength Score (0-200)
- Phishing Detection Accuracy (0-200)
- Pattern Recognition Score (0-200)
- Overall Security Rating

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss proposed changes.

## Contact
For questions or support, please create an issue in the repository.