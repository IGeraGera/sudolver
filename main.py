import tkinter as tk
from tkinter import ttk
from tkinter.constants import CENTER, E, LEFT
from tkinter import filedialog as fd
from tkinter.messagebox import showerror
import numpy as np
import copy
import os

class Sudoku():
    """Class which contains the sudoku variables"""
    def __init__(self):
        # Create Guess
        self.boardStatus=list()
        self.guessStatus=list()
        self.boardOriginal=None
        self.guess = list()
        self.board=list()
        for row in range(0,9):
            self.guess.append([])
            self.board.append([])
            for col in range(0,9):
                self.board[row].append(None)
                self.guess[row].append({1,2,3,4,5,6,7,8,9})
        # Make board a numpy array
        self.board = np.array([np.array(xi) for xi in self.board])

    def solve(self):
        """ Solver Function that solves the given board recursively.
        """
        # Flag
        solved=0
        while True:
            self.elliminateGuesses()
            addedGuess=self.replaceGuesses()
            # check if not added to the board
            if addedGuess==0:
                # Save Status to queue
                self.boardStatus.append(self.board[:,:].copy())
                self.guessStatus.append(copy.deepcopy(self.guess[:]))
                for i in range(0,9):
                    for j in range(0,9):
                        if self.guessStatus[-1][i][j]!=None and len(self.guessStatus[-1][i][j])>1:
                            # Replace an element from guess
                            for el in self.guess[i][j]:
                                self.board=self.boardStatus[-1].copy()
                                self.guess=copy.deepcopy(self.guessStatus[-1])
                                self.board[i,j]=el
                                solved=self.solve()
                                if solved==1:
                                    break
                        if solved==1:
                            break
                    if solved==1:
                        break
                # if the solution failed restore previous status
                if solved==0:
                    self.board=self.boardStatus.pop()
                    self.guess=self.guessStatus.pop()
            if self.checkIfDone()==1:
                if self.checkIfSolved()==1:
                    return 1
                else:
                    return 0
            

    def reset(self):
        """ Function that resets the class
        """
        # Create Guess
        self.guess = list()
        self.board=list()
        self.boardOriginal=None
        self.boardStatus=list()
        self.guessStatus=list()
        for row in range(0,9):
            self.guess.append([])
            self.board.append([])
            for col in range(0,9):
                self.board[row].append(None)
                self.guess[row].append({1,2,3,4,5,6,7,8,9})
        # Make board a numpy array
        self.board = np.array([np.array(xi) for xi in self.board])

    def elliminateGuesses(self):
        """ Function that elliminates possible guesses from guess list. Also if 
            a value in board is not None it sets it as None in guess. Generally it 
            elliminates guesses in a row, column and box.
        """
        for row in range(0,9):
            for col in range(0,9):
                val = self.board[row,col]
                if val !=None:
                    self.guess[row][col]=None
                    for x in range(0,9):
                        if self.guess[row][x]!=None :
                            self.guess[row][x].discard(val)
                    for x in range(0,9):
                        if self.guess[x][col]!=None:
                            self.guess[x][col].discard(val)
                    for x in range(3*(row//3),(3*(row//3))+3):
                        for y in range(3*(col//3),(3*(col//3))+3):
                            if self.guess[x][y]!=None:
                                self.guess[x][y].discard(val)

    
    def replaceGuesses(self):
        """ Function that checks for elligible guesses. It gathers all the guesses in a superset
            and checks if the current chosen guess is NOT present in the superset. This inherently
            means that the current guess is the only possible guess for the row,column or box.
            If any guess is added to the Board it returns 1 else 0. This is for the speculative 
            solving of the board"""
        replacedElementflag=0
        for row in range(0,9):
                for col in range(0,9):
                    # for 1 guess left
                    if self.guess[row][col]!=None:
                        if len(self.guess[row][col])==1:
                            self.board[row,col]=self.guess[row][col].pop()
                            self.guess[row][col]=None
                            replacedElementflag=1
                            continue
                        # for 1 guess in line
                        for el in self.guess[row][col]:
                            testset =set()
                            for y in range(0,9):
                                if y!=col:
                                    if self.guess[row][y]!=None:
                                        testset=testset.union(self.guess[row][y])
                                    else:
                                        testset.add(self.board[row,y])
                            if el not in testset:
                                self.board[row,col]=el
                                self.guess[row][col]=None
                                replacedElementflag=1
                                break
                        if self.board[row,col]!=None:
                            continue
                        # for 1 guess in col
                        for el in self.guess[row][col]:
                            testset =set()
                            for x in range(0,9):
                                if x!=row:
                                    if self.guess[x][col]!=None:
                                        testset=testset.union(self.guess[x][col])
                                    else:
                                        testset.add(self.board[x,col])
                            if el not in testset:
                                self.board[row,col]=el
                                self.guess[row][col]=None
                                replacedElementflag=1
                                break
                        if self.board[row,col]!=None:
                            continue
                        # for 1 guess in box
                        for el in self.guess[row][col]:
                            testset =set()
                            for x in range(3*(row//3),(3*(row//3))+3):
                                for y in range(3*(col//3),(3*(col//3))+3):
                                    if y!=col or x!=row:
                                        if self.guess[x][y]!=None:
                                            testset=testset.union(self.guess[x][y])
                                        else:
                                            testset.add(self.board[x,y])
                            if el not in testset:
                                self.board[row,col]=el
                                self.guess[row][col]=None
                                replacedElementflag=1
                                break
                        if self.board[row,col]!=None:
                            continue
        return replacedElementflag

    def checkIfDone(self):
        """ Fuction that checks if board is full or there is a wrong element in board"""
        # Check is board is full
        if None not in self.board[:,:]:
            flag1=1
        else:
            flag1=0
        flag2=0
        # Check if guess has an empty set. This means that a wrong guess was passed to board
        for i in range(0,9):
            for j in range(0,9):
                
                if self.guess[i][j]!=None and len(self.guess[i][j])==0:
                    flag2=1
        if flag1==1 or flag2==1:
            return 1
        else:
            return 0
    def checkIfSolved(self):
        """ Function that checks if the current Board is solved correctly"""
        # Check if duplicates exist and if all numbers are used
        try:
            for row in range(0,9):
                testSet = set(self.board[row,:].flatten())
                testSet.discard(None)
                if len(testSet)!=len(self.board[row,:].flatten()[self.board[row,:].flatten()!=None]):
                    raise DuplicateError
                if len(testSet)!=9:
                    return 0
            for col in range(0,9):
                testSet = set(self.board[:,col].flatten())
                testSet.discard(None)
                if len(testSet)!=len(self.board[:,col].flatten()[self.board[:,col].flatten()!=None]):
                    raise DuplicateError
                if len(testSet)!=9:
                    return 0
            for boxX in range(0,9,3):
                for boxY in range(0,9,3):
                    testSet = set(self.board[boxX:boxX+3,boxY:boxY+3].flatten())
                    testSet.discard(None)
                    if len(testSet)!=len(self.board[boxX:boxX+3,boxY:boxY+3].flatten()[self.board[boxX:boxX+3,boxY:boxY+3].flatten()!=None]):
                        raise DuplicateError
                    if len(testSet)!=9:
                        return 0
        except DuplicateError as error:
            return 0
            # showerror(title='Error',message="Duplicates found")

        return 1
        
class Error(Exception):
    """Base class for other exceptions"""
    pass

class DuplicateError(Error):
    """Raised when Duplicates exists"""
    pass

class Menu(tk.Menu):
    """ Menu class for the top menu of the App() class"""
    def __init__(self,container):
        super().__init__(container)
        # File cascade 
        self.FileMenu=tk.Menu(self,tearoff=False)
        self.FileMenu.add_command(label='New',command=container.reset)
        self.FileMenu.add_command(label='Open',command=container.openFile)
        self.FileMenu.add_command(label='Save as..',command=lambda:container.saveAsFile())
        self.FileMenu.add_command(label='Exit',command=lambda:container.quit())

        self.add_cascade(label='File',menu=self.FileMenu)

class numFrame(ttk.Frame):
    """ Number frame class that contains the numberframe which numbers are projected and entered"""
    def __init__(self,container):
        super().__init__(container, style='numFrame.TFrame')
        # List of boxes -- Contains Frames for each box
        self.boxes = list()
        # List of entries in the Frame
        self.numWidget=list()
        # Iterate Boxes
        for boxX in range(0,3):
            self.boxes.append([])
            for boxY in range(0,3):
                # Add Frame of the current box 
                self.boxes[boxX].append(ttk.Frame(self))
                for i in range(boxX*3,(boxX*3+3)):
                    # Append entry and Var
                    self.numWidget.append([])
                    for j in range(boxY*3,(boxY*3+3)):
                        # Append widget
                        self.numWidget[i].append(ttk.Entry(self.boxes[boxX][boxY],style='black.TEntry',justify='center',width=2,font=("Arial",30),text=''))
                        # send entry to the frame(grid) of the box
                        self.numWidget[i][j].grid(column=j,row=i,sticky=tk.EW,ipadx=5,ipady=5)
                # Add box frame to numFrame
                self.boxes[boxX][boxY].grid(row=boxX,column=boxY,padx=3,pady=3)
        # Create the Styles for the frame and Entries
        self.style=ttk.Style(container)
        self.style.configure('numFrame.TFrame',background='black')
        self.style1=ttk.Style(container)
        self.style1.configure('black.TEntry',foreground='black')
        self.style2=ttk.Style(container)
        self.style2.configure('red.TEntry',foreground='red')

        self.grid(columnspan=4, row=0, padx=5, pady=5, sticky="nsew")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Root window configuration
        self.title('Sudoku Solver')
        self.geometry('470x520')
        self.resizable(0, 0)
        self.sudoku=Sudoku()
        # Menu Bar
        self.menu=Menu(self)
        self.config(menu=self.menu)
        # Dictionary that contains the numframe with Entries and Labels
        self.numFrame = numFrame(self)
        # Control Frame
        self.controlFrame=ttk.Frame(self)
        self.solveButton = ttk.Button(self.controlFrame,text='Solve',command=lambda: self.solveButtonCommand())
        self.solveButton.pack(expand=True,side=LEFT)
        self.controlFrame.grid(columnspan=4,row=1,sticky="ew")
        # Bind events
        self.bind("<KeyPress-Right>", lambda e : self.keyRight(e))
        self.bind("<KeyPress-Left>", lambda e : self.keyLeft(e))
        self.bind("<KeyPress-Up>", lambda e : self.keyUp(e))
        self.bind("<KeyPress-Down>", lambda e : self.keyDown(e))

    def keyRight(self,event):
        """ Handler for Arrow Keypress"""
        widget = self.focus_get()
        for i in range(0,9):
            for j in range(0,9):
                if widget==self.numFrame.numWidget[i][j]:
                    if j!=8:
                        self.numFrame.numWidget[i][j+1].focus_set()
                    break

    def keyLeft(self,event):
            """ Handler for Arrow Keypress"""
            widget = self.focus_get()
            for i in range(0,9):
                for j in range(0,9):
                    if widget==self.numFrame.numWidget[i][j]:
                        if j!=0:
                            self.numFrame.numWidget[i][j-1].focus_set()
                        break

    def keyUp(self,event):
            """ Handler for Arrow Keypress"""
            widget = self.focus_get()
            for i in range(0,9):
                for j in range(0,9):
                    if widget==self.numFrame.numWidget[i][j]:
                        if i!=0:
                            self.numFrame.numWidget[i-1][j].focus_set()
                        break

    def keyDown(self,event):
            """ Handler for Arrow Keypress"""
            widget = self.focus_get()
            for i in range(0,9):
                for j in range(0,9):
                    if widget==self.numFrame.numWidget[i][j]:
                        if i!=8:
                            self.numFrame.numWidget[i+1][j].focus_set()
                        break


    def openFile(self):
        filetypes=[('csv files','*.csv')]
        # Dialog to open file
        file=fd.askopenfile(filetypes=filetypes,mode='r')
        # Iterate lines
        for i in range(0,9):
            # Read line remove \n and split to the commas ,
            line=file.readline()
            line=line.replace("\n","").split(',')
            # Check if None exists and handle accordingly
            for j in range(0,9):
                if line[j]!='None':
                    self.sudoku.board[i,j]=int(line[j])
                else:
                    self.sudoku.board[i,j]=None
        file.close()
        self.sudoku.boardOriginal=self.sudoku.board.copy()
        self.printBoard()



    def saveAsFile(self):
        self.saveBoard()
        # Set up dialog to open file
        filetypes=[('txt files','*.csv')]
        filename=fd.asksaveasfile(mode='w',filetypes=filetypes)
        # Print to file
        for i in range(0,9):
            for j in range(0,9):
                if self.sudoku.board[i,j]==None:
                    filename.write('None')    
                else:
                    filename.write(str(self.sudoku.board[i,j]))
                if j==8:
                    filename.write(os.linesep)
                else:
                    filename.write(',')
        filename.close()
        

    def reset(self):
        """ Function that resets the whole app"""
        self.sudoku.reset()
        self.numFrame = numFrame(self)
        

    def printBoard(self):
        """ Function that prints the sudoku.board to the numFrame"""
        for i in range(0,9):
            for j in range(0,9):
                if self.sudoku.board[i,j]==None:
                    text =""
                else:
                    text=self.sudoku.board[i,j]
                    # Check for the new elements and make them red
                    if self.sudoku.boardOriginal[i][j]==None:
                        self.numFrame.numWidget[i][j].config(style='red.TEntry')
                self.numFrame.numWidget[i][j].delete(0,'end')
                self.numFrame.numWidget[i][j].insert(0,str(text))
                

    def solveButtonCommand(self):
        """Function that prints the board for debugging"""
        self.saveBoard()
        self.sudoku.boardOriginal=self.sudoku.board.copy()
        self.sudoku.solve()
        self.printBoard()

    def saveBoard(self):
        """Function that saves the Board tot the Sudoku Class. It checks for errors in the numbers."""
        for i in range(0,9):
            for j in range(0,9):
                # Check if the value in the cell is None or not
                if self.numFrame.numWidget[i][j].get()=='':
                    self.sudoku.board[i,j]=None
                else:
                    # Check if value is integer and between 1 and 9 Else raise exception
                    try:
                        value = int(self.numFrame.numWidget[i][j].get())
                        assert value<=9, "Value is larger than 9"
                        assert value>=1, "Value is lesser than 1"
                        self.sudoku.board[i,j]=value
                    except ValueError as error:
                        showerror(title='Error',message=error)
                    except AssertionError as error:
                        showerror(title='Error',message=error)
                    


if __name__ == "__main__":
    app = App()
    app.mainloop()