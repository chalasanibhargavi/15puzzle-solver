"""
                                     ###### 15 Puzzle Solver ######
    The following code takes an intial configuration of the 15 puzzle from the user and gives a short set of moves
    to reach the following goal configuration:

    1 2 3 4
    5 6 7 8
    9 10 11 12
    13 14 15 0

    This puzzle has an option to slide multiple tiles in one move which creates a larger number of successors for
    each board configuration.

    Command line input: File name containing the initial board configuation.

    Search algorithm implemented: A-Star

    Heuristics considered:
    1. Misplaced tiles
    2. Manhattan distance
    3. Manhattan distance with linear conflict
    4. Disjoint pattern matching

    Heuristic implemented: Manhattan distance with linear conflict

    IMPORTANT NOTE: For more details please refer to the problem3_writeup.pdf file

"""


from heapq import *
#import sys
from datetime import datetime
#import time

##Function to get the initial board
def get_board(fname):
    file_inp = open(fname, "r")
    initial_board = []
    for line in file_inp.readlines():
        l1 = line.replace('\n','').split(' ')
        l1_cast = [int(i) for i in l1]
        initial_board.append(l1_cast)

    return initial_board

#########Define heuristic functions #########

## Heuristic to get the Manhattan distance
def heuristic_mhd(board):
    #Manipulate the board values to get a pattern among rows and columns

    distance = 0
    N = 4
    for r in range(N):
        for c in range(N):

            if board[r][c] != 0:
                x_val = (board[r][c] - 1) / N
                y_val = (board[r][c] - 1) % N

                x_dist = abs(r - x_val)
                y_dist = abs(c - y_val)

                distance += (x_dist + y_dist)

    return float(distance)/3

## Heuristic to get the number of misplaced tiles
def heuristic_mt(board):

    #exp_val = goal_state[0][0]
    exp_val = 1
    misplaced = 0

    for r in range(4):
        for c in range(4):
            if board[r][c]!= exp_val:
                misplaced += 1
            exp_val += 1
    if board[3][3] == 0:
        misplaced -= 1

    return float(misplaced)/3

## Heuristic to calculate the number of linear conflicts
#Each tile in conflict are considered for the count
def heuristic_lf(board):
    lf_count = 0

    #Row conflicts
    for r in range(4):
        lcr_list = []
        for c in range(4):
            if board[r][c] != 0:
                x_val = (board[r][c] - 1) / 4

                if x_val == r:
                    lcr_list.append(board[r][c])

                for j in range(len(lcr_list)-1):
                    if lcr_list[j] > lcr_list[j+1]:
                        lf_count+=2

    #Column conflicts
    for c in range(4):
        lcc_list = []
        for r in range(4):
            if board[r][c] != 0:
                y_val = (board[r][c] - 1) % 4

                if y_val == c:
                    lcc_list.append(board[r][c])

                for j in range(len(lcc_list)-1):
                    if lcc_list[j] > lcc_list[j+1]:
                        lf_count += 2

    return float(lf_count)/3

## Heuristic: Manhattan distance + Linear conflicts
def heuristic_mhd_lf(board):

    return heuristic_mhd(board) + heuristic_lf(board)


