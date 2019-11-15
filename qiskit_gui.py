# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 20:06:07 2019

@author: honlin
"""

import numpy as np
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
        self.status = np.zeros(10) #keep the status of the board
        self.pa_dict = {'q':'|O>', 'h':'H', 'x':'X', 'cx':'CX', 'm':'M'}
        self.pb_dict = {'q':'|X>', 'h':'H', 'x':'X', 'cx':'CX', 'm':'M'}
        self.reg0 = IntVar() #keep track of the chosen register
        self.reg1 = 0
        self.winningcond = False #keep track of the winning condition
        
        #GUI
        self.label1 = Label(text= "Turn for Player Alice,|0>:", font='Times 12 bold', bg='light blue',fg='black', height=1, width=25)
        self.label1.grid(row=1, columnspan = 2)
            
        self.choice = Entry(textvariable=self.chosenmove, bd=5)
        self.choice.grid(row=1, column=2)
            
        self.label2 = Label(text= "Choose 2 unitary moves or 1 measurement", font='Times 12 bold', bg='light salmon', fg='black', height=1, width=45)
        self.label2.grid(row=2, columnspan = 3)
        
        self.label3 = Label(text= "q - put a pure state qubit, h - Hadamard gate, \n x - Pauli X gate, m - Measure ", font='Times 12 bold', bg='light salmon', fg='black', height=2, width=45)
        self.label3.grid(row=3, column=0, columnspan = 3) 
            
        self.label4 = Label(text= " ", font='Times 12 bold', bg='white', fg='black', height=1, width=45)
        self.label4.grid(row=4, column=0, columnspan = 3)
        
        self.button1 = Button(text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: self.btn1click())
        self.button1.grid(row=5, column=0)
        
        self.button2 = Button(text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: self.btn2click())
        self.button2.grid(row=5, column=1)
        
        self.button3 = Button(text=" ",font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: self.btn3click())
        self.button3.grid(row=5, column=2)
        
        self.button4 = Button(text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: self.btn4click())
        self.button4.grid(row=6, column=0)
        
        self.button5 = Button(text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: self.btn5click())
        self.button5.grid(row=6, column=1)
        
        self.button6 = Button(text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: self.btn6click())
        self.button6.grid(row=6, column=2)
        
        self.button7 = Button(text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: self.btn7click())
        self.button7.grid(row=7, column=0)
        
        self.button8 = Button(text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: self.btn8click())
        self.button8.grid(row=7, column=1)
        
        self.button9 = Button(text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8, command=lambda: self.btn9click())
        self.button9.grid(row=7, column=2)
    
    #functions
    def btn1click(self):
        self.reg0 = 7
        self.whichbutton = self.button1
        self.btnClick()
    
    def btn2click(self):
        self.reg0 = 8
        self.whichbutton = self.button2
        self.btnClick()
        
    def btn3click(self):
        self.reg0 = 9
        self.whichbutton = self.button3
        self.btnClick()
    
    def btn4click(self):
        self.reg0 = 4
        self.whichbutton = self.button4
        self.btnClick()
    
    def btn5click(self):
        self.reg0 = 5
        self.whichbutton = self.button5
        self.btnClick()
    
    def btn6click(self):
        self.reg0 = 6
        self.whichbutton = self.button6
        self.btnClick()
    
    def btn7click(self):
        self.reg0 = 1
        self.whichbutton = self.button7
        self.btnClick()
    
    def btn8click(self):
        self.reg0 = 2
        self.whichbutton = self.button8
        self.btnClick()
    
    def btn9click(self):
        self.reg0 = 3
        self.whichbutton = self.button9
        self.btnClick()
    
    def btnClick(self):
        reg0 = self.reg0
        reg1 = self.reg1
        isvalid = self.isvalidmove()
        move = self.chosenmove.get()
        print(" The player has chosen to perform {}".format(move))
        print(" The move is {}".format(isvalid))
        print(" Reg0: {} Reg1: {}".format(reg0, reg1))
        print(" Num of move is {}".format(self.num_move))
        if not isvalid:
            return
        outputstate = self.updatestate()
        self.update_status()
            
        print("Current quantum state:",braket_notation(outputstate,9))
        print(" Status is {}".format(self.status))
        buttons = self.whichbutton
        winningcond = self.winningcond #winning condition
        if move == 'm':
            result = measurement_result(outputstate, reg0,9)
            buttons["text"] = str(result)
            winningcond = self.checkForWin()
            self.flag += 1
        else:
            prefix = self.choose_dict()[move]
            if move == 'cx': 
                prefix = prefix + str(reg0) + str(reg1) 
            buttons["text"]  = prefix + " " + buttons["text"] 
        
        if winningcond == False:
            drawcond = self.checkForDraw()
        self.flag += 1
        
        if (self.flag == 20): #measure all once the flag reaches 20 (10 rounds)
            print("10th round! Measuring all qubits...")
            self.disableButton()
            buttonarr = [self.button7,self.button8,self.button9,self.button4,
                         self.button5,self.button6,self.button1,self.button2,self.button3]
            for register,item in enumerate(self.status):
                if item == 1: #measure the box is there is a qubit. 
                   circuit.measure(register-1,register-1)
                   job = execute(circuit,simulator)
                   result = job.result()
                   outputstate = result.get_statevector()
                   result = measurement_result(outputstate,register,9)
                   buttonarr[register-1]["text"] = str(result)
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
        self.button1.configure(state=DISABLED)
        self.button2.configure(state=DISABLED)
        self.button3.configure(state=DISABLED)
        self.button4.configure(state=DISABLED)
        self.button5.configure(state=DISABLED)
        self.button6.configure(state=DISABLED)
        self.button7.configure(state=DISABLED)
        self.button8.configure(state=DISABLED)
        self.button9.configure(state=DISABLED)
    
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

    def update_status(self):
        #0 means empty, #1 means a qubit has been placed in the register
                        #3 means the qubit has been measured
        reg0 = self.reg0
        move = self.chosenmove.get()
        if move == 'q':  
            self.status[reg0] = 1
        if move == 'm':
            self.status[reg0] = 3
        
    def isvalidmove(self):
        #return false if the move is not valid, and print out the error message
        reg0 = self.reg0
        reg1 = self.reg1  
        move = self.chosenmove.get()
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
            
        elif move == 'cx':
            if self.status[reg0] and self.status[reg1] == 1 and reg0 != reg1:
                self.label4['text'] = ""
                self.num_move += 1
                return True
            else:
                self.label4['text'] = 'Invalid move: One of the register is empty/has been measured'
                return False
                
        else: 
            self.label4['text'] = "No such choice"
            return False
        
    def updatestate(self): 
        #register0 = control qubit, register1 = target qubit
        #update and print circuit
        reg0 = self.reg0
        reg1 = self.reg1
        move = self.chosenmove.get()
        if move == 'q':
            if self.pa_turn == False:
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
    
    def checkForWin(self):
        #return true if the winning condition is satisfied
        if (self.button1['text'] == '0' and self.button2['text'] == '0' and self.button3['text'] == '0' or
            self.button4['text'] == '0' and self.button5['text'] == '0' and self.button6['text'] == '0' or
            self.button7['text'] == '0' and self.button8['text'] == '0' and self.button9['text'] == '0' or
            self.button1['text'] == '0' and self.button5['text'] == '0' and self.button9['text'] == '0' or
            self.button3['text'] == '0' and self.button5['text'] == '0' and self.button7['text'] == '0' or
            self.button1['text'] == '0' and self.button4['text'] == '0' and self.button7['text'] == '0' or
            self.button2['text'] == '0' and self.button5['text'] == '0' and self.button8['text'] == '0' or
            self.button7['text'] == '0' and self.button6['text'] == '0' and self.button9['text'] == '0'):
            self.disableButton()
            tkinter.messagebox.showinfo("Qubit Tic-Tac-Toe: Congratulation!", " Player A Wins!")
            return True
        
        elif (self.button1['text'] == '1' and self.button2['text'] == '1' and self.button3['text'] == '1' or
              self.button4['text'] == '1' and self.button5['text'] == '1' and self.button6['text'] == '1' or
              self.button7['text'] == '1' and self.button8['text'] == '1' and self.button9['text'] == '1' or
              self.button1['text'] == '1' and self.button5['text'] == '1' and self.button9['text'] == '1' or
              self.button3['text'] == '1' and self.button5['text'] == '1' and self.button7['text'] == '1' or
              self.button1['text'] == '1' and self.button4['text'] == '1' and self.button7['text'] == '1' or
              self.button2['text'] == '1' and self.button5['text'] == '1' and self.button8['text'] == '1' or
              self.button7['text'] == '1' and self.button6['text'] == '1' and self.button9['text'] == '1'):
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
            disableButton()
            tkinter.messagebox.showinfo("Qubit Tic-Tac-Toe", "It's a draw.")
            return True
        else:
            return False

root = Tk()
myapp = MainApp(root)
root.mainloop()
