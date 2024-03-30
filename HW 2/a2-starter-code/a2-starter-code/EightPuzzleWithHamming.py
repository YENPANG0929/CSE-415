'''EightPuzzleWithHamming.py
by Audrey Gunawan & YenPang Huang
UWNetID: ajesse & yph0929 
Student number: 2079375 & 2273427 

Assignment 2, Part 2, in CSE 415, Autumn 2022.

This file contains my problem formulation for the problem of
the EightPuzzleWithHamming.
'''
from EightPuzzle import * 

position = {}
goal = {}

goal_state = [[0,1,2],[3,4,5],[6,7,8]]

for i, row in enumerate(goal_state):
    for j, value in enumerate(row):
        goal[value] = (i, j)

def h(s):
    '''Function that represents the hamming distance'''
    distance = 0
    board = s.b
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value != 0 and goal[value] != (i, j):
                distance += 1
    return distance
