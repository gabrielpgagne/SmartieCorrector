import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from class_EditQuestion import *
import class_Questionnaire as qu
import text_analysis as ta
import re

def submitAnswers():
    expr = r"\\n"
    for i, b in enumerate(textInputs):
        inputValue = b.get("1.0", END)
        inputValue = re.sub(expr, "", inputValue)
        q = re.sub(expr, "", questionList[i][0])
        a = re.sub(expr, "", questionList[i][1])
        # prints for test purposes
        print(a)
        print(b)
        print(inputValue)
        # end of prints
        analysis = ta.QuestionContainer(q, a, inputValue)

        resOutputs[i].config(text='Result:' + str(analysis.compareAnswers()))


if __name__ == "__main__":
    root = Tk()
    root.title("Student's Answer Box")

    aFrame = Frame(root)
    aFrame.pack()

    with open('data.txt', 'r') as fich:
            questionList = json.load(fich)
    
    textInputs = []
    resOutputs = []
    for i in range(len(questionList)):
        question = Label(aFrame, text=questionList[i][0])
        question.grid(row=2*i, column=0)

        textbox = Text(aFrame, height=3, width=50)
        textbox.insert(END, 'Write answer here...')
        textbox.grid(row=((2*i)+1), column=0)
        textInputs.append(textbox)

        res = Label(aFrame)
        res.grid(row=2*i, column=1)
        resOutputs.append(res)

        if i == (len(questionList) - 1):
            submitButton = Button(aFrame, text='Submit', command=lambda: submitAnswers())
            submitButton.grid(row=((2*i)+2), column=0)
            
    root.mainloop()