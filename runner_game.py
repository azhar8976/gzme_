import streamlit as st
import random
import time

st.set_page_config(page_title="Runner Game", layout="centered")
st.title("🏃‍♂️ Streamlit Runner Game")
st.write("Subway Surfer style – game khud chalega, tum JUMP karo")

# -------- Session State --------
if "score" not in st.session_state:
    st.session_state.score = 0

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "obstacle" not in st.session_state:
    st.session_state.obstacle = False

if "jumped" not in st.session_state:
    st.session_state.jumped = False

# -------- Controls --------
jump = st.button("🦘 JUMP")

if jump:
    st.session_state.jumped = True

# -------- Game Loop --------
if not st.session_state.game_over:

    # Auto running
    time.sleep(0.7)
    st.session_state.score += 1

    # Random obstacle
    if random.randint(1, 4) == 1:
        st.session_state.obstacle = True
    else:
        st.session_state.obstacle = False

    if st.session_state.obstacle:
        st.warning("❌ Obstacle aaya!")

        if st.session_state.jumped:
            st.success("🔥 Nice Jump! Bach gaye")
            st.session_state.jumped = False
        else:
            st.session_state.game_over = True
    else:
        st.info("🏃 Running...")

    st.rerun()

# -------- Game Over --------
else:
    st.error("💀 GAME OVER")
    st.write(f"🏆 Final Score: **{st.session_state.score}**")

    if st.button("🔄 Restart"):
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.obstacle = False
        st.session_state.jumped = False
        st.rerun()

st.markdown("---")
st.write(f"### 🎯 Score: {st.session_state.score}")
