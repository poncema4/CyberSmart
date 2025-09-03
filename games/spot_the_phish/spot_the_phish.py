import streamlit as st

def spot_the_phish():
    st.header("Spot the Phish")
    st.write("Can you spot the phishing email? Select the correct answer for each question, then submit all at once.")

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
                "This is the legitimate bank website.",
                "Phishing sites often use similar names with subtle changes.",
                "This is a legitimate UK bank domain."
            ]
        },
        {
            "question": "Which subject line is suspicious?",
            "options": [
                "Invoice Attached",
                "Urgent: Account Locked!",
                "Team Lunch Tomorrow"
            ],
            "answer": 1,
            "explanations": [
                "Invoices are common, but not always phishing.",
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
                "Phishing emails use addresses that look similar but are fake.",
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
                "Word documents are common, but be cautious."
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
                "Normal sign-off for IT support.",
                "Security teams use professional sign-offs.",
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
                "Phishing emails may use fake numbers."
            ]
        },
        {
            "question": "Which request is suspicious?",
            "options": [
                "Send us your account number.",
                "Confirm your attendance.",
                "Review the attached agenda."
            ],
            "answer": 0,
            "explanations": [
                "Phishing emails often ask for sensitive information.",
                "Normal event confirmation.",
                "Common work request."
            ]
        }
    ]

    user_answers = []
    for idx, q in enumerate(questions):
        st.write(f"**Q{idx+1}: {q['question']}**")
        choice = st.radio("", q["options"], key=f"phish_{idx}")
        user_answers.append(choice)

    if st.button("Submit Answers"):
        score = 0
        for idx, q in enumerate(questions):
            selected = user_answers[idx]
            correct_idx = q["answer"]
            selected_idx = q["options"].index(selected)
            if selected_idx == correct_idx:
                st.success(f"Q{idx+1}: Correct!")
                score += 1
            else:
                st.error(f"Q{idx+1}: Incorrect. {q['explanations'][selected_idx]}")
        st.info(f"Your score: {score}/{len(questions)}")
