# Qubit Tic Tac Toe- A quantum game for quantum mechanics and quantum programming education
Runs in python. Requires sympy package. 

Download tictactoegui.py for Guided User Interface. 

Download qubit tic tac toe tutorial.ipynb to understand the game and circuit logic(this notebook explains how qiskit is implemented in the game)
# Description
Qubit Tic Tac Toe replaces the classical marking with quantum marking. Each player can perform either 1 measurement, or 2 unitary moves. The first to form a straight line with the player's own classical marking will win the game.

This quantization is different from Goff's quantization, where he quantizes the moves instead of the marking.

Rules: 
1. Players choose to make 2 unitary operations OR 1 projective operation on a box.
2. Unitary operations include: Initiate a qubit, X gate and Hadamard Gate.
3. The projective operation will collapse the qubit into a classical bit.
4. The player wins by forming a straight line using 3 classical bit. 

# Game Interface
![GUI](https://user-images.githubusercontent.com/37786219/66732018-ca659d80-ee8c-11e9-96c2-42d7c5c7f2f1.png)


# What is a qubit?
A bit is an classical information carrier, which is simply 0 or 1. In the simplest form, we can store information as a string of 0s and 1s. A qubit is an quantum information carrier. Aside from the classical information(0 and 1), a qubit contains quantum information as well. This extra information makes quantum information and quantum computer different (perhaps more powerful) than a classical computer. 
![070817_essay_qubit_main](https://user-images.githubusercontent.com/37786219/66759347-a9c03680-eed2-11e9-8747-4bde8b383093.png)
(retrieved from https://www.sciencenews.org/article/quarter-century-ago-qubit-was-born)

A qubit can be visualize as a sphere. Classical information 0 and 1 lies on the surface of the sphere, opposite to one another. To retrieve classical information from qubit, one needs to destroy the sphere by projecting the state vector(which describe the type of qubit) onto one of the chosen basis. This is known as the measurement postulate.

The strength of quantum computing comes from the ability to manipulate the qubit before measurement. You can rotate the qubit, entangle 2 qubits to perform computation. These operations don't destroy the quantum state, hence they are given a special name, called unitary operation. 

# Log
13/12/18 Uploaded Quantum Tic Tac Toe V1 

31/8/19 Uploaded Quantum Tic Tac Toe V2 and V4

12/10/19 Uploaded Qubit Tic Tac Toe GUI v1
V4 
1. Players allow to see quantum state.
2. Initial Quantum State is |000000000> 

4/9/19 Fixed bug in QTTT V4

6/9/19 Fixed the display for quantum state QTTT V4

11/10/19 Added round constraint for QTTT V4
