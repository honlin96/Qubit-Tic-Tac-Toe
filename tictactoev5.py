# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 10:35:49 2019

@author: honlin
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 17:29:45 2019

@author: honlin
"""

import numpy as np
import math
#load_ext sympy.interactive.ipythonprinting
from IPython.display import display
from sympy import *
init_printing(use_latex = True)
from sympy.physics.quantum import *
from sympy.physics.quantum.qubit import *
from sympy.physics.quantum.gate import *
from sympy.physics.quantum.circuitplot import circuit_plot
from sympy.physics.quantum.gate import CNOT

#use qiskit to draw circuit
from qiskit import(
  QuantumCircuit,
  execute,
  Aer)
from qiskit.visualization import plot_histogram

# Use Aer's qasm_simulator
simulator = Aer.get_backend('qasm_simulator')
#Create a 9 register quantum circuit
global circuit
circuit = QuantumCircuit(9,9)

#-----------------------Interface Logic-----------------------------#
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
           register0 = int(input('Choose a control qubit(1-9):'))
       elif choice == 0:
           register1 = int(input('Choose a target qubit(1-9):'))
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
           register0 = int(input('Choose a control qubit(1-9):'))
       elif choice == 0:
           register1 = int(input('Choose a target qubit(1-9):'))
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
    
#--------------------Condition Checking and Bit Logic---------------------------#
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
                if status[register0] == 0 or status[register0] == 5:
                    print('Invalid move:Box ',register0 ,'is empty/has been measured')
                if status[register1] == 0 or status[register1] == 5:
                    print('Invalid move:Box ',register1 ,'is empty/has been measured')
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

#-------------------------Qubit Logic-----------------------#
def updatestate(player,register0,register1,playermove,qubit): 
    #register0 = control qubit, register1 = target qubit
    #update and print circuit
    if playermove == 0:
        if player == 2:
            qubit = qapply(X(register0-1)*qubit)
            circuit.x(register0-1)
    elif playermove == 1:
        qubit = qapply(H(register0-1)*qubit)
        circuit.h(register0-1)
    elif playermove == 2:
        qubit = qapply(X(register0-1)*qubit)
        circuit.x(register0-1)
    elif playermove == 3:
        qubit = qapply(Z(register0-1)*qubit)
        circuit.z(register0-1)
    elif playermove == 4:
        qubit = qapply(CNOT(register0-1,register1-1)*qubit)
        circuit.cx(register0-1,register1-1)
    elif playermove == 5:
        qubit = measure_partial_oneshot(qubit,(register0-1,))
        circuit.measure(register0-1,register0-1)
    # Execute the circuit
    return qubit

def measurement_result(qubit,register0):
    #return the measurement result after the collapse of state.
    if type(qubit) == Add:
        partial = measure_partial_oneshot(qubit.args[0],(register0-1,))
        classical = partial[register0-1]
        if classical == Qubit('0')[0]:
            classicalbit = '0'
            print('The qubit collapses to classical state 0')
        elif classical == Qubit('1')[0]:
            classicalbit = '1'
            print('The qubit collapses to classical state 1')
    else:
        if qubit[register0-1] == Qubit('0')[0]:
            classicalbit = '0'
            print('The qubit collapses to classical state 0')
        elif qubit[register0-1] == Qubit('1')[0]:
            classicalbit = '1'
            print('The qubit collapses to classical state 1')
    return classicalbit

def measure_all(qubit,board,status):
    #measure all qubits
    qubit = measure_all_oneshot(qubit)
    #update the board
    register = 0
    for i in qubit:
        #check board's status, if a qubit is prepared, then collapse to the state, else, ignore
        if i == Qubit('0')[0] and status[9-register] == 1:
            board[9-register] = 'O'
            circuit.measure(8-register,8-register) 
        elif i == Qubit('1')[0] and status[9-register] == 1:
            board[9-register] = 'X'
            circuit.measure(8-register,8-register) 
        register = register + 1
    return board
    
def qubitmapping(qubit):
    #evaluate the qubit(2 cases ->pure state/superposition state)
    displayqubitlist = []
    displayqubit = 0
    #print('Error checking:' , qubit) #error checking
    if type(qubit) == Add: #case 1: Superposition
        for element in qubit.args:
            index = 0
            ket = 0
            for x in status:
            #we only need to print the state if there is a qubit in the box
                if int(x) == 1:
                    if element.args[-1][index-1] == Qubit('0')[0]:
                        name = 'O'+ str(index)
                    else:
                        name = 'X' + str(index)
                    if ket == 0:
                        ket = Ket(name)
                    else:
                        ket = TensorProduct(ket,Ket(name))
                index = index + 1
            displayqubit = displayqubit + ket
    else:    #case 2 -> pure state
        #check the status of the board through for loop.
        counter = 0
        for element in status:
            if int(element) == 1:
                #if there is a qubit in the box, check if it is 0 or 1
                if qubit[counter-1] ==  Qubit('0')[0] :
                    name = 'O'+str(counter)
                    displayqubitlist = displayqubitlist + [Ket(name)]
                else :
                    name = 'X'+str(counter)
                    displayqubitlist = displayqubitlist + [Ket(name)]
            counter = counter + 1
        for kets in displayqubitlist:
            if kets != 0:
                if displayqubit == 0:
                    displayqubit = kets
                else:
                    displayqubit = TensorProduct(kets,displayqubit)
    return displayqubit
#----------------Circuit Logic---------------------------#
    

#---------Quantum Tic Tac Toe---------------------#
#First create a 3x3 board. Player 1 will choose a box first, while player 2 will choose another box.
#Create the following entanglement (|01>+|10>)\sqrt(2) on these 2 boxes. Then, measure 1 of the box
#The output determines if the box belongs to player 1 or player 2.   
#---------Create the 3x3 box---------------------#
board = [' ']*10 #board keeps track of the board status
letter = ['O', 'X']
global status
status = np.zeros(10)
qubit = Qubit('000000000')#initial qubit state
drawBoard([' ','1','2','3','4','5','6','7','8','9'])
print("Number 1 to 9 represent the box")
winning_cond = False
Round = 0 #this is a counter to count which round we are in

#------------Pipeline--------------------#
while winning_cond == False : #system will collapse at round 5
    player = Round % 2 + 1
    print("Current board")
    drawBoard(board)
    print("Current quantum state:",qubitmapping(qubit))
    print(circuit.draw())
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
        qubit = updatestate(player,register0,register1,playermove,qubit)
        print("Current quantum state:",qubitmapping(qubit))
        result = measurement_result(qubit,register0)
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
        qubit = updatestate(player,register0,register1,playermove,qubit)
        print_move(playermove)
        print("Current quantum state:",qubitmapping(qubit))
        playermove,register0,register1 = ask_move_2nd(chosenbox)
        if playermove < 5:
            validmove = isvalidmove(playermove,register0,register1)
            while validmove == False:
                playermove,register0,register1= ask_move_2nd(chosenbox)
                validmove = isvalidmove(playermove,register0,register1)
            update_board(playermove,register0)
            qubit = updatestate(player,register0,register1,playermove,qubit)
            print_move(playermove)
            print("Current quantum state:",qubitmapping(qubit))
        else:
            print('You have ended your turn.')
            print(' ')
        unitaryno = unitaryno + 1
    #break the loop in round 5
    if int(math.floor(Round/2)) == 5 and player == 2:
        break
    #measure all qubit
board = measure_all(qubit, board,status)
drawBoard(board)
#-----------Check winner-----------------#           
if isWinner(board,letter[0]) == True:
    print("Congratulation! Player 1 won the game!") 
elif isWinner(board,letter[1]) == True:
    print("Congratulation! Player 2 won the game!")
        
