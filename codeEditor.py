import os
from tkinter import *
from tkinter import messagebox, filedialog

#Globals
indexCount = 0.0

# Initial window setup
root = Tk()
root.geometry('1200x750+200+30')
root.resizable(True, True)
root.title('   codeEditor | THE_ARYA')
icon = PhotoImage(file="codeEditorIcon.png")
root.iconphoto(False, icon)
root['bg'] = 'black'

# Menu Functions
def openFile():
    filePtr = filedialog.askopenfile(mode='r', filetypes=[('All Files', '*.*')], initialdir=os.getcwd(), title="Open a file to edit | THE_ARYA")
    if filePtr:
        root.title = os.getcwd()
        editBox.delete(0.0, END)
        for line in filePtr.readlines():
            editBox.insert(END, line)
        filePtr.close()

def saveFile():
    pass
def saveAsFile():
    pass
def aboutApp():
    messagebox.showinfo("codeEditor | THE_ARYA\n", "This is a code Editor that supports Text, "
                                                   "Python, C, HTML, CSS, JavaScript, Php, Java, "
                                                   "C++ files\n\n NO ERROR DETECTION")

def indexer(keyType):
    global indexCount
    if keyType == 'key':
        indexCount += 0.1
    else:
        indexCount += 1.0

def editting(event):
    pass
# Menu
menu = Menu(root)

file = Menu(menu, tearoff=False)
file.add_command(label="Open", command=openFile)
file.add_command(label="Save", command=saveFile)
file.add_command(label="Save As", command=saveAsFile)
menu.add_cascade(label="File", menu=file)
file['bg'] = 'black'
file['fg'] = 'white'
file['activebackground'] = 'yellow'
file['activeforeground'] = 'black'

about = Menu(menu, tearoff=False)
about.add_command(label="About App", command=aboutApp)
menu.add_cascade(label="About", menu=about)
about['bg'] = 'black'
about['fg'] = 'white'
about['activebackground'] = 'yellow'
about['activeforeground'] = 'black'
root.config(menu=menu)

#Editor Box
editBox = Text(root, height=20, width=90, font=("lucida", 18), spacing1=15)
editBox.pack()
editBox['bg'] = 'black'
editBox['fg'] = 'white'
editBox['insertbackground'] = 'white'

# editBox.bind("<Return>", lambda event: indexer('enter'))
# editBox.bind("<space>", editting)
editBox.bind("<Key>", editting)







root.mainloop()

