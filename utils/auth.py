import streamlit as st
from utils.db import db
from typing import Optional

def show_auth_page() -> Optional[dict]:
    """
    Display authentication page with login or register option, and returns
    the user's info if authenticated, if not return none
    """
    st.markdown("""
    <style>
    .auth-title {
        text-align: center;
        color: #1a1a1a;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .auth-subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    .exam-type-container {
        margin: 2rem 0;
        padding: 1.5rem;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 12px;
        border-left: 5px solid #0066cc;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .exam-type-title {
        font-weight: 700;
        color: white;
        margin-bottom: 0.8rem;
        font-size: 1.4rem;
    }
    .score-history-container {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .score-card {
        background: rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .metric-container {
        background: rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    </style>
    """, unsafe_allow_html=True)

    if 'auth_tab' not in st.session_state:
        st.session_state.auth_tab = 'login'
    if 'user_authenticated' not in st.session_state:
        st.session_state.user_authenticated = False
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
    if 'session_initialized' not in st.session_state:
        st.session_state.session_initialized = True

    if st.session_state.user_authenticated and st.session_state.user_info:
        return st.session_state.user_info

    st.markdown('<h1 class="auth-title">CyberSmart 🛡️</h1>', unsafe_allow_html=True)
    st.markdown('<p class="auth-subtitle">Secure your digital future</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", use_container_width=True, 
                    type="primary" if st.session_state.auth_tab == 'login' else "secondary"):
            st.session_state.auth_tab = 'login'
            st.rerun()
    
    with col2:
        if st.button("Register", use_container_width=True,
                    type="primary" if st.session_state.auth_tab == 'register' else "secondary"):
            st.session_state.auth_tab = 'register'
            st.rerun()

    if st.session_state.auth_tab == 'login':
        show_login_form()
    else:
        show_register_form()

    return None

def show_login_form():
    """
    Display the login form for the user to fill out if 
    they already have an account
    """
    st.subheader("Welcome Back!")
    
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        submitted = st.form_submit_button("Login", use_container_width=True, type="primary")
        
        if submitted:
            if not username or not password:
                st.error("Please fill out all the required fields")
                return
            
            success, user_info, message = db.login_user(username, password)
            
            if success:
                st.session_state.user_authenticated = True
                st.session_state.user_info = user_info
                st.rerun()
            else:
                st.error(message)

