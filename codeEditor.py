from tkinter import *
from tkinter import messagebox, filedialog, ttk
import json

# Globals
current_dir = r"c:/documents"
global key_words, comment_line
key_words = ""
comment_line = ""
imageTypes = ['jpeg', 'jpg', 'png', 'ico', 'gif']

# Menu Functions
def new_file(event):
    confirm = messagebox.askyesno("Open New File", "Click yes if older file is saved")
    if confirm:
        global current_dir
        current_dir = r"c:/documents"
        editBox.delete(1.0, END)
        root.title(' THE_ARYA | New File')


def open_file(event):
    global current_dir
    file_ptr = filedialog.askopenfile(mode='r', filetypes=[('All Files', '*.*')],
                                      initialdir=current_dir, title="Open a file | THE_ARYA")
    if file_ptr:
        current_dir = file_ptr.name
        name = current_dir.split("/")[-1]
        file_type = name.split(".")[-1]

        # Check if Image file
        if file_type in imageTypes:
            try:
                editBox["image"] = current_dir
                editBox.delete(0.0, END)
                for record in lineNo.get_children():
                    lineNo.delete(record)
                root.title(" " + name)
                return
            except Exception:
                messagebox.showerror(f"\tUnsupported Image type",
                                     f"This image is not supported try {', '.join(imageTypes)}")
                return

        # Get the keyword list
        with open("keyWordsList.json", "r") as keyJson:
            global key_words, comment_line
            json_list = keyJson.read()
            json_list = json.loads(json_list)
            try:
                key_words = json_list[file_type]["keywords"]
                comment_line = json_list[file_type]["comments"]
            except KeyError:
                messagebox.showerror("\tUnsupported file type", "Goto 'About' Menu to look at the supported file types.")
                return
        keyJson.close()

        for record in lineNo.get_children():
            lineNo.delete(record)
        index = 1
        name = current_dir.split("/")[-1]
        root.title(" "+name)
        editBox.delete(0.0, END)

        # Access line... one at a time
        for line in file_ptr.readlines():
            # print(line.split(' '))
            editBox.insert(END, line)

            # Check if line is a comment
            try:
                if (file_type == "html" or file_type == "html") and line.lstrip()[0]+line.lstrip()[1] in comment_line:
                    editBox.tag_configure("comments", foreground="#EC8B5E", selectforeground='#000000')
                    editBox.tag_add("comments", index + 0.0, "current")
                    lineNo.insert("", index, values=(index,))
                    index += 1
                    continue
                if line.lstrip()[0] in comment_line:
                    editBox.tag_configure("comments", foreground="#EC8B5E", selectforeground='#000000')
                    editBox.tag_add("comments", index + 0.0, "current")
                    lineNo.insert("", index, values=(index,))
                    index += 1
                    continue
            except IndexError:
                pass

            # Check for functions
            i = 0
            while i < len(line):
                if line[i] == '(':
                    if line[i - 1].isalnum() or line[i - 1] == "_":
                        j = i - 1
                        while j >= 0 and (line[j].isalnum() or line[j] == "_" or line[j] == "."):
                            j -= 1
                        start = str(index) + '.' + str(j + 1)
                        end = str(index) + '.' + str(i)
                        editBox.tag_add("functions", start, end)
                i += 1

            # Check for keywords
            for key in key_words:
                i = index + 0.0
                start = editBox.search(rf'{key}[\s:{{\n;(>]', index=i, regexp=True,
                                       forwards=True, stopindex=END)
                if start != "":
                    word = editBox.get(start, start + " wordend")
                    start_int = start.split('.')[0]
                    start_deci = int(start.split('.')[-1])
                    if word == "<":
                        i = start_deci
                        while i < len(line)-1 and line[i] != " " and line[i] != ">":
                            i += 1
                        end = start_int + "." + str(i+1)
                    else:
                        end = start_int + "." + str(start_deci + len(word))
                    editBox.tag_remove("functions", start, end)
                    editBox.tag_add("keywords", start, end)

            # Check for Strings
            i = 0
            while i < len(line):
                if line[i] == '"':
                    j = i + 1
                    while j < len(line) - 1 and line[j] != '"':
                        j += 1
                    start = str(index) + '.' + str(i)
                    end = str(index) + '.' + str(j+1)
                    editBox.tag_remove("functions", start, end)
                    editBox.tag_remove("keywords", start, end)
                    editBox.tag_add("strings", start, end)
                    i = j + 1
                else:
                    i += 1

            lineNo.insert("", index, values=(index,))
            index += 1
        file_ptr.close()


