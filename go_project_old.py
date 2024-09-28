import pygame
from random import randint
#https://baduk.sourceforge.net/about/ might be useful later
#https://webdocs.cs.ualberta.ca/~mmueller/ps/seki.pdf
#https://webdocs.cs.ualberta.ca/~mmueller/ps/goeval.pdf
#https://www.davidsilver.uk/wp-content/uploads/2020/03/master-level-go.pdf
#https://pasky.or.cz/go/pachi-tr.pdf HMM
#https://www.moderndescartes.com/essays/implementing_go/ Very useful
#https://github.com/brilee/go_implementation/blob/master/go_naive.py also useful
# https://boardgames.stackexchange.com/questions/19233/how-to-apply-the-ko-rule-go for KO RULES
#https://www.gnu.org/software/gnugo/gnugo_11.html#SEC144

#https://levelup.gitconnected.com/zobrist-hashing-305c6c3c54d0 ZOBRIST HASHING
# https://dl.acm.org/doi/pdf/10.1145/1476793.1476819
# https://www.chessprogramming.org/Go#1960_... USEFUL

#chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://helios2.mi.parisdescartes.fr/~bouzy/publications/Bouzy-IJPRAI.pdf
#May decide to use BOUZY intead of ZOBRIST influence formula - appears more accurate
'''
TODO:
Board setup DONE
captures DONE
UI (Captured pieces, turn, etc) DONE
KO rule DONE
other rules:
- no self capture DONE
- 
scoring (BENSONS ALGORITHM?) https://senseis.xmp.net/?BinMatrix
AI
IDEAS FOR AI:
GREEDY TERRITORY BASED (REQ HIGH LEVEL OF ACCURACY REGARDING TERRITORY EVAL)
LOCAL / GLOBAL FOCUS - EVAL WHETHER FIGHT VS MOVE
HEURISTIC INVOLVING OPTIONS - ATTACK, DEFENSE, SURROUND ETC
OVERALL BOARD EVAL BASED - DIFFICULT TO ACCURATELY MEASURE


ALPHA BETA PRUNING LIKELY
leela type network is very different to NNUE type networks because NNUE just gives 'a-better-than-handcrafted' static evaluation while still been driven by the alpha-beta search while leela type one drives the Monte-Carlo search and gives a probability percentage of win/draw/lose instead of just a scalar evaluation of the position reached. Since Go mostly doesn't have forcing variations other than life and death problems which can be solved easily by a computer the major scope is 'how-to-teach-computer-thinking-about-territory' and here's where the probability beats scalar evaluations because of driving the search.
I don't have anything now, but thinking about leela type network, maybe there's a framework exist, it's really challenging thing to do to say the least but after starting playing Go as a Human I've realized that alpha-beta type engines no matter how fantastic their static evaluation is are doomed to lose because of the originally wrong approach if applied to Go.'
- chessprogramming : perhaps wrong approach, though high level network unfeasible.

lambda tree? only 1 paper explanation
Efficiency is not stated - may req high computation

HOWEVER, LESS EFFICIENT AND EFFECTIVE DUE TO THE ENORMOUS CALCULATION REQ
MAY NEED TO SEPARATE CALCULATIONS INTO "LOCAL GROUPS" 9X9 SQUARES
(FOR FIGHTS)

5.1.1 Heuristic evaluation 
Our heuristic evaluation function for small-board Go aims at five goals:
1. maximising the number of stones on the board,
2. maximising the number of liberties,
3. avoiding moves on the edge,
4. connecting stones, and
5. making eyes

FOR HEURISTICS - must have some way of evaluating threats/forcing positions (dep 2)
^ only way to do common ladder positions (!)

Flood filling DONE
recursively marks empty points to their adjacent colour. In the case that a flood
fill for Black overlaps with a flood fill for White the overlapping region becomes
neutral. (As a consequence all non-neutral empty regions must be completely
enclosed by one colour.) Scoring by distance marks each point based on the
distance towards the nearest remaining black or white stone(s). If the point is
closer to a black stone it is marked black, if the point is closer to a white stone
it is marked white, otherwise (if the distance is equal) the point does not affect
the score and is marked neutral.

Final decision -
attempt to recreate a somewhat faithful Python program with heuristics similar to Zobrist's thesis
^ may utilize Bouzy's territory alg instead of Zobrist (more effective)

....
perhaps a more modern approach, using MCTS may be better
Zobrist describes his process in detail, as do others of his time, but
it is difficult to replicate, especially given the lack of "patterns" provided
that he mentions, or examples of code for the heuristics.

On the other hand, while much more complicated, open source MCTS code is available,
the only question is whether I can parse through it and implement it myself.

https://www.youtube.com/watch?v=Fbs4lnGLS8M
VERY VERY USEFUL

MCTS does not use an evaluation function - allows for easier application besides
extensive eval functions (Zobrist, Bouzy influence not necessary)
But it does require a pattern database to refer to.


'These situations are characterized by the repeated occurrence
of moves which force the opponent to reply or to be captured'
- Zobrist of the ladder pattern search
'''