def show_register_form():
    """
    Display the registration form for new users to fill out
    and create their new account
    """
    st.subheader("Create Account")
    
    with st.form("register_form", clear_on_submit=False):
        username = st.text_input("Username", placeholder="Choose a username")
        password = st.text_input("Password", type="password", placeholder="Create a password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        
        submitted = st.form_submit_button("Register", use_container_width=True, type="primary")
        
        if submitted:
            if not all([username, password, confirm_password]):
                st.error("Please fill out all the required fields")
                return
            
            if password != confirm_password:
                st.error("Passwords do not match")
                return
            
            if len(password) < 6:
                st.error("Password must be at least 6 characters long")
                return
            
            success, message = db.register_user(username, password)
            
            if success:
                login_success, user_info, login_message = db.login_user(username, password)
                if login_success:
                    st.session_state.user_authenticated = True
                    st.session_state.user_info = user_info
                    st.rerun()
                else:
                    st.error(f"Registration successful but login failed: {login_message}")
            else:
                st.error(message)

def show_exam_type_selection() -> Optional[str]:
    """
    Show exam type selection page, pre, practice or post assessment
    and will prompt the user to select the assessment type
    """
    if 'exam_type_selected' not in st.session_state:
        st.session_state.exam_type_selected = False
    if 'selected_exam_type' not in st.session_state:
        st.session_state.selected_exam_type = None

    if st.session_state.exam_type_selected and st.session_state.selected_exam_type:
        return st.session_state.selected_exam_type

    st.markdown('<div class="exam-type-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="exam-type-title">Choose Your Assessment Type</h2>', unsafe_allow_html=True)
    st.markdown("Select the type of cybersecurity assessment you would like to take :)")
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Pre-Assessment", use_container_width=True, type="primary"):
            st.session_state.selected_exam_type = 'pre'
            st.session_state.exam_type_selected = True
            st.session_state.scores_saved = False
            if st.session_state.user_info:
                session_id = db.create_session(st.session_state.user_info['id'], 'pre')
                st.session_state.current_session_id = session_id
            st.rerun()
    
    with col2:
        if st.button("📝 Practice Mode", use_container_width=True, type="secondary"):
            st.session_state.selected_exam_type = 'practice'
            st.session_state.exam_type_selected = True
            st.session_state.scores_saved = False
            if st.session_state.user_info:
                session_id = db.create_session(st.session_state.user_info['id'], 'practice')
                st.session_state.current_session_id = session_id
            st.rerun()
    
    with col3:
        if st.button("🎯 Post-Assessment", use_container_width=True, type="primary"):
            st.session_state.selected_exam_type = 'post'
            st.session_state.exam_type_selected = True
            st.session_state.scores_saved = False
            if st.session_state.user_info:
                session_id = db.create_session(st.session_state.user_info['id'], 'post')
                st.session_state.current_session_id = session_id
            st.rerun()

    st.markdown("---")
    st.markdown("**Assessment Types:**")
    st.markdown("- **Pre-Assessment**: Test your current cybersecurity knowledge")
    st.markdown("- **Practice Mode**: Practice without affecting your overall score")
    st.markdown("- **Post-Assessment**: Test your knowledge after training")

    return None

def logout_user():
    """
    Logout the current user and redirect them to the log in screen
    and clear all session state
    """
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    st.session_state.step = 0
    st.session_state.auth_tab = 'login'
    st.session_state.user_authenticated = False
    st.session_state.user_info = None
    st.session_state.session_initialized = True

    st.rerun()

def show_user_dashboard():
    """
    Show user dashboard with logout option so they can see
    their username, assessment history, and log out when needed
    """
    if st.session_state.user_info:
        with st.sidebar:
            st.markdown(f"**Welcome, {st.session_state.user_info['username']}!**")
            
            with st.expander("📊 Your Assessment History", expanded=False):
                show_score_history_sidebar()
            
            if st.button("🚪 Logout", use_container_width=True, type="secondary"):
                logout_user()

def show_score_history_sidebar():
    """
    Display detailed score history in sidebar for the user's dashboard sidebar
    """
    if not st.session_state.get('user_authenticated', False):
        return
    
    user_id = st.session_state.user_info['id']
    user_scores = db.get_user_scores(user_id)
    
    if not user_scores:
        st.info("📊 No assessment history yet. Complete your first assessment!")
    else:
        for _, score in enumerate(user_scores[:5]):
            exam_type_emoji = {'pre': '🔍', 'post': '🎯', 'practice': '📝'}
            emoji = exam_type_emoji.get(score['exam_type'], '📊')
            
            if score['overall_score'] >= 140:
                color = "#4CAF50"
                border_color = "#388E3C"
            elif score['overall_score'] >= 100:
                color = "#FF9800"
                border_color = "#F57C00"
            else:
                color = "#f44336"
                border_color = "#D32F2F"
            
            st.markdown(f'''
            <div style="
                border-left: 4px solid {border_color}; 
                background: linear-gradient(90deg, {color}20 0%, #f8f9fa 100%);
                padding: 1rem;
                margin: 0.5rem 0;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <strong>{emoji} {score['exam_type'].title()} Assessment</strong><br>
                Overall Score: <strong style="color: {border_color};">{score['overall_score']:.1f}/200</strong><br>
                Phishing: {score['phishing_score']:.1f} | Password Match: {score['password_match_score']:.1f} | Strength: {score['password_strength_entropy']:.1f}<br>
                <small>Completed: {score['completed_at']}</small>
            </div>
            ''', unsafe_allow_html=True)

def show_score_history():
    """
    Display detailed score history in the assessment expander at the last step
    """
    if not st.session_state.get('user_authenticated', False):
        return
    
    user_id = st.session_state.user_info['id']
    
    user_scores = db.get_user_scores(user_id)

    assessment_scores = [score for score in user_scores if score['exam_type'] in ['pre', 'post']]
    
    if assessment_scores:
        st.markdown("**💯 Assessment History**")
        for _, score in enumerate(assessment_scores[:5]):
            exam_type_emoji = {'pre': '🔍', 'post': '🎯', 'practice': '📝'}
            emoji = exam_type_emoji.get(score['exam_type'], '📊')
            
            if score['overall_score'] >= 140:
                color = "#4CAF50"
                border_color = "#388E3C"
            elif score['overall_score'] >= 100: 
                color = "#FF9800"
                border_color = "#F57C00"
            else:
                color = "#f44336"
                border_color = "#D32F2F"
            
            st.markdown(f'''
            <div style="
                border-left: 4px solid {border_color}; 
                background: linear-gradient(90deg, {color}20 0%, #f8f9fa 100%);
                padding: 1rem;
                margin: 0.5rem 0;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <strong>{emoji} {score['exam_type'].title()} Assessment</strong><br>
                Overall Score: <strong style="color: {border_color};">{score['overall_score']:.1f}/200</strong><br>
                Phishing: {score['phishing_score']:.1f} | Password Match: {score['password_match_score']:.1f} | Strength: {score['password_strength_entropy']:.1f}<br>
                <small>Completed: {score['completed_at']}</small>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("📊 No assessment history yet. Complete your first assessment!")
        st.markdown("<br>", unsafe_allow_html=True)
    
    improvement = db.get_user_improvement(user_id)
    if improvement['has_both']:
        st.markdown("**⭐ Personal Progress Analysis**")
        imp = improvement['improvements']
        
        overall_change = imp['overall']
        if overall_change > 0:
            progress_color = "#4CAF50"
            progress_icon = "📈"
            progress_text = f"Improved by {overall_change:.1f} points!"
        elif overall_change < 0:
            progress_color = "#f44336"
            progress_icon = "📉"
            progress_text = f"Decreased by {abs(overall_change):.1f} points"
        else:
            progress_color = "#ff9800"
            progress_icon = "↔️"
            progress_text = "No change in overall score"
        
        st.markdown(f'''
        <div style="
            background-color: {progress_color}20; 
            border: 1px solid {progress_color};
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
            text-align: center;
        ">
            <h4>{progress_icon} {progress_text}</h4>
            <p>Phishing: {imp['phishing']:+.1f} | Password Match: {imp['password_match']:+.1f} | Strength: {imp['password_strength']:+.1f}</p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

    global_stats = db.get_global_averages()
    st.markdown("**🌍 Global Community Statistics**")
    
    col1, col2 = st.columns(2)
    with col1:
        pre_avg = global_stats['pre_averages']
        if pre_avg['count'] > 0:
            st.markdown(f'''
            <div style="
                background: rgba(255,255,255,0.1);
                border-radius: 8px;
                padding: 1rem;
                margin: 0.5rem;
                text-align: center;
                border: 1px solid #ddd;
            ">
                <h5>📝 Pre-Assessment Average</h5>
                <p><strong>{pre_avg['overall']:.1f}/200</strong></p>
                <small>{pre_avg['count']} participants</small>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div style="
                background: rgba(255,255,255,0.1);
                border-radius: 8px;
                padding: 1rem;
                margin: 0.5rem;
                text-align: center;
                border: 1px solid #ddd;
            ">
                <h5>📝 Pre-Assessment Average</h5>
                <p><strong>No data yet</strong></p>
                <small>0 participants</small>
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        post_avg = global_stats['post_averages']
        if post_avg['count'] > 0:
            st.markdown(f'''
            <div style="
                background: rgba(255,255,255,0.1);
                border-radius: 8px;
                padding: 1rem;
                margin: 0.5rem;
                text-align: center;
                border: 1px solid #ddd;
            ">
                <h5>🎯 Post-Assessment Average</h5>
                <p><strong>{post_avg['overall']:.1f}/200</strong></p>
                <small>{post_avg['count']} participants</small>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div style="
                background: rgba(255,255,255,0.1);
                border-radius: 8px;
                padding: 1rem;
                margin: 0.5rem;
                text-align: center;
                border: 1px solid #ddd;
            ">
                <h5>🎯 Post-Assessment Average</h5>
                <p><strong>No data yet</strong></p>
                <small>0 participants</small>
            </div>
            ''', unsafe_allow_html=True)