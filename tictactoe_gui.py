"""
Created on Sat 12/10/2019

@author: Hon Lin, Yasin
"""

from tkinter import *
import tkinter.messagebox
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

tk = Tk() # blank window
tk.title("Qubit Tic Tac Toe")

c = StringVar()
x1 = StringVar()

pa_dict = {'q':'|0>', 'h':'H', 'x':'X', 'cx':'CX', 'm':'M'}
pb_dict = {'q':'|1>', 'h':'H', 'x':'X', 'cx':'CX', 'm':'M'}

pa_turn = True
num_move = 0
flag = 0
global status
status = np.zeros(10)
qubit = Qubit('000000000')#initial qubit state

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
        return 'Alice,|0>'
    else:
        return 'Bob,|1>'
    
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
                    #5 means the qubit has been measured
    if move == 'q':  
        status[reg0] = 1
    if move == 'm':
        status[reg0] = 5
    
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
    
def updatestate(pa_turn, reg0, reg1, move, qubit): 
    #register0 = control qubit, register1 = target qubit
    #update and print circuit
    if move == 'q':
        if pa_turn == False:
            qubit = qapply(X(reg0-1)*qubit)
    elif move == 'h':
        qubit = qapply(H(reg0-1)*qubit)
    elif move == 'x':
        qubit = qapply(X(reg0-1)*qubit)
    elif move == 'cx':
        qubit = qapply(CNOT(reg0-1,reg1-1)*qubit)
    elif move == 'm':
        qubit = measure_partial_oneshot(qubit,(reg0-1,))
    return qubit

def measurement_result(qubit, reg0):
    #return the measurement result after the collapse of state.
    if type(qubit) == Add:
        partial = measure_partial_oneshot(qubit.args[0],(reg0-1,))
        classical = partial[reg0-1]
        if classical == Qubit('0')[0]:
            classicalbit = '0'
            print('The qubit collapses to classical state 0')
        elif classical == Qubit('1')[0]:
            classicalbit = '1'
            print('The qubit collapses to classical state 1')
    else:
        if qubit[reg0-1] == Qubit('0')[0]:
            classicalbit = '0'
            print('The qubit collapses to classical state 0')
        elif qubit[reg0-1] == Qubit('1')[0]:
            classicalbit = '1'
            print('The qubit collapses to classical state 1')
    return classicalbit

def measure_all(qubit,status):
    #measure all qubits
    qubit = measure_all_oneshot(qubit)
    #update the board
    button = [button7, button8,button9, button4, button5, button6, button1, button2, button3]
    for index,item in enumerate(qubit):
        #check board's status, if a qubit is prepared, then collapse to the state, else, ignore
#        qprint(index), print(item)
        if item == Qubit('0')[0] and status[9-index] == 1:
            button[8-index]["text"] = '0'
        elif item == Qubit('1')[0] and status[9-index] == 1:
            button[8-index]["text"] = '1'

def qubitmapping(qubit):
    #evaluate the qubit(2 cases ->pure state/superposition state)
    global status
    displayqubitlist = []
    displayqubit = 0
    print('Error checking:' , qubit) #error checking
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
            

def btnClick(buttons, label, choice, bt_name):
    global pa_turn, num_move, flag, qubit, status
        
    move, reg0, reg1 = ask_move(bt_name, choice)
    isvalid = isvalidmove(move, reg0, reg1, label[2])
    print(" The move is {}".format(isvalid))
    print(" Reg0: {} Reg1: {}".format(reg0, reg1))
    print(" Num of move is {}".format(num_move))
    if not isvalid:
        return
    qubit = updatestate(pa_turn, reg0, reg1, move, qubit)
    update_status(move, reg0)
        
    print("Current quantum state:",qubitmapping(qubit))
    print(" Status is {}".format(status))
        
    if move == 'm':
        result = measurement_result(qubit, reg0)
        buttons["text"] = str(result)
        checkForWin()
    else:
        prefix = choose_dict(pa_turn)[move]
        if move == 'cx': 
            prefix = prefix + str(reg0) + str(reg1) 
        buttons["text"] = prefix + " " + buttons["text"] 
                
    if num_move == 2:
        pa_turn = not pa_turn
        num_move = 0
        tkinter.messagebox.showinfo("Qubit Tic Tac Toe","It's Player {}'s turn!".format(turn_for(pa_turn)))
        label[0]["text"] = "Turn for Player {}:".format(turn_for(pa_turn))
        label[0]["bg"] = color(pa_turn)
        label[0]["fg"] = color(not(pa_turn))
    flag += 1

        