def save_file(event):
    save_confirm = messagebox.askyesno("Save the file", "Are you sure you want to save this file.")
    if save_confirm:
        global current_dir
        try:
            with open(current_dir, "w") as f:
                f.write(editBox.get(1.0, END))
                f.close()
            root.title(f"  {current_dir.split('/')[-1]} --- Modified and Saved")
        except PermissionError:
            save_file_as("e")


def save_file_as(event):
    global current_dir
    file_ptr = filedialog.asksaveasfile(filetypes=[('All Files', '*.*')],
                                        initialdir=current_dir, title="Save file as | THE_ARYA")
    if file_ptr:
        current_dir = file_ptr.name
        root.title(f"  {current_dir.split('/')[-1]}")
        file_ptr.write(editBox.get(1.0, END))
        # Get the keyword list
        with open("keyWordsList.json", "r") as keyJson:
            global key_words, comment_line
            json_list = keyJson.read()
            json_list = json.loads(json_list)
            key_words = json_list[current_dir.split('.')[-1]]["keywords"]
            comment_line = json_list[current_dir.split('.')[-1]]["comments"]
        file_ptr.close()


def theme_set(theme_name):
    if theme_name == "light":
        editBox.tag_configure("functions", foreground="blue", selectforeground='#000000')
        editBox.tag_configure("keywords", foreground="#EE4E34", selectforeground='#000000')
        editBox.tag_configure("strings", foreground="#295F2D", selectforeground='#000000')
        editBox.tag_configure("fg", foreground="black", selectforeground='#000000')
        editBox['bg'] = 'light blue'
        editBox['fg'] = 'black'
        editBox['insertbackground'] = 'black'
    else:
        editBox.tag_configure("functions", foreground="yellow", selectforeground='#000000')
        editBox.tag_configure("keywords", foreground="#2F3C7E", selectforeground='#000000')
        editBox.tag_configure("strings", foreground="#FFE67C", selectforeground='#000000')
        editBox.tag_configure("fg", foreground="white", selectforeground='#000000')
        editBox['bg'] = '#161B21'
        editBox['fg'] = 'white'
        editBox['insertbackground'] = 'white'


def about_app():
    messagebox.showinfo("codeEditor | THE_ARYA\n", "This is a code Editor that supports Text, "
                                                   "Python, C, HTML, CSS, JavaScript, Php, Java, "
                                                   "C++ files\n\n NO ERROR DETECTION SUPPORT")


def editing(event):
    global key_words
    current_pos = editBox.index(INSERT)
    line = editBox.get(current_pos.split(".")[0]+".0", current_pos+" lineend")
    j = int(current_pos.split(".")[-1]) - 1

    # Check for functions
    global func
    func = False
    if len(line) and line[j] == "(":
        j -= 1
        while j >= 0 and (line[j].isalnum() or line[j] == "_" or line[j] == "."):
            j -= 1
        editBox.tag_remove("fg", current_pos.split(".")[0]+"."+str(j), current_pos.split(".")[0]+"."+str(int(current_pos.split(".")[-1])-1))
        editBox.tag_add("functions", current_pos.split(".")[0]+"."+str(j), current_pos.split(".")[0]+"."+str(int(current_pos.split(".")[-1])-1))
        func = True
    else:
        if "(" in line:
            func = True

    # Check for keywords
    j = int(current_pos.split(".")[-1]) - 1
    while j >= 0 and line[j] != " " and line[j] != "\t":
        j -= 1
    word = editBox.get(current_pos.split(".")[0]+"."+str(j+1), current_pos)
    htm = int(current_pos.split(".")[-1]) - 1
    try:
        if line[htm] == ">":
            word = editBox.get(current_pos.split(".")[0]+"."+str(j+1), current_pos.split(".")[0]+"."+str(htm))
    except Exception:
        pass
    if word in key_words:
        editBox.tag_remove("fg", current_pos.split(".")[0]+"."+str(j+1), current_pos)
        editBox.tag_remove("functions", current_pos.split(".")[0]+"."+str(j+1), current_pos)
        editBox.tag_add("keywords", current_pos.split(".")[0]+"."+str(j+1), current_pos)
    else:
        if not func:
            editBox.tag_remove("keywords", current_pos.split(".")[0]+"."+str(j+1), current_pos)
            editBox.tag_remove("functions", current_pos.split(".")[0]+"."+str(j+1), current_pos)
            editBox.tag_add("fg", current_pos.split(".")[0]+"."+str(j+1), current_pos)


