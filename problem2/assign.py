#!/usr/bin/env python3
# assign.py : Given n number of students with their preferences, assign them to teams such that overall time for
#             grading the assignment is minimum.
# Team - Ankita Alshi, Bhargavi Chalasa, Dheeraj Singh, 2017
#
# Comments:


import sys
import datetime

# Create result string to print the final teams in required output format
def print_sol(board):
    result = ""
    for row in board:
        for col in row:
            result += col
            result += " "
        if (not (len(row) == 0 or (len(board) == board.index(row) + 1) )):
            result += "\n"
    return result

def trim(board):
    s = []
    for each_row in board:
        if (not each_row == []):
            s.append(each_row)
    return s

# Remove student from ith team and add him to nth team
def add_student(board, n, i, student):
    s = [[val for val in row] for row in board]
    s[n].append(student)
    s[i].remove(student)
    return s

# Calculate number of students assign to team size other than their preference
def wrong_team_size(team):
    count = 0
    for mem in team:
        index = listuserid.index(mem)
        prefteam = listdict[index]['teamnum']
        if (not (prefteam == "0")):
            if (not (str(len(team)) == prefteam)):
                count += 1
    return count

# Calculate number of students who did not get team members of their choice
def notgotwanted(team):
    count = 0
    for memi in team:
        indexi = listuserid.index(memi)
        for memj in listdict[indexi]['wantedmem']:
            if (memj not in team):
                count += 1              
    return count

# Calculate number of student who got team member that they did not wanted to work with
def gotunwanted(team):
    count = 0
    for memi in team:
        indexi = listuserid.index(memi)
        for memj in listdict[indexi]['unwantedmem']:
            if (memj in team):
                count += 1
    return count

# Define initial team arrangement as one student per team
def initial_board():
    for student in listuserid:
        initial.append([student])
    return [val for val in initial]

# Find the successor with lowest cost
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

# Calculate cost for a team
def cost_team(team):
    if (len(team) == 0):
        return 0
    else:
        number_wrongteamnum = wrong_team_size(team)
        number_notgotwanted = notgotwanted(team)
        number_gotunwanted = gotunwanted(team)
        cost = k + (1 * number_wrongteamnum) + (n * number_notgotwanted) + (m * number_gotunwanted)
    return cost

# Calculate total cost for given arrangement of teams
def tot_cost(board):
    total_cost = 0
    for row in board:
        if (not len(row) == 0):
            total_cost += cost_team(row)
    return total_cost

# Create successors by adding students to different teams
def successor(board, i):
    move_student = board[i][0]
    succ = []
    for n in range(len(board)):
        if (not i == n):
            curr_size = len(board[n])
            if (curr_size > 0 and curr_size < 3):
                 temp = add_student(board, n, i, move_student)
                 if (tot_cost(temp) <= curr_cost):
                     succ.append(temp)
    return succ

# Solve the problem recursively till all the team members of ith team are assigned to other teams
def recur_solve(s, i):
    if(not len(s[i]) == 0):
        for x in successor(s, i):
            fringe.append(x)
            recur_solve(x, i)
    return

# Solve the problem by adding team member from ith team to other teams to find minimum cost
def solve():
    global fringe, curr_cost
    fringe = [initial_board()]
    s = getmin(fringe)
    for i in range(rows):
        curr_cost = tot_cost(s)
        recur_solve(s, i)
        s = getmin(fringe)
        fringe = [s]
    return s 

# Store student preference to work with each other. (used to calculate the cost of a team) 
def storepref():
    for i in range(0, len(listuserid)):
        for j in range(0, len(listuserid)):
            if (i == j):
                mem_pref[i][j] += 1
            else:
                if (listuserid[j] in listdict[i]['unwantedmem']):
                    mem_pref[i][j] = -1
                elif (listuserid[j] in listdict[i]['wantedmem']):
                    mem_pref[i][j] += 1

# Storin input data from file to dictionary
def filetodict():
    for a in ifile:
        line = a.split()
        d = {'userid': line[0], 'teamnum': line[1], 'wantedmem': line[2].split(","), 'unwantedmem': line[3].split(",")}
        if (line[2] == "_"):
            d['wantedmem'] = []
        if (line[3] == "_"):
            d['unwantedmem'] = []
        listdict.append(d)
    return

# Input from command line: 1. input file1                     2. Time taken to grade one team 
#                          3. time taken to answer mail query 4. time for a meeting to resolve issue
filename = sys.argv[1]
k = int(sys.argv[2])
n = int(sys.argv[3]) 
m = int(sys.argv[4])

# Open input file containing student userid with their preferences
ifile = open(filename, "r")

# List of Dictionaries to store input values
listdict = []
filetodict()

# List of userids given
listuserid = [a['userid'] for a in listdict]

# Student preference stored in N*N list (where N is number of userids)
rows = cols = len(listdict)
mem_pref = [[0 for j in range(cols)] for i in range(rows)]
storepref()

# Solve the the problem and print final list of team with the time required to grade them.
initial = []
goal = solve()
print (print_sol(trim(goal)))
print (tot_cost(goal)) 
