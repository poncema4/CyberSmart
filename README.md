<h1 align="center">
  CyberSmart 🛡️
</h1>

<p align="center">
  <strong>Interactive AI-Powered Cybersecurity Education Platform</strong>
</p>

<p align="left">
  <strong><a href="https://github.com/poncema4/CyberSmart">CyberSmart</a></strong> is an innovative cybersecurity education platform that uses machine learning algorithms to provide personalized learning experiences in password security and phishing awareness. The platform employs neural networks and advanced scoring algorithms to evaluate user performance and provide tailored security recommendations.
</p>

<div align="center">
  
  <a href="https://github.com/poncema4/CyberSmart">![GitHub Stars](https://img.shields.io/github/stars/poncema4/CyberSmart?style=social)</a>
  <a href="https://github.com/poncema4/CyberSmart">![GitHub Forks](https://img.shields.io/github/forks/poncema4/CyberSmart?style=social)</a>
  <a href="https://github.com/poncema4/CyberSmart/issues">![GitHub Issues](https://img.shields.io/github/issues/poncema4/CyberSmart)</a>
  <a href="https://python.org">![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)</a>

<a href="#quickstart">⚡️ QuickStart</a> • <a href="#features">🎯 Features</a> • <a href="#architecture">🏗️ Architecture</a>
<br>
<a href="#ml-algorithms">🤖 ML Algorithms</a> • <a href="#contributing">👫 Contribute</a> • <a href="#contact">📧 Contact</a>
<br>

</div>

<h3 align="left">
  <strong>Key Features:</strong>
</h3>
<ul align="left">
    <li><strong>🎮 Interactive Learning:</strong> Engaging cybersecurity games including phishing detection, password strength analysis, and security pattern matching.</li>
    <li><strong>🤖 AI-Powered Scoring:</strong> Neural network evaluation with sigmoid transformation and exponential weighting for accurate assessment.</li>
    <li><strong>🔐 User Authentication:</strong> Secure login system with PBKDF2 password hashing and persistent session management.</li>
    <li><strong>📊 Progress Tracking:</strong> Comprehensive score history with pre/post assessment comparisons and improvement analytics.</li>
    <li><strong>🎯 Personalized Recommendations:</strong> Adaptive feedback system that provides tailored security suggestions based on performance.</li>
    <li><strong>📈 Real-time Analytics:</strong> Global statistics and community averages for competitive learning experience.</li>
    <li><strong>🛡️ Security-First Design:</strong> Built with privacy and security best practices, including SQL injection protection and secure data handling.</li>
    <li><strong>🎨 Modern UI/UX:</strong> Beautiful Streamlit interface with custom CSS styling and responsive design.</li>
</ul>

## QuickStart

> [!Note]
> Make sure you have [Python 3.8+](https://www.python.org/downloads/) installed

1. **Clone the repository:**

   ```bash
   git clone https://github.com/poncema4/CyberSmart.git
   cd CyberSmart
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables (optional):**

   ```bash
   # For GitHub integration (optional)
   export GITHUB_TOKEN=your_github_token
   ```

4. **Run the application:**

   ```bash
   streamlit run app.py
   ```

5. **Navigate to http://localhost:8501/**

To stop CyberSmart, press `Ctrl+C` in the terminal where the application is running.

> [!Note]
> The application will automatically create a local SQLite database for user data and scores.

## Features

### 🎯 **Interactive Cybersecurity Games**
- **Phishing Email Detection:** Test your ability to spot malicious emails
- **Password Strength Analysis:** Learn what makes passwords secure  
- **Password Pattern Matching:** Identify weak vs strong password patterns
- **Secure Password Generation:** Create robust passwords with custom criteria

### 🤖 **AI-Powered Assessment System**
- **Neural Network Evaluation:** Advanced ML algorithms for accurate scoring
- **Pattern Recognition:** Intelligent detection of security vulnerabilities
- **Entropy-Based Analysis:** Mathematical assessment of password complexity
- **Comprehensive Scoring:** 0-200 scale metrics across all assessments

### 📊 **User Progress & Analytics**
- **Personal Dashboard:** Track your cybersecurity knowledge improvement
- **Score History:** Complete assessment timeline with detailed breakdowns
- **Global Statistics:** Compare your progress with community averages
- **Pre/Post Assessment:** Measure learning effectiveness over time

## ML Algorithms

### 1. **Neural Network Architecture**
Multi-Layer Perceptron with optimized structure:
```python
MLPClassifier(
    hidden_layer_sizes=(64, 32, 16),
    activation='relu',
    solver='adam',
    max_iter=1000
)
```

### 2. **Password Strength Evaluation**
Mathematical formulation for entropy calculation:
```
Entropy = L * log2(R)
where:
L = password length
R = character set size (94 possible characters)
```

### 3. **Phishing Detection Scoring**
Sigmoid transformation for nuanced assessment:
```
score = 200 / (1 + e^(-0.05 * (base_score - 100)))
```

### 4. **Password Matching Score**
Exponential weighting system:
```
score = 200 * (1 - e^(-0.02 * base_score))
```

## Architecture

### **Tech Stack**
- **Frontend:** Streamlit with custom CSS styling
- **Backend:** Python 3.8+ with scikit-learn ML pipeline
- **Database:** SQLite for user management and score tracking
- **Security:** PBKDF2 password hashing with salt
- **Analytics:** NumPy and Pandas for data processing

### **Project Structure**
```
CyberSmart/
├── app.py                 # Main application entry point
├── utils/                 # Core utilities and modules
│   ├── auth.py           # Authentication system
│   ├── db.py             # Database management
│   ├── cyber_smart.py    # ML algorithms and scoring
│   └── step_flow.py      # Application flow control
├── games/                # Interactive learning modules
│   ├── spot_the_phish/   # Phishing detection game
│   ├── password_match/   # Password pattern matching
│   ├── password_generator/ # Secure password creation
│   └── password_strength/ # Password analysis tool
└── requirements.txt      # Python dependencies
```

### **Security Features**
- **Password Hashing:** PBKDF2 with 100,000 iterations
- **SQL Injection Protection:** Parameterized queries
- **Session Security:** Unique session IDs and persistent authentication
- **Data Validation:** Input sanitization and type checking

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

For major changes, please open an issue first to discuss your proposed changes.

## Contact

For questions, support, or collaboration opportunities:

- **GitHub Issues:** [Report bugs or request features](https://github.com/poncema4/CyberSmart/issues)
- **Discussions:** [Join community discussions](https://github.com/poncema4/CyberSmart/discussions)