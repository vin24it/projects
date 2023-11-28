import tkinter as tk
from tkinter import filedialog, simpledialog

def open_file():
    file_path = filedialog.askopenfilename()
    with open(file_path, 'r') as file:
        text_widget.delete(1.0, "end")
        text_widget.insert("end", file.read())

def save_file():
    file_path = filedialog.asksaveasfilename()
    with open(file_path, 'w') as file:
        file.write(text_widget.get("1.0", "end"))

def new_file():
    text_widget.delete(1.0, "end")

def close_tab():
    text_widget.delete(1.0, "end")

def close_window():
    root.destroy()

def cut_text():
    text_widget.event_generate("<<Cut>>")

def copy_text():
    text_widget.event_generate("<<Copy>>")

def paste_text():
    text_widget.event_generate("<<Paste>>")

def delete_text():
    text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)

def select_all_text():
    text_widget.tag_add("sel", "1.0", "end")
    text_widget.mark_set(tk.SEL_FIRST, "1.0")
    text_widget.mark_set(tk.SEL_LAST, "end")

text_font = ("Times New Roman", 12)

def zoom_in():
    global text_font
    text_font_size = int(text_font[1])
    text_font_size += 4
    text_font = ("Times New Roman", text_font_size)
    text_widget.configure(font=text_font)

def zoom_out():
    global text_font
    text_font_size = int(text_font[1])
    text_font_size = max(6, text_font_size - 2)
    text_font = ("Times New Roman", text_font_size)
    text_widget.configure(font=text_font)

def find_text():
    search_query = simpledialog.askstring("Find", "Enter text to find:")
    if search_query:
        search_text(search_query)

def search_text(query):
    text_widget.tag_remove("found", "1.0", "end")
    start = "1.0"
    while True:
        start = text_widget.search(query, start, stopindex="end", nocase=True)
        if not start:
            break
        end = f"{start}+{len(query)}c"
        text_widget.tag_add("found", start, end)
        text_widget.tag_configure("found", background="yellow")
        start = end


def new_window():
    new_root = tk.Tk()
    new_root.title("Text Editor - New Window")
    new_text_widget = tk.Text(new_root, font=text_font)
    new_text_widget.pack(fill="both", expand=True)
   
    new_menu = tk.Menu(new_root)
    new_root.config(menu=new_menu)
    new_file_menu = tk.Menu(new_menu)
    new_edit_menu = tk.Menu(new_menu)
    new_view_menu = tk.Menu(new_menu)
    new_menu.add_cascade(label="File", menu=new_file_menu)
    new_file_menu.add_command(label="New", command=new_file)
    new_file_menu.add_separator()
    new_file_menu.add_command(label="New Window", command=new_window)
    new_file_menu.add_separator()
    new_file_menu.add_command(label="Open", command=open_file)
    new_file_menu.add_separator()
    new_file_menu.add_command(label="Save", command=save_file)
    new_file_menu.add_separator()
    new_file_menu.add_command(label="Exit", command=new_root.quit)
    new_file_menu.add_separator()
    new_file_menu.add_command(label="Close Tab", command=close_tab)
    new_file_menu.add_separator()
    new_file_menu.add_command(label="Close Window", command=close_window)
    
    new_menu.add_cascade(label="Edit", menu=new_edit_menu)
    new_edit_menu.add_command(label="Cut", command=cut_text)
    new_edit_menu.add_separator()
    new_edit_menu.add_command(label="Copy", command=copy_text)
    new_edit_menu.add_separator()
    new_edit_menu.add_command(label="Paste", command=paste_text)
    new_edit_menu.add_separator()
    new_edit_menu.add_command(label="Delete", command=delete_text)
    new_edit_menu.add_separator()
    new_edit_menu.add_command(label="Select All", command=select_all_text)
    
    new_menu.add_cascade(label="Edit", menu=new_view_menu)
    new_view_menu.add_command(label="Zoom In", command=zoom_in)
    new_view_menu.add_separator()
    new_view_menu.add_command(label="Zoom Out", command=zoom_out)
    new_view_menu.add_separator()
    new_view_menu.add_command(label="Find", command=find_text)

    new_root.mainloop()

def exit_editor():
    root.quit()

root = tk.Tk()
root.title("Text Editor")

text_widget = tk.Text(root, font=text_font)
text_widget.pack(fill="both", expand=True)

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu)
edit_menu = tk.Menu(menu)
view_menu = tk.Menu(menu)


menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_separator()
file_menu.add_command(label="New Window", command=new_window)
file_menu.add_separator()
file_menu.add_command(label="Open", command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Close Tab", command=close_tab)
file_menu.add_separator()
file_menu.add_command(label="Close Window", command=close_window)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_editor)

menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_separator()
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_separator()
edit_menu.add_command(label="Paste", command=paste_text)
edit_menu.add_separator()
edit_menu.add_command(label="Delete", command=delete_text)
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=select_all_text)

menu.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Zoom In", command=zoom_in)
view_menu.add_separator()
view_menu.add_command(label="Zoom Out", command=zoom_out)
view_menu.add_separator()
view_menu.add_command(label="Find", command=find_text)

root.mainloop()
