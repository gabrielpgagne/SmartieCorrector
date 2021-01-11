from tkinter import *
from tkinter.ttk import *
import json
           
class EditQuestion(Toplevel):
    """
    This class is used to generate a pop-up window to edit a question and see its attributes.
    """
    def __init__(self, Ques, Ans=0, master=None):
        super().__init__(master)
        self.title(f'{Ques} Viewer and Editor')
        self.Data = [Ques, Ans]
        
        self.QABox = Frame(self)
        self.QABox.grid(row=0, column=0)

        L1 = Label(self.QABox, text='Question:')
        L1.grid(row=0, column=0, sticky=W)

        L2 = Label(self.QABox, text='Current Answer:')
        L2.grid(row=0, column=1, sticky=W)


        self.QLabel = Label(self.QABox, text=self.Data[0])
        self.QLabel.grid(row=1, column=0, padx = 4, pady=4)

        self.ALabel = Label(self.QABox, text=self.Data[1])
        self.ALabel.grid(row=1, column=1, padx = 4, pady=4)

        self.updateQABox()

        self.bBox = Frame(self)
        self.bBox.grid(row=1, column=0, padx=4, pady=4)

        editB = Button(self.bBox, text='Edit', command=self.editQuestion)
        editB.grid(row=1, column=0)
        confirmB = Button(self.bBox, text='Confirm', command=self.confirm)
        confirmB.grid(row=1, column=1)
        cancelB = Button(self.bBox, text='Cancel', command=self.destroy)
        cancelB.grid(row=1, column=2)

    def editQuestion(self):
        """
        This method is called when the user wants to edit the question.
        It pops up a Toplevel widget with a simple textbox and a Confirm and Delete buttons.
        """
        def ConfirmBInput():
            self.Data[1] = str(textbox.get('1.0', END)) #Line 1 char 0 to end
            if len(self.Data[1]) == 0:
                self.Data[1] = None
            self.updateQABox()
            editWin.destroy()
        
        editWin = Toplevel(self)
        editWin.title(f'Editing Question {self.Data[0]}')

        textbox = Text(editWin)
        textbox.insert(END, 'Enter new answer here...')
        textbox.grid(row=0, column=0)

        bBox = Frame(editWin)
        bBox.grid(row=1, column=0)

        ConfirmB = Button(bBox, text='Confirm', command=ConfirmBInput)
        ConfirmB.grid(row=0, column=0)
        CancelB = Button(bBox, text='Cancel', command=editWin.destroy)
        CancelB.grid(row=0, column=1)

    def confirm(self):
        with open('edits.txt', 'w') as fich:
            json.dump(self.Data, fich)

        self.destroy()

    def updateQABox(self):
        """
        Updates the question and answer box at the top of the screen with 
        Data attribute's values.
        """
        self.QLabel.config(text=self.Data[0])

        if self.Data[1] == None:
            self.ALabel.config(text='No answer has been set for this question.')
        else: 
            self.ALabel.config(text=self.Data[1])