board = [] #Main array

#WINDOW STATS
height = 600 
width = 900

#BOARD STATS
bheight = 570 
bwidth = 570
col_squares = 19
row_squares = 19
square_size = bheight/col_squares 

#Buffer between WINDOW and BOARD
vert_buffer = (height-bheight)/2.0
hor_buffer = vert_buffer

#SIDEBOARD STATS
side_x = bwidth + 2*hor_buffer
side_w = width-bwidth-3*hor_buffer

#BOARD VALUES
E = 0
B = 1
W = 2
'''
empty - 0
black - 1
white - 2
'''

#Visual Marks
mark_points_r = [3, 9, 15] 
mark_points_c = [3, 9, 15]
mark_scale = .2 #scaling bsed on square size

#FLOOD SEARCH VARS
visited_squares = [] #0 = not visited, 1 = visited

experimental_scores = []
experimental_score = 0

blackColor = (0,0,0)
whiteColor = (255,255,255)
black_alpha = (0,0,0,150)
white_alpha = (255,255,255,150)
pieceScale = .5 #Scaling of the piece based on the square size (.5 = 50% size)

default_distance = 999
minimum_distance_w = default_distance
minimum_distance_b = default_distance

white_captures = 0
black_captures = 0

#LAST BOARD POSITION (KO RULE)
zobrist = []
last_hash = 0
hashes = []

#GROUPS (AI)
chains = []
influence = []
liberties = []
weighting = []

turn = 1 #1 black , 2 white
FPS = 60

# easier way to make transparent overlay (hover piece)
def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

def update_groups(): #TO BE IMPLEMENTED
    global groups
    for r in range(0, len(board)):
        for c in range(0,len(board[0])):
            if board[r][c] == W:
                return
            elif board[r][c] == B:
                return
            else:
                return

def update_liberties():
    #TO BE IMPLEMENTED
    return

def random_point():
    return (randint(0,19), randint(0,19))

def zobrist_table():
    z = [[[randint(1,2**64-1) for player in range(0,2)] for row in range(0, row_squares)] for col in range(0,col_squares)]
    return z

def get_hash(pos): #Unsure if this is useful whatsoever
    h = 0
    for r in range(pos):
        for c in range(pos[0]):
            if pos[r][c] != E:
                h ^= zobrist[r][c][pos[r][c]]
    return h

def remove_hash(rp, remove_pos, hash_):
    #Add is 2d-array, Remove is a 2d-array,
    #eg. update_hash(W, (3,4), B, [(3,3), (4,3)], 34298392)
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

def check_hash(h): #Yes, this does not serve much purpose. BUT it is easier to read
    if h in hashes:
        return True
    else:
        return False

def possible_moves(): #TO BE IMPLEMENTED
    
    return

def area_score():
    score = score_board_flood()
    black_p = 0
    white_p = 0
    for r in range(0, score):
        for c in range(0,score[0]):
            if score[r][c] == B:
                black_p +=1
            elif score[r][c] == W:
                white_p +=1
    return (black_p, white_p)

def score_board_distance(): #YEt ANOTHER VERSION
    global visited_squares
    experimental_scores = [[0 for r in range(0,row_squares)] for c in range(0, col_squares)]
    for r in range(0, row_squares):
        for c in range(0,col_squares):
            if board[r][c] == E:
##                visited_squares = [[0 for r in range(0,row_squares)] for c in range(0, col_squares)]
##                reset_minimum_distance()
##                experimental_scores[r][c] = check_distance_color(r,c)
                experimental_scores[r][c] = distance(r,c)
            else:
                experimental_scores[r][c] = board[r][c]
    return experimental_scores

