import streamlit as st
import random

def spot_the_phish():
    st.header("Spot the Phish")
    st.write("""
        Can you spot the phishing email? Select the correct answer for each question and see how good you are at spotting phishing vulnerabilities!
    """)

    questions = [
        {
            "question": "Which email is most likely a phishing attempt?",
            "options": [
                "Your bank: 'Please verify your account by clicking this secure link.'",
                "Your friend: 'Check out these vacation photos!'",
                "Your employer: 'Meeting rescheduled to 3pm.'"
            ],
            "answer": 0,
            "explanations": [
                "Phishing emails often ask you to click a link to verify your account.",
                "Personal emails from friends are less likely to be phishing.",
                "Work emails about meetings are usually safe."
            ]
        },
        {
            "question": "Which link should you avoid clicking?",
            "options": [
                "www.yourbank.com",
                "www.y0urbank-secure.com",
                "www.yourbank.co.uk"
            ],
            "answer": 1,
            "explanations": [
                "This would be a legitimate bank website.",
                "Phishing sites often use similar names with some small changes.",
                "This is a legitimate UK bank domain."
            ]
        },
        {
            "question": "Which subject line is suspicious?",
            "options": [
                "Invoice Attached",
                "Urgent: Your Account Is Locked!",
                "Team Lunch Tomorrow"
            ],
            "answer": 1,
            "explanations": [
                "Invoices are common, but not always phishing, always check your sender id.",
                "Phishing emails often use urgency to trick you.",
                "Normal work-related subjects are usually safe."
            ]
        },
        {
            "question": "Which sender address is likely fake?",
            "options": [
                "support@yourbank.com",
                "support@yourbank-security.com",
                "support@yourbank.co.uk"
            ],
            "answer": 1,
            "explanations": [
                "This is a legitimate address.",
                "Phishing emails use addresses that look similar but are fake and try their best to make their sender id seem legitimate.",
                "This is a legitimate UK address."
            ]
        },
        {
            "question": "Which greeting is suspicious?",
            "options": [
                "Dear Customer",
                "Hi John",
                "Hello Team"
            ],
            "answer": 0,
            "explanations": [
                "Phishing emails often use generic greetings.",
                "Personalized greetings are less likely to be phishing.",
                "Group greetings are common in work emails."
            ]
        },
        {
            "question": "Which attachment should you avoid?",
            "options": [
                "report.pdf",
                "invoice.exe",
                "agenda.docx"
            ],
            "answer": 1,
            "explanations": [
                "PDFs are usually safe.",
                "Executable files (.exe) can contain malware.",
                "Word documents are common, but be cautious if they ask for login or a verification process."
            ]
        },
        {
            "question": "Which message is a red flag?",
            "options": [
                "Please update your password.",
                "Click here to claim your prize!",
                "Your subscription is expiring soon."
            ],
            "answer": 1,
            "explanations": [
                "Password updates are normal, but verify the source.",
                "Phishing emails often promise prizes.",
                "Subscription reminders are common, but check the sender."
            ]
        },
        {
            "question": "Which sign-off is suspicious?",
            "options": [
                "Best regards, IT Support",
                "Sincerely, YourBank Security Team",
                "Yours truly, Prize Department"
            ],
            "answer": 2,
            "explanations": [
                "Normal sign off for IT support.",
                "Security teams use professional sign offs.",
                "Phishing emails often use fake departments."
            ]
        },
        {
            "question": "Which phone number should you avoid?",
            "options": [
                "1-800-YOURBANK",
                "1-800-123-4567",
                "Call us at 555-FAKE-NUM"
            ],
            "answer": 2,
            "explanations": [
                "Legitimate bank number.",
                "Generic support number.",
                "Phishing emails may use fake numbers and promote their audience to call them immediately for a 'deal'."
            ]
        },
        {
            "question": "Which request is suspicious?",
            "options": [
                "Send us your account number.",
                "Please confirm your attendance.",
                "Review the attached agenda."
            ],
            "answer": 0,
            "explanations": [
                "Phishing emails often ask for sensitive information.",
                "Normal event confirmation, be cautious and make sure you even registered to this event in the first place.",
                "Common work request, just double check the sender."
            ]
        }
    ]

    if "phish_attempted" in st.session_state:
        st.success(f"You have already submitted. Your score: {st.session_state['spot_the_phish_score']} / {len(questions)}")
        return st.session_state['spot_the_phish_score']

    if "phish_answers" not in st.session_state:
        st.session_state.phish_answers = {}
    if "phish_order" not in st.session_state:
        st.session_state.phish_order = random.sample(range(len(questions)), len(questions))
    question_order = st.session_state.phish_order

    for idx, q in enumerate(question_order, start=1):
        question = questions[q]
        st.write(f"**Q{idx}: {question['question']}**")
        st.session_state.phish_answers[q] = st.radio(
            "", question["options"], key=f"phish_{q}"
        )

    if st.button("Check Results", key="phish_submit"):
        score = 0
        user_answers = {}
        for idx, q in enumerate(question_order, start=1):
            question = questions[q]
            selected = st.session_state.phish_answers[q]
            selected_index = question["options"].index(selected)
            user_answers[q] = selected_index
            if selected_index == question["answer"]:
                st.success(f"✔ Q{idx}")
                score += 1
            else:
                st.error(f"✘ Q{idx}: {question['explanations'][selected_index]}")
        st.session_state['spot_the_phish_score'] = score
        st.session_state['phish_attempted'] = True
        st.session_state['phish_user_answers'] = user_answers
        st.info(f"Your score: {score}/{len(questions)}")
        return score

    return None