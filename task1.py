import streamlit as st
import random

# Game settings
GRID_SIZE = 10

# Initialize session state
if "snake" not in st.session_state:
    st.session_state.snake = [(5, 5)]
    st.session_state.direction = "RIGHT"
    st.session_state.food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    st.session_state.score = 0
    st.session_state.game_over = False

def move_snake():
    if st.session_state.game_over:
        return

    head_x, head_y = st.session_state.snake[0]
    direction = st.session_state.direction

    if direction == "UP":
        new_head = (head_x, head_y - 1)
    elif direction == "DOWN":
        new_head = (head_x, head_y + 1)
    elif direction == "LEFT":
        new_head = (head_x - 1, head_y)
    elif direction == "RIGHT":
        new_head = (head_x + 1, head_y)
    else:
        new_head = (head_x, head_y)

    # Check for collisions
    if (
        new_head[0] < 0 or new_head[0] >= GRID_SIZE or
        new_head[1] < 0 or new_head[1] >= GRID_SIZE or
        new_head in st.session_state.snake
    ):
        st.session_state.game_over = True
        return

    st.session_state.snake = [new_head] + st.session_state.snake

    # Check for food
    if new_head == st.session_state.food:
        st.session_state.score += 1
        while True:
            new_food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
            if new_food not in st.session_state.snake:
                st.session_state.food = new_food
                break
    else:
        st.session_state.snake.pop()

def reset_game():
    st.session_state.snake = [(5, 5)]
    st.session_state.direction = "RIGHT"
    st.session_state.food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    st.session_state.score = 0
    st.session_state.game_over = False

st.title("🐍 Snake Game (Step-based)")

st.write(f"Score: {st.session_state.score}")

# Game controls
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("⬆️ Up"):
        if st.session_state.direction != "DOWN":
            st.session_state.direction = "UP"
with col1:
    if st.button("⬅️ Left"):
        if st.session_state.direction != "RIGHT":
            st.session_state.direction = "LEFT"
with col3:
    if st.button("➡️ Right"):
        if st.session_state.direction != "LEFT":
            st.session_state.direction = "RIGHT"
with col2:
    if st.button("⬇️ Down"):
        if st.session_state.direction != "UP":
            st.session_state.direction = "DOWN"

if st.button("Next Step"):
    move_snake()

if st.button("Restart Game"):
    reset_game()

# Draw the grid
grid = [["⬜" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
for x, y in st.session_state.snake:
    grid[y][x] = "🟩"
fx, fy = st.session_state.food
grid[fy][fx] = "🍎"

st.write("Game Board:")
for row in grid:
    st.write("".join(row))

if st.session_state.game_over:
    st.error("Game Over! Click 'Restart Game' to play again.")
