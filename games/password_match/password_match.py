import streamlit as st
import random
import time
from utils.db import db

def password_match() -> int | None:
    st.header("Password Match")
    st.write("""
        Determine if each password would be considered Weak or Strong. Select the correct strength category for each password and get your final score!
    """)

    assessment_type = st.session_state.get('selected_exam_type', 'practice')
    user_id = st.session_state.get('user_info', {}).get('id')
    
    if 'password_start_times' not in st.session_state:
        st.session_state.password_start_times = {}
    
    pre_passwords = {
        "123456": {"strength": "Weak", "explanation": "Very common and easily guessable."},
        "password": {"strength": "Weak", "explanation": "One of the most common passwords in the world."},
        "MyDog20": {"strength": "Weak", "explanation": "Short, based on simple pattern words and numbers."},
        "abc123": {"strength": "Weak", "explanation": "Very common and predictable sequence."},
        "qwerty": {"strength": "Weak", "explanation": "Common keyboard pattern, easily guessed."},
        "Summer2024!": {"strength": "Strong", "explanation": "Good length with mix of cases, numbers, and symbol."},
        "C@tLover#88": {"strength": "Strong", "explanation": "Good mix of symbols, numbers, and words."},
        "MyP@ssw0rd!": {"strength": "Strong", "explanation": "Contains uppercase, lowercase, numbers, and symbols."},
        "BlueSky@9": {"strength": "Strong", "explanation": "Good combination of words, symbols, and numbers."},
        "hello": {"strength": "Weak", "explanation": "Too short and common word."},
        "Testing123!": {"strength": "Strong", "explanation": "Good length with mixed characters and symbols."},
        "Admin": {"strength": "Weak", "explanation": "Short and common administrative term."}
    }
    
    practice_passwords = {
        "X}7f@44_=C72": {"strength": "Strong", "explanation": "Long with random characters, making it harder to guess."},
        "5k_U2q2N+%": {"strength": "Strong", "explanation": "Contains a mix of symbols, numbers, and letters."},
        "!Qaz2wsx#": {"strength": "Strong", "explanation": "Complex mix of symbols, numbers, and letters."},
        "6z[MO": {"strength": "Weak", "explanation": "Too short, brute forceable needs to be longer."},
        "password123": {"strength": "Weak", "explanation": "Common word with predictable number sequence."},
        "welcome": {"strength": "Weak", "explanation": "Common word, no complexity."},
        "Dragon$78": {"strength": "Strong", "explanation": "Good mix of word, symbol, and numbers."},
        "iloveyou": {"strength": "Weak", "explanation": "Common phrase, no complexity."},
        "Tr0ub4dor&3": {"strength": "Strong", "explanation": "Good length with character substitution and symbols."},
        "Monday1": {"strength": "Weak", "explanation": "Predictable pattern with day and number."},
        "SecurePass@123": {"strength": "Strong", "explanation": "Long password with good character variety."},
        "12345678": {"strength": "Weak", "explanation": "Sequential numbers, extremely predictable."}
    }
    
    post_passwords = {
        "P@$$w0rd": {"strength": "Weak", "explanation": "Despite symbols/numbers, it's based on the common word 'password'."},
        "Tr0ub4dor&3": {"strength": "Strong", "explanation": "Good length with character substitution and symbols."},
        "correcthorsebatterystaple": {"strength": "Strong", "explanation": "Very long passphrase that's hard to crack despite being all lowercase."},
        "Admin@123": {"strength": "Weak", "explanation": "Common admin term with predictable number/symbol pattern."},
        "M0nk3y!": {"strength": "Weak", "explanation": "Short length makes it weak despite character variety."},
        "MySecretP@ssw0rd2024": {"strength": "Strong", "explanation": "Long with good character variety and current year."},
        "Pa$$word1": {"strength": "Weak", "explanation": "Based on 'password' with minimal complexity additions."},
        "9C#mK8@vN2$eL": {"strength": "Strong", "explanation": "Random characters with good length and complexity."},
        "Summer2024!": {"strength": "Weak", "explanation": "Predictable seasonal pattern that could be easily guessed."},
        "ILovePizza123": {"strength": "Weak", "explanation": "Common phrase pattern with predictable numbers."},
        "Xp$9#Kw2&Mq7": {"strength": "Strong", "explanation": "Random mix of characters, symbols, and numbers."},
        "sunshine": {"strength": "Weak", "explanation": "Common word, no complexity, too short."}
    }
    
    if assessment_type == 'pre':
        password_pool = pre_passwords
    elif assessment_type == 'post':
        password_pool = post_passwords
        if user_id:
            weak_areas = db.get_user_weak_areas(user_id)
            if weak_areas['password_match']['is_weak'] or weak_areas['password_match']['is_slow']:
                st.info("Adaptive Learning: Extra challenging password questions based on your pre-assessment!")
    else:
        password_pool = practice_passwords

        if user_id:
            weak_areas = db.get_user_weak_areas(user_id)
            if weak_areas['password_match']['is_weak']:
                st.info("Practice Mode: Focus on password strength, needs improvement based on pre-assessment!")
            if weak_areas['password_match']['is_slow']:
                st.info("Practice Mode: Work on speed, tracking your response time!")
    
    if "selected_passwords" not in st.session_state or st.session_state.get('current_match_assessment_type') != assessment_type:
        selected_items = random.sample(list(password_pool.items()), 10)
        st.session_state.selected_passwords = dict(selected_items)
        st.session_state.current_match_assessment_type = assessment_type
        st.session_state.password_start_times = {}
        for pwd in st.session_state.selected_passwords.keys():
            st.session_state.password_start_times[pwd] = time.time()
    
    passwords = st.session_state.selected_passwords

    if "match_attempted" in st.session_state:
        st.success(f"You have already submitted. Your score: {st.session_state['password_match_score']} / 10")
        return st.session_state['password_match_score']

    if "match_answers" not in st.session_state:
        st.session_state.match_answers = {}

    if "password_order" not in st.session_state:
        st.session_state.password_order = list(passwords.keys())
        
    password_order = st.session_state.password_order

    current_time = time.time()
    for idx, p in enumerate(password_order, start=1):
        if p not in st.session_state.password_start_times:
            st.session_state.password_start_times[p] = current_time
        
        st.write(f"**Q{idx}: Password:** `{p}`")
        
        previous_answer = st.session_state.match_answers.get(p)
        st.session_state.match_answers[p] = st.radio(
            "", ["Strong", "Weak"], key=f"password_{p}"
        )
        
        if previous_answer != st.session_state.match_answers[p]:
            st.session_state.password_start_times[p] = time.time()

    if st.button("Check Results", key="match_submit"):
        score = 0
        user_answers = {}
        session_id = st.session_state.get('session_id', 'unknown')
        
        end_time = time.time()
        
        for idx, p in enumerate(password_order, start=1):
            user_choice = st.session_state.match_answers[p]
            correct_choice = passwords[p]["strength"]
            explanation = passwords[p]["explanation"]
            user_answers[p] = user_choice
            
            start_time = st.session_state.password_start_times.get(p, end_time)
            response_time = end_time - start_time
            
            is_correct = user_choice == correct_choice
            if is_correct:
                st.success(f"✔ Q{idx} (took {response_time:.1f}s)")
                score += 1
            else:
                st.error(f"✘ Q{idx}: {explanation} (took {response_time:.1f}s)")
            
            if user_id and session_id:
                password_id = f"pwd_{hash(p) % 10000}"
                db.save_performance_metric(
                    user_id=user_id,
                    session_id=session_id,
                    exam_type=assessment_type,
                    game_type='password_match',
                    question_id=password_id,
                    is_correct=is_correct,
                    response_time=response_time
                )
        
        st.session_state['password_match_score'] = score
        st.session_state['match_attempted'] = True
        st.session_state['match_user_answers'] = user_answers
        
        avg_time = sum(end_time - st.session_state.password_start_times.get(p, end_time) 
                       for p in password_order) / len(password_order)
        st.info(f"Your score: {score}/10 | Average response time: {avg_time:.1f}s per question")
        
        return score

    return None