##Function to implement a* search
def solve_astar3(initial_board, goal_state):
    if initial_board == goal_state:
        return (initial_board)

    fringe = []
    fringe_set = [] #Fringe board list for faster lookup
    closed = []
    closed_set = [] #Closed board list for faster lookup
    cskip_i = 0 # Count of number of nodes skipped because already expanded

    eval_initial = 0
    heappush(fringe, (eval_initial, ("",initial_board))) #Push initial board to fringe
    fringe_set.append(initial_board)

    while len(fringe) > 0:

        ##Pop the item with the least cost in the fringe
        s1 = heappop(fringe)
        cost_g = s1[0]/3 #Cost to reach the present state, scaled down to be inline with heuristic range

        #Remove from fringe lookup
        fringe_set = [x for x in fringe_set if x !=s1[1][1]]

        ##Check goal state
        if s1[1][1] == goal_state:
            print "Number of nodes skipped: ",cskip_i

            #Return final set of moves
            print "Final set of moves: "
            return s1[1][0].strip(" ")

        ##Add visited states to closed
        heappush(closed, (eval_initial, ("", initial_board)))
        closed_set.append(s1[1][1])

        #Build successors based on valid moves
        for s2_tuple in successors(s1[1][1]):

            #Calculate evaluation function
            eval_new = cost_g + (heuristic_mhd_lf(s2_tuple[1])- heuristic_mhd_lf(s1[1][1]))
            #Heuristic was used to represent the distance between current state and successor such that lowest distance is prioritized

            ##If s2 in closed skip
            if s2_tuple[1] in closed_set:
                cskip_i +=1 #Count number of nodes skipped
                continue

            else:
                if s2_tuple[1] in fringe_set:
                    for i in range(len(fringe)):
                        if fringe[i][1][1] == s2_tuple[1]:
                            eval_old = fringe[i][0]
                            if eval_new < eval_old:
                                del fringe[i]

                                new_path = str(s1[1][0]) + " " + s2_tuple[0]
                                new_board = s2_tuple[1]
                                s3_tuple = (new_path, new_board)
                                heappush(fringe, (eval_new,s3_tuple))

                            break
                else:
                    new_path = str(s1[1][0]) + " " + s2_tuple[0]
                    new_board = s2_tuple[1]
                    s3_tuple =  (new_path,new_board)
                    heappush(fringe, (eval_new, s3_tuple))
                    fringe_set.append(s2_tuple[1]) #Add to fringe lookup

    return False

##Sliding tiles by moving the empty tile
def move_empty_tile(board, move, n, row, col):
    if move == 'L':
        return ("R"+str(n)+str(row+1), board[0:row] + [board[row][0:col-n] + [0,] + board[row][col-n:col] + board[row][col+1:]] + board[row+1:])
    elif move == 'R':
        return ("L"+str(n)+str(row+1), board[0:row] + [board[row][0:col] + board[row][col+1:col+n+1] + [0,]+ board[row][col+n+1:]] + board[row+1:])
    elif move == 'U':
        updated_urows = []
        for i in range(1,n+1):
            updated_urows.append(board[row-n+i][0:col]+[board[row-n+i-1][col]]+board[row-n+i][col+1:])

        return ("D"+str(n)+str(col+1),board[0:row-n] + [board[row-n][0:col]+[0,]+board[row-n][col+1:]] + updated_urows + board[row+1:])
    else:
        updated_drows = []
        for i in range(1, n+1):
            updated_drows.append(board[row+i-1][0:col] + [board[row+i][col]] + board[row+i-1][col+1:])

        return ("U"+str(n)+str(col+1), board[0:row] + updated_drows + [board[row+n][0:col] + [0,] + board[row+n][col+1:]] +  board[row+n+1:])



def successors(board):
    #Define set of possible moves
    #Append path of the move and return it with output
    succ_list = []

    for r in range(4):
        for c in range(4):
            if board[r][c] == 0:
                (erow,ecol) = (r,c)
                break

    #Move left
    if ecol > 0:
        for m in range(1,ecol+1):

            succ_list.append(move_empty_tile(board, 'L', m, erow, ecol))

    #Move right
    if ecol < 3:
        for m in range(1, 4-ecol):
            succ_list.append(move_empty_tile(board, 'R', m, erow, ecol))

    #Move up
    if erow > 0:
        for m in range(1,erow+1):
            succ_list.append(move_empty_tile(board, 'U', m, erow, ecol))

    #Move down
    if erow < 3:
        for m in range(1,4-erow):
            succ_list.append(move_empty_tile(board, 'D', m, erow, ecol))

    return succ_list

## Get the initial board
initial_board = get_board("input3.txt")
print "Initial board ",initial_board

## Required goal state
goal_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

print solve_astar3(initial_board, goal_state)
