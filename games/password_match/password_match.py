import streamlit as st
import random

def password_match():
    st.header("Password Match")
    st.write("""
        Determine is each password would be considered to be Weak or Strong. 
        Select the correct strength category for each password and get your final score!
    """)

    passwords = {
        "123456": "Weak",
        "X}7f@44_=C72": "Strong",
        "MyDog20": "Weak",
        "password": "Weak",
        "5k_U2q2N+%": "Strong",
        "!Qaz2wsx#": "Strong",
        "6z[MO": "Weak",
        "Summer2024!": "Strong",
        "abc123": "Weak",
        "C@tLover#88": "Strong"
    }

    password_shuffle = random.sample(list(passwords.keys()), len(passwords))

    if "answer" not in st.session_state:
        st.session_state.answer = {}

    for password in passwords:
        st.write(f"**Password:** `{password}`")
        st.session_state.answer[password] = st.radio(
            "Choose category:", ["Strong", "Weak"], key=f"password_{password}"
        )

    if st.button("Check Results"):
        score = 0
        for i, password in enumerate(password_shuffle):
            user_choice = st.session_state.answer[password]
            correct_choice = passwords[password]
            if user_choice == correct_choice:
                st.success(f"Password {i+1}: Correct!")
                score += 1
            else:
                st.error(f"Password {i+1}: Incorrect.")
        st.info(f"You matched {score}/{len(passwords)} correctly!")