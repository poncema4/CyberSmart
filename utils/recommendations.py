import random

def get_personalized_recommendations(phish_score, match_score, entropy):
    recommendations = []
    
    # Phishing awareness recommendations
    phish_recommendations = [
        "Review common phishing indicators like suspicious sender addresses and urgent requests",
        "Always verify unexpected requests through official channels",
        "Enable two-factor authentication on all your accounts",
        "Be cautious of links in emails, even from known senders",
        "Check for spelling errors and poor grammar in emails",
        "Hover over links to preview URLs before clicking",
        "Never share sensitive information via email"
    ]
    
    # Password strength recommendations
    password_recommendations = [
        "Use different passwords for each account",
        "Consider using a password manager",
        "Create memorable passphrases instead of complex passwords",
        "Regularly update your passwords",
        "Enable biometric authentication when available",
        "Avoid using personal information in passwords",
        "Add random numbers and symbols to strengthen passwords"
    ]
    
    # Add targeted recommendations based on scores (now using 0-200 scale)
    if phish_score < 120:  # Less than 60%
        recommendations.extend(random.sample(phish_recommendations, 2))
    elif phish_score < 160:  # Less than 80%
        recommendations.append(random.choice(phish_recommendations))
        
    if match_score < 120:  # Less than 60%
        recommendations.extend(random.sample(password_recommendations, 2))
    elif match_score < 160:  # Less than 80%
        recommendations.append(random.choice(password_recommendations))
    
    # Entropy-based recommendations (entropy is already 0-200)
    if entropy < 80:
        recommendations.append("Critical: Your passwords are extremely weak. Start using longer passwords with a mix of characters.")
    elif entropy < 120:
        recommendations.append("Your passwords need improvement. Use longer passwords with more variety.")
    elif entropy < 160:
        recommendations.append("Consider adding more complexity to your passwords for better security.")
    
    # Ensure we have at least 3 recommendations
    if len(recommendations) < 3:
        available_recs = phish_recommendations + password_recommendations
        recommendations.extend(random.sample([r for r in available_recs if r not in recommendations], 3 - len(recommendations)))
    
    return recommendations[:5]  # Return top 5 recommendations