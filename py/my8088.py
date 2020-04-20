#pyinstaller --onefile --hidden-import tkinter new.py

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
from os import system
import spi8088

def donothing():
   print("Hello World")

def new_file():
    text_field.delete(1.0,END)
    main_window.title("8088 Uploader")
    main_window.file_and_path = ''

def open_file():
    file_name = filedialog.askopenfilename(initialdir = "/home/pi",title = "Open",filetypes = (("Assembly","*.asm"),("all files","*.*")))
    if file_name:
        file_open = open(file_name)
        file_data = file_open.read()
        file_open.close()
        text_field.delete(1.0,END)
        text_field.insert(END, file_data)
        main_window.file_and_path = file_name
        main_window.title("8088 Uploader " + main_window.file_and_path)

def save_file():
    if(main_window.file_and_path == ''):
        file_save = filedialog.asksaveasfile(mode='w', initialdir = "/home/pi",title = "Save",filetypes = (("Assembly","*.asm"),("all files","*.*")))
        if file_save:
            file_save.write(text_field.get(1.0,END))
            main_window.file_and_path = file_save.name
            main_window.title("8088 Uploader " + main_window.file_and_path)
            file_save.close()
    else:
        file_save = open(main_window.file_and_path, 'w')
        file_save.write(text_field.get(1.0,END))
        file_save.close()

def save_as_file():
        file_save = filedialog.asksaveasfile(mode='w', initialdir = "/home/pi",title = "Save As",filetypes = (("Assembly","*.asm"),("all files","*.*")))
        if file_save:
            file_save.write(text_field.get(1.0,END))
            main_window.file_and_path = file_save.name
            main_window.title("8088 Uploader " + main_window.file_and_path)
            file_save.close()

def Compile_and_Upload():
    if(main_window.file_and_path == ''):
        messagebox.showinfo("Compiler Error", "File not open or saved!")

    else:
        file_save = open(main_window.file_and_path, 'w')
        file_save.write(text_field.get(1.0,END))
        file_save.close()

        main_window.file_and_path_bin = main_window.file_and_path[:-4] + '.bin'
        os.system("nasm " + main_window.file_and_path + ' -o ' + main_window.file_and_path_bin)

        if os.path.exists(main_window.file_and_path[:-4] + '.bin'):
            file_open = open(main_window.file_and_path[:-4] + '.bin', mode='rb')
            file_data = file_open.read()
            file_open.close()

            Jump_code = [0XEA, 0X00, 0X00, 0X00, 0XF0]

            spi8088.Hold(True)
            spi8088.Write_Memory_Array(0xFFFF0, Jump_code)
            spi8088.Write_Memory_Array(0xF0000, file_data)
            spi8088.Hold(False)

            spi8088.Reset()
        else:
            messagebox.showinfo("Compiler Error", "bin file was not compiled check NASM output for errors")

def Compile_code():
    if(main_window.file_and_path == ''):
        messagebox.showinfo("Compiler Error", "File not open or saved!")

    else:
        file_save = open(main_window.file_and_path, 'w')
        file_save.write(text_field.get(1.0,END))
        file_save.close()

        main_window.file_and_path_bin = main_window.file_and_path[:-4] + '.bin'
        os.system("nasm " + main_window.file_and_path + ' -o ' + main_window.file_and_path_bin)

def Upload_code():
    if(main_window.file_and_path != ''):
        if os.path.exists(main_window.file_and_path[:-4] + '.bin'):
            file_open = open(main_window.file_and_path[:-4] + '.bin', mode='rb')
            file_data = file_open.read()
            file_open.close()

            Jump_code = [0XEA, 0X00, 0X00, 0X00, 0XF0]

            spi8088.Hold(True)
            spi8088.Write_Memory_Array(0xFFFF0, Jump_code)
            spi8088.Write_Memory_Array(0xF0000, file_data)
            spi8088.Hold(False)

            spi8088.Reset()



def Bus_Hold():
    spi8088.Hold(True)

def Bus_Release():
    spi8088.Hold(False)

def Reset_CPU():
    spi8088.Reset()


# Create the main window
main_window = Tk()
main_window.title("8088 Uploader")
main_window.minsize(800, 600)



menubar = Menu(main_window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=new_file)
filemenu.add_command(label="Open", command=open_file)
filemenu.add_command(label="Save", command=save_file)
filemenu.add_command(label="Save As", command=save_as_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=main_window.destroy)
menubar.add_cascade(label="File", menu=filemenu)

controlmenu = Menu(menubar, tearoff=0)
controlmenu.add_command(label="Hold", command=Bus_Hold)
controlmenu.add_command(label="Release", command=Bus_Release)
controlmenu.add_command(label="Reset CPU", command=Reset_CPU)
menubar.add_cascade(label="CPU Control", menu=controlmenu)

buildmenu = Menu(menubar, tearoff=0)
buildmenu.add_command(label="Compile -> Upload", command=Compile_and_Upload)
buildmenu.add_command(label="Compile", command=Compile_code)
menubar.add_cascade(label="Build", menu=buildmenu)

main_window.config(menu=menubar)

main_window.file_and_path = ''
main_window.file_and_path_bin = ''

text_field = Text(main_window)
#text_field.wrap (WORD)
text_field.pack(expand=True, fill='both')
# Run forever!
scrollbar = Scrollbar(text_field)
scrollbar.pack( side = RIGHT, fill = Y )


spi8088.Start_SPI()

main_window.mainloop()

spi8088.spi.close()