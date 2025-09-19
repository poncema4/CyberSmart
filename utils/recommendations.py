import random
from typing import List

def get_personalized_recommendations(phish_score: float, match_score: float, entropy: float) -> List:
    """
    Generate personalized recommendations based on phishing awareness, password strenght, and
    password entropy scores
    """
    recommendations = []
    
    phish_recommendations = [
        "Review common phishing indicators like suspicious sender addresses and urgent requests",
        "Always verify unexpected requests through official channels",
        "Enable two-factor authentication on all your accounts",
        "Be cautious of links in emails, even from known senders",
        "Check for spelling errors and poor grammar in emails",
        "Hover over links to preview URLs before clicking",
        "Never share sensitive information via email"
    ]
    
    password_recommendations = [
        "Use different passwords for each account",
        "Consider using a password manager",
        "Create memorable passphrases instead of complex passwords",
        "Regularly update your passwords",
        "Enable biometric authentication when available",
        "Avoid using personal information in passwords",
        "Add random numbers and symbols to strengthen passwords"
    ]
    
    """
    Add targeted recommendations based on scores (using the 0 - 200 scale)

    Scale:
    phish_score < 120 (less than 60%) --> add 2 random phish recommendations
    phish_score < 160 (more than 60% but less than 80%) --> add 1 random phish recommendation

    match_score < 120 (less than 60%) --> add 2 random match recommendations
    match_score < 160 (more than 60% but less than 80%) --> add 1 random match recommendation
    """
    if phish_score < 120:
        recommendations.extend(random.sample(phish_recommendations, 2))
    elif phish_score < 160:
        recommendations.append(random.choice(phish_recommendations))

    if match_score < 120:
        recommendations.extend(random.sample(password_recommendations, 2))
    elif match_score < 160:
        recommendations.append(random.choice(password_recommendations))
    
    """
    Entropy-based recommendations (entropy is already at the 0 - 200 scale)

    Scale:
    entropy < 80 bits --> very weak password, adds a critical warning
    entropy < 120 bits --> weak password, could have serious improvements
    entropy < 160 bits --> moderate password, consider adding more complexity
    entropy > 160 bits --> strong password, no entropy recommendation needed
    """
    if entropy < 80:
        recommendations.append("Critical: Your password is extremely weak. Start using longer passwords with a mix of characters.")
    elif entropy < 120:
        recommendations.append("Your password needs improvement. Use a longer password with more variety.")
    elif entropy < 160:
        recommendations.append("Consider adding more complexity to your password for better security.")
    
    """
    Ensures a minimum of 3 recommendations

    Scale:
    - If fewer than 3 have been added so far, randomly fill in the rest from the phishing and password recommendation pools
    - This ensures the function never returns fewer than 3 recommendations and lets the user always be alert

    Final Step:
    - Trim the recommendations list to a maximum of 5 items
    - Ensures the user is not overloaded with too many tips at once and returns the most important tips before others based on score
    """
    if len(recommendations) < 3:
        available_recs = phish_recommendations + password_recommendations
        recommendations.extend(random.sample([r for r in available_recs if r not in recommendations], 3 - len(recommendations)))
    
    return recommendations[:5]