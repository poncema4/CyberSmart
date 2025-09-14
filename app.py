import streamlit as st
from games.spot_the_phish.spot_the_phish import spot_the_phish
from games.password_match.password_match import password_match
from games.password_generator.password_generator import password_generator
from games.password_strength.password_strength import password_strength

def intro():
    st.title("Welcome to CyberSmart!")
    st.write("""
        CyberSmart is an educational platform that helps users learn about cybersecurity through
        fun, interactive games. Choose a game below to get started!
    """)

def main():
    intro()
    game = st.selectbox(
        "Choose a game:",
        [
            "Spot the Phish",
            "Password Match",
            "Password Generator",
            "Password Strength"
        ]
    )
    if game == "Spot the Phish":
        spot_the_phish()
    elif game == "Password Match":
        password_match()
    elif game == "Password Generator":
        password_generator()
    elif game == "Password Strength":
        password_strength()

if __name__ == "__main__":
    main()