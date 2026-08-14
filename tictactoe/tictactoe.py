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
    if action not in actions(board):
        raise ValueError("Ação inválida para este tabuleiro!")
     
    # Copia o tabuleiro para um novo totalmente individual, ou seja, com endereços novos na memória para poder testar a situação sem mudar o original
    boardWithAction = copy.deepcopy(board)
    boardWithAction[action[0]][action[1]] = player(board)

    return boardWithAction




def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Linhas e Colunas
    playerXdiagonalL = 0
    playerOdiagonalL = 0
    playerXdiagonalR = 0
    playerOdiagonalR = 0
    k = 2

    for i in range(3):
        playerXline = 0
        playerOline = 0
        playerXcol = 0
        playerOcol = 0

        for j in range(3):
            if board[i][j] == X: # Verifica cada linha de X
                playerXline += 1
            if board[i][j] == O: # Verifica cada linha de O
                playerOline += 1            
            if board[j][i] == X: # Verifica cada coluna de X
                playerXcol += 1
            if board[j][i] == O: # Verifica cada coluna de O
                playerOcol += 1

        # Verifica vencedor linha e coluna
        if  playerXline == 3 or playerXcol == 3: 
            return X
        if  playerOline == 3 or playerOcol == 3:
            return O

        # Verifica Diagonais 
        if board[i][i] == X: 
            playerXdiagonalL += 1
        if board[i][i] == O: 
            playerOdiagonalL += 1
        if board[i][k] == X:
            playerXdiagonalR += 1
        if board[i][k] == O:
            playerOdiagonalR += 1
        k -= 1

    if playerXdiagonalL == 3 or playerXdiagonalR == 3:
        return X

    if playerOdiagonalL == 3 or playerOdiagonalR == 3:
        return O

    # Se ninguém ganhou
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Se houver vencedor
    if winner(board) in (X, O): 
        return True
    # Se ainda existe pelo menos uma casa EMPTY, o jogo NÃO acabou
    for row in board:
        if EMPTY in row:
            return False

    # Se não há vencedor nem casas vazias, é empate (jogo acabou)
    return True
     


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # Para o jogador X, sendo este +1 como vitória
    if player(board) == X:
        bestValue = -math.inf
        bestAction = None
        
        for action in actions(board): # Para cada ação possível de se fazer na sua vez, devolve aquela em que vc ganha / se sai melhor 
            move_val = minValue(result(board, action))

            if move_val > bestValue:
                bestValue = move_val
                bestAction = action

            if bestValue == 1:
                return bestAction
        return bestAction

    else: # Para o jogador O, sendo este -1 como vitória
        bestValue = math.inf
        bestAction = None
        
        for action in actions(board): # Para cada ação possível de se fazer na sua vez, devolve aquela em que vc ganha / se sai melhor 
            move_val = maxValue(result(board, action))

            if move_val < bestValue:
                bestValue = move_val
                bestAction = action

            if bestValue == -1:
                return bestAction
            
        return bestAction

def minValue(board):
    """
    Retorna o menor valor possível dentre os maiores para cada jogada
    """
    if terminal(board):
        return utility(board) # Aqui encerra a recursao de chamadas após verificar todas as possíveis jogadas

    value = math.inf

    for action in actions(board): # Para cada possível jogada
        value = min(value, maxValue(result(board, action))) # compara os valores para poder retornar o menor deles
        if value == -1: # Otimiza a função
            return value

    return value



def maxValue(board):
    """
    Retorna o maior valor possível dentre os menores para cada jogada
    """
    if terminal(board):
        return utility(board)

    value = -math.inf
    
    for action in actions(board): 
        value = max(value, minValue(result(board, action)))
        if value == 1:
            return value

    return value