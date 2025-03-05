import streamlit as st
import openai
import toml

# Load API key from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(
    page_title="OpenAI Tic-Tac-Toe",
    page_icon="🎮",
    layout="wide"
)
SIDEBAR = st.sidebar # SIDEBAR SECTION
st.markdown(
    """
        <style>
            button[kind="secondary"] > div > p {
                font-size:100px !important;
                color: #66CC00;
            }
            button[kind="secondary"] {
                height:200px;
                width:200px;
            }
        </style>
    """,
    unsafe_allow_html=True
)

def check_winner(board):
    """Check if there's a winner."""
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    return None

def board_to_string(board):
    """Convert the board to a string format for AI processing."""
    return "\n".join([" | ".join(row) for row in board])

def get_ai_move(board):
    """Query OpenAI's API for an optimal Tic-Tac-Toe move."""
    prompt = f"""
    You are an expert Tic-Tac-Toe player. Your goal is to always make the best possible move.

    - You play as 'O'.
    - Always check for a winning move and play it.
    - If no winning move, block the opponent's winning move.
    - Otherwise, prioritize center, then corners, then sides.
    - Only choose empty spaces.

    Here is the current board state:
    {board_to_string(board)}

    Respond only with a tuple (row, col), nothing else.
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are an expert Tic-Tac-Toe player."},
                  {"role": "user", "content": prompt}],
        temperature=0  # Ensures optimal deterministic responses
    )

    move = response.choices[0].message.content.strip()
    ai_move = eval(move) if move else None

    # Ensure the AI selects a valid move
    if ai_move and board[ai_move[0]][ai_move[1]] == "":
        return ai_move

    # If AI gives an invalid move, find the first available space
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                return (i, j)
    return None

def reset_game():
    """Reset game state."""
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.turn = "X"
    st.session_state.winner = None
    st.rerun()

def main():
    st.title("Tic-Tac-Toe with OpenAI")


    if "board" not in st.session_state:
        reset_game()

    st.write("Current Board:")
    for i in range(3):
        cols = st.columns(3, gap="small")
        for j in range(3):
            button_label = st.session_state.board[i][j] if st.session_state.board[i][j] else " "
            disabled = st.session_state.winner is not None or st.session_state.board[i][j] != ""
            if cols[j].button(button_label, key=f"{i}-{j}", disabled=disabled, type="secondary") and not disabled:
                st.session_state.board[i][j] = "X"
                st.session_state.turn = "O"
                st.session_state.winner = check_winner(st.session_state.board)
                st.rerun()

    if st.session_state.turn == "O" and not st.session_state.winner:
        ai_move = get_ai_move(st.session_state.board)
        if ai_move:
            st.session_state.board[ai_move[0]][ai_move[1]] = "O"
            st.session_state.turn = "X"
            st.session_state.winner = check_winner(st.session_state.board)
            st.rerun()

    if st.session_state.winner:
        st.success(f"{st.session_state.winner} wins!")
        if st.session_state.winner == "X":
            st.balloons()
    elif all(cell != "" for row in st.session_state.board for cell in row):
        st.info("It's a draw!")

    if st.button("Restart Game", type="primary"):
        reset_game()

if __name__ == "__main__":
    main()
