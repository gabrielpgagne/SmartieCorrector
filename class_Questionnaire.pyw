"""
This module's purpose is to set up the GUI and manage it.
"""
import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from class_EditQuestion import *

class Questionnaire(Frame):
    """
    Class that manages the question boxes. It is derived from the Frame mother class.
    It includes buttons, question viewer.
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.questionList = [] #general form: [(Q1, A1), (Q2, A2), (Qn, An)]

        f = open('edits.txt', 'w')
        f.close()

        self.userInput = Text(self, height=2, padx=4, pady=4)
        self.userInput.insert(END, 'Write the question here, then press the Add button...')
        self.userInput.grid(row=0)
                
        buttonBox = Frame(self)
        buttonBox.grid(row=1, column=0)

        self.addButton = Button(buttonBox, text='Add', width=8, command=self.addQuestion)
        self.addButton.grid(row=0, column=0, padx=2)
        
        self.editButton = Button(buttonBox, text='Edit', width=8, command=self.editQuestion, state=DISABLED)
        self.editButton.grid(row=0, column=1, padx=2)

        self.delButton = Button(buttonBox, text='Delete', width=8, command=self.delQuestion, state=DISABLED)
        self.delButton.grid(row=0, column=2, padx=2)

        self.reButton = Button(buttonBox, text='Refresh', width=8, command=self.refresh, state=DISABLED)
        self.reButton.grid(row=0, column=3, padx=2)

        self.ldButton = Button(buttonBox, text='Load', width=8, command=self.loadData)
        self.ldButton.grid(row=0, column=4, padx=2)

        self.questionFrame = Frame(self)
        self.questionFrame.grid(row=2)

        self.qBox = Listbox(self.questionFrame)
        self.qBox.insert(END, "Question List")
        self.qBox.grid(row=0, column=0)

        self.qBoxSB = Scrollbar(self.questionFrame, orient='vertical')
        self.qBoxSB.grid(row=0, column=1, sticky='ns')

        self.qBox.config(yscrollcommand=self.qBoxSB.set, width=100)

    def addQuestion(self):
        """
        This method is called when the user wants to add a new question upon the Add button press.
        It doesn't allow for duplicate questions.
        """
        newQ = self.userInput.get('1.0', END)

        if self.duplicateCheck(newQ) == False:
            self.questionList.append((newQ, None))
            if str(self.editButton['state']) == 'disabled':
                self.switchButtonState()
            self.saveData()
            self.updateQuestions()

    def delQuestion(self):
        """
        This method is called when the user wants to delete a question.
        """
        if ((len(self.qBox.curselection()) == 0) or (self.qBox.curselection()[0] == 0)):
            pass
        else:
            self.questionList.pop(self.qBox.curselection()[0]-1)
            self.updateQuestions()
            if len(self.questionList) == 0:
                self.switchButtonState()
            self.saveData()

    def editQuestion(self):
        """
        This method is called when the user wants to edit a question.
        After selecting the question and pressing the Edit button, a pop-up appears asking
        to write the new text. You have to press Refresh afterwards to update.
        """
        if ((len(self.qBox.curselection()) == 0) or (self.qBox.curselection()[0] == 0)):
            pass
        else: 
            selectedIndex = self.qBox.curselection()[0]
            selectedQ = self.questionList[selectedIndex-1]

            EditQuestion(master=self, Ques=selectedQ[0], Ans=selectedQ[1])
            self.reButton.config(state=NORMAL)

    def updateQuestions(self):
        """
        This method updates the question viewing box at the bottom of the screen with the values stored in questionList.
        """
        self.qBox.delete(1, END)
        for i, b in enumerate(self.questionList):
            self.qBox.insert(i+1, b[0])

    def refresh(self):
        """
        This method is called when the user presses the Refresh button.
        Its purpose is to read from the edits done and update the question.
        If the question is unexisting (i.e. refreshing on startup), the question
        is added to questionList.
        """
        try:
            with open('edits.txt', 'r') as fich:
                up = tuple(json.load(fich))
                exists = False
                for i, b in enumerate(self.questionList):
                    if b[0] == up[0]:
                        exists = True
                        self.questionList[i] = up
                    
                if exists == False:
                    self.questionList.append(up)
                    
                self.saveData()
                self.updateQuestions()
        except:
            pass
        self.reButton.config(state=DISABLED)

    def saveData(self):
        """
        This method is called whenever a change has been made to a question or if a new one is added.
        It saves questionList in text file 'data.txt' in List type.
        """
        with open('data.txt', 'w') as fich:
            json.dump(self.questionList, fich)
    
    def loadData(self):
        """
        This method is called when the Load button is pressed.
        It loads the questions stored in the "data.txt" file and updates
        the application.
        """
        pass

    def duplicateCheck(self, question):
        """
        This method checks if question parameter is already existing in questionList.
        If yes, it returns True. If not (the question is unique), False.
        """
        for i in self.questionList:
            if question == i[0]:
                messagebox.showinfo(title='Question Already Existing', message='The question entered already exists.')
                return True
        return False

    def switchButtonState(self):
        """
        Method used to dynamically change the state of the Edit and Delete buttons.
        """
        if str(self.editButton['state']) == 'disabled':
            self.editButton.config(state=NORMAL)
        
        else:
            self.editButton.config(state=DISABLED)

        if str(self.delButton['state']) == 'disabled':
            self.delButton.config(state=NORMAL)
        
        else:
            self.delButton.config(state=DISABLED)

root = Tk()
root.title("Teacher's Question Box Manager")

qFrame = Questionnaire(root)
qFrame.pack()

root.mainloop()
