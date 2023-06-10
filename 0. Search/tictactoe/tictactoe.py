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
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
