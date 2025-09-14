# Copilot Instructions for CyberSmart

## Project Overview
- **CyberSmart** is a Streamlit-based educational platform for cybersecurity awareness, featuring interactive games.
- Main entry point: `app.py` (uses Streamlit UI, imports games from `games/` subfolders).
- Each game is a Python module with a single function (e.g., `spot_the_phish()`, `password_match()`, `password_generator()`, `password_strength()`) that renders its UI and logic.

## Key Patterns & Conventions
- **Game Structure:**
  - Each game lives in its own subfolder under `games/`.
  - Game logic is encapsulated in a function named after the folder (e.g., `games/password_match/password_match.py` → `password_match()`).
  - All games use Streamlit widgets for UI (e.g., `st.header`, `st.write`, `st.radio`, `st.button`).
- **State Management:**
  - Use `st.session_state` for per-user state (e.g., answer tracking, random order).
- **Adding a New Game:**
  - Create a new subfolder in `games/`.
  - Implement a function matching the folder name.
  - Import and add to the `selectbox` in `app.py`.

## Developer Workflows
- **Run the app:**
  - `streamlit run app.py`
- **Dependencies:**
  - All requirements in `requirements.txt` (must include `streamlit`).
- **Testing:**
  - No formal test suite; manual testing via UI.

## Project-Specific Details
- **Password Generator:**
  - User selects character types and length, generates password, can copy to clipboard.
- **Password Strength:**
  - User enters password, receives color-coded strength and time-to-crack estimate.
- **Spot the Phish / Password Match:**
  - Multiple-choice quiz format, randomized order, instant feedback, score display.

## Integration Points
- No external APIs; all logic is local.
- No database or persistent storage; all state is in Streamlit session.

## Example: Adding a Game
1. Create `games/example_game/example_game.py` with `def example_game(): ...`.
2. Import and add to the menu in `app.py`.

---

For more, see `app.py` and the `games/` directory for working examples.
