#!/usr/bin/env python3
# a0.py : Solve the N-Queens and N-Rooks problem!
# Ankita Alshi, 2017

# Input from command line: 1. input file1                     2. Time taken to grade one team 
#                          3. time taken to answer mail query 4. time for a meeting to resolve issue

import sys
import datetime

def print_sol(board):
    result = ""
    for row in board:
        for col in row:
            result += col
            result += " "
        if (not (len(row) == 0 or (len(board) == board.index(row) + 1) )):
            result += "\n"
    return result

def iscosteff(student, team):
    indexi = listuserid.index(student)
    for mem in team:
        indexj = listuserid.index(mem)
        if (mem_pref[indexi][indexj] == -1 or mem_pref[indexj][indexi] == -1):
            return False
    return True

def add_student(board, n, i, student):
    s = [[val for val in row] for row in board]
    s[n].append(student)
    s[i].remove(student)
    return s

def wrong_team_size(team):
    count = 0
    for mem in team:
            index = listuserid.index(mem)
            if (not listdict[index]['teamnum'] == 0):
                if (not (len(team) == listdict[index]['teamnum'])):
                    count += 1
    return count

def notgotwanted(team):
    count = 0
    for memi in team:
        indexi = listuserid.index(memi)
        if (not len(listdict[indexi]['wantedmem']) == 0):
            for memj in team:
                indexj = listuserid.index(memj)
                if (not mem_pref[indexi][indexj] == 1):
                        count += 1
    return count

def gotunwanted(team):
    count = 0
    for memi in team:
        indexi = listuserid.index(memi)
        for memj in team:
            indexj = listuserid.index(memj)
            if (mem_pref[indexi][indexj] == -1):
                        count += 1
    return count

def initial_board():
    for student in listuserid:
        initial.append([student])
    return [val for val in initial]

def getmin(board_list):
    for x in range(len(board_list)):
        if (x == 0):
            mincost = tot_cost(board_list[x])
            minindex = x
        else:
            curr_cost = tot_cost(board_list[x])
            if (curr_cost < mincost):
                mincost = tot_cost(board_list[x])
                minindex = x
    return board_list[minindex]

def cost_team(team):
    if (len(team) == 0):
        return 0
    else:
        number_wrongteamnum = wrong_team_size(team)
        number_notgotwanted = notgotwanted(team)
        number_gotunwanted = gotunwanted(team)
        cost = k + (1 * number_wrongteamnum) + (n * number_notgotwanted) + (m * number_gotunwanted)
    return cost

def tot_cost(board):
    total_cost = 0
    for row in board:
        if (not len(row) == 0):
            total_cost += cost_team(row)
    return total_cost

def successor(board, i):
    move_student = board[i][0]
    succ = []
    for n in range(len(board)):
        if (not i == n):
            curr_size = len(board[n])
            if (curr_size > 0 and curr_size < 3 and iscosteff(move_student, board[n])):
                succ.append(add_student(board, n, i, move_student))                          
    return succ
        
def solve():
    fringe = [initial_board()]
    s = getmin(fringe)
    for i in range(rows):
        if(not len(s[i]) == 0):
            for x in successor(s, i):
                fringe.append(x)
                if (not len(x[i]) == 0):
                    for y in successor(x, i):
                        fringe.append(y)
                        if (not len(y[i]) == 0):
                            for z in successor(y, i):
                                fringe.append(z)
        s = getmin(fringe)
        fringe = [s]
    return s


filename = sys.argv[1]
k = int(sys.argv[2])
n = int(sys.argv[3]) 
m = int(sys.argv[4])

ifile = open(filename, "r")
listdict = []
initial = []

for a in ifile:
    line = a.split()
    d = {'userid': line[0], 'teamnum': line[1], 'wantedmem': line[2].split(","), 'unwantedmem': line[3].split(",")}
    if (line[2] == "_"):
        d['wantedmem'] = []
    if (line[3] == "_"):
        d['unwantedmem'] = []
    listdict.append(d)

rows = cols = len(listdict)
mem_pref = [[0 for j in range(cols)] for i in range(rows)]

listuserid = [a['userid'] for a in listdict]

for i in range(0, len(listuserid)):
    for j in range(0, len(listuserid)):
        if (i == j):
            mem_pref[i][j] += 1
        else:
            if (listuserid[j] in listdict[i]['unwantedmem']):
                mem_pref[i][j] = -1
            elif (listuserid[j] in listdict[i]['wantedmem']):
                mem_pref[i][j] += 1

goal = solve()
print (print_sol(goal))
print (tot_cost(goal))




            
                    
 
