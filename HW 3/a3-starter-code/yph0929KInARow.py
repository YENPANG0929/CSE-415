'''
yph0929KInARow.py
Author: Yenpang Huang
An agent for playing "K-in-a-Row with Forbidden Squares"
CSE 415, University of Washington

THIS IS A TEMPLATE WITH STUBS FOR THE REQUIRED FUNCTIONS.
YOU CAN ADD WHATEVER ADDITIONAL FUNCTIONS YOU NEED IN ORDER
TO PROVIDE A GOOD STRUCTURE FOR YOUR IMPLEMENTATION.

'''

import time
import copy
import random

# Global variables to hold information about the opponent and game version:
INITIAL_STATE = None
OPPONENT_NICKNAME = 'Not yet known'
OPPONENT_PLAYS = 'O' # Update this after the call to prepare.

# Information about this agent:
MY_LONG_NAME = 'Templatus Skeletus'
MY_NICKNAME = 'Tea-ess'
I_PLAY = 'X' # Gets updated by call to prepare.

 
# GAME VERSION INFO
M = 0
N = 0
K = 0
TIME_LIMIT = 0
 
############################################################
# INTRODUCTION
def introduce():
    intro = '\nMy name is Yenpang Huang.\n'+\
            '"I am not good in this game.\n'+\
            'Please let me win or just surrender!!!\n' 
    return intro
 
def nickname():
    return 'YPH'
 
############################################################

# Receive and acknowledge information about the game from
# the game master:
def prepare(initial_state, k, what_side_I_play, opponent_nickname):
    # Write code to save the relevant information in either
    # global variables.
    global INITIAL_STATE, K, I_PLAY, OPPONENT_NICKNAME, N, M
    INITIAL_STATE = initial_state
    K = k
    I_PLAY = what_side_I_play
    OPPONENT_NICKNAME = opponent_nickname
    N = len(initial_state[0][:][:]) # Row
    M = len(initial_state[0][0]) # Col
    print("OK")
    return "Not-OK"
 
############################################################
def makeMove(currentState, currentRemark, timeLimit=10000):

    # Here's a placeholder:
    a_default_move = [0, 0]

    currentboard = currentState[0]
    default_score = 0
    rowBest = 0
    colBest = 0
    n = 1
    tf = time.time() + timeLimit/1000 # Final time

    while time.time() <= tf: # while loop break after time reaches tf
        for row in range(N):
            for col in range(M):
                
                if currentboard[row][col] == ' ':
                    currentboard[row][col] = I_PLAY # Assign my move to the state temporary
                    
                    temp = minimax(currentState, I_PLAY, n) # Evaluate the score for this temporary state
                    
                    if temp > default_score: # if this condition meets, stores the informations
                        rowBest = row
                        colBest = col
                        default_score = temp

                    currentboard[row][col] = ' ' # Initialize back to the original state

        n += 1

    a_default_move = [rowBest, colBest] # The best move determined in while loop 
    
    newState = copy.deepcopy(currentState)
    newState[0][a_default_move[0]][a_default_move[1]] = I_PLAY # Officially place my decision
    
    remarks = ["I hope this is a wise move.", "Maybe this move would help me toward the victory.",
           "Trying hard to survive.", "Wish I am smart like an AI algorithm."]

    newRemark = random.choice(remarks)

    return [[a_default_move, newState], newRemark]
 
 
##########################################################################
 
# The main adversarial search function:
def minimax(state, whoseMove, depthRemaining, pruning=False, alpha= - float('inf'), beta= float('inf'), zHashing=None):

    board = state[0]
    
    default_score = 0 # Value of the passed-in state. Needs to be computed.
    if depthRemaining == 0:
        return staticEval(state) # Leaf node of the tree
    
    if whoseMove == I_PLAY:
        default_score = alpha 
        for row in range(N):
            for col in range(M):
                if board[row][col] == ' ':
                    board[row][col] = I_PLAY # Assign
                    temp = minimax(state, OPPONENT_PLAYS, depthRemaining - 1) # Evaluate
                    default_score = max(default_score, temp) # Max the score
                    board[row][col] = ' ' # Initialize
    else:
        default_score = beta
        for row in range(N):
            for col in range(M):
                if board[row][col] == ' ':
                    board[row][col] = OPPONENT_PLAYS # Assign
                    temp = minimax(state, I_PLAY, depthRemaining - 1) # Evaluate
                    default_score = min(default_score, temp) # Min the score
                    board[row][col] = ' ' # Initialize
    
    return default_score
 
##########################################################################
 
