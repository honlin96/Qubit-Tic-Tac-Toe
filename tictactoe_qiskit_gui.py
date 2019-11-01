"""
Created on Sat 12/10/2019

@author: Hon Lin, Yasin
"""

from tkinter import *
import tkinter.messagebox
import numpy as np
import math
from qiskit import(
  QuantumCircuit,
  execute,
  Aer)

# Use Aer's statevector simulator
simulator = Aer.get_backend('statevector_simulator')

#Create a 9 register quantum circuit
global circuit
circuit = QuantumCircuit(9,9)

#Create a blank window
tk = Tk() 
tk.title("Qubit Tic Tac Toe")

c = StringVar() 
x1 = StringVar() #record down the choice

pa_dict = {'q':'|O>', 'h':'H', 'x':'X', 'cx':'CX', 'm':'M'}
pb_dict = {'q':'|X>', 'h':'H', 'x':'X', 'cx':'CX', 'm':'M'}

pa_turn = True
num_move = 0
flag = 0
global status
status = np.zeros(10)

def disableButton():
    button1.configure(state=DISABLED)
    button2.configure(state=DISABLED)
    button3.configure(state=DISABLED)
    button4.configure(state=DISABLED)
    button5.configure(state=DISABLED)
    button6.configure(state=DISABLED)
    button7.configure(state=DISABLED)
    button8.configure(state=DISABLED)
    button9.configure(state=DISABLED)

def color(pa_turn):
    #Change the background and foreground colour for different players
    if pa_turn:
        return 'white' 
    else:
        return 'black'
    
def choose_dict(pa_turn):
    #If player A, use A's dictionary. Otherwise, use player B's dictionary 
    if pa_turn:
        return pa_dict
    else:
        return pb_dict
    
def turn_for(pa_turn):
    #Turns for Player 1 and Player 2
    if pa_turn:
        return 'Alice,|O>'
    else:
        return 'Bob,|X>'
    
def ask_move(reg0, choice):
    move = choice.get()
    reg1 = 0
    #if cx ask for the control and target
    if move.startswith('cx'):
        reg0 = move[-2]
        reg1 = move[-1]
        move = move[:-2]

    return move, int(reg0), int(reg1)

def update_status(move, reg0):
    global status
    #0 means empty, #1 means a qubit has been placed in the register
                    #3 means the qubit has been measured
    if move == 'q':  
        status[reg0] = 1
    if move == 'm':
        status[reg0] = 3
    
def isvalidmove(move, reg0, reg1, label):
    #return false if the move is not valid, and print out the error message
    global num_move, status
        
    if move == 'q':
        #check if the box is empty/has not been measured
        if status[reg0] == 0:
            label['text'] = ""
            num_move += 1
            return True
        else:
            label['text'] = 'Invalid move: A qubit has been allocated to the box.'
            return False
        
    elif move in ['h', 'x']:
        if status[reg0] == 1:
            label['text'] = ""
            num_move += 1
            return True
        else:
            label['text'] = 'Invalid move: The register is empty/has been measured'
            return False
        
    elif move == 'm':
        if status[reg0] == 1:
            label['text'] = ""
            num_move += 2
            if num_move<=2:
                return True
            else:
                label['text'] = 'Invalid move: 2nd move cannot be Measure'
                num_move -= 2
                return False
        else:
            label['text'] = 'Invalid move: The register is empty/has been measured'
            return False
        
    elif move == 'cx':
        if status[reg0] and status[reg1] == 1 and reg0 != reg1:
            label['text'] = ""
            num_move += 1
            return True
        else:
            label['text'] = 'Invalid move: One of the register is empty/has been measured'
            return False
            
    else: 
        label['text'] = "No such choice"
        return False
    
def updatestate(pa_turn, reg0, reg1, move): 
    #register0 = control qubit, register1 = target qubit
    #update and print circuit
    if move == 'q':
        if pa_turn == False:
            circuit.x(reg0-1)
            circuit.iden(reg0-1)
        else:
            circuit.iden(reg0-1) 
    elif move == 'h':
        circuit.h(reg0-1)
    elif move == 'x':
        circuit.x(reg0-1)
    #elif move == 'cx':
        #qubit = qapply(CNOT(reg0-1,reg1-1)*qubit)
    elif move == 'm':
        circuit.measure(reg0-1,reg0-1)
     # Execute the circuit
    job = execute(circuit,simulator)
    result = job.result()
    outputstate = result.get_statevector()
    return outputstate

