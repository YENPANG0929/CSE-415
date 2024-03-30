'''
nyychuiKInARow.py
Author: CHUI Nok Yan Yannis
An agent for playing "K-in-a-Row with Forbidden Squares"
CSE 415, University of Washington

THIS IS A TEMPLATE WITH STUBS FOR THE REQUIRED FUNCTIONS.
YOU CAN ADD WHATEVER ADDITIONAL FUNCTIONS YOU NEED IN ORDER
TO PROVIDE A GOOD STRUCTURE FOR YOUR IMPLEMENTATION.

'''

import time
import random

# Global variables to hold information about the opponent and game version:
INITIAL_STATE = None
OPPONENT_NICKNAME = 'Not yet known'
OPPONENT_PLAYS = 'O' # Update this after the call to prepare.

# Information about this agent:
MY_LONG_NAME = 'ToeTacTic'
MY_NICKNAME = 'Tic'
I_PLAY = 'X' # Gets updated by call to prepare.

 
# GAME VERSION INFO
M = 0
N = 0
K = 0
TIME_LIMIT = 0

SIDE = {'X': 0,
        'O': 1}

SIDES = ['X', 'O']

Z_HASH = [0]
 
############################################################
# (DONE) Function 2:
# INTRODUCTION
def introduce():
    intro = '\nMy name is ToeTacTic.\n'+\
            'Yannis CHUI (UWNetID: nyychui) made me.\n'+\
            'I am a friendly game-playing agent!\n' 
    return intro

# (DONE) Function 3:
def nickname():
    return MY_NICKNAME
 
############################################################

# (DONE) Function 1: 
# Receive and acknowledge information about the game from
# the game master:
def prepare(initial_state, k, what_side_I_play, opponent_nickname):
    global M, N ,K, I_PLAY, OPPONENT_PLAYS, OPPONENT_NICKNAME
    # Write code to save the relevant information in either
    # global variables.
    INITIAL_STATE = initial_state
    M = len(INITIAL_STATE[0][0])
    N = len(INITIAL_STATE[0])

    K = k

    I_PLAY = what_side_I_play
    OPPONENT_PLAYS = SIDES[SIDE[what_side_I_play]]

    OPPONENT_NICKNAME = opponent_nickname

    #Z_HASH = [Z_HASH*2]*(M*N)
    #for i in range(N):
    #    for j in range(M):
    #        if INITIAL_STATE[0][N][M] == 'X' or INITIAL_STATE[0][N][M] == 'O':
    #            Z_HASH[N*M+M][SIDE[INITIAL_STATE[0][N][M]]] = 1
    
    #print("Change this to return 'OK' when ready to test the method.")
    #return "Not-OK"
    return 'OK'
 
############################################################
 
def makeMove(currentState, currentRemark, timeLimit=10000):
    # print("makeMove has been called")

    board = currentState[0]
    player = currentState[1]
    possible_moves = [] #2D array that stores all the possible moves
    return_move = [0,0]
    return_remark = ['','']
    depth = 3
    dummy = ' '

    # getting current possible moves (blank spots on the board)
    for i in range(len(board)*len(board[0])):
        row = i // len(board[0])
        col = i % len(board[0])
        if board[row][col] == ' ':
            possible_moves.append([row, col])

    new_state = [[[x for x in row] for row in board], player]
    starting_time = time.time()
    
    # increase depth
    #while time.time() < starting_time + timeLimit/100 :
    if player == 'X':
        current_score = -float('inf')
    else:
        current_score = float('inf')
    
    for moves in possible_moves:
        new_state[0][moves[0]][moves[1]] = player
        minmax = minimax(new_state, depth)
        if player == 'X' and minmax[0] > current_score:
            return_move = moves
            current_score = minmax[0]
        if player == 'O' and minmax[0] < current_score:
            return_move = moves
            current_score = minmax[0]
        new_state[0][moves[0]][moves[1]] = ' '
        #depth += 1
            
    new_state[0][return_move[0]][return_move[1]] = player
    new_state[1] = SIDES[1-SIDE[player]]

    index = random.randint(1,2)
    new_remark = minmax[index]

    # if (type(new_remark) != type(dummy)):
    #    print('type = '+ str(type(new_remark)))
    #    print(minmax)

    # print("Returning from makeMove")
    return [[return_move, new_state], new_remark]

    # print("code to compute a good move should go here.")
    # Here's a placeholder:
    # a_default_move = [0, 0] # This might be legal ONCE in a game,
    # if the square is not forbidden or already occupied.
    
    # newState = currentState # This is not allowed, and even if
    # it were allowed, the newState should be a deep COPY of the old.
    
    # newRemark = "I need to think of something appropriate.\n" +\
    # "Well, I guess I can say that this move is probably illegal."

##########################################################################

# Funcion 6:
def optionalStuff(score):
    if score > 0:
        return ['Haha', 'Thank you for giving me this opportunity']
    elif score == 0:
        return ['Hmmm', 'It is interesting']
    else:
        return ['Well...', 'Nice move']
    
# The main adversarial search function:
def minimax(state, depthRemaining, pruning=False, alpha=-float('inf'), beta=float('inf'), zHashing=None):
    # print("Calling minimax. We need to implement its body.")
    default_score = 0 # Value of the passed-in state. Needs to be computed.
    board = state[0]
    player = state[1]
    return_value = [0, 0, 0]

    # Base case
    if (depthRemaining == 0):
        default_score = staticEval(state)
        optional = optionalStuff(default_score)
        return [default_score, optional[0], optional[1]]

    if player == 'X':
        default_score = -float('inf')
    if player == 'O':
        default_score = float('inf')

    # Minimax searching 
    for i in range(N*M):
        row = i // M
        col = i % M
        if board[row][col] == ' ':
            board[row][col] = player
            result = minimax([board, SIDES[1- SIDE[player]]], depthRemaining -1, pruning, alpha, beta, zHashing)
            if player == 'X' and result[0] > default_score:
                default_score = result[0]
                return_value = result
                if pruning:
                    alpha = max(alpha, default_score)#update alpha as the current score is the largest in the child node
                    if (alpha >= beta):
                        break
            elif player == 'O' and result[0] < default_score:
                default_score = result[0]
                return_value = result
                if pruning:
                    beta = min(beta, default_score)
                    if (alpha >= beta):
                        break
            board[row][col] = ' '

    return return_value
    # return [default_score, "my own optional stuff", "more of my stuff"]
    # Only the score is required here but other stuff can be returned
    # in the list, after the score.
 
##########################################################################
    
# (DONE) Function 5:
def calValueofList(Row):
    if 'O' not in Row:              # only have X in the row/column
        X_count = 0                 
        for item in Row:            # checking how many X in the row/column
            if item == 'X':         
                X_count += 1
        return 10**(X_count-1)      # 1X: 1, 2X: 10, 3X: 100...
    elif 'X' not in Row:            # only have O in the row/column
        O_count = 0
        for item in Row:
            if item == 'O':
                O_count += 1
        return (10**(O_count-1))*-1 # 1O: -1, 2O: -10, 3O: -100
    else:
        return 0                    # either have both X and O or blank
    
def staticEval(state):
    # print('calling staticEval. Its value needs to be computed!')
    # Values should be higher when the states are better for X,
    # lower when better for O.
    board = state[0]
    value = 0
    for i in range(N):
        value += calValueofList(board[i])
    for i in range(M):
        col = [column[i] for column in board]
        value += calValueofList(col)
    return value
 
##########################################################################
