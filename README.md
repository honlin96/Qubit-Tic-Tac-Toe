# Qubit Tic Tac Toe- A quantum game for quantum mechanics and quantum programming education
Runs in python. Requires sympy package. 

Download tictactoegui.py for Guided User Interface. 

# Descripition
Qubit Tic Tac Toe replaces the classical marking with quantum marking. Each player can perform either 1 measurement, or 2 unitary moves. The first to form a straight line with the player's own classical marking will win the game.

This quantization is different from Goff's quantization, where he quantizes the moves instead of the marking.

Rules: 
1. Player chooses one of the boxes each turn 
2. Players choose to make 2 unitary operations OR 1 projective operation on the box.
3. Unitary operations include: Initiate a qubit, X gate and Hadamard Gate.
4. The projective operation will collapse the qubit into a classical bit.
5. The player wins by forming a straight line using 3 classical bit. 



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
