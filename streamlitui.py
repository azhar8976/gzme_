import streamlit as st
import random

st.title("🎯 Guess Game - Computer vs User")

# session state initialize
if "number" not in st.session_state:
    st.session_state.number = random.randint(1, 100)
    st.session_state.attempts = 0

st.write("Guess the number between **1 and 100**")

guess = st.number_input(
    "Enter a number",
    min_value=1,
    max_value=100,
    step=1
)

if st.button("Check Guess"):
    st.session_state.attempts += 1

    if guess < st.session_state.number:
        st.warning("Too Low 📉")
    elif guess > st.session_state.number:
        st.warning("Too High 📈")
    else:
        st.success(
            f"🎉 Golu Won!\n\nAttempts: {st.session_state.attempts}"
        )

if st.button("Reset Game"):
    st.session_state.number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.info("Game Reset 🔄")
