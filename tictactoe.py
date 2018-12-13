# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 18:33:05 2018

@author: honlin
"""

from projectq import MainEngine  # import the main compiler engine
from projectq.ops import H,Z, X, CNOT, Entangle, Measure  # import the operations we want to perform
from projectq.backends import CircuitDrawer
import projectq.setups.ibm
from projectq.backends import IBMBackend

#---------Function-----------------#
def drawBoard(board):
 # This function prints out the board that it was passed.
 # "board" is a list of 10 strings representing the board (ignore index 0)
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')

def inputPlayerLetter():
# Let the player types which letter they want to be.
# Returns a list with the player 1’s letter as the first item, and player 2's letter as the second.
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        print('Do you want to be X or O?')
        letter = input().upper()
# the first element in the list is the player 1’s letter, the second is player 2's letter.
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def makeMove(board, letter, move):
    board[move] = letter
    
def isWinner(bo, le):
# Given a board and a player’s letter, this function returns True if that player has won.
# We use bo instead of board and le instead of letter so we don’t have to type as much.
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top
            (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
            (bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom
            (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
            (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
            (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
            (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
            (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal   

#---------Quantum Tic Tac Toe---------------------#
#First create a 3x3 board. Player 1 will choose a box first, while player 2 will choose another box.
#Create the following entanglement (|01>+|10>)\sqrt(2) on these 2 boxes. Then, measure 1 of the box
#The output determines if the box belongs to player 1 or player 2.   
#---------Create the 3x3 box---------------------#
print("PLayer 1, you can choose either cross or circle")
letter = inputPlayerLetter()
board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',' ']
drawBoard([' ','1','2','3','4','5','6','7','8','9'])
print("Number 1 to 9 represent the box")
winning_cond = False
while winning_cond == False:
    box1 = int(input('Player 1, please choose a box to tick:'))
    while box1 not in (1,2,3,4,5,6,7,8,9):
        print("Error. You can only number between 1 to 9")
        box1 = int(input('Player 1, please choose a box to tick:'))

    box2 = int(input('Player 2, please choose a box to cross:'))
    while box2 not in (1,2,3,4,5,6,7,8,9):
        print("Error. You can only number between 1 to 9")
        box2 = int(input('Player 2, please choose a box to cross:'))
        while box2 == box1:
            print("Error! You can't choose a box that has been chosen. Player 1 has chosen",box1)
            box2 = int(input('Player 2, please choose a box to cross:'))
            if box2 not in (1,2,3,4,5,6,7,8,9):
                print("Error. You can only number between 1 to 9")
                box2 = int(input('Player 2, please choose a box to cross:')) 
#--------Pass the 2 choices into quantum computer------#
    eng = MainEngine()  # create a default compiler (the back-end is a simulator)
    b1 = eng.allocate_qubit()
    b2 = eng.allocate_qubit()

#create a bell state |01>+|10>
    H | b1
    X | b2
    CNOT | (b1, b2)

#measure box1 and box2
    Measure | b1
    Measure | b2

    b1 = int(b1)
    b2 = int(b2)
#--------------Result ---------------#
#if b1 returns 0, the box belongs to player 1; if box1 returns 1, the box belongs to player 2
    if b1 == 0:
        makeMove(board,letter[0],box1)
        makeMove(board,letter[1],box2)
    else:
        makeMove(board,letter[1],box1)
        makeMove(board,letter[0],box2)
    drawBoard(board)
    winning_cond = isWinner(board,letter[0])
    if winning_cond == False:
        winning_cond = isWinner(board,letter[1])
    
if isWinner(board,letter[0]) == True:
    print("Congratulation! Player 1 won the game!")
else:
    print("Congratulation! Player 2 won the game!")