def score_board_flood(): #OTHER VERSION
    global visited_squares
    experimental_scores = [[0 for r in range(0,row_squares)] for c in range(0, col_squares)]
    
    for r in range(0, row_squares):
        for c in range(0,col_squares):
            if board[r][c] == E:
                visited_squares = [[0 for r in range(0,row_squares)] for c in range(0, col_squares)]
                experimental_scores[r][c] = check_empty_color(r,c)
            else:
                experimental_scores[r][c] = board[r][c]
    return experimental_scores

def score_board(): 
    #IDEA - ONE POINT TOWARD BLACK/WHITE PER SQUARE, UTILIZE EVAL PER SQ
    global visited_squares
    experimental_scores = [[0 for r in range(0,row_squares)] for c in range(0, col_squares)]
    for r in range(0, row_squares):
        for c in range(0,col_squares):
            if board[r][c] == E:
                visited_squares = [[0 for r in range(0,row_squares)] for c in range(0, col_squares)]
                result = flood_square(r,c,0)
                if (result > 0):
                    experimental_scores[r][c] = W
                elif result < 0:
                    experimental_scores[r][c] = B
                else:
                    experimental_scores[r][c] = E
            else:
                experimental_scores[r][c] = board[r][c]
    return experimental_scores

def flood_square(x,y,current_score): # black -1 white +1, eval positive or negative EXPERIMENTAL, NOT FOR SCORING AT END OF GAME
    score = current_score

    if visited_squares[x][y] == 1:
        return score
    else:
        visited_squares[x][y] = 1


    if board[x][y] == B:
        score -= 1
        return score
    elif board[x][y] == W:
        score+=1
        return score
    else:
        left = flood_square(x-1,y,score) if x > 0  else 0
        right = flood_square(x+1, y, score) if x<row_squares-1 else 0
        up = flood_square(x, y-1, score) if y > 0  else 0
        down = flood_square(x,y+1,score) if y<col_squares-1 else 0
        score += left
        score += right
        score+= up
        score+= down
        return score
        
        

def click(x,y):
    global turn, board, white_captures, black_captures, hashes, last_hash
    square = board[x][y]
    if square == E:
        board[x][y] = turn
        turn = 3-turn #Flips player turn from 1 to 2 or vice versa (Next turn)

        captures = 0
        captured = check_captures(turn)

        for r in range(0,len(board)):
            for c in range(len(board[0])):
                if captured[r][c] == 1:
                    board[r][c] = E
                    captures+=1
        if captures == 0:
            h = add_hash_one(3-turn, [x,y], last_hash)
        else:
            h = add_hash_one(3-turn, [x,y], last_hash)
            h = remove_hash(turn, captured, h)


        possible_captured = check_captures(3-turn)
        if check_hash(h) or any(1 in sublist for sublist in possible_captured):
            print("Ko spotted! Or self capture.")
            for r in range(0, len(board)):
                for c in range(len(board[0])):
                    if captured[r][c] == 1:
                        board[r][c] = turn
            board[x][y] = E
            h = last_hash
            turn = 3-turn
            hashes.append(h)
        else:
            hashes.append(h)
            last_hash = h
        
            if turn == B:
                white_captures += captures
            else:
                black_captures += captures
        

def flood_fill(x,y, color):
    if visited_squares[x][y] == 1:
        return False
    else:
        visited_squares[x][y] = 1
    if board[x][y] == E:
        return True #not completely surrounded, thus alive
    elif board[x][y] != color:
        return False #hit a opposite colored square
    else:
        live = x > 0 and flood_fill(x-1,y, color)
        live|= x<row_squares-1 and flood_fill(x+1, y, color)
        live|= y > 0 and flood_fill(x, y-1, color)
        live|= y<col_squares-1 and flood_fill(x,y+1,color)
        return live

def check_empty_color(x,y):
    global visited_squares
    if flood_fill_empty(x,y,W):
        return W
    visited_squares = [[0 for r in range(0,row_squares)] for c in range(0, col_squares)]
    if flood_fill_empty(x,y,B):
        return B
    return E