def measurement_result(outputstate,measured_register,qubitnumber):
    for index,element in enumerate(outputstate):
        if element != 0:
            ket = bin(index)[2:].zfill(qubitnumber)
            print("The ket is |"+str(ket) +"> with probability amplitude " + str(element))
            result = ket[qubitnumber-measured_register] #the ket is read from right to left(|987654321>)
            break #break the iteration since we have obtained the result
    print("The qubit collapsed to " + result)
    return result


def braket_notation(outputstate,qubitnumber):
    #print out the wavefunction in braket notation.
    #binary reads from right to left
    ket = ''
    for index,element in enumerate(outputstate):
        if element != 0:
            if ket == '':
            #only print out states with non-zero probability amplitude
                ket += str(element)+'|'+ bin(index)[2:].zfill(qubitnumber) +'>'
               # print(index)
            else:
                ket = ket + ' + ' + str(element)+'|'+ bin(index)[2:].zfill(qubitnumber) +'>'
               # print(index)
    return ket
            
def btnClick(buttons, label, choice, bt_name):
    global pa_turn, num_move, flag, status
    #buttontextarr =[button7['text'],button8['text'],button9['text'],button4['text'],button5['text'],button6['text'],button1['text'],button2['text'],button3['text']]   
    move, reg0, reg1 = ask_move(bt_name, choice)
    isvalid = isvalidmove(move, reg0, reg1, label[3])
    print(" The move is {}".format(isvalid))
    print(" Reg0: {} Reg1: {}".format(reg0, reg1))
    print(" Num of move is {}".format(num_move))
    if not isvalid:
        return
    outputstate = updatestate(pa_turn, reg0, reg1, move)
    update_status(move, reg0)
        
    print("Current quantum state:",braket_notation(outputstate,9))
    print(" Status is {}".format(status))
    
    winningcond = False #winning condition
    if move == 'm':
        result = measurement_result(outputstate, reg0,9)
        buttons["text"] = str(result)
        winningcond = checkForWin()
        flag += 1
    else:
        prefix = choose_dict(pa_turn)[move]
        if move == 'cx': 
            prefix = prefix + str(reg0) + str(reg1) 
        buttons["text"]  = prefix + " " + buttons["text"] 
    
    drawcond = checkForDraw(winningcond)
    flag += 1
    
    if (flag == 20): #measure all once the flag reaches 20 (10 rounds)
        print("10th round! Measuring all qubits...")
        disableButton()
        buttonarr = [button7,button8,button9,button4,button5,button6,button1,button2,button3]
        for register,item in enumerate(status):
            if item == 1: #measure the box is there is a qubit. 
               circuit.measure(register-1,register-1)
               job = execute(circuit,simulator)
               result = job.result()
               outputstate = result.get_statevector()
               result = measurement_result(outputstate,register,9)
               buttonarr[register-1]["text"] = str(result)
        winningcond = checkForWin()
        if winningcond != True:
            tkinter.messagebox.showinfo("Qubit Tic-Tac-Toe", "It is a Tie")
            
    if num_move == 2 and winningcond == False and drawcond == False:
        pa_turn = not pa_turn
        num_move = 0
        tkinter.messagebox.showinfo("Qubit Tic Tac Toe,Round {} ".format(flag/2),"It's Player {}'s turn!".format(turn_for(pa_turn)))
        label[0]["text"] = "Turn for Player {}:".format(turn_for(pa_turn))
        label[0]["bg"] = color(pa_turn)
        label[0]["fg"] = color(not(pa_turn))           
    

