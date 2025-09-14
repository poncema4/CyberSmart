import streamlit as st
import random
import string

def password_generator():
    st.header("Password Generator")
    st.write("Select your password criteria, then generate a strong password!")

    col1, col2 = st.columns(2)
    with col1:
        use_lower = st.checkbox("Include lowercase letters (a-z)", value=True)
        use_upper = st.checkbox("Include uppercase letters (A-Z)", value=True)
    with col2:
        use_digits = st.checkbox("Include numbers (0-9)", value=True)
        use_symbols = st.checkbox("Include symbols (!@#$...)", value=True)

    length = st.slider("Password length", min_value=4, max_value=64, value=12)

    char_pool = ""
    if use_lower:
        char_pool += string.ascii_lowercase
    if use_upper:
        char_pool += string.ascii_uppercase
    if use_digits:
        char_pool += string.digits
    if use_symbols:
        char_pool += string.punctuation

    if not char_pool:
        st.warning("Please select at least one character type.")
        return

    if 'generated_password' not in st.session_state:
        st.session_state.generated_password = ""

    if st.button("Generate Password"):
        st.session_state.generated_password = ''.join(random.choices(char_pool, k=length))

    password = st.session_state.generated_password

    if password:
        st.subheader("Your generated password:")
        # Use st.code() instead of st.text_input to get automatic copy button
        st.code(password, language="text")