def scroll_bar_check():
    try:
        a, b, c, d = ebscrolly.get()
    except Exception:
        x, y = ebscrolly.get()
        lineNo.yview_moveto(str(x))
    threading.Timer(0.01, scroll_bar_check).start()


# def tabbing(event):
#     editBox.insert(editBox.index(INSERT), "   ")


if __name__ == '__main__':
    import threading
    # Initial window setup
    root = Tk()
    root.geometry('1200x750+200+30')
    # root.geometry('500x500')
    root.resizable(True, True)
    root.title(' THE_ARYA | New File')
    icon = PhotoImage(file="codeEditorIcon.png")
    root.iconphoto(False, icon)
    root['bg'] = '#161B21'

    # Menu
    menu = Menu(root)

    file = Menu(menu, tearoff=False)
    file.add_command(label="New", command=lambda: new_file("e"), accelerator="(ctrl+N)")
    file.add_command(label="Open", command=lambda: open_file("e"), accelerator="(ctrl+O)")
    file.add_command(label="Save", command=lambda: save_file("e"), accelerator="(ctrl+S)")
    file.add_command(label="Save As", command=lambda: save_file_as("e"), accelerator="(ctrl+sft+S)")
    menu.add_cascade(label="File", menu=file)
    file['bg'] = 'black'
    file['fg'] = 'white'
    file['activebackground'] = 'yellow'
    file['activeforeground'] = 'black'

    theme = Menu(menu, tearoff=False)
    theme.add_radiobutton(label="Dark", selectcolor="blue", variable='theme',
                          value=1, command=lambda: theme_set('dark'))
    theme.add_radiobutton(label="light", selectcolor="blue", variable='theme',
                          value=0, command=lambda: theme_set('light'))
    menu.add_cascade(label="Theme", menu=theme)
    theme['bg'] = 'black'
    theme['fg'] = 'white'
    theme['activebackground'] = 'yellow'
    theme['activeforeground'] = 'black'

    about = Menu(menu, tearoff=False)
    about.add_command(label="About App", command=about_app)
    menu.add_cascade(label="About", menu=about)
    about['bg'] = 'black'
    about['fg'] = 'white'
    about['activebackground'] = 'yellow'
    about['activeforeground'] = 'black'
    root.config(menu=menu)

    main = Frame(root)
    main.pack(fill=BOTH, expand=True)

    # Scrollbar
    lnscrolly = Scrollbar(main, orient=VERTICAL)
    ebscrolly = Scrollbar(main, orient=VERTICAL)
    ebscrolly.pack(side="right", fill=Y)

    # Line number
    lineNo = ttk.Treeview(main, yscrollcommand=lnscrolly.set)
    lineNo.pack(side="left", fill=Y)
    lineNo["columns"] = ("1",)
    lineNo["show"] = ""
    lineNo.column("1", width=55, anchor=N)
    s = ttk.Style()
    s.theme_use("clam")
    s.configure("Treeview", rowheight=48, background="#161B21", foreground='white', fieldbackground='#161B21', border=SOLID)
    s.map("Treeview", background=[('selected', "white")], foreground=[('selected', "black")])


    # Editor Box
    editBox = Text(main, font=("lucida", 18), pady=15, relief="solid", undo=True, yscrollcommand=ebscrolly.set)
    editBox.pack(fill=BOTH, expand=True, ipadx=15)
    editBox.tag_configure("highlight", background="black")
    editBox['bg'] = '#161B21'
    editBox['fg'] = '#FFFFFF'
    editBox['insertbackground'] = 'white'
    editBox['selectbackground'] = '#F0E68C'
    editBox['selectforeground'] = '#000000'

    # Add scroll command
    lnscrolly.configure(command=lineNo.yview)
    ebscrolly.configure(command=editBox.yview)

    # Call default dark theme
    theme_set('dark')

    # Shortcuts
    editBox.bind("<KeyRelease>", editing)
    root.bind("<Control-n>", new_file)
    root.bind("<Control-o>", open_file)
    root.bind("<Control-s>", save_file)
    root.bind("<Control-Shift-S>", save_file_as)
    root.bind("<Control-z>", lambda e: editBox.edit_undo)
    root.bind("<Control-y>", lambda e: editBox.edit_redo)
    # editBox.bind("<Tab>", tabbing)
    scroll_bar_check()
    root.mainloop()














