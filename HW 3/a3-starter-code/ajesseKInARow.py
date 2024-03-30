'''
<yourUWNetID>KInARow.py
Author: Audrey Gunawan
An agent for playing "K-in-a-Row with Forbidden Squares"
CSE 415, University of Washington

THIS IS A TEMPLATE WITH STUBS FOR THE REQUIRED FUNCTIONS.
YOU CAN ADD WHATEVER ADDITIONAL FUNCTIONS YOU NEED IN ORDER
TO PROVIDE A GOOD STRUCTURE FOR YOUR IMPLEMENTATION. 

'''

import time
import copy

# Global variables to hold information about the opponent and game version:
INITIAL_STATE = None
OPPONENT_NICKNAME = 'Not yet known'
OPPONENT_PLAYS = 'O' # Update this after the call to prepare.

# Information about this agent:
MY_LONG_NAME = 'Cashew Nut'
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
    intro = '\nMy name is Cashew Nut.\n'+\
            '"Audrey Gunawan (ajesse@uw.edu)" made me.\n'+\
            '!\n' 
    return intro
 
def nickname():
    return 'Tea-ess'
 
####################################################################

# Receive and acknowledge information about the game from
# the game master:
def prepare(initial_state, k, what_side_I_play, opponent_nickname):
    # Write code to save the relevant information in either
    # global variables.

    global INITIAL_STATE, OPPONENT_NICKNAME, I_PLAY, K, N, M

    INITIAL_STATE = initial_state
    OPPONENT_NICKNAME = opponent_nickname
    I_PLAY = what_side_I_play
    N = len(initial_state[0][:][:])
    M = len(initial_state[0][0])

    K = k

    #rows and columns on the board
   
    

    print("Change this to return 'OK' when ready to test the method.")
    return "OK"
 

############################################################
import time

import time

def makeMove(currentState, currentRemark, timeLimit=10):
    def is_valid_move(i, j):
        return currentboard[i][j] == ' '

    def find_best_move():
        best_score, best_i, best_j = -float('inf'), 0, 0
        for i in range(N):
            for j in range(M):
                if is_valid_move(i, j):
                    currentboard[i][j] = I_PLAY
                    temp = minimax(currentState, I_PLAY, n)
                    if temp > best_score:
                        best_score, best_i, best_j = temp, i, j
                    currentboard[i][j] = ' '
        return best_i, best_j

    a_default_move = [0, 0]
    currentboard = currentState[0]
    iBest, jBest, n = 0, 0, 1
    time_limit = time.time() + timeLimit / 1000

    while time.time() <= time_limit:
        iBest, jBest = find_best_move()
        n += 1

    a_default_move = [iBest, jBest]
    newState = [currentState[0][:], currentState[1]]  # Clone the current state
    newState[0][a_default_move[0]][a_default_move[1]] = I_PLAY

    newRemark = "I need to think of something appropriate.\n" + "Well, I guess I can say that this move is probably illegal."

    return [a_default_move, newState], newRemark



 #call minimax


##########################################################################
 
# The main adversarial search function:
def minimax(state, whoseMove, depthRemaining, alpha=-float('inf'), beta=float('inf')):
    if depthRemaining == 0:
        return staticEval(state)

    best_score = -float('inf') if whoseMove == I_PLAY else float('inf')
    board = state[0]

    for i in range(N):
        for j in range(M):
            if board[i][j] == ' ':
                player = I_PLAY if whoseMove == I_PLAY else OPPONENT_PLAYS
                board[i][j] = player

                temp = minimax(state, OPPONENT_PLAYS if whoseMove == I_PLAY else I_PLAY, depthRemaining - 1, alpha, beta)
                board[i][j] = ' '

                if whoseMove == I_PLAY:
                    best_score = max(best_score, temp)
                    alpha = max(alpha, temp)
                else:
                    best_score = min(best_score, temp)
                    beta = min(beta, temp)

                if beta <= alpha:
                    break  # Beta cutoff
    return best_score


#what score and what state we should go
#if you win, you should have high score, if you lose, you have low score
#have a case where if the current player is x or o, for each case, find min, 
#and other is find max, then return
#call minimax of the next state, then compare the values, do this in makemove
#choose the worst for the opposing player, and pick the highest score. 


    #default_score = 0 # Value of the passed-in state. Needs to be computed.
    
   # return [default_score, "my own optional stuff", "more of my stuff"]
    # Only the score is required here but other stuff can be returned
    # in the list, after the score.
 
 
##########################################################################
def count_consecutive_sequences(board, k, player):
    count = 0

    for i in range(N):
        row_sequence = [0] * (M - k + 1)
        for j in range(M - k + 1):
            row_sequence[j] = board[i][j:j + k].count(player)
        count += row_sequence.count(k)

    for j in range(M):
        col_sequence = [0] * (N - k + 1)
        for i in range(N - k + 1):
            col_sequence[i] = [board[i + x][j] for x in range(k)].count(player)
        count += col_sequence.count(k)

    for i in range(N - k + 1):
        for j in range(M - k + 1):
            diag_sequence = [board[i + x][j + x] for x in range(k)].count(player)
            reverse_diag_sequence = [board[i + x][j + k - 1 - x] for x in range(k)].count(player)
            count += (diag_sequence == k) + (reverse_diag_sequence == k)

    return count


def count_open_lines(board, I_PLAY, OPPONENT_PLAYS):
    C, D = 0, 0
    for i in range(N):
        for j in range(M):
            if board[i][j] == I_PLAY:
                if (i == 0 or board[i - 1][j] == ' ') and (j == 0 or board[i][j - 1] == ' '):
                    C += 1
            elif board[i][j] == OPPONENT_PLAYS:
                if (i == 0 or board[i - 1][j] == ' ') and (j == 0 or board[i][j - 1] == ' '):
                    D += 1
    return C, D

def check_potential_wins(board, K, I_PLAY, OPPONENT_PLAYS):
    for i in range(N):
        for j in range(M - K + 1):
            sequence = board[i][j:j + K]
            if sequence.count(OPPONENT_PLAYS) == K - 1 and sequence.count(' ') == 1:
                # Block the opponent by placing I_PLAY in the empty cell
                empty_index = sequence.index(' ')
                board[i][j + empty_index] = I_PLAY

def staticEval(state):
    board = state[0]
    A, B, C, D = 0, 0, 0, 0

    # Check potential wins for the opponent
    check_potential_wins(board, K, I_PLAY, OPPONENT_PLAYS)


    A += count_consecutive_sequences(board, K, I_PLAY)
    B += count_consecutive_sequences(board, K, OPPONENT_PLAYS)

    C, D = count_open_lines(board, I_PLAY, OPPONENT_PLAYS)

    H = A - B + C - D
    return H
