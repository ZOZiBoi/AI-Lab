import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    count = 0
    for i in board:
        for j in i:
            if j:
                count += 1
    if count % 2 != 0:
        return O
    return X

def actions(board):
    res = set()
    board_len = len(board)
    for i in range(board_len):
        for j in range(board_len):
            if board[i][j] == EMPTY:
                res.add((i, j))
    return res

def result(board, action):
    curr_player = player(board)
    result_board = copy.deepcopy(board)
    (i, j) = action
    result_board[i][j] = curr_player
    return result_board


def get_horizontal_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]
    return None


def get_vertical_winner(board):
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]
    return None


def get_diagonal_winner(board):
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None


def winner(board):
    return get_horizontal_winner(board) or get_vertical_winner(board) or get_diagonal_winner(board)

def terminal(board):
    if winner(board) is not None:
        return True
    for row in board:
        for cell in row:
            if cell is None:
                return False
    return True

def utility(board):
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    return 0

def minimax(board):
    if terminal(board):
        return None
    curr_player = player(board)
    if curr_player == X:
        value, best_action = max_value(board)
    else:
        value, best_action = min_value(board)
    return best_action

def max_value(board):
    if terminal(board):
        return utility(board), None

    v = -float('inf')
    best_action = None
    for action in actions(board):
        min_val, _ = min_value(result(board, action))
        if min_val > v:
            v = min_val
            best_action = action
    return v, best_action
def min_value(board):
    if terminal(board):
        return utility(board), None
    v = float('inf')
    best_action = None
    for action in actions(board):
        max_val, _ = max_value(result(board, action))
        if max_val < v:
            v = max_val
            best_action = action
    return v, best_action
def draw_board(board):
    print("-------------")
    for row in board:
        print("|", end="")
        for cell in row:
            if cell is None:
                print("   ", end=" |")
            else:
                print(f" {cell} ", end="|")
        print()
        print("-------------")
def play_game():
    board = initial_state()
    draw_board(board)
    while not terminal(board):
        if player(board) == X:
            print("Your turn! (Player X)")
            row, col = map(int, input("Enter row and column (0, 1, or 2): ").split())
            if (row, col) in actions(board):
                board = result(board, (row, col))
            else:
                print("Invalid move, try again.")
                continue
        else:
            print("AI's turn (Player O)...")
            action = minimax(board)
            board = result(board, action)
        draw_board(board)
    if winner(board):
        print(f"Winner: {winner(board)}")
    else:
        print("It's a draw!")
play_game()