def flood_fill_empty(x,y,color):
    if visited_squares[x][y] == 1:
        return True
    else:
        visited_squares[x][y] = 1
        
    if board[x][y] == color:
        return True 
    elif board[x][y] == E:
        live = True
        if x>0:
            live = flood_fill_empty(x-1,y, color)
        if x<row_squares-1:
            live&=flood_fill_empty(x+1, y, color)
        if y > 0:
            live&=flood_fill_empty(x, y-1, color)
        if y<col_squares-1:
            live&=flood_fill_empty(x,y+1,color)
##        live = x > 0 and flood_fill_empty(x-1,y, color)
##        live&= x<row_squares-1 and flood_fill_empty(x+1, y, color)
##        live&= y > 0 and flood_fill_empty(x, y-1, color)
##        live&= y<col_squares-1 and flood_fill_empty(x,y+1,color)
        return live
    else:
        return False

def check_distance_color(x,y):
    flood_fill_distance(x,y, 0)
    if minimum_distance_w > minimum_distance_b:
        return B
    elif minimum_distance_b > minimum_distance_w:
        return W
    else:
        return E

def reset_minimum_distance():
    global minimum_distance_w, minimum_distance_b
    minimum_distance_w = default_distance
    minimum_distance_b = default_distance
    
def flood_fill_distance(x,y, dist):
    global minimum_distance_w, minimum_distance_b
    if visited_squares[x][y] == 1:
        return
    else:
        visited_squares[x][y] = 1
    if dist >= minimum_distance_w or dist >= minimum_distance_b:
        return
    if board[x][y] == W:
        minimum_distance_w = dist
        return
    if board[x][y] == B:
        minimum_distance_b = dist
        return
    else:
        if x>0:
            flood_fill_distance(x-1,y, dist+1)
        if x<row_squares-1:
            flood_fill_distance(x+1, y, dist+1)
        if y > 0:
            flood_fill_distance(x, y-1, dist+1)
        if y<col_squares-1:
            flood_fill_distance(x,y+1, dist+1)

def distance(x,y): #Spight Influence Model (wavefront analysis, or just distance in simple terms)
    minimum_distance = 999
    color = E
    for r in range(0,row_squares):
        for c in range(0,col_squares):
            if board[r][c] != E:
                d = dist(x,y,r,c)
                if d<minimum_distance:
                    minimum_distance = d
                    color = board[r][c]
                elif d == minimum_distance and color != board[r][c]:
                    color = E
    return color

def dist(a,b,c,d):
    return abs(c-a)+abs(d-b)

##def zobrist_influence(repetitions):
##    influence = [[elem*50 for elem in row_squares] for row_squares in board]
##    for i in range(0,repetitions):
##        for r in range(0, row_squares):
##            for c in range(0, col_squares):
##                

def check_captures(color):
    global board, visited_squares, black_captures
    removed_squares = [[0 for c in range(col_squares)] for r in range(row_squares)] #0 - not 1 - captured
    for r in range(0, len(board)):
        for c in range(0,len(board[0])):
            if board[r][c] == color:
                visited_squares = [[0 for c in range(col_squares)] for r in range(row_squares)]
                if not flood_fill(r,c,color):
                    removed_squares[r][c] = 1

    return removed_squares




def setup(): 
    global board, window, gameRunning, first_click, num_flags, zobrist, hashes
    gameRunning = True
    pygame.init()
    window = pygame.display.set_mode((width, height))
    window.fill((242,176,109))
    board = [[E for c in range(col_squares)] for r in range(row_squares)]
    visited_squares = [[0 for c in range(col_squares)] for r in range(row_squares)]
    zobrist = zobrist_table()
    hashes = []


def main():
    setup()
    clock = pygame.time.Clock()
    hover_row = 0
    hover_col = 0
    alpha = 150 #Transparency of the hover piece
    
    stat_font = pygame.font.SysFont("georgia", 20)
    text_buffer = 20

    is_displaying_experimental_score = False
    score_type = 0
