import os
from tkinter import *
from tkinter import messagebox, filedialog
import json
import string

# Globals
paranthesis = ['(', ')', '{', '}', '[', ']', '<', '>']

def editor():
    pass

# Menu Functions
def openFile():
    filePtr = filedialog.askopenfile(mode='r', filetypes=[('All Files', '*.*')], initialdir=os.getcwd(), title="Open a file | THE_ARYA")
    if filePtr:
        index = 1
        name = filePtr.name.split("/")[-1]
        type = name.split(".")[1]
        root.title("  "+name)
        editBox.delete(0.0, END)

        # Get the keyword list
        with open("keyWordsList.json", "r") as keyJson:
            jsonList = keyJson.read()
            jsonList = json.loads(jsonList)
            keyWords = jsonList[type]["keywords"]
            commentLine = jsonList[type]["comments"]
            keyJson.close()

        # Access line... one at a time
        for line in filePtr.readlines():
            editBox.insert(END, line)
            # Call editor
            # editor()

            # Check if line is a comment
            strippedLine = line.lstrip()
            # print(line)
            try:
                if strippedLine[0] in commentLine:
                    editBox.tag_configure("comments", foreground="#EC8B5E")
                    editBox.tag_add("comments", index + 0.0, "current")
                    index += 1
                    continue
            except Exception as e:
                pass

            # Check for string
            i = 0
            while i < len(line):
                if line[i] == '"':
                    j = i + 1
                    while j < len(line)-1 and line[j] != '"':
                        j += 1
                    if line[j] == '"':
                        start = index + float('0.' + str(i))
                        end = index + float('0.' + str(j+1))
                        editBox.tag_configure("string", foreground="green")
                        editBox.tag_add("string", start, end)
                        i = j + 1
                    else:
                        i += 1
                else:
                    i += 1

            # Check for functions
            i = 0
            while i < len(line):
                if line[i] == '(':
                    if line[i-1].isalnum() or line[i-1] == "_":
                        j = i - 1
                        while (line[j].isalnum() or line[j] == "_" or line[j] == ".") and j >= 0:
                            j -= 1
                        start = index + float('0.' + str(j+1))
                        end = index + float('0.' + str(i))
                        editBox.tag_configure("functions", foreground="yellow")
                        editBox.tag_remove("string", start, end)
                        editBox.tag_add("functions", start, end)
                i += 1

            # Check for keywords
            i = 0
            while i < len(line) and (line[i] == " " or line[i] == "\t"):
                i += 1
            while i < len(line):
                j = i
                while j < len(line) and line[j].isalnum():
                    j += 1
                start = index + float('0.' + str(i))
                end = index + float('0.' + str(j))
                word = editBox.get(start, end)
                if word in keyWords:
                    editBox.tag_configure("keyword", foreground="#2F3C7E")
                    editBox.tag_remove("string", start, end)
                    editBox.tag_remove("functions", start, end)
                    editBox.tag_add("keyword", start, end)
                i = j + 1

            index += 1

        filePtr.close()


def saveFile():
    pass

def saveAsFile():
    pass

def themeSet(theme):
    if theme == "light":
        editBox['bg'] = '#AA96DA'
        editBox['fg'] = 'black'
        editBox['insertbackground'] = 'black'
    else:
        editBox['bg'] = '#161B21'
        editBox['fg'] = 'white'
        editBox['insertbackground'] = 'white'

def aboutApp():
    messagebox.showinfo("codeEditor | THE_ARYA\n", "This is a code Editor that supports Text, "
                                                   "Python, C, HTML, CSS, JavaScript, Php, Java, "
                                                   "C++ files\n\n NO ERROR DETECTION SUPPORT")

def editting(event):
    pass


if __name__ == '__main__':
    # Initial window setup
    root = Tk()
    # root.geometry('1200x750+200+30')
    root.geometry('500x500')
    root.resizable(True, True)
    root.title('   codeEditor | THE_ARYA')
    icon = PhotoImage(file="codeEditorIcon.png")
    root.iconphoto(False, icon)
    root['bg'] = '#161B21'

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

    theme = Menu(menu, tearoff=False)
    theme.add_radiobutton(label="Dark", selectcolor="blue", variable='theme', value='dark', command=lambda :themeSet('dark'))
    theme.add_radiobutton(label="light", selectcolor="blue", variable='theme', value='light', command=lambda :themeSet('light'))
    menu.add_cascade(label="Theme", menu=theme)
    theme['bg'] = 'black'
    theme['fg'] = 'white'
    theme['activebackground'] = 'yellow'
    theme['activeforeground'] = 'black'

    about = Menu(menu, tearoff=False)
    about.add_command(label="About App", command=aboutApp)
    menu.add_cascade(label="About", menu=about)
    about['bg'] = 'black'
    about['fg'] = 'white'
    about['activebackground'] = 'yellow'
    about['activeforeground'] = 'black'
    root.config(menu=menu)

    # Scrollbar
    scroll = Scrollbar(root)
    scroll.pack(side="right", fill=Y)

    #Editor Box
    editBox = Text(root, font=("lucida", 18), spacing1=15, relief="solid", yscrollcommand=scroll.set)
    editBox.pack(fill=BOTH, padx=(18, 5), ipadx=15)
    editBox['bg'] = '#161B21'
    editBox['fg'] = '#FFFFFF'
    editBox['insertbackground'] = 'white'
    editBox.bind("<Key>", editting)
    # Add scroll command
    scroll.configure(command=editBox.yview)

    # openFile()


    root.mainloop()

