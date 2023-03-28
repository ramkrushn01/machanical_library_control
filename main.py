import sqlite3
from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import shutil
import os
from PIL import ImageTk,Image
import random


sqliteConnection = sqlite3.connect('db_main.db')
cursor = sqliteConnection.cursor()
m_table_name = "Material_info"

class AddItem:
    def __init__(self):
        self.root = Tk()
        self.root.geometry(
            f'{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0')
        self.root.title("Add Item")

        self.mainFrame = Frame(self.root)
        self.mainFrame.pack()

        self.m_number = StringVar()
        self.m_location = StringVar()
        self.m_name = StringVar()
        self.m_image_uri = ''

        self.l_number = Label(self.mainFrame, text="Enter Material Number: ")
        self.l_number.grid(column=0, row=0)
        self.m_number_entry = ttk.Entry(
            self.mainFrame, textvariable=self.m_number, width=30)
        self.m_number_entry.grid(column=1, row=0, pady=10, padx=5)

        self.l_location = Label(
            self.mainFrame, text="Enter Material Location: ")
        self.l_location.grid(column=0, row=1)
        self.m_location_entry = ttk.Entry(
            self.mainFrame, textvariable=self.m_location, width=30)
        self.m_location_entry.grid(column=1, row=1, pady=10, padx=5)

        self.l_name = Label(self.mainFrame, text="Enter Material Name: ",)
        self.l_name.grid(column=0, row=2)
        self.m_name_entry = ttk.Entry(
            self.mainFrame, textvariable=self.m_name, width=30)
        self.m_name_entry.grid(column=1, row=2, pady=10, padx=5)

        self.l_photo_uri = Label(
            self.mainFrame, text="Choice File for Material Image: ")
        self.l_photo_uri.grid(column=0, row=3)
        self.m_photo_uri_entry = ttk.Button(
            self.mainFrame, text='Choice File', width=30, command=self.getImageLocation)
        self.m_photo_uri_entry.grid(column=1, row=3, pady=10, padx=5)

        self.add_btn = ttk.Button(self.mainFrame, text='Add', command=self.saveTheData)
        self.add_btn.grid(column=1, row=4)

        self.root.mainloop()

    def getImageLocation(self):
        if not os.path.exists('Material_Images'):
            os.mkdir('Material_Images')

        self.m_photo_uri = fd.askopenfile(
            filetypes=[("Image", ".png .jpg .jpeg")])
        if self.m_photo_uri is not None:
            self.file_name = self.m_photo_uri.name
            self.new_file_name = f'Material_Images/{self.m_number.get()}{os.path.splitext(self.m_photo_uri.name)[1]}'

            if os.path.exists(self.new_file_name):
                if mb.askquestion("Replace File", 'File allready Exist You want replace the file') == 'yes':
                    shutil.copy(self.file_name, self.new_file_name)
                    print('file_relpaced')
            else:
                shutil.copy(self.file_name, self.new_file_name)

            self.m_image_uri = self.new_file_name

            self.img = Image.open(self.m_image_uri)
            self.img = self.img.resize((500,500))

            self.img = ImageTk.PhotoImage(self.img)
            self.ImgPanel = ttk.Label(self.mainFrame,image=self.img)
            self.ImgPanel.grid(column=0,row=5,columnspan=3)

            return self.new_file_name
        ...

    def saveTheData(self):
        try:
            if self.m_name.get() == '' or self.m_location.get() == '' or self.m_name.get() == '' or self.m_image_uri == '':
                mb.showerror(title="Field required",message="Please Enter all fields")
                return
            
            cursor.execute(f'''INSERT INTO {m_table_name} VALUES ('{self.m_number.get()}', '{self.m_location.get()}', '{self.m_name.get()}', '{self.m_image_uri}')''')
            sqliteConnection.commit()

            mb.showinfo(title="Success",message="Data save successfully!")
            self.m_name.set('')
            self.m_location.set('')
            self.m_number.set('')
            self.m_name.set('')
            self.m_image_uri = ''

            self.ImgPanel.destroy()

        except Exception as ee:
            mb.showerror(title="Error",message=str(ee))


class SearchItem:
    TableColumnName = ('Material_Number', 'Location',
                       'Name', 'Image', 'Edit','Delete')

    def __init__(self) -> None:
        self.root = Tk()
        self.root.geometry(
            f'{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0')
        self.root.title('Search Item')

        self.topFrame = Frame(self.root)
        self.topFrame.pack()
        
        
        self.itemNumberValue = StringVar(self.root)

        textLabel = ttk.Label(self.topFrame, text="Item Number: ")
        textLabel.grid(column=0,row=0)

        self.itemNumber = ttk.Entry(self.topFrame, textvariable=self.itemNumberValue)
        self.itemNumber.grid(column=1,row=0,pady=10)

        self.b_search = ttk.Button(self.topFrame,text='search',command=self.searchAdd)
        self.b_search.grid(column=1,row=1)

        self.frameTreeView = ttk.Frame(self.root)
        self.frameTreeView.pack(fill=BOTH, expand=True)

        self.treeView = ttk.Treeview(
            self.frameTreeView, columns=self.TableColumnName)
        self.treeView['show'] = 'headings'

        self.scbar = ttk.Scrollbar(
            self.frameTreeView, orient=VERTICAL, command=self.treeView.yview)
        self.scbar.pack(side=RIGHT, fill=BOTH)
        self.treeView.configure(xscrollcommand=self.scbar)

        for i in self.TableColumnName:
            self.treeView.heading(i, text=i)

        self.treeView.pack(expand=True, fill=BOTH)
        self.root.mainloop()
    
    def searchAdd(self):
        q = f'''SELECT * FROM {m_table_name} WHERE Material_number='{self.itemNumberValue.get()}' '''
        data = cursor.execute(q)
            
        for i in data:
            self.treeView.insert('','end',text=i[0],values=i)


class MainPage:
    def __init__(self):

        self.root = Tk()

        w_screen = self.root.winfo_screenwidth()
        h_screen = self.root.winfo_screenheight()

        self.root.geometry(f'400x200+{w_screen//2-200}+{h_screen//2-100}')
        self.root.resizable(False, False)

        btn_search = ttk.Button(self.root, text="Search", width=25, command=SearchItem)
        btn_search.pack()

        btn_add = ttk.Button(self.root, text="Add", width=25, command=AddItem)
        btn_add.pack(pady=20)

        self.root.mainloop()
    



def createRequiredTables():
    res = cursor.execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{m_table_name}'")

    if len(list(res)) == 0:
        cursor.execute(f""" 
            CREATE TABLE {m_table_name} (
            Material_number VARCHAR(255) NOT NULL UNIQUE,
            Material_location VARCHAR(255) NOT NULL,
            Material_name VARCHAR(255) NOT NULL,
            Material_photo_uri VARCHAR(255) NOT NULL
        )
        """)
        print(f'table create successfully {m_table_name}')
    else:
        print(f'Table {m_table_name} is all ready exists')

if __name__ == "__main__":
    createRequiredTables()

    main_page = MainPage()
    # addItem = AddItem()
    # searchItem = SearchItem()
