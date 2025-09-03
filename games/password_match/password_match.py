import streamlit as st

def password_match():
    st.header("Password Match")
    st.write("Match the passwords to 'Strong' or 'Weak'. Select the correct category for each password, then submit all at once.")

    passwords = [
        ("123456", "Weak"),
        ("P@ssw0rd!", "Strong"),
        ("qwerty", "Weak"),
        ("MyDog$2024", "Strong"),
        ("password", "Weak"),
        ("!Qaz2wsx#", "Strong"),
        ("letmein", "Weak"),
        ("Summer2024!", "Strong"),
        ("abc123", "Weak"),
        ("C@tLover#88", "Strong")
    ]

    user_answers = []
    for pw, correct in passwords:
        st.write(f"**Password:** `{pw}`")
        choice = st.radio("Choose category:", ["Strong", "Weak"], key=f"pw_{pw}")
        user_answers.append((choice, correct))

    if st.button("Submit Answers"):
        score = 0
        for idx, (user, correct) in enumerate(user_answers):
            if user == correct:
                st.success(f"Password {idx+1}: Correct!")
                score += 1
            else:
                st.error(f"Password {idx+1}: Incorrect.")
        st.info(f"You matched {score}/{len(passwords)} correctly!")
