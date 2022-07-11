"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = 0
    count_o = 0

    for (i,j) in [(0,0),(1,0),(2,0),(0,1),(1,1),(2,1),(0,2),(1,2),(2,2)]:
        if board[i][j] == X:
            count_x += 1
        elif board[i][j] == O:
            count_o += 1
    if count_x <= count_o:
        return X
    else :
        return O
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    if terminal(board):
        return None
    for (i,j) in [(0,0),(1,0),(2,0),(0,1),(1,1),(2,1),(0,2),(1,2),(2,2)]:
        if board[i][j] is None:
            actions.add((i,j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    copy_board = copy.deepcopy(board)
    
    if action in actions(board): 
        copy_board[action[0]][action[1]] = player(board)
        return copy_board
    raise NotImplementedError



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Horizontal
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
    #Vertical
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j]:
            return board[0][j]
    # Diagonals
    if (board[0][0] == board[1][1] == board[2][2]) or (board[0][2] == board[1][1] == board[2][0]):
        return board[1][1]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Compare if is already a winner or a Tie
    if winner(board) == X or winner(board) == O:
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Assing a numerical value for each possible result
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else :
            return 0
    else :
        raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Check if the board is already finished
    if terminal(board):
        return None
    
    # Max Value Function
    def MaxValue(board):
        if terminal(board):
            return utility(board)
        v = -2
        for (i,j) in actions(board):
            v = max(v, MinValue(result(board, (i,j))))
        return v
    # Min Value Function
    def MinValue(board):
        if terminal(board):
            return utility(board)
        v = 2
        for (i,j) in actions(board):
            v = min(v, MaxValue(result(board, (i,j))))
        return v
    
    possible_values = []
    # Select wich player is the Computer playing
    if player(board) == O:
        for action in actions(board):
            possible_values.append((MaxValue(result(board, action)),action))
        best_move = min(possible_values)
    elif player(board) == X:
        for action in actions(board): 
            possible_values.append((MinValue(result(board, action)),action))
        best_move = max(possible_values)

    return best_move[1]

