import re  # Regular expressions for pattern matching in strings
import hashlib  # To create secure hash of passwords
import math  # For mathematical calculations, like entropy
import random  # For generating random characters
import string  # Contains pre-defined character sets like ascii_letters, digits, punctuation
from datetime import datetime  # To log date and time of password checks
import streamlit as st

# ---------------- Password strength and helper functions ----------------

def check_strength(password):
    """
    Checks the strength of the given password by evaluating:
    - Length
    - Presence of uppercase letters
    - Presence of lowercase letters
    - Presence of digits
    - Presence of special characters

    Returns:
        strength (str): 'STRONG', 'MODERATE', or 'WEAK'
        reasons (list): List of checks passed or failed
        suggestions (list): Suggestions for improvement if not strong
    """
    reasons = []
    suggestions = []

    # Check if password length is at least 8 characters
    if len(password) < 8:
        reasons.append("✘ Less than 8 characters")
        suggestions.append("✓ Use at least 8 characters")
    else:
        reasons.append("✔ Good length")

    # Check for uppercase letters
    if not re.search(r"[A-Z]", password):
        reasons.append("✘ No uppercase letters")
        suggestions.append("✓ Add uppercase letters (A-Z)")
    else:
        reasons.append("✔ Has uppercase letter(s)")

    # Check for lowercase letters
    if not re.search(r"[a-z]", password):
        reasons.append("✘ No lowercase letters")
        suggestions.append("✓ Add lowercase letters (a-z)")
    else:
        reasons.append("✔ Has lowercase letter(s)")

    # Check for digits
    if not re.search(r"[0-9]", password):
        reasons.append("✘ No numbers")
        suggestions.append("✓ Include numbers (0-9)")
    else:
        reasons.append("✔ Has number(s)")

    # Check for special characters
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        reasons.append("✘ No special characters")
        suggestions.append("✓ Include symbols like !@#$%^")
    else:
        reasons.append("✔ Has special character(s)")

    # Calculate score by summing boolean checks
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
    elif score >= 3:
        strength = "Password is MODERATE"
    else:
        strength = "Password is WEAK"

    return strength, reasons, suggestions

def calculate_entropy(password):
    """
    Estimates the entropy (randomness) of the password,
    which is a measure of how hard it is to guess or brute-force.

    Entropy is calculated as:
        entropy = length_of_password * log2(size_of_charset)

    The charset size depends on the categories of characters present:
    - Lowercase letters: 26
    - Uppercase letters: 26
    - Digits: 10
    - Special characters: estimated 32

    Returns:
        entropy (float): Estimated entropy rounded to 2 decimals
    """
    charset_size = 0
    if re.search(r"[a-z]", password):
        charset_size += 26
    if re.search(r"[A-Z]", password):
        charset_size += 26
    if re.search(r"[0-9]", password):
        charset_size += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        charset_size += 32  # rough estimate for special chars

    if charset_size == 0:
        return 0  # No valid characters detected

    entropy = len(password) * math.log2(charset_size)
    return round(entropy, 2)

def generate_strong_password(length=12):
    """
    Generates a random strong password using a mix of:
    - uppercase letters
    - lowercase letters
    - digits
    - punctuation/special characters

    Args:
        length (int): Desired length of password (default 12)

    Returns:
        str: Randomly generated password string
    """
    all_chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(all_chars, k=length))

def hash_password(password):
    """
    Creates a secure SHA-256 hash of the password.

    Args:
        password (str): Plain text password

    Returns:
        str: Hexadecimal SHA-256 hash of the password
    """
    return hashlib.sha256(password.encode()).hexdigest()

def save_to_file(password, strength, entropy):
    """
    Logs the password check event to a file with timestamp.
    The actual password is masked with '*' characters for privacy.

    Args:
        password (str): The original password (masked in file)
        strength (str): Strength classification of the password
        entropy (float): Estimated entropy in bits
    """
    line = f"{datetime.now()} | Password: {'*' * len(password)} | Strength: {strength} | Entropy: {entropy} bits\n"
    with open("password_report.txt", "a", encoding="utf-8") as file:
        file.write(line)