#    if (flag == 50):
#        disableButton()
#        measure_all(qubit,status)
#        checkForWin()
#        if checkForWin != True:
#            tkinter.messagebox.showinfo("Qubit Tic-Tac-Toe", "It is a Tie")
#    #else:
    #    tkinter.messagebox.showinfo("Tic-Tac-Toe", "Button already Clicked!")

def checkForWin():
    if (button1['text'] == '0' and button2['text'] == '0' and button3['text'] == '0' or
        button4['text'] == '0' and button5['text'] == '0' and button6['text'] == '0' or
        button7['text'] == '0' and button8['text'] == '0' and button9['text'] == '0' or
        button1['text'] == '0' and button5['text'] == '0' and button9['text'] == '0' or
        button3['text'] == '0' and button5['text'] == '0' and button7['text'] == '0' or
        button1['text'] == '0' and button4['text'] == '0' and button7['text'] == '0' or
        button2['text'] == '0' and button5['text'] == '0' and button8['text'] == '0' or
        button7['text'] == '0' and button6['text'] == '0' and button9['text'] == '0'):
        disableButton()
        tkinter.messagebox.showinfo("Qubit Tic-Tac-Toe: Congratulation!", " Player A!")

    elif (button1['text'] == '1' and button2['text'] == '1' and button3['text'] == '1' or
          button4['text'] == '1' and button5['text'] == '1' and button6['text'] == '1' or
          button7['text'] == '1' and button8['text'] == '1' and button9['text'] == '1' or
          button1['text'] == '1' and button5['text'] == '1' and button9['text'] == '1' or
          button3['text'] == '1' and button5['text'] == '1' and button7['text'] == '1' or
          button1['text'] == '1' and button4['text'] == '1' and button7['text'] == '1' or
          button2['text'] == '1' and button5['text'] == '1' and button8['text'] == '1' or
          button7['text'] == '1' and button6['text'] == '1' and button9['text'] == '1'):
        disableButton()
        tkinter.messagebox.showinfo("Qubit Tic-Tac-Toe: Congratulation!", "Player B")

buttons = StringVar()

label1 = Label( tk, text= "Turn for Player Alice,|0>:", font='Times 12 bold', bg='white', fg='black', height=1, width=25)
label1.grid(row=1, columnspan = 2)

choice = Entry(tk, textvariable=x1, bd=5)
choice.grid(row=1, column=2)

label2 = Label( tk, text= "Choose 2 unitary moves or 1 measurement \n q, h, x, m,\n (a = control qubit, b = target qubit Ex: cx12", font='Times 12 bold', bg='yellow', fg='black', height=3, width=45)
label2.grid(row=2, columnspan = 3)

label3 = Label( tk, text= " ", font='Times 12 bold', bg='white', fg='black', height=1, width=44)
label3.grid(row=3, column=0, columnspan = 3)

label = [label1, label2, label3]

button1 = Button(tk, text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: btnClick(button1, label, choice, bt_name=7))
button1.grid(row=4, column=0)

button2 = Button(tk, text=' ', font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: btnClick(button2, label, choice, bt_name=8))
button2.grid(row=4, column=1)

button3 = Button(tk, text=' ',font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: btnClick(button3, label, choice, bt_name=9))
button3.grid(row=4, column=2)

button4 = Button(tk, text=' ', font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: btnClick(button4, label, choice, bt_name=4))
button4.grid(row=5, column=0)

button5 = Button(tk, text=' ', font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: btnClick(button5, label, choice, bt_name=5))
button5.grid(row=5, column=1)

button6 = Button(tk, text=' ', font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: btnClick(button6, label, choice, bt_name=6))
button6.grid(row=5, column=2)

button7 = Button(tk, text=' ', font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: btnClick(button7, label, choice, bt_name=1))
button7.grid(row=6, column=0)

button8 = Button(tk, text=' ', font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: btnClick(button8, label, choice, bt_name=2))
button8.grid(row=6, column=1)

button9 = Button(tk, text=' ', font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: btnClick(button9, label, choice, bt_name=3))
button9.grid(row=6, column=2)

tk.mainloop()