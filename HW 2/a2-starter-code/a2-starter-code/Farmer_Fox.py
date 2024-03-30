'''Farmer_Fox.py
by Yenpang Huang
UWNetID: yph0929
Student number: 2273427

Assignment 2, in CSE 415, Autumn 2023.
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

# Put your formulation of the Farmer-Fox-Chicken-and-Grain problem here.
# Be sure your name, uwnetid, and 7-digit student number are given above in 
# the format shown.

H = 0  # Farmer
F = 1  # Fox
C = 2  # Chicken
G = 3  # Grain
LEFT = 0 # left side of bank
RIGHT = 1 # etc

class State():
    
    def __init__(self, d=None):
        if d == None:
            d = {'agents': [[0, 0], [0, 0], [0, 0], [0, 0]], # H, F, C, G
                 'boat': LEFT}
        self.d = d

    def __eq__(self, s2):
        for prop in ['agents', 'boat']:
            if self.d[prop] != s2.d[prop]: return False
        return True
    
    def __str__(self):
        p = self.d['agents']
        txt = "H on left:" + str(p[H][LEFT]) + "\n"
        txt += "F on left:" + str(p[F][LEFT]) + "\n"
        txt += "C on left:" + str(p[C][LEFT]) + "\n"
        txt += "G on left:" + str(p[G][LEFT]) + "\n"
        txt += "   H on right:" + str(p[H][RIGHT]) + "\n"
        txt += "   F on right:" + str(p[F][RIGHT]) + "\n"
        txt += "   C on right:" + str(p[C][RIGHT]) + "\n"
        txt += "   G on right:" + str(p[G][RIGHT]) + "\n"
        side = 'left'
        if self.d['boat'] == 1: side = 'right'
        txt += " boat is on the "+side+".\n"
        return txt
    
    def __hash__(self):
        return (self.__str__()).__hash__()
    
    def copy(self):
        news = State({})
        news.d['agents'] = [self.d['agents'][H_or_F_or_C_or_G][:] for H_or_F_or_C_or_G in [H, F, C, G]]
        news.d['boat'] = self.d['boat']
        return news
    
    def can_move(self, h, f, c, g):
        side = self.d['boat'] # Where the boat is.
        p = self.d['agents']
        if h < 1: return False # Need an H to be on the boat
        if p[H][side] < h: return False
        if p[F][side] < f: return False
        if p[C][side] < c: return False
        if p[G][side] < g: return False

        if p[F][side] - f == p[C][side] - c == 1 and p[H][side] - h == 0: return False # F must never be left along with the C
        if p[C][side] - c == p[G][side] - g == 1 and p[H][side] - h == 0: return False # C must never be left along with the G

        return True

    def move(self, h, f, c, g):
        news = self.copy()
        side = self.d['boat']
        p = news.d['agents']

        p[H][side] = p[H][side] - h
        p[F][side] = p[F][side] - f
        p[C][side] = p[C][side] - c
        p[G][side] = p[G][side] - g

        p[H][1-side] = p[H][1-side] + h
        p[F][1-side] = p[F][1-side] + f
        p[C][1-side] = p[C][1-side] + c
        p[G][1-side] = p[G][1-side] + g

        news.d['boat'] = 1-side
        return news
    
def goal_test(s):
        p = s.d['agents']
        return (p[H][RIGHT]==1 and p[F][RIGHT]==1 and p[C][RIGHT]==1 and p[G][RIGHT]==1)
    
def goal_message(s):
        return "Congratulations on successfully guiding the human, fox, chicken and grain all across the river!!!"
    
class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)
    
    def apply(self, s):
        return self.state_transf(s)
    
CREATE_INITIAL_STATE = lambda : State(d = {'agents':[[1, 0], [1, 0], [1, 0], [1, 0]], 'boat': LEFT })

# (h, f, c, g)
HFCG_combinations = [(1, 0, 0, 0), (1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1)] # 1. Only H moves; 2. H and F moves; 3. H and C moves; 4. H and G moves

OPERATORS = [Operator(
  f"Move the Farmer and {'the Fox' if f == 1 else 'the Chicken' if c == 1 else 'the Grain'}",
  lambda s, h1=h, f1=f, c1=c, g1=g: s.can_move(h1, f1, c1, g1),
  lambda s, h1=h, f1=f, c1=c, g1=g: s.move(h1, f1, c1, g1) ) 
  for (h, f, c, g) in HFCG_combinations]

GOAL_TEST = lambda s: goal_test(s)

GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)