##    score = score_board()
##    score = score_board_flood()
    score = score_board_distance()

    while gameRunning:
        window.fill((242,176,109))
        if turn == B:
            pieceColor = blackColor
            alphaColor = black_alpha
        else:
            pieceColor = whiteColor
            alphaColor = white_alpha

        #draw stat screen
        stat_screen = pygame.Rect(side_x, vert_buffer, side_w, height-2*vert_buffer)
        pygame.draw.rect(window, (0,0,0), stat_screen)

        turn_string = "Black To Play" if turn == B else "White to Play"
        turn_text = stat_font.render("Current Turn: "+turn_string, True, "aqua")
        turn_rect = pygame.Rect(side_x+text_buffer, vert_buffer+text_buffer, side_w, 30)
        window.blit(turn_text, turn_rect)

        wcapture_text = stat_font.render("White Captures: "+str(white_captures), True, "aqua")
        wcapture_rect = pygame.Rect(turn_rect.x, turn_rect.y+turn_rect.height+text_buffer, side_w, turn_rect.height)
        window.blit(wcapture_text, wcapture_rect)

        bcapture_text = stat_font.render("Black Captures: "+str(black_captures), True, "aqua")
        bcapture_rect = pygame.Rect(turn_rect.x, wcapture_rect.y+wcapture_rect.height+text_buffer, side_w, wcapture_rect.height)
        window.blit(bcapture_text, bcapture_rect)

        
        score_text = "distance" if score_type == 0 else "flood" if score_type ==1 else "density"
        experimental_score_text = stat_font.render("Score: "+score_text, True, "aqua")
        experimental_score_rect = pygame.Rect(bcapture_rect.x, bcapture_rect.y+bcapture_rect.height+text_buffer, side_w, bcapture_rect.height)
        window.blit(experimental_score_text, experimental_score_rect)

        #draw grid
        for r in range(0, len(board)):
            pygame.draw.line(window, (0,0,0), (hor_buffer+r*square_size, vert_buffer), (hor_buffer+r*square_size, square_size*col_squares-vert_buffer))
        for c in range(0, len(board[0])):
            pygame.draw.line(window, (0,0,0), (hor_buffer, vert_buffer+c*square_size), (square_size*row_squares-hor_buffer, vert_buffer+c*square_size))
    
        #get mouse
        mousex, mousey = pygame.mouse.get_pos()

        if mousex > 0 and mousex < row_squares * square_size and mousey > 0 and mousey < col_squares * square_size:
            hover_row = int(mousex//square_size)
            hover_col = int(mousey//square_size)
            
        #draw pieces on board
        for r in range(0, len(board)):
            for c in range(0,len(board[0])):
                if r == hover_row and c == hover_col:
                    draw_circle_alpha(window, alphaColor, (hor_buffer + square_size*hover_row, vert_buffer+square_size*hover_col),square_size*pieceScale)
                if r in mark_points_r and c in mark_points_c:
                    mark = pygame.Rect(0,0,square_size*mark_scale, square_size*mark_scale)
                    mark.center = (hor_buffer+square_size*r, vert_buffer+square_size*c)
                    pygame.draw.rect(window, blackColor, mark)
                if board[r][c] == B:
                    pygame.draw.circle(window, blackColor, (hor_buffer+square_size*r, vert_buffer+square_size*c), square_size*pieceScale)
                if board[r][c] == W:
                    pygame.draw.circle(window, whiteColor, (hor_buffer+square_size*r, vert_buffer+square_size*c), square_size*pieceScale)

        
        if is_displaying_experimental_score:
            for r in range(0, len(board)):
                for c in range(0, len(board[0])):
                    if score[r][c] == B:
                        draw_circle_alpha(window, black_alpha, (hor_buffer + square_size*r, vert_buffer+square_size*c),square_size*pieceScale)
                    elif score[r][c] == W:
                        draw_circle_alpha(window, white_alpha, (hor_buffer + square_size*r, vert_buffer+square_size*c),square_size*pieceScale)

                        
                        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click(hover_row, hover_col) #Click and Update board
                    if score_type==0:
                        score = score_board_distance()
                    elif score_type == 1:
                        score = score_board_flood()
                    else:
                        score = score_board()

##                    score = score_board()
##                    score = score_board_flood()

                if event.button == 3:
                    is_displaying_experimental_score = not is_displaying_experimental_score
            if event.type==pygame.KEYDOWN:
                if score_type==0:
                    score = score_board_flood()
                    score_type +=1
                elif score_type==1:
                    score_type+=1
                    score = score_board()
                elif score_type==2:
                    score_type = 0
                    score = score_board_distance()
        pygame.display.update()
            
main()
