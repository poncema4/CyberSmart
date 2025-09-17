import streamlit as st
import random

def password_match():
    st.header("Password Match")
    st.write("""
        Determine if each password would be considered Weak or Strong. Select the correct strength category for each password and get your final score!
    """)

    passwords = {
        "123456": {"strength": "Weak", "explanation": "Very common and easily guessable."},
        "X}7f@44_=C72": {"strength": "Strong", "explanation": "Long with random characters, making it harder to guess."},
        "MyDog20": {"strength": "Weak", "explanation": "Short, based on simple pattern words and numbers."},
        "password": {"strength": "Weak", "explanation": "One of the most common passwords in the world."},
        "5k_U2q2N+%": {"strength": "Strong", "explanation": "Contains a mix of symbols, numbers, and letters."},
        "!Qaz2wsx#": {"strength": "Strong", "explanation": "Complex mix of symbols, numbers, and letters."},
        "6z[MO": {"strength": "Weak", "explanation": "Too short, brute forceable needs to be longer."},
        "Summer2024!": {"strength": "Strong", "explanation": "Good length with mix of cases, numbers, and symbol."},
        "abc123": {"strength": "Weak", "explanation": "Very common and predictable sequence."},
        "C@tLover#88": {"strength": "Strong", "explanation": "Less guessable since it has a mix of symbols, numbers, and words."}
    }

    if "match_attempted" in st.session_state:
        st.success(f"You have already submitted. Your score: {st.session_state['password_match_score']} / {len(passwords)}")
        return st.session_state['password_match_score']

    if "match_answers" not in st.session_state:
        st.session_state.match_answers = {}
    if "password_order" not in st.session_state:
        st.session_state.password_order = random.sample(list(passwords.keys()), len(passwords))
    password_order = st.session_state.password_order

    for idx, p in enumerate(password_order, start=1):
        st.write(f"**Q{idx}: Password:** `{p}`")
        st.session_state.match_answers[p] = st.radio(
            "", ["Strong", "Weak"], key=f"password_{p}"
        )

    if st.button("Check Results", key="match_submit"):
        score = 0
        user_answers = {}
        for idx, p in enumerate(password_order, start=1):
            user_choice = st.session_state.match_answers[p]
            correct_choice = passwords[p]["strength"]
            explanation = passwords[p]["explanation"]
            user_answers[p] = user_choice
            if user_choice == correct_choice:
                st.success(f"✔ Q{idx}")
                score += 1
            else:
                st.error(f"✘ Q{idx}: {explanation}")
        st.session_state['password_match_score'] = score
        st.session_state['match_attempted'] = True
        st.session_state['match_user_answers'] = user_answers
        st.info(f"Your score: {score}/{len(passwords)}")
        return score

    return None