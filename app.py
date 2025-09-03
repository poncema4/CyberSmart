import streamlit as st
from games.spot_the_phish.spot_the_phish import spot_the_phish
from games.password_match.password_match import password_match

def intro():
    st.title("Welcome to CyberSmart!")
    st.write("""
        CyberSmart helps you learn about cybersecurity through fun, interactive games.
        Choose a game below to get started!
    """)

def main():
    intro()
    game = st.selectbox("Choose a game:", ["Spot the Phish", "Password Match"])
    if game == "Spot the Phish":
        spot_the_phish()
    elif game == "Password Match":
        password_match()

if __name__ == "__main__":
    main()