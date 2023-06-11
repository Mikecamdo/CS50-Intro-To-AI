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
    if board == initial_state():
        return X
    else:
        totalEmpty = 0 # The total number of empty squares left

        for row in board:
            totalEmpty += row.count(EMPTY)

        if totalEmpty % 2 == 0:
            return O
        else:
            return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleMoves = set()

    for i in range(3): # For each row of the board
        for j in range(3): # For each square of the row
            if board[i][j] == EMPTY: # If the square is empty, then the square is a possible move
                possibleMoves.add((i, j))

    return possibleMoves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newBoard = copy.deepcopy(board)
    currentPlayer = player(board)
    i, j = action

    if newBoard[i][j] == EMPTY:
        newBoard[i][j] = currentPlayer
    else:
        raise Exception("Not a valid move")

    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board: # Checking each row
        if (row[0] != EMPTY) and (row[0] == row[1] == row[2]):
            return row[0]
    
    for column in range(3): # Checking each column
        if (board[0][column] != EMPTY) and (board[0][column] == board[1][column] == board[2][column]):
            return board[0][column]
    
    if board[1][1] != EMPTY: # Checking diagonals
        if board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]
        elif board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    elif (board[0].count(EMPTY) + board[1].count(EMPTY) + board[2].count(EMPTY)) == 0:
        return True
    
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    theWinner = winner(board)
    if theWinner == X:
        return 1
    elif theWinner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    currentPlayer = player(board)
    
    if currentPlayer == X: # Trying to maximize score
        v = float('-inf')
        bestAction = None
        for action in actions(board):
            minimum = minValue(result(board, action))
            if v < minimum:
                v = minimum
                bestAction = action
            #v = max(v, minValue(result(board, action)))

        return bestAction
    else: # Trying to minimize score
        v = float('inf')
        bestAction = None
        for action in actions(board):
            maximum = maxValue(result(board, action))
            if v > maximum:
                v = maximum
                bestAction = action
            #v = max(v, minValue(result(board, action)))

        return bestAction
    

def maxValue(board):
    if terminal(board):
        return utility(board)
    
    v = float('-inf')
    for action in actions(board):
        v = max(v, minValue(result(board, action)))

    return v

def minValue(board):
    if terminal(board):
        return utility(board)
    
    v = float('inf')
    for action in actions(board):
        v = min(v, maxValue(result(board, action)))

    return v

