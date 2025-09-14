import re
import hashlib
import math
from datetime import datetime
import streamlit as st
from github_push import push_to_github
import time

def check_strength(password):
    reasons = []
    suggestions = []

    # Check if the password is at least 8 characters long
    if len(password) < 8:
        reasons.append("✘ Less than 8 characters")
        suggestions.append("Use at least 8 characters")
    else:
        reasons.append("✔ Good length")

    # Check for uppercase letters
    if not re.search(r"[A-Z]", password):
        reasons.append("✘ No uppercase letters")
        suggestions.append("Add uppercase letters (A-Z)")
    else:
        reasons.append("✔ Has uppercase letter(s)")

    # Check for lowercase letters
    if not re.search(r"[a-z]", password):
        reasons.append("✘ No lowercase letters")
        suggestions.append("Add lowercase letters (a-z)")
    else:
        reasons.append("✔ Has lowercase letter(s)")

    # Check for numbers
    if not re.search(r"[0-9]", password):
        reasons.append("✘ No numbers")
        suggestions.append("Include numbers (0-9)")
    else:
        reasons.append("✔ Has number(s)")

    # Check for symbols/special characters
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        reasons.append("✘ No special characters")
        suggestions.append("Include symbols like !@#$%^")
    else:
        reasons.append("✔ Has special character(s)")

    # Calculate score by the sum of boolean checks
    score = sum([
        len(password) >= 8,
        bool(re.search(r"[A-Z]", password)),
        bool(re.search(r"[a-z]", password)),
        bool(re.search(r"[0-9]", password)),
        bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
    ])

    # Determine strength category based on score
    if score == 5:
        strength = "Password is STRONG"
    elif 4 >= score >= 3:
        strength = "Password is MODERATE"
    else:
        strength = "Password is WEAK"

    return strength, reasons, suggestions

def calculate_entropy(password):
    charset_size = 0

    if re.search(r"[a-z]", password):
        charset_size += 26
    if re.search(r"[A-Z]", password):
        charset_size += 26
    if re.search(r"[0-9]", password):
        charset_size += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        charset_size += 32

    if charset_size == 0:
        return 0

    entropy = len(password) * math.log2(charset_size)
    return round(entropy, 2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_to_file(password, strength, entropy):
    line = f"{datetime.now()} | Password: {'*' * len(password)} | Strength: {strength} | Entropy: {entropy} bits\n"
    with open("password_report.txt", "a", encoding="utf-8") as file:
        file.write(line)

    # Push to Github
    try:
        push_to_github("password_report.txt", commit_message="Updated password report from CyberSmart!", branch="main")
    except Exception as e:
        print(f"Failed to push to GitHub: {e}")

def password_strength():
    st.header("Password Strength Checker")
    st.write("""
        Enter a password below to analyze its strength, entropy, and security. Get detailed feedback and suggestions for improvements in your current password!
    """)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        password = st.text_input("Enter password to check:", type="password", key="password_input")
    
    with col2:
        st.write("")
        check_button = st.button("Check Strength", key="check_btn")

    # Initialize session state flags
    if "password_checked" not in st.session_state:
        st.session_state["password_checked"] = False
    if "last_password" not in st.session_state:
        st.session_state["last_password"] = ""
    if "last_push_time" not in st.session_state:
        st.session_state["last_push_time"] = 0

    # Reset flag if password changed
    if password != st.session_state["last_password"]:
        st.session_state["password_checked"] = False
        st.session_state["last_password"] = password
    
    # Check password strength when button is clicked or password is entered
    if (check_button or password) and password:
        strength, reasons, suggestions = check_strength(password)
        entropy = calculate_entropy(password)
        hashed = hash_password(password)

        RATE_LIMIT_SECONDS = 5

        if not st.session_state["password_checked"]:
            now = time.time()
            if now - st.session_state["last_push_time"] >= RATE_LIMIT_SECONDS:
                save_to_file(password, strength, entropy)
                st.session_state["password_checked"] = True
                st.session_state["last_push_time"] = now
            else:
                st.info(f"Wait {RATE_LIMIT_SECONDS} seconds between pushes to GitHub.")

        # Display results
        if "STRONG" in strength:
            st.success(f"**{strength}**")
        elif "MODERATE" in strength:
            st.warning(f"**{strength}**")
        else:
            st.error(f"**{strength}**")
        
        # Display entropy and hash
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Entropy", f"{entropy} bits")
        with col2:
            st.metric("Password Length", len(password))
        
        # Display SHA-256 hash
        with st.expander("SHA-256 Hash"):
            st.code(hashed, language="text")
        
        # Display analysis
        st.subheader("Analysis:")
        for reason in reasons:
            if "✔" in reason:
                st.success(reason)
            else:
                st.error(reason)
        
        # Show suggestions only if password is not strong
        if "STRONG" not in strength:
            st.subheader("Suggestions:")
            for suggestion in suggestions:
                st.info(suggestion)
    
    elif check_button and not password:
        st.warning("Please enter a password to check its strength.")
    
    # Display information section
    st.divider()
    with st.expander("ℹ️ About Password Security"):
        st.write("""
        **Password Strength Criteria:**
        - **Length**: At least 8 characters
        - **Uppercase Letters**: A-Z
        - **Lowercase Letters**: a-z  
        - **Numbers**: 0-9
        - **Special Characters**: !@#$%^&*(),.?\":{}|<>
        """)

        st.write("""
        **Strength Levels:**
        - **Strong**: All 5 criteria met
        - **Moderate**: 3-4 criteria met
        - **Weak**: Less than 3 criteria met
        """)

        st.markdown('<hr style="margin:5px 0;">', unsafe_allow_html=True)

        st.write("""
        **Entropy (Password Randomness):**
        - **0-30 bits**: Very predictable, easily cracked
        - **30-50 bits**: Weak, vulnerable to attacks
        - **50-70 bits**: Moderate strength, acceptable for low-risk accounts
        - **70-90 bits**: Strong, good for most accounts
        - **90+ bits**: Very strong, excellent for high-security accounts

        Higher entropy means your password has more possible combinations, making it exponentially harder to crack through brute force attacks.
        """)

        st.markdown('<hr style="margin:5px 0;">', unsafe_allow_html=True)

        st.write("""
        **SHA-256 Hash:**
                
        Secure Hash Algorithm 256-bit (SHA-256) is a cryptographic hash function that converts your password into a fixed 64-character string.
                 
        - **One-way function**: Cannot be reversed to get the original password
        - **Deterministic**: Same password always produces the same hash
        - **Avalanche effect**: Small password changes create completely different hashes
        - **Collision resistant**: Nearly impossible for two different passwords to have the same hash           
        
        Websites store password hashes instead of actual passwords for security. When you log in, your entered password is hashed and compared to the stored hash value. 
        
        """)

        st.markdown('<hr style="margin:5px 0;">', unsafe_allow_html=True)

        st.write("""
        **Tips for Strong Passwords:**
        - Use a unique password for each account
        - Consider using a password manager
        - Avoid personal information (names, birthdays, etc.)
        - Update passwords regularly
        - Use passphrases (multiple random words)
        """)
    
    # Display log file info
    with st.expander("📁 Password Check Logs"):
        st.write("""
        Password checks are logged to `password_report.txt` with:
        - Timestamp of check
        - Masked password (actual password not stored)
        - Strength assessment
        - Entropy value
        
        This helps track password security practices over time.
        """)

        # Password report file link
        st.markdown(
            "[View Password Report on GitHub](https://github.com/poncema4/CyberSmart/blob/main/password_report.txt)",
            unsafe_allow_html=True
        )