# ---------------- Main Streamlit Application Function ----------------

def password_strength():
    """
    Main Streamlit application for password strength checking and
    password generation.
    """
    st.header("🔐 Advanced Password Strength Checker 🔐")
    
    # ---------------- Password Strength Check Section ----------------
    
    st.subheader("Check Password Strength")
    
    # Create columns for password input and show password checkbox
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Password input with option to show/hide
        show_password = st.checkbox("Show Password", key="show_password_check")
        if show_password:
            password = st.text_input("Enter password to check:", key="password_input")
        else:
            password = st.text_input("Enter password to check:", type="password", key="password_input")
    
    with col2:
        st.write("")  # Empty space for alignment
        check_button = st.button("Check Strength", key="check_btn")
    
    # Check password strength when button is clicked or password is entered
    if (check_button or password) and password:
        # Call the check_strength function to get strength details
        strength, reasons, suggestions = check_strength(password)
        entropy = calculate_entropy(password)  # Calculate entropy
        hashed = hash_password(password)  # Create SHA-256 hash

        save_to_file(password, strength, entropy)  # Save results to file

        # Display results
        # Create color coding for strength
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
        
        # Display SHA-256 hash in an expandable section
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
        st.warning("Please enter a password to check.")
    
    # ---------------- Password Generator Section ----------------------
    
    st.divider()
    st.subheader("Generate Strong Password")
    
    # Create columns for length input and generate button
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        length = st.number_input("Enter password length (min 8):", 
                                min_value=8, max_value=100, value=12, 
                                key="length_input")
    
    with col2:
        st.write("")  # Empty space for alignment
        generate_button = st.button("Generate Password", key="generate_btn")
    
    with col3:
        show_generated = st.checkbox("Show Generated Password", key="show_generated")
    
    # Initialize session state for generated password
    if 'generated_password' not in st.session_state:
        st.session_state.generated_password = ""
    
    # Generate password when button is clicked
    if generate_button:
        try:
            length = int(length)
            if length < 8:
                st.error("Minimum password length is 8.")
            else:
                new_password = generate_strong_password(length)
                st.session_state.generated_password = new_password
                st.success("Password generated successfully!")
        except ValueError:
            st.error("Please enter a valid number for length.")
    
    # Display generated password
    if st.session_state.generated_password:
        st.subheader("Generated Password:")
        if show_generated:
            st.code(st.session_state.generated_password, language="text")
        else:
            st.code("*" * len(st.session_state.generated_password), language="text")
        
        # Option to copy password (display instruction)
        st.info("💡 Tip: You can select and copy the password above, or use it in the strength checker above!")
        
        # Auto-check generated password strength
        if st.checkbox("Check generated password strength", key="auto_check"):
            gen_strength, gen_reasons, gen_suggestions = check_strength(st.session_state.generated_password)
            gen_entropy = calculate_entropy(st.session_state.generated_password)
            
            if "STRONG" in gen_strength:
                st.success(f"**{gen_strength}**")
            elif "MODERATE" in gen_strength:
                st.warning(f"**{gen_strength}**")
            else:
                st.error(f"**{gen_strength}**")
            
            st.metric("Generated Password Entropy", f"{gen_entropy} bits")
    
    # ---------------- Information Section ----------------------
    
    st.divider()
    with st.expander("ℹ️ About Password Security"):
        st.write("""
        **Password Strength Criteria:**
        - **Length**: At least 8 characters (longer is better)
        - **Uppercase Letters**: A-Z
        - **Lowercase Letters**: a-z  
        - **Numbers**: 0-9
        - **Special Characters**: !@#$%^&*(),.?\":{}|<>
        
        **Entropy**: Measures password randomness in bits. Higher entropy means harder to crack.
        
        **SHA-256 Hash**: A secure one-way function that converts your password into a fixed-length string.
        
        **Tips for Strong Passwords:**
        - Use a unique password for each account
        - Consider using a password manager
        - Avoid personal information (names, birthdays, etc.)
        - Update passwords regularly
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