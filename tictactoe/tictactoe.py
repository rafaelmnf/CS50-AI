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


def is_empty(board):
    for line in board:
        for col in line:
            if col != EMPTY:
                return False
    return True # All positions has empty values


# Return the quantity of moves of specific player
def quantityInBoard(board, player):
    quantity = 0
    for line in board:
        for col in line:
            if col == player:
                quantity += 1
    return quantity


# Should take a board state as input, and return which player’s turn it is (either X or O)
def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Verify initial state -> X gets the first move
    if is_empty(board):
        return X
    
    if quantityInBoard(board, X) <= quantityInBoard(board, O): # Como X começa, se tiver a mesma qnt ou menor que O, ele joga
        return X
    else: 
        return O



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions
                    

# The result function takes a board and an action as input, and should return a new board state, without modifying the original board
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # If action is not a valid action for the board, raise an error. Se a ação for diferente de EMPTY, ela já está preenchida
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError("Invalid action: position already taken")
     
    # Copia o tabuleiro para um novo totalmente individual, ou seja, com endereços novos na memória para poder testar a situação sem mudar o original
    boardWithAction = copy.deepcopy(board)
    boardWithAction[action[0]][action[1]] = player(board)
    return boardWithAction




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
