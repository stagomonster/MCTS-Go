#Rewrite of old go engine code - for clarity
import pygame
from random import randint

#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLACK_ALPHA = (0,0,0,150)
WHITE_ALPHA = (255,255,255,150)


#Window Values
WHEIGHT = 600
WWIDTH = 900

#Board Values
BHEIGHT = 570
BWIDTH = 570

#Square + Piece Scaling 
COL_SQUARES = 19
ROW_SQUARES = 19
SQUARE_SIZE = BHEIGHT/COL_SQUARES
PIECE_SCALE = 0.5

#Graphics Buffers + Sideboard
VERT_BUFFER = (WHEIGHT-BHEIGHT)/2.0
HOR_BUFFER = VERT_BUFFER
SIDEBOARD_X = BWIDTH + 2*HOR_BUFFER
SIDEBOARD_Y = WWIDTH - BWIDTH - 3 * HOR_BUFFER

MINIMUM_DIsTANCE_W = 999
MINIMUM_DISTANCE_B = 999

#Markings on Board
MARK_POINTS_R = [3,9,15]
MARK_POINTS_C = [3,9,15]
MARK_SCALE = 0.2

#Flood Search and Scoring
visited_squares = []

experimental_scores = []
experimental_score = 0

#Zobrist Hash for KO Rule
zobrist = []
last_hash = 0
hashes = [] 

#Board Values
board = [] #Board State

E = 0 #value of empty move
B = 1 #value of black piece
W = 2 #value of white piece

#Misc
FPS = 60
turn = 1 #starts with black

#Zobrist Functions for KO Rule
def zobrist_table():
    z = [[[randint(1, 2**64-1) for player in range(0, 2)]
          for row in range(0, ROW_SQUARES)]
          for col in range(0, COL_SQUARES)]
    return z

def get_hash(pos):
    h = 0
    for row in range(pos):
        for col in range(pos[0]):
            if pos[r][c] != E:
                h ^= zobrist[r][c][pos[r][c]]
    return h

def remove_hash(rp, remove_pos, hash_):
    remove_piece = rp - 1
    h = hash_
    for r in range(len(remove_pos)):
        for c in range(len(remove_pos[0])):
            if remove_pos[r][c] != 0:
                h^= zobrist[r][c][remove_piece]
    return h

def remove_hash_one(rp, remove_pos, hash_):
    remove_piece = rp - 1
    h = hash_ ^ zobrist[remove_pos[0]][remove_pos[1]][remove_piece]
    return h

def add_hash_one(ap, add_pos, hash_):
    add_piece = ap - 1

    h = hash_ ^ zobrist[add_pos[0]][add_pos[1]][add_piece]
    return h

def add_hash_mult(ap, add_pos, hash_):
    add_piece = ap - 1

    h = hash_
    for r in range(len(add_pos)):
        for c in range(len(add_pos[0])):
            if add_pos[r][c] != 0:
                h ^= zobrist[r][c][add_piece]
    return h


