import streamlit as st

# Configure Streamlit page settings
st.set_page_config(
    page_title="Minimax Tic-Tac-Toe",
    page_icon="🎮",
    layout="wide"
)

# Apply custom CSS styles for button appearance
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
    """Check if there's a winner by evaluating rows, columns, and diagonals."""
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]  # Row match
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]  # Column match
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]  # Main diagonal match
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]  # Opposite diagonal match
    return None

def minimax(board, depth, is_maximizing):
    """Minimax algorithm for optimal AI move."""
    winner = check_winner(board)
    if winner == "O":
        return 10 - depth
    if winner == "X":
        return depth - 10
    if all(cell != "" for row in board for cell in row):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ""
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ""
                    best_score = min(best_score, score)
        return best_score

def get_ai_move(board):
    """Find the best move using Minimax."""
    best_score = -float("inf")
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

def reset_game():
    """Reset the game board and turn state."""
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.turn = "X"
    st.session_state.winner = None
    st.rerun()

def main():
    """Main function to run the Tic-Tac-Toe game interface."""
    st.title("Tic-Tac-Toe with Minimax AI")

    # Initialize board state if not present
    if "board" not in st.session_state:
        reset_game()

    # Display current board state
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

    # AI's turn if applicable
    if st.session_state.turn == "O" and not st.session_state.winner:
        ai_move = get_ai_move(st.session_state.board)
        if ai_move:
            st.session_state.board[ai_move[0]][ai_move[1]] = "O"
            st.session_state.turn = "X"
            st.session_state.winner = check_winner(st.session_state.board)
            st.rerun()

    # Display game results
    if st.session_state.winner:
        st.success(f"{st.session_state.winner} wins!")
    elif all(cell != "" for row in st.session_state.board for cell in row):
        st.info("It's a draw!")

    # Restart game button
    if st.button("Restart Game", type="primary"):
        reset_game()

# Run the application
if __name__ == "__main__":
    main()
