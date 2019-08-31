# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 13:04:18 2018

@author: honlin
"""
import numpy as np
import qiskit,operator,math
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit,execute,Aer
from IPython.display import display
from sympy import init_printing,symbols
init_printing(use_latex = True)
from sympy.physics.quantum import *
from sympy.physics.quantum.qubit import *
from sympy.physics.quantum.gate import *
from sympy.physics.quantum.circuitplot import circuit_plot

#-------Quantum Simulator----------#
# Use Aer's qasm_simulator
simulator = Aer.get_backend('qasm_simulator')

# Create a 10 qubits Quantum Circuit acting on the q register(ignore 0th register due to index)
q = QuantumRegister(10)
c = ClassicalRegister(1)
qc = QuantumCircuit(q, c)

def drawbarrier():
    #draw a barrier after the end of each turn
    qc.barrier()
    
#---------Game interface-----------------#
def drawBoard(board):
 # This function prints out the board that it was passed.
 # "board" is a list of 10 strings representing the board (ignore index 0)
    print('   |   |')
    print(' ' + str(board[7]) + ' | ' + str(board[8]) + ' | ' + str(board[9]))
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + str(board[4]) + ' | ' + str(board[5]) + ' | ' + str(board[6]))
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + str(board[1]) + ' | ' + str(board[2]) + ' | ' + str(board[3]))
    print('   |   |')

def round_counter(Round):
    if player == 1:
        print("Round ",int(Round/2),",begin!")
        Round = Round + 1
    elif player == 2:
        print("Round ",int(math.floor(Round/2)),",begin!")
        Round = Round + 1
    return Round   
            
def unitarycounter(unitaryno,playermove):
    if playermove>-1 and playermove < 5:
        unitaryno = unitaryno + 1
    return unitaryno

def chooseBox():
    box = int(input("Choose a box: "))
    while box not in (1,2,3,4,5,6,7,8,9) or status[box] == 5:
        print("Error. You can only number between 1 to 9/box which has not been measured")
        box = int(input('Choose a box:'))
    return box

def ask_move(register0):
    print("Choose 2 unitary moves or measurement")
    print("0: 'Prepare a pure state qubit', 1: 'Hadamard gate',2: 'Pauli X gate', 3: 'Pauli Z gate',4: 'CNOT gate',5: measure")
    playermove = 1
    while playermove < 6 and playermove > -1:
        try:
            playermove = int(input("Choose a move:"))
            break
        except ValueError:
            print("Oops!  That's not a valid move. Try again...")
    register1 = 0
    #ask for control and target qubit if player chooses to play cnot
    if playermove == 4:
       choice = int(input('Do you want the chosen register to be control or target?(0 for control, 1 for target)'))
       while choice<0 or choice>2:
           print('You can only input either 0 or 1')
           choice = int(input('Do you want the chosen register to be control or target?(0 for control, 1 for target)'))          
       if choice == 1:
           register1 = register0
           register0 = int(input('Choose a control qubit:'))
       elif choice == 0:
           register1 = int(input('Choose a target qubit:'))
    return playermove,register0,register1

def ask_move_2nd(register0):
    print("Choose 1 more unitary move to act on box/register",register0," or end your turn now")
    print("1: 'Hadamard gate',2: 'Pauli X gate', 3: 'Pauli Z gate',4: 'CNOT gate',5:End turn ")
    playermove = 1
    while playermove < 6 and playermove > 0:
        try:
            playermove = int(input("Choose a move:"))
            break
        except ValueError:
            print("Oops!  That's not a valid move. Try again...")
    #ask for control and target qubit if player chooses to play cnot
    register1 =0 #target qubit
    if playermove == 4:
       choice = int(input('Do you want the chosen register to be control or target?(0 for control, 1 for target)'))
       while choice<0 or choice>2:
           print('You can only input either 0 or 1')
           choice = int(input('Do you want the chosen register to be control or target?(0 for control, 1 for target)'))          
       if choice == 1:
           register1 = register0
           register0 = int(input('Choose a control qubit:'))
       elif choice == 0:
           register1 = int(input('Choose a target qubit:'))
    return playermove,register0,register1

def print_move(i):
    switcher = {0: 'Prepare a pure state qubit',
                1: 'Hadamard gate',
                2: 'Pauli X gate',
                3: 'Pauli Z gate',
                4: 'CNOT gate',
                5: 'Measurement'}
    print('You are performing :',switcher.get(i))
    print(' ')


#-------Quantum Move-----------#
def move(i,player,register0,register1):
    #call the function based on the player's choice    
    if i == 0:
        pure_state(register0,player)
    elif i == 1:
        Hadamard(register0)
    elif i== 2:
        PauliX(register0)
    elif i== 3:
        PauliZ(register0)
    elif i == 4:
        CNOT(register0,register1)
    elif i == 5:
        measure(register0)
   
def Hadamard(register):
    qc.h(q[register])

def PauliX(register):
    qc.x(q[register])

def PauliZ(register):
    qc.z(q[register])

def CNOT(controlqubit,targetqubit):
    qc.cx(q[controlqubit],q[targetqubit])

def measure(register):
    #measure takes a qubit as input and perform measurement on Z basis
    qc.measure(q[register],c)
    job = execute(qc,simulator,shots = 1000)
    result = job.result()
    counts = result.get_counts(qc)
    print("\nTotal count for 0 and 1 are:",counts)
    return counts

def pure_state(register,player):
    if player == 2:
        qc.x(q[register])
        #the default qubit is |0>, for player 1, place a x gate to flip the qubit
         
#--------Condition Checking-------------------#
def update_board(move,register0):
    if move == 0:  #0 means empty, 1 means a qubit has been placed in the register
                   #5 means the qubit has been measured
        status[register0] = 1
    if move == 5:
        status[register0] = 5
         
def isvalidmove(move,register0,register1):
    #return false if the move is not valid, and print out the error message
    if move == 0:
        #check if the box is empty/has not been measured
        if status[register0] == 0:
            return True
        else:
            print('Invalid move: A qubit has been allocated to the box.')
            print(' ')
            return False
    elif move>0 and move<6:
        if move!= 4:
            #if not CNOT gate, check only the chosen register
            if status[register0] == 1:
                return True
            else:
                print('Invalid move: The register is empty/has been measured')
                print(' ')
                return False
        else: 
            #if CNOT gate, check both registers
            if status[register0] and status[register1] == 1 and register0 != register1:
                return True
            else:
                print('Invalid move: One of the register is empty/has been measured')
                print(' ')
                return False
            
def marker(result,board,register0):
    #mark the board based on the result
    if result == '0':
        board[register0] = 'O'
    elif result == '1':
        board[register0] = 'X'
    
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
board = [' ']*10 #board keeps track of the board status
global status
status = np.zeros(10)
letter = ['O', 'X']
drawBoard([' ','1','2','3','4','5','6','7','8','9'])
print("Number 1 to 9 represent the box")
winning_cond = False
Round = 0 #this is a counter to count which round we are in

#------------Pipeline--------------------#
while winning_cond == False:
    qc.draw()
    player = Round % 2 + 1
    print("Current board")
    drawBoard(board)
#-----------Choose box----------#
    Round = round_counter(Round)
    print("It's your turn now, player ", player)
    chosenbox = chooseBox()
    register0 = chosenbox 
#-----------Choose move---------#
    playermove,register0,register1 = ask_move(register0)

#---------Condtional checking------------------#
    validmove = isvalidmove(playermove,register0,register1)
    while validmove == False:
        playermove,register0,register1= ask_move(register0)
        validmove = isvalidmove(playermove,register0,register1)
    update_board(playermove,register0)
#---------Execute move----------------------#
     #projective
    if playermove == 5:
        print_move(playermove)
        counts = measure(register0)
        result = max(counts.items(), key=operator.itemgetter(1))[0]
        marker(result,board,register0)
#-----------Check winner-----------------#           
        if isWinner(board,letter[0]) == True:
            drawBoard(board)
            print("Congratulation! Player 1 won the game!")
            winning_cond = True 
        elif isWinner(board,letter[1]) == True:
            drawBoard(board)
            print("Congratulation! Player 2 won the game!")
            winning_cond = True 
    
        #unitary
    unitaryno = 0
    unitaryno = unitarycounter(unitaryno,playermove) #count the number of unitary move that has been made
    while unitaryno == 1:
        move(playermove,player,register0,register1)
        print_move(playermove)
        playermove,register0,register1 = ask_move_2nd(chosenbox)
        if playermove < 5:
            validmove = isvalidmove(playermove,register0,register1)
            while validmove == False:
                playermove,register0,register1= ask_move_2nd(chosenbox)
                validmove = isvalidmove(playermove,register0,register1)
            update_board(playermove,register0)
            move(playermove,player,register0,register1)  
            print_move(playermove)
        else:
            print('You have ended your turn.')
            print(' ')
        unitaryno = unitaryno + 1
    