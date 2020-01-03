# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 02:37:13 2019

@author: honlin
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 20:06:07 2019

@author: honlin
"""

import numpy as np
import math
from tkinter import *
import tkinter.messagebox
from qiskit import(
  QuantumCircuit,
  execute,
  Aer)

# Use Aer's statevector simulator
simulator = Aer.get_backend('statevector_simulator')

#Create a 9 register quantum circuit
global circuit
circuit = QuantumCircuit(9,9)
#logic function
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
#Create a blank window

class MainApp:                         ### (1)
    def __init__(self, Parent):      ### (1a)
        self.myContainer1 = Frame(Parent)
        #variables
        self.num_move = 0
        self.chosenmove = StringVar() #keep the string variable from the entry
        self.flag = 0 #keep track of the number of moves made
        self.pa_turn = True #Return True if it is player A's turn, otherwise return false
        self.status = np.zeros(9) #keep the status of the board
        self.pa_dict = {'q':'|O>', 'h':'H', 'x':'X', 'cx':'CX', 'm':'M'}
        self.pb_dict = {'q':'|X>', 'h':'H', 'x':'X', 'cx':'CX', 'm':'M'}
        self.reg0 = IntVar() #keep track of the chosen register
        self.reg1 = 0
        self.winningcond = False #keep track of the winning condition
        
        #GUI
        self.label1 = Label(text= "Turn for Player Alice,|0>:", font='Times 12 bold', bg='light blue',fg='black', height=1, width=30)
        self.label1.grid(row=1, columnspan = 2)
            
        self.choice = Entry(textvariable=self.chosenmove, bd=5)
        self.choice.grid(row=1, column=2)
            
        self.label2 = Label(text= "Choose 2 unitary moves or 1 measurement", font='Times 12 bold', bg='light salmon', fg='black', height=1, width=45)
        self.label2.grid(row=2, columnspan = 3)
        
        self.label3 = Label(text= "q - put a pure state qubit, h - Hadamard gate, \n x - Pauli X gate, m - Measure ", font='Times 12 bold', bg='light salmon', fg='black', height=2, width=45)
        self.label3.grid(row=3, column=0, columnspan = 3) 
            
        self.label4 = Label(text= " ", font='Times 12 bold', bg='white', fg='black', height=1, width=45)
        self.label4.grid(row=4, column=0, columnspan = 3)
        
    #create 3x3 boxes
        self.buttons = []
        for i in range(9):
            self.buttons.append(Button(text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8,command=lambda i=i :self.btnClick(i)))
            #Note: command lambda i=i to ensure the value i is stored and passed into the function when the button is created
            self.buttons[i].grid(row= 5 + math.floor(i/3), column=i%3)
    
    #functions    
    def btnClick(self,reg0):
        isvalid = self.isvalidmove(reg0)
        move = self.chosenmove.get()
        if move[:2] == 'cx':
            reg1 = int(move[3])
            self.reg1 = reg1
        print(" The player has chosen to perform {}".format(move))
        #print(" The move is {}".format(isvalid))
        #print(" Reg0: {} Reg1: {}".format(reg0, reg1))
        #print(" Num of move is {}".format(self.num_move))
        if not isvalid:
            return
        outputstate = self.updatestate(reg0)
        self.update_status(reg0)
            
        print("Current quantum state:",braket_notation(outputstate,9))
        print(" Status is {}".format(self.status))
        button = self.buttons[reg0]
        winningcond = self.winningcond #winning condition
        if move == 'm':
            result = measurement_result(outputstate, reg0,9)
            #change the color of the box once it is measured
            if str(result) == '0':
                button["bg"] = 'light slate blue'
                button["text"] = 'O'
            else:
                button["bg"] = 'forest green'
                button["text"] = 'X'
            winningcond = self.checkForWin()
            self.flag += 1
        else:
            if move[:2] != 'cx':
                prefix = self.choose_dict()[move]
            else:
                SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
                prefix = 'CX' + str(reg0) + str(reg1) 
                prefix = prefix.translate(SUB)
                targetbutton = self.buttons[reg1-1]
                targetbutton['text'] = prefix + " " + targetbutton['text']
            button["text"]  = prefix + " " + button["text"] 
            
        if winningcond == False:
            drawcond = self.checkForDraw()
        self.flag += 1
        
        if (self.flag == 20): #measure all once the flag reaches 20 (10 rounds)
            print("10th round! Measuring all qubits...")
            self.disableButton()
            for register,item in enumerate(self.status):
                if item == 1: #measure the box is there is a qubit. 
                   circuit.measure(register-1,register-1)
                   job = execute(circuit,simulator)
                   result = job.result()
                   outputstate = result.get_statevector()
                   result = measurement_result(outputstate,register,9)
                   self.buttons[register]["text"] = str(result)
            winningcond = self.checkForWin()
            if winningcond != True:
                tkinter.messagebox.showinfo("Qubit Tic-Tac-Toe", "It is a Tie")
                
        if self.num_move == 2 and winningcond == False and drawcond == False:
            self.pa_turn = not self.pa_turn
            self.num_move = 0
            tkinter.messagebox.showinfo("Qubit Tic Tac Toe,Round {} ".format(self.flag/2),"It's Player {}'s turn!".format(self.turn_for()))
            self.label1["text"] = "Turn for Player {}:".format(self.turn_for())
            self.label1["bg"] = self.color()   
            
    def disableButton(self):
        for button in self.buttons:
            button.configure(state = DISABLED)
            
    def color(self):
    #Change the background and foreground colour for different players
        if self.pa_turn:
            return 'light blue' 
        else:
            return 'forest green'
        
    def choose_dict(self):
    #If player A, use A's dictionary. Otherwise, use player B's dictionary 
        if self.pa_turn:
            return self.pa_dict
        else:
            return self.pb_dict
  
    def turn_for(self):
        #Turns for Player 1 and Player 2
        if self.pa_turn:
            return 'Alice,|O>'
        else:
            return 'Bob,|X>'

    def update_status(self,reg0):
        #0 means empty, #1 means a qubit has been placed in the register
                        #3 means the qubit has been measured
        move = self.chosenmove.get()
        if move == 'q':  
            self.status[reg0] = 1
        if move == 'm':
            self.status[reg0] = 3
        
    def isvalidmove(self,reg0):
        #return false if the move is not valid, and print out the error message
        move = self.chosenmove.get()
        if len(move) == 1:
            if move == 'q':
                #check if the box is empty/has not been measured
                if self.status[reg0] == 0:
                    self.label4["text"] = ""
                    self.num_move += 1
                    return True
                else:
                    self.label4['text'] = 'Invalid move: A qubit has been allocated to the box.'
                    return False
                
            elif move in ['h', 'x']:
                if self.status[reg0] == 1:
                    self.label4['text'] = ""
                    self.num_move += 1
                    return True
                else:
                    self.label4['text'] = 'Invalid move: The register is empty/has been measured'
                    return False
                
            elif move == 'm':
                if self.status[reg0] == 1:
                    self.label4['text'] = ""
                    self.num_move += 2
                    if self.num_move<=2:
                        return True
                    else:
                        self.label4['text'] = 'Invalid move: 2nd move cannot be Measure'
                        self.num_move -= 2
                        return False
                else:
                    self.label4['text'] = 'Invalid move: The register is empty/has been measured'
                    return False
            
        elif len(move) == 4: 
            if move[:2] == 'cx':
            #if both registers has a qubit, and the registers do not repeat itself
                labelreg0 = move[2]
            #return false if the clicked control qubit is not the same as the entered control qubit
                if int(labelreg0) != reg0:
                    print(labelreg0, reg0)
                    self.label4['text'] = 'Invalid move: Wrong Control Qubit'
                    return False
                if self.status[reg0] != 1:
                    self.label4['text'] = 'Invalid move: The control register is empty/has been measured'
                    return False
                reg1 = int(move[3])
                if reg0 == reg1:
                    self.label4['text'] = 'Invalid move: The control and target register cannot be the same'
                    return False
            
                if self.status[reg1] == 1:
                    self.label4['text'] = ""
                    self.num_move += 1
                    return True
                else:
                    self.label4['text'] = 'Invalid move: The target register is empty/has been measured'
                    return False     
        else: 
            self.label4['text'] = "No such choice"
            return False
        
    def updatestate(self,reg0): 
        #register0 = control qubit, register1 = target qubit
        #update and print circuit
        reg1 = self.reg1
        move = self.chosenmove.get()
        if move == 'q':
            if self.pa_turn == False:
                circuit.x(reg0)
                circuit.iden(reg0)
            else:
                circuit.iden(reg0) 
        elif move == 'h':
            circuit.h(reg0)
        elif move == 'x':
            circuit.x(reg0)
        elif move[:2] == 'cx':
            circuit.cx(reg0,reg1-1)
        elif move == 'm':
            circuit.measure(reg0,reg0)
         # Execute the circuit
        job = execute(circuit,simulator)
        result = job.result()
        outputstate = result.get_statevector()
        return outputstate
    
    def checkForWin(self):
        #return true if the winning condition is satisfied
        if (self.buttons[0]['text'] == 'O' and self.buttons[1]['text'] == 'O' and self.buttons[2]['text'] == 'O' or
            self.buttons[3]['text'] == 'O' and self.buttons[4]['text'] == 'O' and self.buttons[5]['text'] == 'O' or
            self.buttons[6]['text'] == 'O' and self.buttons[7]['text'] == 'O' and self.buttons[8]['text'] == 'O' or
            self.buttons[0]['text'] == 'O' and self.buttons[4]['text'] == 'O' and self.buttons[8]['text'] == 'O' or
            self.buttons[2]['text'] == 'O' and self.buttons[4]['text'] == 'O' and self.buttons[6]['text'] == 'O' or
            self.buttons[0]['text'] == 'O' and self.buttons[3]['text'] == 'O' and self.buttons[6]['text'] == 'O' or
            self.buttons[1]['text'] == 'O' and self.buttons[4]['text'] == 'O' and self.buttons[7]['text'] == 'O' or
            self.buttons[2]['text'] == 'O' and self.buttons[5]['text'] == 'O' and self.buttons[8]['text'] == 'O'):
            self.disableButton()
            tkinter.messagebox.showinfo("Qubit Tic-Tac-Toe: Congratulation!", " Player A Wins!")
            return True
        
        elif (self.buttons[0]['text'] == 'X' and self.buttons[1]['text'] == 'X' and self.buttons[2]['text'] == 'X' or
            self.buttons[3]['text'] == 'X' and self.buttons[4]['text'] == 'X' and self.buttons[5]['text'] == 'X' or
            self.buttons[6]['text'] == 'X' and self.buttons[7]['text'] == 'X' and self.buttons[8]['text'] == 'X' or
            self.buttons[0]['text'] == 'X' and self.buttons[4]['text'] == 'X' and self.buttons[8]['text'] == 'X' or
            self.buttons[2]['text'] == 'X' and self.buttons[4]['text'] == 'X' and self.buttons[6]['text'] == 'X' or
            self.buttons[0]['text'] == 'X' and self.buttons[3]['text'] == 'X' and self.buttons[6]['text'] == 'X' or
            self.buttons[1]['text'] == 'X' and self.buttons[4]['text'] == 'X' and self.buttons[7]['text'] == 'X' or
            self.buttons[2]['text'] == 'X' and self.buttons[5]['text'] == 'X' and self.buttons[8]['text'] == 'X'):
            self.disableButton()
            tkinter.messagebox.showinfo("Qubit Tic-Tac-Toe: Congratulation!", "Player B Wins!")
            return True
        else:
            return False
     
    def checkForDraw(self):
        draw = 0
        #check if the game is drawed after measuring all boxes. 
        for index,element in enumerate(self.status):
            if element == 3:
                draw += 1
        if draw == 9:
            self.disableButton()
            tkinter.messagebox.showinfo("Qubit Tic-Tac-Toe", "It's a draw.")
            return True
        else:
            return False

root = Tk()
root.title('Qubit Tic Tac Toe')
myapp = MainApp(root)
root.mainloop()