def staticEval(state):
    # Values should be higher when the states are better for X,
    # lower when better for O.

    board = state[0]
    A = 0
    B = 0
    C = 0
    D = 0
    E = 0

    k = 2

    while k <= K:

        # Row
        for row in range(N):
            for col in range(M - k):
                if board[row][col] == I_PLAY:
                    if (all(board[row][col + i] == I_PLAY for i in range(k)) and # Check k in a row for player's mark
                        board[row].count(I_PLAY) == k): # Check the total # of player's mark in a row
                        A += 10**(k-1) # A increases by 10 to the power of (k-1)th
                    elif (all(board[row][col + i] == I_PLAY for i in range(k-2)) and  # Check (k-2) in a row
                          all(board[row][col + i + 1] == ' ' for i in range(k-2)) and  # Check the next position of k-2 is empty
                          board[row][col + k - 1] != OPPONENT_PLAYS):  # Ensure the kth position isn't occupied by the opponent
                        E += 10**(k) # Reward for not being blocked

                elif board[row][col] == OPPONENT_PLAYS: 
                    if (all(board[row][col + i] == OPPONENT_PLAYS for i in range(k)) and # Check k in a row for opponent's mark
                        board[row].count(OPPONENT_PLAYS) == k): # Check the total # of player's mark in a row
                        B += 10**(k-1) 
        # Same logic for Col, diagonal and antidiagnal

        # Col
        for row in range(N - k):
            for col in range(M):
                if board[row][col] == I_PLAY:
                    if (all(board[row + i][col] == I_PLAY for i in range(k)) and
                        sum(board[r][col] == I_PLAY for r in range(N)) == k):
                        A += 10**(k-1)
                    elif (all(board[row + i][col] == I_PLAY for i in range(k-2)) and
                          all(board[row + i + 1][col] == ' ' for i in range(k-2)) and
                          board[row + k -1][col] != OPPONENT_PLAYS):
                        E += 10**(k)
                    
                elif board[row][col] == OPPONENT_PLAYS:
                    if (all(board[row + i][col] == OPPONENT_PLAYS for i in range(k)) and
                        sum(board[r][col] == OPPONENT_PLAYS for r in range(N)) == k):
                        B += 10**(k-1)

        # Diag
        for row in range(N - k):
            for col in range(M - k):
                if board[row][col] == I_PLAY:
                    if (all(board[row + i][col + i] == I_PLAY for i in range(k)) and 
                        sum(board[row + i][col + i] == I_PLAY for i in range(k)) == k):
                        A += 10**(k-1)
                    elif (all(board[row + i][col + i] == I_PLAY for i in range(k-2)) and
                          all(board[row + i +1][col + i + 1] == ' ' for i in range(k-2)) and
                          board[row + k -1][col + k - 1] != OPPONENT_PLAYS):
                        E += 10**(k)
                elif board[row][col] == OPPONENT_PLAYS:
                    if (all(board[row + i][col + i] == OPPONENT_PLAYS for i in range(k)) and
                        sum(board[row + i][col + i] == OPPONENT_PLAYS for i in range(k)) == k):
                        B += 10**(k-1)

        # Antidiag
        for row in range(N - k):
            for col in range(k - 1, M - 1):
                if board[row][col] == I_PLAY:
                    if (all(board[row + i][col - i] == I_PLAY for i in range(k)) and
                        sum(board[row + i][col - i] == I_PLAY for i in range(k)) == k):
                        A += 10**(k-1)
                    elif (all(board[row + i][col - i] == I_PLAY for i in range(k-2)) and 
                          all(board[row + i +1][col - i - 1] == ' ' for i in range(k-2)) and
                          board[row + k -1][col - k + 1] != OPPONENT_PLAYS):
                        E += 10**(k)
                elif board[row][col] == OPPONENT_PLAYS:
                    if (all(board[row + i][col - i] == OPPONENT_PLAYS for i in range(k)) and
                        sum(board[row + i][col - i] == OPPONENT_PLAYS for i in range(k)) == k):
                        B += 10**(k-1)

        k += 1 
    
    # Counting singular
    for row in range(N):
        for col in range(M):
            if board[row][col] == I_PLAY:
                if ((row == 0 or board[row - 1][col] == ' ') and (col == 0 or board[row][col - 1] == ' ') and
                    (row == 0 or col == 0 or board[row - 1][col - 1] == ' ') and
                    (row == 0 or col == M - 1 or board[row - 1][col + 1] == ' ')): # Check 8 tiles surrounding are blank
                    C += 1
            elif board[row][col] == OPPONENT_PLAYS:
                if ((row == 0 or board[row - 1][col] == ' ') and (col == 0 or board[row][col - 1] == ' ') and
                    (row == 0 or col == 0 or board[row - 1][col - 1] == ' ') and
                    (row == 0 or col == M - 1 or board[row - 1][col + 1] == ' ')):
                    D += 1

    H = A - B + C - D + E

    return H

##########################################################################