"""
Task 1 — Minimax Search Algorithm
===================================
Implements the Minimax algorithm applied to Tic-Tac-Toe.

The Minimax algorithm is a recursive decision-making algorithm used in
two-player zero-sum games. The MAX player tries to maximise the score
while the MIN player tries to minimise it.
"""

import math
import time


# ---------------------------------------------------------------------------
# Board representation
# ---------------------------------------------------------------------------
EMPTY = " "
MAX_PLAYER = "X"   # AI (maximiser)
MIN_PLAYER = "O"   # Opponent (minimiser)


def create_board():
    """Return an empty 3x3 board as a flat list of 9 cells."""
    return [EMPTY] * 9


def print_board(board):
    """Pretty-print the board."""
    row_sep = "+---+---+---+"
    print(row_sep)
    for row in range(3):
        cells = " | ".join(board[row * 3 + col] for col in range(3))
        print(f"| {cells} |")
        print(row_sep)


def get_empty_cells(board):
    """Return indices of empty cells."""
    return [i for i, cell in enumerate(board) if cell == EMPTY]


def check_winner(board):
    """
    Return the winner ('X' or 'O') if there is one, else None.
    Checks all rows, columns, and diagonals.
    """
    wins = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
        (0, 4, 8), (2, 4, 6),              # diagonals
    ]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] != EMPTY:
            return board[a]
    return None


def is_terminal(board):
    """Return True if the game is over (win or draw)."""
    return check_winner(board) is not None or not get_empty_cells(board)


def evaluate(board):
    """
    Static evaluation of the board.
      +10 if X wins, -10 if O wins, 0 for draw.
    """
    winner = check_winner(board)
    if winner == MAX_PLAYER:
        return 10
    if winner == MIN_PLAYER:
        return -10
    return 0


# ---------------------------------------------------------------------------
# Minimax
# ---------------------------------------------------------------------------
nodes_explored = 0  # global counter reset before each search


def minimax(board, depth, is_maximising):
    """
    Classic Minimax — explores the full game tree.

    Parameters
    ----------
    board          : list[str] — current board state
    depth          : int       — current recursion depth (used for score adjustment)
    is_maximising  : bool      — True if it is the MAX player's turn

    Returns
    -------
    int — the minimax value of the board
    """
    global nodes_explored
    nodes_explored += 1

    score = evaluate(board)

    # Terminal states
    if score == 10:
        return score - depth   # prefer faster wins
    if score == -10:
        return score + depth   # prefer slower losses
    if not get_empty_cells(board):
        return 0

    if is_maximising:
        best = -math.inf
        for cell in get_empty_cells(board):
            board[cell] = MAX_PLAYER
            best = max(best, minimax(board, depth + 1, False))
            board[cell] = EMPTY
        return best
    else:
        best = math.inf
        for cell in get_empty_cells(board):
            board[cell] = MIN_PLAYER
            best = min(best, minimax(board, depth + 1, True))
            board[cell] = EMPTY
        return best


def best_move_minimax(board):
    """
    Find the best move for MAX_PLAYER using Minimax.

    Returns
    -------
    (int, int, int) — (best_cell, best_score, nodes_explored)
    """
    global nodes_explored
    nodes_explored = 0

    best_score = -math.inf
    best_cell = -1
    move_scores = {}

    for cell in get_empty_cells(board):
        board[cell] = MAX_PLAYER
        score = minimax(board, 0, False)
        board[cell] = EMPTY
        move_scores[cell] = score
        if score > best_score:
            best_score = score
            best_cell = cell

    return best_cell, best_score, nodes_explored, move_scores


# ---------------------------------------------------------------------------
# Test Cases
# ---------------------------------------------------------------------------
def run_tests():
    print("=" * 60)
    print("MINIMAX TEST CASES")
    print("=" * 60)

    test_cases = [
        {
            "name": "Empty board — first move",
            "board": list("         "),
            "description": "X should play centre (4) or a corner.",
        },
        {
            "name": "X can win immediately",
            "board": list("XX O O   "),
            "description": "X plays index 2 to win the top row.",
        },
        {
            "name": "X must block O's win",
            "board": list("OO X X   "),
            "description": "X plays index 2 to block O winning top row.",
        },
        {
            "name": "Near-draw — pick best remaining",
            "board": list("XOXOXXO  "),
            "description": "Only two moves left; X picks the better one.",
        },
        {
            "name": "O about to complete diagonal",
            "board": list("O X XO   "),
            "description": "X must block O's diagonal win at index 8.",
        },
    ]

    for tc in test_cases:
        board = [c if c != " " else EMPTY for c in tc["board"]]
        start = time.perf_counter()
        cell, score, explored, move_scores = best_move_minimax(board)
        elapsed = (time.perf_counter() - start) * 1000

        print(f"\nTest : {tc['name']}")
        print(f"Info : {tc['description']}")
        print_board(board)
        print(f"Best Move    : cell {cell}")
        print(f"Score        : {score}")
        print(f"Nodes        : {explored}")
        print(f"Time         : {elapsed:.2f} ms")
        print(f"Move Scores  : {move_scores}")


if __name__ == "__main__":
    run_tests()

    print("\n" + "=" * 60)
    print("INTERACTIVE GAME  (you are O, AI is X)")
    print("=" * 60)
    print("Board positions:")
    print_board([str(i) for i in range(9)])

    board = create_board()
    current = MIN_PLAYER   # human goes first

    while not is_terminal(board):
        print_board(board)
        if current == MIN_PLAYER:
            while True:
                try:
                    move = int(input("Your move (0-8): "))
                    if 0 <= move <= 8 and board[move] == EMPTY:
                        break
                    print("Invalid move, try again.")
                except ValueError:
                    print("Enter a number 0-8.")
        else:
            print("AI thinking (Minimax)...")
            move, score, explored, _ = best_move_minimax(board)
            print(f"AI plays cell {move}  (score={score}, nodes={explored})")

        board[move] = current
        current = MIN_PLAYER if current == MAX_PLAYER else MAX_PLAYER

    print_board(board)
    winner = check_winner(board)
    print("Result:", f"{winner} wins!" if winner else "Draw!")
