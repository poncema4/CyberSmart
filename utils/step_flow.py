import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO
from utils.github_push import push_to_github
from utils.cyber_smart import get_phishing_score, get_match_score
from games.spot_the_phish.spot_the_phish import spot_the_phish
from games.password_match.password_match import password_match
from games.password_generator.password_generator import password_generator
from games.password_strength.password_strength import password_strength
from utils.recommendations import get_personalized_recommendations
from utils.auth import show_auth_page, show_exam_type_selection, show_user_dashboard, show_score_history
from utils.db import db
import csv
import os
import csv

STEPS = [
    "auth",
    "exam_type",
    "intro",
    "spot_the_phish",
    "password_match",
    "password_generator",
    "password_strength",
    "feedback",
    "results"
]

def run_step_flow() -> None:
    st.markdown("""
    <style>
    .step-title {font-size:2.2rem;font-weight:700;margin-bottom:0.5em;}
    .step-desc {font-size:1.1rem;color:#555;}
    .feedback-container {
        margin: 20px 0;
        padding: 1em;
        border-radius: 8px;
    }
    .feedback-item {
        background: #f1f3f6;
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        color: #333;
        font-size: 1rem;
    }
    .results-score {
        font-size: 2.5em;
        font-weight: bold;
        color: #1a1a1a;
        margin: 20px 0;
    }
    .score-metrics {
        margin: 2em 0;
    }
    .section-heading {
        font-size: 1.5em;
        font-weight: 600;
        margin: 1.5em 0 1em;
        color: #1a1a1a;
    }
    .return-button {
        margin-top: 2rem;
        padding: 0.75rem 1.5rem;
        background: #4CAF50;
        color: white;
        border-radius: 8px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .return-button:hover {
        background: #45a049;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    if "step" not in st.session_state:
        st.session_state.step = 0

    step = st.session_state.step

    def next_step() -> None:
        """
        Move to the next step in the steps instruction to analyze and correctly update the step state variable
        """
        st.session_state.step += 1

    if st.session_state.get('user_authenticated', False):
        show_user_dashboard()

    if step == 0:
        user_info = show_auth_page()
        if user_info:
            next_step()
            st.rerun()
        return

    if step == 1:
        exam_type = show_exam_type_selection()
        if exam_type:
            next_step()
            st.rerun()
        return

    if step == 2:
        st.markdown('<div class="step-title">Welcome to CyberSmart!</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-desc">CyberSmart is an interactive cybersecurity course. You will go through a series of activities and games to learn and test your knowledge. Click Start to begin!</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("start_form"):
            if st.form_submit_button("Start"):
                st.session_state.scores_saved = False
                next_step()
                st.rerun()

    elif step == 3:
        st.markdown('<div class="step-title">Step 1: Spot the Phish</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-desc">Identify phishing attempts. You have <b>one attempt</b>. Your score will be recorded.</div>', unsafe_allow_html=True)
        if "spot_the_phish_score" not in st.session_state:
            score = spot_the_phish()
            if score is not None:
                with st.form("phish_next_form"):
                    if st.form_submit_button("Continue"):
                        next_step()
                        st.rerun()
        else:
            st.markdown("<br>", unsafe_allow_html=True)
            st.success("Step completed!")
            with st.form("phish_continue_form"):
                if st.form_submit_button("Continue"):
                    next_step()
                    st.rerun()

    elif step == 4:
        st.markdown('<div class="step-title">Step 2: Password Match</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-desc">Classify passwords as strong or weak. <b>One attempt only.</b> Your score will be recorded.</div>', unsafe_allow_html=True)
        if "password_match_score" not in st.session_state:
            score = password_match()
            if score is not None:
                with st.form("match_next_form"):
                    if st.form_submit_button("Continue"):
                        next_step()
                        st.rerun()
        else:
            st.markdown("<br>", unsafe_allow_html=True)
            st.success("Step completed!")
            with st.form("match_continue_form"):
                if st.form_submit_button("Continue"):
                    next_step()
                    st.rerun()

    elif step == 5:
        st.markdown('<div class="step-title">Step 3: Password Generator</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-desc">Experiment with generating strong passwords. When you are ready, click Continue.</div>', unsafe_allow_html=True)
        password_generator()
        with st.form("gen_next_form"):
            if st.form_submit_button("Continue"):
                next_step()
                st.rerun()

    elif step == 6:
        st.markdown('<div class="step-title">Step 4: Password Strength Checker</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-desc">Test the strength of your own password. <b>One attempt only.</b> Your score will be recorded.</div>', unsafe_allow_html=True)
        password_strength()
        if st.session_state.get("password_strength_attempted", False) and st.session_state.get("last_strength", None):
            with st.form("strength_next_form"):
                if st.form_submit_button("Continue"):
                    next_step()
                    st.rerun()

    elif step == 7:
        st.markdown('<div class="step-title">Step 5: Feedback</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-desc">Please provide feedback on your experience (max 500 characters).</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        feedback_form = st.form("feedback_form")
        with feedback_form:
            feedback = st.text_area(
                "Your feedback (optional):",
                max_chars=500,
                height=150,
                key="feedback_text"
            )
            submit_feedback = st.form_submit_button("Submit")
        
        if submit_feedback:
            if feedback.strip():
                
                csv_file = "reports/feedback.csv"
                file_exists = os.path.isfile(csv_file)
                
                with open(csv_file, "a", newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    
                    if not file_exists:
                        writer.writerow(["Timestamp", "Feedback"])

                    local_time = datetime.now().astimezone()
                    timestamp = local_time.strftime("%Y-%m-%d %H:%M:%S")
                    writer.writerow([timestamp, feedback.strip()])
                
                try:
                    push_to_github("reports/feedback.csv")
                except Exception as e:
                    print(f"Failed to push feedback to GitHub: {e}")
                
                if "all_feedback" not in st.session_state:
                    st.session_state["all_feedback"] = []
                st.session_state["all_feedback"].append(feedback.strip())
                st.success("Thank you for your feedback!")
            next_step()
            st.rerun()

    elif step == 8:
        if "results_calculated" not in st.session_state:

            phish_raw = float(st.session_state.get('spot_the_phish_score', 0))
            match_raw = float(st.session_state.get('password_match_score', 0))
            entropy_raw = float(st.session_state.get('last_entropy', 0))
            
            st.session_state.phish_normalized = min(200, get_phishing_score(phish_raw, 10))
            st.session_state.match_normalized = min(200, get_match_score(match_raw, 10))
            st.session_state.entropy_normalized = min(200, entropy_raw)
            
            st.session_state.final_score = (
                st.session_state.phish_normalized + 
                st.session_state.match_normalized + 
                st.session_state.entropy_normalized
            ) / 3
            
            st.session_state.phish_score = st.session_state.phish_normalized
            st.session_state.match_score = st.session_state.match_normalized
            st.session_state.final_entropy = st.session_state.entropy_normalized
            st.session_state.results_calculated = True
            
            security_score = (
                (st.session_state.phish_normalized * 0.4) +
                (st.session_state.match_normalized * 0.3) +
                (st.session_state.entropy_normalized * 0.3)
            )
            st.session_state.risk_score = 100 - (security_score / 2)
            
            fig, ax = plt.subplots(figsize=(5, 2.5))
            bars = [st.session_state.phish_normalized, 
                   st.session_state.match_normalized, 
                   st.session_state.entropy_normalized]
            labels = ["Phishing\nAwareness", "Password\nRecognition", "Password\nStrength"]
            ax.bar(labels, bars, color=["#4CAF50", "#2196F3", "#FF9800"])
            ax.set_ylim(0, 200)
            ax.set_yticks([0, 50, 100, 150, 200])
            ax.set_ylabel("Score", color='white')
            ax.set_title("Security Metrics", color='white', pad=10)
            ax.tick_params(colors='white')
            plt.xticks(rotation=0, ha='center')
            ax.set_facecolor('#2b2b2b')
            fig.patch.set_facecolor('#2b2b2b')
            plt.tight_layout()
            
            buf = BytesIO()
            plt.savefig(buf, format="png", facecolor='#2b2b2b', edgecolor='none')
            plt.close()
            st.session_state.graph = buf.getvalue()
            
            st.session_state.recommendations = get_personalized_recommendations(
                st.session_state.phish_normalized/20,
                st.session_state.match_normalized/20,
                st.session_state.entropy_normalized
            )

            if (st.session_state.get('user_authenticated', False) and 
                st.session_state.get('user_info') and 
                st.session_state.get('current_session_id') and
                st.session_state.get('selected_exam_type') and
                not st.session_state.get('scores_saved', False)):
                
                user_id = st.session_state.user_info['id']
                session_id = st.session_state.current_session_id
                exam_type = st.session_state.selected_exam_type
                
                db.save_user_scores(
                    user_id=user_id,
                    session_id=session_id,
                    exam_type=exam_type,
                    phishing_score=st.session_state.phish_normalized,
                    password_match_score=st.session_state.match_normalized,
                    password_strength_entropy=st.session_state.entropy_normalized,
                    overall_score=st.session_state.final_score
                )
                
                newly_awarded = db.check_and_award_badges(user_id)
                if newly_awarded:
                    st.session_state.new_badges = newly_awarded
                
                st.session_state.scores_saved = True
                st.session_state.sidebar_refresh = True
        
        st.markdown('<div class="step-title" style="margin-bottom:5px;">Thank you for completing CyberSmart!</div>', unsafe_allow_html=True)

        if st.session_state.get('new_badges'):
            st.success("🎉 Congratulations! You earned new badges!")
            badge_names = {
                'phish_hunter': '🎣 Phish Hunter',
                'password_pro': '🔐 Password Pro',
                'cyber_defender': '🛡️ Cyber Defender',
                'quick_learner': '⚡ Quick Learner',
                'perfect_score': '⭐ Perfect Score',
                'dedicated_student': '📚 Dedicated Student'
            }
            for badge_id in st.session_state.new_badges:
                if badge_id in badge_names:
                    st.info(f"**{badge_names[badge_id]}** unlocked!")
        
        st.markdown('<div class="section-heading" style="color: #ffffff; margin-top:10px;">Your Results</div>', unsafe_allow_html=True)
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        
        categories = ['Phishing\nAwareness', 'Password\nSkills', 'Password\nEntropy']
        values = [
            min(1.0, st.session_state.phish_normalized / 200),
            min(1.0, st.session_state.match_normalized / 200),
            min(1.0, st.session_state.entropy_normalized / 200)
        ]
        values += values[:1]
        
        angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False)
        angles = np.concatenate((angles, [angles[0]]))
        
        ax.plot(angles, values, 'o-', linewidth=2, color='#2E86C1')
        ax.fill(angles, values, alpha=0.25, color='#2E86C1')
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, size=10)
        ax.set_ylim(0, 1.0)
        ax.grid(True, alpha=0.3)
        plt.title("Security Skills Analysis", pad=20, size=12)
        
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=300)
        buf.seek(0)
        plt.close()
        
        st.markdown('<h3 style="font-size: 1.2em;">Score Breakdown</h3>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Phishing Awareness", 
                f"{st.session_state.phish_normalized:.0f}/200",
                help="Score based on phishing email identification"
            )
        with col2:
            st.metric(
                "Password Skills", 
                f"{st.session_state.match_normalized:.0f}/200",
                help="Score based on password strength assessment"
            )
        with col3:
            st.metric(
                "Password Entropy", 
                f"{st.session_state.entropy_normalized:.0f}/200",
                help="Score based on password complexity analysis"
            )
        
        st.markdown('<h3 style="font-size: 1.2em;">Skills Analysis</h3>', unsafe_allow_html=True)
        st.image(buf, use_container_width=True)

        security_score = (
            st.session_state.phish_normalized +
            st.session_state.match_normalized +
            st.session_state.entropy_normalized
        ) / 3

        risk_score = max(0, min(100, 100 - (security_score / 2)))
        
        if risk_score < 25:
            risk_level = "Low Risk"
            risk_color = "#4CAF50"
        elif risk_score < 50:
            risk_level = "Moderate Risk"
            risk_color = "#FFA500"
        else:
            risk_level = "High Risk"
            risk_color = "#FF0000"
        
        st.markdown('<h3 style="font-size: 1.2em;">Security Risk Assessment</h3>', unsafe_allow_html=True)
        st.markdown(
            f'<div style="text-align: center; padding: 10px; '
            f'background-color: {risk_color}10; border-radius: 8px; '
            f'margin: 10px 0; border: 1px solid {risk_color}30;">'
            f'<div style="color: {risk_color}; font-size: 1.3em; margin: 5px 0;">'
            f'Risk Score: {risk_score:.0f}%</div>'
            f'<div style="color: {risk_color}; font-size: 1.1em;">{risk_level}</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown('---')
        st.markdown('<div class="section-heading" style="color: #ffffff;">Statistics & Recommendations</div>', unsafe_allow_html=True)
    
        if st.session_state.risk_score < 20:
            cvss_category = "LOW"
            cvss_color = "#4CAF50"
        elif st.session_state.risk_score < 40:
            cvss_category = "MEDIUM"
            cvss_color = "#FFC107"
        elif st.session_state.risk_score < 60:
            cvss_category = "HIGH" 
            cvss_color = "#FF9800"
        else:
            cvss_category = "CRITICAL"
            cvss_color = "#F44336"

        st.markdown(f'<div style="color: {cvss_color}; font-size: 1.5em; font-weight: bold; margin: 10px 0;">CVSS Severity: {cvss_category}</div>', unsafe_allow_html=True)

        st.image(st.session_state.graph, use_container_width=True)

        st.markdown('\n<p style="color: #ffffff; font-weight: bold; font-size: 1.2em;">Personalized Recommendations:</p>', unsafe_allow_html=True)

        for rec in st.session_state.recommendations:
            st.markdown(f'<p style="color: #ffffff; margin: 0.5em 0;">• {rec}</p>', unsafe_allow_html=True)

        st.markdown('---')
        st.markdown('<div class="section-heading" style="color: #ffffff;">User Feedback </div>', unsafe_allow_html=True)
        
        feedbacks = []
        try:
            with open("reports/feedback.csv", "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if len(row) >= 2:
                        timestamp, feedback_text = row[0], row[1]
                        feedbacks.append(f"**[{timestamp}]**\n\n{feedback_text}")
        except FileNotFoundError:
            pass

        if feedbacks:
            with st.expander("View all feedback", expanded=False):
                for feedback in feedbacks:
                    st.markdown(feedback)
                    st.markdown("---")
        else:
            st.info("No feedback yet. Be the first to leave a review!")

        if (st.session_state.get('user_authenticated', False) and 
            st.session_state.get('user_info')):
            with st.expander("📊 Your Assessment History", expanded=False):
                show_score_history()

        st.markdown('---')
        st.markdown('<div class="section-heading" style="color: #ffffff;">Thank you for participating!</div>', unsafe_allow_html=True)
        
        with st.form("return_form"):
            if st.form_submit_button("Return to Main Menu", use_container_width=True):
                keys_to_keep = ['user_authenticated', 'user_info', 'auth_tab']
                session_backup = {key: st.session_state.get(key) for key in keys_to_keep}
                
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                
                for key, value in session_backup.items():
                    if value is not None:
                        st.session_state[key] = value
                
                st.session_state.step = 1
                st.rerun()