def checkForWin():
    #return true if the winning condition is satisfied
    if (button1['text'] == '0' and button2['text'] == '0' and button3['text'] == '0' or
        button4['text'] == '0' and button5['text'] == '0' and button6['text'] == '0' or
        button7['text'] == '0' and button8['text'] == '0' and button9['text'] == '0' or
        button1['text'] == '0' and button5['text'] == '0' and button9['text'] == '0' or
        button3['text'] == '0' and button5['text'] == '0' and button7['text'] == '0' or
        button1['text'] == '0' and button4['text'] == '0' and button7['text'] == '0' or
        button2['text'] == '0' and button5['text'] == '0' and button8['text'] == '0' or
        button7['text'] == '0' and button6['text'] == '0' and button9['text'] == '0'):
        disableButton()
        tkinter.messagebox.showinfo("Qubit Tic-Tac-Toe: Congratulation!", " Player A Wins!")
        return True
    
    elif (button1['text'] == '1' and button2['text'] == '1' and button3['text'] == '1' or
          button4['text'] == '1' and button5['text'] == '1' and button6['text'] == '1' or
          button7['text'] == '1' and button8['text'] == '1' and button9['text'] == '1' or
          button1['text'] == '1' and button5['text'] == '1' and button9['text'] == '1' or
          button3['text'] == '1' and button5['text'] == '1' and button7['text'] == '1' or
          button1['text'] == '1' and button4['text'] == '1' and button7['text'] == '1' or
          button2['text'] == '1' and button5['text'] == '1' and button8['text'] == '1' or
          button7['text'] == '1' and button6['text'] == '1' and button9['text'] == '1'):
        disableButton()
        tkinter.messagebox.showinfo("Qubit Tic-Tac-Toe: Congratulation!", "Player B Wins!")
        return True
    else:
        return False
 
def checkForDraw(winningcond):
    draw = 0
    #check if the game is drawed after measuring all boxes. 
    for index,element in enumerate(status):
        if element == 3:
            draw += 1
    if draw == 9 and winningcond != True:
        disableButton()
        tkinter.messagebox.showinfo("Qubit Tic-Tac-Toe", "It's a draw.")
        return True
    else:
        return False
    
buttons = StringVar()

label1 = Label( tk, text= "Turn for Player Alice,|0>:", font='Times 12 bold', bg='white', fg='black', height=1, width=25)
label1.grid(row=1, columnspan = 2)

choice = Entry(tk, textvariable=x1, bd=5)
choice.grid(row=1, column=2)

label2 = Label( tk, text= "Choose 2 unitary moves or 1 measurement", font='Times 12 bold', bg='yellow', fg='black', height=1, width=45)
label2.grid(row=2, columnspan = 3)

label3 = Label( tk, text= "q - put a pure state qubit, h - Hadamard gate, \n x - Pauli X gate, m - Measure ", font='Times 12 bold', bg='yellow', fg='black', height=2, width=45)
label3.grid(row=3, column=0, columnspan = 3) 

label4 = Label( tk, text= " ", font='Times 12 bold', bg='white', fg='black', height=1, width=45)
label4.grid(row=4, column=0, columnspan = 3)

label = [label1, label2, label3, label4]

button1 = Button(tk, text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: btnClick(button1, label, choice, bt_name=7))
button1.grid(row=5, column=0)

button2 = Button(tk, text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: btnClick(button2, label, choice, bt_name=8))
button2.grid(row=5, column=1)

button3 = Button(tk, text=" ",font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: btnClick(button3, label, choice, bt_name=9))
button3.grid(row=5, column=2)

button4 = Button(tk, text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: btnClick(button4, label, choice, bt_name=4))
button4.grid(row=6, column=0)

button5 = Button(tk, text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: btnClick(button5, label, choice, bt_name=5))
button5.grid(row=6, column=1)

button6 = Button(tk, text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: btnClick(button6, label, choice, bt_name=6))
button6.grid(row=6, column=2)

button7 = Button(tk, text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: btnClick(button7, label, choice, bt_name=1))
button7.grid(row=7, column=0)

button8 = Button(tk, text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: btnClick(button8, label, choice, bt_name=2))
button8.grid(row=7, column=1)

button9 = Button(tk, text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: btnClick(button9, label, choice, bt_name=3))
button9.grid(row=7, column=2)

#set an infinite loop so window stay in view
tk.mainloop()
