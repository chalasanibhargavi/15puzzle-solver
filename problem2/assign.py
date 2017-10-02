#!/usr/bin/env python3
# assign.py : Given n number of students with their preferences, assign them to teams such that overall time for
#             grading the assignment is minimum.
# Team - Ankita Alshi, Bhargavi Chalasa, Dheeraj Singh, 2017
#
# Comments:
# Search Problem: write a program to find an assignment of students to teams that minimizes the total amount of 
# work the course staff needs to do, subject to the constraint that no team may have more than 3 students.
#
# (1)State Space: Maximum N teams with combination of not more than 3 students per team. (where N is number of students)
# Initial State: board arrangement having N teams, each team having one student. (where N is number of students)
# Goal State: Set of teams such that all students belong to a team and every team contains max 3 students with least amount of work required.
# Successor: It creates new combination teams removing one student from a team and adds it to others. 
# Cost: Cost is total cost to grade all the teams for given arrangement of teams
#
# (2) Search Algorithm: We have used beam search algorithm to solve this problem. Instaed of randomly initializing first set of states, we are 
# starting with a board having N teams with one student per team. For this beam search the value of k for the loop we have taken as N (where N is
# number of students). We are also using fringe in form of heap queue and selecting 2 states from heapqueue with least cost. Then the successors
# of those two states are created and added to heapqueue. And we are not checking goal state in each loop. the goal state is the arrangement of teams
# with least cost present in heap queue after N loops are done.
#
# (3) As number of student increases (N>100) the algorithm was taking a lot of time if we take 2 nsmallest states from heap queue, so for larger
# number students we are taking only 1 smallest cost state to pass on to the successor function.
#
# References:
# We have referenced following link to understand heapqueue implementation:
# https://docs.python.org/3.0/library/heapq.html#heapq.nsmallest
# We have referenced following links for List and dictionary methods:
# https://www.tutorialspoint.com/python/python_lists.htm
# https://www.tutorialspoint.com/python/python_dictionary.htm
#

from heapq import *
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
    return initial

# Calculate cost for a team
def cost_team(team):
    if (len(team) == 0):
        return 0
    else:
        cost = k + (1 * wrong_team_size(team)) + (n * notgotwanted(team)) + (m * gotunwanted(team))
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
                 succ_cost = tot_cost(temp)
                 if (succ_cost <= curr_cost):
                     succ.append([succ_cost, temp])
    return succ

# Solve the problem recursively till all the team members of ith team are assigned to other teams
def recur_solve(s, i):
    if(not len(s[i]) == 0):
        for x in successor(s, i):
            heappush(fringe, (x[0], x[1]))
            recur_solve(x[1], i)
    return

# Solve the problem by adding team member from ith team to other teams to find minimum cost
def solve():
    global fringe, curr_cost
    smin = []
    fringe = []
    s = initial_board()
    curr_cost = tot_cost(s)
    heappush(fringe, (curr_cost, s))
    for i in range(rows):
        if (i == 0):
            recur_solve(s, i)
        else:
            for each in smin:
                curr_cost = each[0]
                s = each[1]
                heappush(fringe, (curr_cost, s))
                recur_solve(s, i)
                
        if (i == rows-1):
            curr_cost, s = heappop(fringe)
        else:
            smin = nsmallest(nsmall, fringe)
    return s 

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
rows = cols = len(listdict)
if (rows > 50):
    nsmall = 1
else:
    nsmall = 2

# Solve the the problem and print final list of team with the time required to grade them.
initial = []
goal = solve()
print (print_sol(trim(goal)))
print (tot_cost(goal))
