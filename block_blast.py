import streamlit as st
import numpy as np
import random

st.set_page_config(page_title="Block Blast", layout="centered")

GRID_SIZE = 8

# Initialize game
if "grid" not in st.session_state:
    st.session_state.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    st.session_state.score = 0

st.title("🧱 Block Blast (Streamlit Edition)")
st.write("Fill rows or columns to score points!")

# Create random block
def get_block():
    shapes = [
        [(0,0)],
        [(0,0),(1,0)],
        [(0,0),(0,1)],
        [(0,0),(1,0),(0,1)],
        [(0,0),(1,0),(2,0)],
        [(0,0),(0,1),(0,2)]
    ]
    return random.choice(shapes)

if "block" not in st.session_state:
    st.session_state.block = get_block()

block = st.session_state.block

st.subheader("🧩 Current Block")
st.write(block)

row = st.number_input("Row", 0, GRID_SIZE-1, 0)
col = st.number_input("Column", 0, GRID_SIZE-1, 0)

def can_place(block, r, c):
    for dr, dc in block:
        if r+dr >= GRID_SIZE or c+dc >= GRID_SIZE:
            return False
        if st.session_state.grid[r+dr][c+dc] == 1:
            return False
    return True

def place_block(block, r, c):
    for dr, dc in block:
        st.session_state.grid[r+dr][c+dc] = 1

if st.button("Place Block"):
    if can_place(block, row, col):
        place_block(block, row, col)
        st.session_state.block = get_block()
        st.session_state.score += 5
    else:
        st.error("❌ Invalid Move")

# Clear full rows & columns
for i in range(GRID_SIZE):
    if all(st.session_state.grid[i]):
        st.session_state.grid[i] = 0
        st.session_state.score += 10

    if all(st.session_state.grid[:, i]):
        st.session_state.grid[:, i] = 0
        st.session_state.score += 10

st.subheader("🎯 Score")
st.success(st.session_state.score)

st.subheader("🧱 Game Board")
st.dataframe(st.session_state.grid)

if st.button("Restart Game"):
    st.session_state.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    st.session_state.score = 0
    st.session_state.block = get_block()
