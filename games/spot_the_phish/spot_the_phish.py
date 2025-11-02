import streamlit as st
import random
import time
from utils.db import db

def spot_the_phish() -> int | None:
    st.header("Spot the Phish")
    st.write("""
        Can you spot the phishing email? Select the correct answer for each question and see how good you are at spotting phishing vulnerabilities!
    """)

    assessment_type = st.session_state.get('selected_exam_type', 'practice')
    user_id = st.session_state.get('user_info', {}).get('id')
    
    if 'question_start_times' not in st.session_state:
        st.session_state.question_start_times = {}
    
    pre_questions = [
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
            "question": "Which request is suspicious?",
            "options": [
                "Send us your account number.",
                "Please confirm your attendance.",
                "Review the attached agenda."
            ],
            "answer": 0,
            "explanations": [
                "Phishing emails often ask for sensitive information.",
                "Normal event confirmation, but always verify.",
                "Common work request, just double check the sender."
            ]
        },
        {
            "question": "Which email sign-off is suspicious?",
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
            "question": "Which subject line is suspicious?",
            "options": [
                "Invoice Attached",
                "Urgent: Your Account Is Locked!",
                "Team Lunch Tomorrow"
            ],
            "answer": 1,
            "explanations": [
                "Invoices are common, but always check the sender.",
                "Phishing emails often use urgency to trick you.",
                "Normal work-related subjects are usually safe."
            ]
        },
        {
            "question": "Which email sender should you trust?",
            "options": [
                "noreply@bank-security.net",
                "support@yourbank.com",
                "security@yourbank-alert.org"
            ],
            "answer": 1,
            "explanations": [
                "Suspicious domain with 'security' added.",
                "This is the legitimate bank domain.",
                "Suspicious domain trying to look official."
            ]
        },
        {
            "question": "What should you do with unexpected prize emails?",
            "options": [
                "Click the link to see what you won",
                "Delete the email immediately",
                "Forward it to friends"
            ],
            "answer": 1,
            "explanations": [
                "Never click links in unexpected prize emails.",
                "Delete suspicious emails to avoid phishing attempts.",
                "Don't spread potential phishing emails."
            ]
        },
        {
            "question": "Which phone request is suspicious?",
            "options": [
                "1-800-YOURBANK (official bank number)",
                "Call 555-URGENT for immediate account help",
                "Contact us at our main office number"
            ],
            "answer": 1,
            "explanations": [
                "Official bank numbers are legitimate.",
                "Phishing emails often use urgent phone tactics.",
                "Main office numbers are typically legitimate."
            ]
        },
        {
            "question": "Which email looks most legitimate?",
            "options": [
                "From: security@gmail.com (Your account needs verification)",
                "From: alerts@yourbank.com (Monthly statement available)",
                "From: winner@freemoney.com (You've won $1000!)"
            ],
            "answer": 1,
            "explanations": [
                "Generic email domains are suspicious for bank communications.",
                "Legitimate bank communications come from official domains.",
                "Obviously suspicious prize offers are phishing attempts."
            ]
        },
        {
            "question": "What's the biggest red flag in an email?",
            "options": [
                "Asking for your password or PIN",
                "Having your name in the greeting",
                "Being sent during business hours"
            ],
            "answer": 0,
            "explanations": [
                "Legitimate companies never ask for passwords via email.",
                "Having your name is actually a good sign.",
                "Business hours timing is normal."
            ]
        }
    ]
    
    practice_questions = [
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
                "Phishing sites often use similar names with character substitutions.",
                "This is a legitimate UK bank domain."
            ]
        },
        {
            "question": "Which email pattern indicates phishing?",
            "options": [
                "Personalized greeting with your full name",
                "Generic greeting and urgent action required",
                "Professional signature with contact info"
            ],
            "answer": 1,
            "explanations": [
                "Personalized greetings suggest legitimate communication.",
                "Generic greetings + urgency are classic phishing tactics.",
                "Professional signatures are signs of legitimate emails."
            ]
        },
        {
            "question": "Which URL structure is most suspicious?",
            "options": [
                "https://secure.yourbank.com/login",
                "http://yourbank.security-check.net/verify",
                "https://online.yourbank.com/account"
            ],
            "answer": 1,
            "explanations": [
                "Legitimate bank subdomain with HTTPS.",
                "Suspicious domain with bank name embedded in larger domain.",
                "Standard online banking URL with HTTPS."
            ]
        },
        {
            "question": "What makes this email suspicious: 'Dear Valued Customer, We have noticed unusual activity. Click here within 24 hours or account will be closed.'?",
            "options": [
                "It uses HTTPS links",
                "It combines generic greeting, urgency, and threats",
                "It mentions account activity"
            ],
            "answer": 1,
            "explanations": [
                "HTTPS doesn't guarantee legitimacy of the email content.",
                "Multiple phishing tactics combined make this highly suspicious.",
                "Legitimate banks do monitor activity, but not with threats."
            ]
        },
        {
            "question": "Which attachment type combination is most dangerous?",
            "options": [
                "invoice.pdf and receipt.pdf",
                "document.exe and update.bat",
                "photo.jpg and video.mp4"
            ],
            "answer": 1,
            "explanations": [
                "PDF files are generally safe.",
                "Executable files (.exe, .bat) can contain malware.",
                "Image and video files are typically safe."
            ]
        },
        {
            "question": "Which sender address uses a common phishing technique?",
            "options": [
                "support@yourbank.com",
                "support@yourbank-security.com",
                "customercare@yourbank.com"
            ],
            "answer": 1,
            "explanations": [
                "This is a legitimate bank domain.",
                "Adding security-related words to create fake legitimacy.",
                "This is a legitimate customer service domain."
            ]
        },
        {
            "question": "What's suspicious about: 'Congratulations! You've been selected for our exclusive offer. Limited time only - respond now!'?",
            "options": [
                "It's too enthusiastic",
                "It uses pressure tactics and exclusivity claims",
                "It mentions an offer"
            ],
            "answer": 1,
            "explanations": [
                "Enthusiasm alone isn't suspicious.",
                "Combining pressure, exclusivity, and urgency are phishing tactics.",
                "Legitimate companies also send offers."
            ]
        },
        {
            "question": "Which email timing pattern suggests automation/phishing?",
            "options": [
                "Sent during normal business hours",
                "Sent at exactly 12:00 AM with urgent requests",
                "Sent on weekdays"
            ],
            "answer": 1,
            "explanations": [
                "Business hours timing is normal.",
                "Automated phishing often sends at exact times with urgency.",
                "Weekday timing is normal for business emails."
            ]
        },
        {
            "question": "Which grammar pattern is a phishing indicator?",
            "options": [
                "Perfect grammar and spelling",
                "Multiple urgent punctuation marks and poor grammar",
                "Standard business language"
            ],
            "answer": 1,
            "explanations": [
                "Good grammar suggests legitimate communication.",
                "Poor grammar and excessive punctuation indicate phishing.",
                "Standard business language is normal."
            ]
        },
        {
            "question": "What makes this request suspicious: 'Please confirm your identity by replying with your full name, DOB, and last 4 digits of SSN'?",
            "options": [
                "It asks for name confirmation",
                "It requests multiple pieces of sensitive information via email",
                "It uses the word 'confirm'"
            ],
            "answer": 1,
            "explanations": [
                "Name confirmation alone isn't suspicious.",
                "Legitimate companies never request sensitive info via email.",
                "The word 'confirm' is commonly used legitimately."
            ]
        },
        {
            "question": "Which email header detail is most concerning?",
            "options": [
                "From: YourBank <support@yourbank.com>",
                "From: YourBank <noreply@not-yourbank.net>",
                "From: Customer Service <help@yourbank.com>"
            ],
            "answer": 1,
            "explanations": [
                "Legitimate bank name and domain match.",
                "Display name doesn't match the actual domain.",
                "Legitimate customer service email format."
            ]
        },
        {
            "question": "Which call-to-action is most suspicious?",
            "options": [
                "View your monthly statement online",
                "URGENT: Verify now or lose access forever!",
                "Update your contact preferences"
            ],
            "answer": 1,
            "explanations": [
                "Normal banking service request.",
                "Combines urgency, threats, and permanent consequences.",
                "Standard account management request."
            ]
        }
    ]
    
    post_questions = [
        {
            "question": "Which subtle domain spoofing technique is being used in 'www.goog1e.com'?",
            "options": [
                "Subdomain spoofing",
                "Character substitution (homograph attack)",
                "Domain shadowing"
            ],
            "answer": 1,
            "explanations": [
                "This isn't using subdomains to confuse.",
                "Using '1' instead of 'l' is a character substitution attack.",
                "Domain shadowing involves compromised legitimate domains."
            ]
        },
        {
            "question": "What advanced technique is shown in: 'From: security@bank.com <attacker@evil.com>'?",
            "options": [
                "Email spoofing with display name manipulation",
                "Domain typosquatting",
                "Subdomain hijacking"
            ],
            "answer": 0,
            "explanations": [
                "Display name shows legitimate bank but actual sender is malicious.",
                "Typosquatting involves similar but different domain names.",
                "Subdomain hijacking involves compromising legitimate subdomains."
            ]
        },
        {
            "question": "Which URL redirection technique is most dangerous: 'https://bit.ly/urgentbankupdate'?",
            "options": [
                "Open redirects on trusted domains",
                "URL shortening to hide destination",
                "Deep linking manipulation"
            ],
            "answer": 1,
            "explanations": [
                "Open redirects are dangerous but this isn't that specific technique.",
                "URL shorteners hide the true destination, making verification impossible.",
                "Deep linking isn't the primary concern here."
            ]
        },
        {
            "question": "What makes this social engineering attempt sophisticated: 'Hi John, your colleague Sarah mentioned you handle IT security. I'm from your bank's new cyber team and need to verify your department's security protocols.'?",
            "options": [
                "Uses generic social proof",
                "Combines personalization, false authority, and pretexting",
                "Simple impersonation attempt"
            ],
            "answer": 1,
            "explanations": [
                "This goes beyond generic social proof.",
                "Uses personal name, references colleague, claims authority, creates false scenario.",
                "This is much more sophisticated than simple impersonation."
            ]
        },
        {
            "question": "Which psychological manipulation is used in: 'CONFIDENTIAL: Internal security audit found vulnerabilities in your account. Immediate action required - do not discuss with others.'?",
            "options": [
                "Simple urgency tactics",
                "Combining authority, urgency, and secrecy to prevent verification",
                "Basic fear appeals"
            ],
            "answer": 1,
            "explanations": [
                "This goes beyond simple urgency.",
                "Uses fake authority, urgency, and secrecy to prevent victim from checking with others.",
                "This is more sophisticated than basic fear tactics."
            ]
        },
        {
            "question": "What advanced header spoofing technique is indicated by 'Return-Path: <bounce@legitimate-bank.com>' but 'From: security@different-domain.com'?",
            "options": [
                "Simple email spoofing",
                "Return-path manipulation with mixed signals",
                "Standard forwarding"
            ],
            "answer": 1,
            "explanations": [
                "This is more complex than simple spoofing.",
                "Mismatched return-path and from headers create confusing legitimacy signals.",
                "This isn't standard email forwarding."
            ]
        },
        {
            "question": "Which attack vector is demonstrated by: 'Your security certificate expires today. Download the updated certificate from: https://securityupdate-yourbank.net/cert.exe'?",
            "options": [
                "Simple malware distribution",
                "Combining urgency, technical intimidation, and malware delivery",
                "Basic phishing attempt"
            ],
            "answer": 1,
            "explanations": [
                "This is more sophisticated than simple malware distribution.",
                "Uses technical terms to intimidate, urgency, and delivers executable malware.",
                "This goes beyond basic phishing to advanced technical deception."
            ]
        },
        {
            "question": "What makes this business email compromise (BEC) sophisticated: 'From: CEO <ceo@company.com> Subject: Urgent wire transfer - confidential acquisition'?",
            "options": [
                "Uses executive impersonation",
                "Combines authority impersonation with financial urgency and confidentiality",
                "Simple CEO fraud"
            ],
            "answer": 1,
            "explanations": [
                "This is more than just executive impersonation.",
                "Uses CEO authority, financial request, urgency, and secrecy to prevent verification.",
                "This is advanced BEC, not simple CEO fraud."
            ]
        },
        {
            "question": "Which evasion technique is used in: 'V3r1fy y0ur 4cc0unt 1mm3d14t3ly t0 pr3v3nt susp3ns10n'?",
            "options": [
                "Character encoding obfuscation",
                "Leetspeak to evade text-based filters",
                "Language translation errors"
            ],
            "answer": 1,
            "explanations": [
                "This isn't using special character encoding.",
                "Using numbers for letters (leetspeak) to bypass automated detection.",
                "This is intentional obfuscation, not translation errors."
            ]
        },
        {
            "question": "What advanced technique is shown in: 'This email appears to be from yourbank.com but the DKIM signature is from malicious-domain.net'?",
            "options": [
                "DKIM signature spoofing",
                "Email authentication bypass with signature mismatch",
                "Simple domain spoofing"
            ],
            "answer": 1,
            "explanations": [
                "This shows a mismatch rather than spoofing the signature itself.",
                "The email appears legitimate but authentication signatures reveal the true source.",
                "This is more sophisticated than simple domain spoofing."
            ]
        },
        {
            "question": "Which multi-stage attack is indicated by: 'Please verify your account at this secure portal' followed by a legitimate-looking login page that harvests credentials?",
            "options": [
                "Simple credential theft",
                "Sophisticated credential harvesting with convincing fake portals",
                "Basic password phishing"
            ],
            "answer": 1,
            "explanations": [
                "This is more elaborate than simple credential theft.",
                "Creates convincing fake login portals that closely mimic legitimate sites.",
                "This goes beyond basic password phishing to sophisticated web-based harvesting."
            ]
        },
        {
            "question": "What makes this supply chain attack email dangerous: 'From: TrustedVendor <vendor@legitimate-company.com> Your software update is ready for download'?",
            "options": [
                "Compromised legitimate vendor account used for distribution",
                "Simple vendor impersonation",
                "Basic software update fraud"
            ],
            "answer": 0,
            "explanations": [
                "The legitimate vendor's email system has been compromised to send malicious updates.",
                "This appears to actually be from the legitimate vendor.",
                "This is a sophisticated supply chain compromise, not simple fraud."
            ]
        }
    ]
    
    if assessment_type == 'pre':
        question_pool = pre_questions
    elif assessment_type == 'post':
        question_pool = post_questions
        if user_id:
            weak_areas = db.get_user_weak_areas(user_id)
            if weak_areas['phishing']['is_weak'] or weak_areas['phishing']['is_slow']:
                st.info("Adaptive Learning: Extra challenging phishing questions added based on your pre-assessment performance!")
    else:
        question_pool = practice_questions
        if user_id:
            weak_areas = db.get_user_weak_areas(user_id)
            if weak_areas['phishing']['is_weak']:
                st.info("Practice Mode: Focus on phishing - your pre-assessment showed this needs improvement!")
            if weak_areas['phishing']['is_slow']:
                st.info("Practice Mode: Try to answer faster - tracking your response time for improvement!")
    
    if "selected_questions" not in st.session_state or st.session_state.get('current_assessment_type') != assessment_type:
        st.session_state.selected_questions = random.sample(question_pool, 10)
        st.session_state.current_assessment_type = assessment_type
        st.session_state.question_start_times = {}
        for i in range(10):
            st.session_state.question_start_times[i] = time.time()
    
    questions = st.session_state.selected_questions

    if "phish_attempted" in st.session_state:
        st.success(f"You have already submitted. Your score: {st.session_state['spot_the_phish_score']} / 10")
        return st.session_state['spot_the_phish_score']

    if "phish_answers" not in st.session_state:
        st.session_state.phish_answers = {}

    if "phish_order" not in st.session_state:
        st.session_state.phish_order = list(range(10))
        
    question_order = st.session_state.phish_order

    current_time = time.time()
    for idx, q in enumerate(question_order, start=1):
        question = questions[q]

        if q not in st.session_state.question_start_times:
            st.session_state.question_start_times[q] = current_time
        
        st.write(f"**Q{idx}: {question['question']}**")

        previous_answer = st.session_state.phish_answers.get(q)
        st.session_state.phish_answers[q] = st.radio(
            "", question["options"], key=f"phish_{q}"
        )

        if previous_answer != st.session_state.phish_answers[q]:
            st.session_state.question_start_times[q] = time.time()

    if st.button("Check Results", key="phish_submit"):
        score = 0
        user_answers = {}
        session_id = st.session_state.get('session_id', 'unknown')
        
        end_time = time.time()
        
        for idx, q in enumerate(question_order, start=1):
            question = questions[q]
            selected = st.session_state.phish_answers[q]
            selected_index = question["options"].index(selected)
            user_answers[q] = selected_index

            start_time = st.session_state.question_start_times.get(q, end_time)
            response_time = end_time - start_time
            
            is_correct = selected_index == question["answer"]
            if is_correct:
                st.success(f"✔ Q{idx} (took {response_time:.1f}s)")
                score += 1
            else:
                st.error(f"✘ Q{idx}: {question['explanations'][selected_index]} (took {response_time:.1f}s)")

            if user_id and session_id:
                question_id = f"phish_{hash(question['question']) % 10000}"
                db.save_performance_metric(
                    user_id=user_id,
                    session_id=session_id,
                    exam_type=assessment_type,
                    game_type='phishing',
                    question_id=question_id,
                    is_correct=is_correct,
                    response_time=response_time
                )
        
        st.session_state['spot_the_phish_score'] = score
        st.session_state['phish_attempted'] = True
        st.session_state['phish_user_answers'] = user_answers
        
        avg_time = sum(end_time - st.session_state.question_start_times.get(q, end_time) 
                       for q in question_order) / len(question_order)
        st.info(f"Your score: {score}/10 | Average response time: {avg_time:.1f}s per question")
        
        return score

    return None