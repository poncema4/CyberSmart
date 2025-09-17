import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt
from utils.github_push import push_to_github
from utils.ml_scoring import get_password_score, get_phishing_score, get_match_score
from games.spot_the_phish.spot_the_phish import spot_the_phish
from games.password_match.password_match import password_match
from games.password_generator.password_generator import password_generator
from games.password_strength.password_strength import password_strength

STEPS = [
    "intro",
    "spot_the_phish",
    "password_match",
    "password_generator",
    "password_strength",
    "feedback",
    "results"
]

def run_step_flow():
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

    def next_step():
        st.session_state.step = step + 1

    if step == 0:
        st.markdown('<div class="step-title">Welcome to CyberSmart!</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-desc">CyberSmart is an interactive cybersecurity course. You will go through a series of activities and games to learn and test your knowledge. Click Start to begin!</div>', unsafe_allow_html=True)
        with st.form("start_form"):
            if st.form_submit_button("Start"):
                next_step()
                st.rerun()

    elif step == 1:
        st.markdown('<div class="step-title">Step 1: Spot the Phish</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-desc">Identify phishing attempts. You have <b>one attempt</b>. Your score will be recorded.</div>', unsafe_allow_html=True)
        if "spot_the_phish_score" not in st.session_state:
            score = spot_the_phish()
            if score is not None:
                st.success("Response recorded!")
                with st.form("phish_next_form"):
                    if st.form_submit_button("Continue"):
                        next_step()
                        st.rerun()
        else:
            st.success("Step completed!")
            with st.form("phish_continue_form"):
                if st.form_submit_button("Continue"):
                    next_step()
                    st.rerun()

    elif step == 2:
        st.markdown('<div class="step-title">Step 2: Password Match</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-desc">Classify passwords as strong or weak. <b>One attempt only.</b> Your score will be recorded.</div>', unsafe_allow_html=True)
        if "password_match_score" not in st.session_state:
            score = password_match()
            if score is not None:
                st.success("Response recorded!")
                with st.form("match_next_form"):
                    if st.form_submit_button("Continue"):
                        next_step()
                        st.rerun()
        else:
            st.success("Step completed!")
            with st.form("match_continue_form"):
                if st.form_submit_button("Continue"):
                    next_step()
                    st.rerun()

    elif step == 3:
        st.markdown('<div class="step-title">Step 3: Password Generator</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-desc">Experiment with generating strong passwords. When you are ready, click Next.</div>', unsafe_allow_html=True)
        password_generator()
        with st.form("gen_next_form"):
            if st.form_submit_button("Continue"):
                next_step()
                st.rerun()

    elif step == 4:
        st.markdown('<div class="step-title">Step 4: Password Strength Checker</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-desc">Test the strength of your own passwords. When finished, click Next.</div>', unsafe_allow_html=True)
        password_strength()
        # Only show continue button after a valid password check
        if st.session_state.get("password_strength_attempted", False) and st.session_state.get("last_strength", None):
            with st.form("strength_next_form"):
                if st.form_submit_button("Continue"):
                    next_step()
                    st.rerun()

    elif step == 5:
        st.markdown('<div class="step-title">Step 5: Feedback</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-desc">Please provide feedback on your experience (max 500 characters).</div>', unsafe_allow_html=True)
        
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
                # Save feedback locally
                with open("reports/feedback.txt", "a", encoding="utf-8") as f:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{timestamp}] {feedback.strip()}\n-------------------\n")
                
                # Push to GitHub
                try:
                    push_to_github("reports/feedback.txt")
                except Exception as e:
                    print(f"Failed to push feedback to GitHub: {e}")
                
                if "all_feedback" not in st.session_state:
                    st.session_state["all_feedback"] = []
                st.session_state["all_feedback"].append(feedback.strip())
                st.success("Thank you for your feedback!")
            next_step()
            st.rerun()

    elif step == 6:
        if "results_calculated" not in st.session_state:
            # Calculate scores once and store in session state
            st.session_state.phish_score = st.session_state.get('spot_the_phish_score', 0) * 20
            st.session_state.match_score = st.session_state.get('password_match_score', 0) * 20
            st.session_state.final_entropy = st.session_state.get('last_entropy', 0)
            st.session_state.results_calculated = True
            
            # Pre-calculate other metrics
            security_score = (
                (st.session_state.phish_score * 0.4) +
                (st.session_state.match_score * 0.3) +
                (min(200, st.session_state.final_entropy) * 0.3)
            )
            st.session_state.risk_score = 100 - (security_score / 2)
            
            # Get recommendations once
            from utils.recommendations import get_personalized_recommendations
            st.session_state.recommendations = get_personalized_recommendations(
                st.session_state.phish_score/20,
                st.session_state.match_score/20,
                st.session_state.final_entropy
            )
            
            # Create and store the graph
            fig, ax = plt.subplots(figsize=(5,2.5))
            bars = [st.session_state.phish_score, 
                   st.session_state.match_score, 
                   min(200, st.session_state.final_entropy)]
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
            st.session_state.graph = buf.getvalue()
        
        st.markdown('<div class="step-title">Thank you for completing CyberSmart!</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="section-heading" style="color: #ffffff;">Your Results</div>', unsafe_allow_html=True)
        
        # Display metrics in 3 columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Phishing Awareness", f"{st.session_state.phish_score}/200")
        with col2:
            st.metric("Password Recognition", f"{st.session_state.match_score}/200")
        with col3:
            scaled_entropy = min(200, st.session_state.final_entropy)
            st.metric("Password Entropy", f"{scaled_entropy:.0f}/200")
        
        st.markdown('<div style="color: #ffffff; font-size: 1.8em; font-weight: bold; margin: 10px 0;">Cybersecurity Risk Score: {:.0f}%</div>'.format(st.session_state.risk_score), unsafe_allow_html=True)

        st.markdown('---')
        st.markdown('<div class="section-heading" style="color: #ffffff;">Statistics & Recommendations</div>', unsafe_allow_html=True)

        # Map risk score to CVSS categories
        if st.session_state.risk_score < 20:
            cvss_category = "LOW"
            cvss_color = "#4CAF50"  # Material green
        elif st.session_state.risk_score < 40:
            cvss_category = "MEDIUM"
            cvss_color = "#FFC107"  # Material amber
        elif st.session_state.risk_score < 60:
            cvss_category = "HIGH" 
            cvss_color = "#FF9800"  # Material orange
        else:
            cvss_category = "CRITICAL"
            cvss_color = "#F44336"  # Material red

        st.markdown(f'<div style="color: {cvss_color}; font-size: 1.5em; font-weight: bold; margin: 10px 0;">CVSS Severity: {cvss_category}</div>', unsafe_allow_html=True)

        # Display the pre-generated graph
        st.image(st.session_state.graph, use_container_width=True)

        # --- Personalized Recommendations ---
        st.markdown('\n<p style="color: #ffffff; font-weight: bold; font-size: 1.2em;">Personalized Recommendations:</p>', unsafe_allow_html=True)
        
        # Display pre-calculated recommendations
        for rec in st.session_state.recommendations:
            st.markdown(f'<p style="color: #ffffff; margin: 0.5em 0;">• {rec}</p>', unsafe_allow_html=True)

        st.markdown('---')
        st.markdown('<div class="section-heading" style="color: #ffffff;">User Feedback </div>', unsafe_allow_html=True)
        
        # Load all feedback from file for persistent display
        feedbacks = []
        try:
            with open("reports/feedback.txt", "r", encoding="utf-8") as f:
                content = f.read()
                feedbacks = [fb for fb in content.split("-------------------\n") if fb.strip()]
        except FileNotFoundError:
            pass

        if feedbacks:
            with st.expander("View all feedback", expanded=True):
                st.markdown(
                    '<div style="background-color: white; padding: 15px; border-radius: 5px; max-height: 300px; overflow-y: auto; color: black;">'
                    + '<hr style="margin: 10px 0; border-top: 1px solid #e0e0e0;">'.join([f"{f}" for f in feedbacks])
                    + '</div>',
                    unsafe_allow_html=True
                )
        else:
            st.info("No feedback yet. Be the first to leave a review!")

        st.markdown('---')
        st.markdown('<div class="section-heading" style="color: #ffffff;">Thank you for participating!</div>', unsafe_allow_html=True)
        
        # Return to main menu button at the bottom
        with st.form("return_form"):
            if st.form_submit_button("Return to Main Menu", use_container_width=True):
                # Reset all session state variables
                for key in list(st.session_state.keys()):
                    if key != "step":  # Keep step until after rerun
                        del st.session_state[key]
                st.session_state.step = 0
                st.rerun()