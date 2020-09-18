from tkinter import *
from tkinter import messagebox, filedialog
import json

# Global
# parantises = ['(', ')', '{', '}', '[', ']', '<', '>']
current_dir = r"c:/documents"


def editor(event):
    pass


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
        index = 1
        name = current_dir.split("/")[-1]
        file_type = name.split(".")[-1]
        root.title(" "+name)
        editBox.delete(0.0, END)

        # Get the keyword list
        with open("keyWordsList.json", "r") as keyJson:
            json_list = keyJson.read()
            json_list = json.loads(json_list)
            key_words = json_list[file_type]["keywords"]
            comment_line = json_list[file_type]["comments"]
        keyJson.close()

        # Access line... one at a time
        for line in file_ptr.readlines():
            editBox.insert(END, line)
            # Call editor
            # editor()

            # Check if line is a comment
            try:
                if line.lstrip()[0] in comment_line:
                    editBox.tag_configure("comments", foreground="#EC8B5E")
                    editBox.tag_add("comments", index + 0.0, "current")
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
                        editBox.tag_configure("functions", foreground="yellow")
                        editBox.tag_add("functions", start, end)
                i += 1

            # Check for keywords
            for key in key_words:
                i = index + 0.0
                start = editBox.search(rf'{key}[\s:{{\n;(]', index=i, regexp=True,
                                       forwards=True, stopindex=END)
                if start != "":
                    word = editBox.get(start, start + " wordend")
                    start_int = start.split('.')[0]
                    start_deci = int(start.split('.')[-1])
                    end = start_int + "." + str(start_deci + len(word))
                    editBox.tag_configure("keywords", foreground="#2F3C7E")
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
                    editBox.tag_configure("strings", foreground="#FFE67C")
                    editBox.tag_remove("functions", start, end)
                    editBox.tag_remove("keywords", start, end)
                    editBox.tag_add("strings", start, end)
                    i = j + 1
                else:
                    i += 1

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
        file_ptr.close()


def theme_set(theme_name):
    if theme_name == "light":
        editBox.tag_configure("functions", foreground="blue")
        editBox.tag_configure("keywords", foreground="#EE4E34")
        editBox.tag_configure("strings", foreground="#295F2D")
        editBox['bg'] = 'light blue'
        editBox['fg'] = 'black'
        editBox['insertbackground'] = 'black'
    else:
        editBox.tag_configure("functions", foreground="yellow")
        editBox.tag_configure("keywords", foreground="#2F3C7E")
        editBox.tag_configure("strings", foreground="#FFE67C")
        editBox['bg'] = '#161B21'
        editBox['fg'] = 'white'
        editBox['insertbackground'] = 'white'


def about_app():
    messagebox.showinfo("codeEditor | THE_ARYA\n", "This is a code Editor that supports Text, "
                                                   "Python, C, HTML, CSS, JavaScript, Php, Java, "
                                                   "C++ files\n\n NO ERROR DETECTION SUPPORT")


def editing():
    pass


if __name__ == '__main__':
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
    file.add_command(label="Save As", command=lambda: save_file_as("e"), accelerator="(ctrl+shift+N)")
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

    # Scrollbar
    scrolly = Scrollbar(root, orient=VERTICAL)
    scrolly.pack(side="right", fill=Y)
    scrollx = Scrollbar(root, orient=HORIZONTAL)
    scrollx.pack(side="bottom", fill=X)

    # Editor Box
    editBox = Text(root, font=("lucida", 18), spacing1=15, relief="solid", undo=True,
                   yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    editBox.pack(fill=BOTH, expand=True, padx=(18, 0), ipadx=15)
    editBox['bg'] = '#161B21'
    editBox['fg'] = '#FFFFFF'
    editBox['insertbackground'] = 'white'
    # editBox.bind("<Key>", editing)
    # Add scroll command
    scrolly.configure(command=editBox.yview)
    scrollx.configure(command=editBox.xview)

    # Save file shortcut
    root.bind("<Control-n>", new_file)
    root.bind("<Control-o>", open_file)
    root.bind("<Control-s>", save_file)
    root.bind("<Control-Shift-S>", save_file_as)
    root.bind("<Control-z>", lambda e: editBox.edit_undo)
    root.bind("<Control-y>", lambda e: editBox.edit_redo)

    root.mainloop()



