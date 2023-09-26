# ***** PROJECT 'PROGRAMMATORE PYTHON' SEPTEMBER 2023   *****
# ***** Author: Agnese Re (with learners collaboration) *****
# ***** Last update: Wednesday 2023-09-27T01:13:30      ***** 
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk

# ***** FUNCTIONS *****
def add_contact():
    # Extract data from entry fields
    name = name_entry.get()
    telephone = telephone_entry.get()
    email = email_entry.get()
    address = address_entry.get()
    if name and telephone and email and address:
        # Create a new dictionary for collecting contact information
        contact = {"Nome":name, "Telefono":telephone, "Email":email, "Indirizzo":address}
        # Add dictionary to the list 'rubrica'
        rubrica.append(contact)
        cursor.execute("INSERT INTO CONTATTI VALUES (?, ?, ?, ?)", (name, telephone, email, address))
        conn.commit()
        print_contacts(rubrica, treeview_contacts)
        # Clear fields
        name_entry.delete(0, tk.END)
        telephone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
    else:
        tk.messagebox.showwarning("Errore", message = "Alcuni campi NON sono compilati")

def search_contact():
    treeview_sr.delete(*treeview_sr.get_children())
    searched_field = wanted_entry.get()
    contatti_cercati = []
    for contatto in rubrica:
        if(contatto["Nome"] == searched_field or contatto["Email"] == searched_field or
            contatto["Indirizzo"] == searched_field):
            contatti_cercati.append(contatto)
    print_contacts(contatti_cercati, treeview_sr)

def print_contacts(lista_contatti: list, treeview: ttk.Treeview):
    treeview.delete(*treeview.get_children())
    for contatto in lista_contatti:
        treeview.insert("", tk.END, values = [contatto["Nome"], contatto["Telefono"], contatto["Email"], contatto["Indirizzo"]])

def present_contact(contatto):
    # return "%-20s %-15s %-30s %-20s" %(contatto["Nome"], contatto["Telefono"], contatto["Email"], contatto["Indirizzo"])
    return f"{contatto['Nome']:20}{contatto['Telefono']:15}{contatto['Email']:30}{contatto['Indirizzo']:20}"

def hide_initial_empty_column_tree(treeview: ttk.Treeview):
    treeview.column("#0", width = 0, stretch = tk.NO)
    
def set_treeview(treeview: ttk.Treeview):
    treeview.heading("Nome", text = "Nome", anchor = tk.W)
    treeview.heading("Telefono", text = "Telefono", anchor = tk.W)
    treeview.heading("Email", text = "Email", anchor = tk.W)
    treeview.heading("Indirizzo", text = "Indirizzo", anchor = tk.W)
    treeview.column("Nome", width = 150)
    treeview.column("Telefono", width = 100)
    treeview.column("Email", width = 200)
    treeview.column("Indirizzo", width = 150)

# ***** FUNCTIONS DB ******
def db_connect():
    conn = sqlite3.connect("rubrica.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS CONTATTI(name VARCHAR(255), telefono VARCHAR(255), email VARCHAR(255), address VARCHAR(255))")
    return conn, cursor

def load_contact():
    result = cursor.execute("SELECT * FROM CONTATTI")
    contacts_saved = result.fetchall()  # lista di tuple
    contacts_saved_dict = []    # lista di dizionari
    for contatto in contacts_saved:
        contatto_dict = {"Nome":contatto[0], "Telefono": contatto[1], "Email": contatto[2], "Indirizzo": contatto[3]}
        contacts_saved_dict.append(contatto_dict)
    print_contacts(contacts_saved_dict, treeview_save)


rubrica = []    # lista inizialmente vuota

window = tk.Tk()
window.title("Rubrica")
window.iconbitmap("logo_meg.ico")   # format .ico
# window.bind("<Configure>", resize)

ttk.Style().configure("Treeview.Heading", font = ("Verdana", 9, "bold"))

header_label = tk.Label(window, text = "Rubrica Telefonica", font = ('Verdana', 20, 'bold'))
header_label.grid(row = 0, column = 0, padx = (500, 0), pady = 30)
image = Image.open("icons8-telefono-50.png")
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(window, image = photo)
image_label.grid(row = 0, column = 1, padx = (0, 500))

# 1. NEW CONTACTS MANAGEMENT
frame_add = tk.LabelFrame(window, text = "Aggiungi nuovo contatto")
frame_add.grid(row = 1, column = 0, padx = 10, sticky = "NESW")
# 1.1 NAME FIELD
name_label = tk.Label(frame_add, text = "Nome")
name_label.grid(row = 0, column = 0, padx = (50, 10) , pady = 5)
name_entry = tk.Entry(frame_add, width = 60, font = ('Verdana', 10))
name_entry.grid(row = 0, column = 1, padx = (10, 50), pady = 5)
# 1.2 TELEPHONE FIELD
telephone_label = tk.Label(frame_add, text = "Telefono")
telephone_label.grid(row = 1, column = 0, padx = (50, 10), pady = 5)
telephone_entry = tk.Entry(frame_add, width = 60, font = ('Verdana', 10))
telephone_entry.grid(row = 1, column = 1, padx = (10, 50), pady = 5)
# 1.3 EMAIL FIELD
email_label = tk.Label(frame_add, text = "Email")
email_label.grid(row = 2, column = 0, padx = (50, 10), pady = 5)
email_entry = tk.Entry(frame_add, width = 60, font = ('Verdana', 10))
email_entry.grid(row = 2, column = 1, padx = (10, 50), pady = 5)
# 1.4 ADDRESS FIELD
address_label = tk.Label(frame_add, text = "Indirizzo")
address_label.grid(row = 3, column = 0, padx = (50, 10), pady = 5)
address_entry = tk.Entry(frame_add, width = 60, font = ('Verdana', 10))
address_entry.grid(row = 3, column = 1, padx = (10, 50), pady = 5)
# 1.5 BUTTON
add_button = tk.Button(frame_add, text = "Aggiungi", bg = "#000000", fg = "#ffffff", 
                       padx = 30, pady = 5, command = add_contact)
add_button.grid(row = 4, column = 0, columnspan = 2, padx = 10, pady = 5)

# 2. CONTACTS MANAGEMENT ADDED IN THIS SESSION
frame_contacts = tk.LabelFrame(window, text = "Contatti aggiunti in questa sessione")
frame_contacts.grid(row = 2, column = 0, padx = 10, pady = (0, 10), sticky = "NESW")
# 2.1 TREEVIEW FOR CLEAR AND HIERARCHICAL DATA PRESENTATION
treeview_contacts = ttk.Treeview(frame_contacts, columns = ["Nome", "Telefono", "Email", "Indirizzo"])
treeview_contacts.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = "nsew")
set_treeview(treeview_contacts)
hide_initial_empty_column_tree(treeview_contacts)
# 2.2 SCROLLBAR FOR MORE CONTACTS
scrollbar_contacts = tk.Scrollbar(frame_contacts)
scrollbar_contacts.grid(row = 0, column = 1, sticky = "NS") 
treeview_contacts.config(yscrollcommand = scrollbar_contacts.set)
scrollbar_contacts.config(command = treeview_contacts.yview)

# 3. SEARCH AND REMOVE CONTACTS
frame_sr = tk.LabelFrame(window, text = "Ricerca/Rimuovi")
frame_sr.grid(row = 2, column = 1, padx = (0, 10), pady = (0, 10), sticky = "NESW")
wanted_entry = tk.Entry(frame_sr, width = 50)
wanted_entry.grid(row = 0, column = 0, padx = 10)
search_button = tk.Button(frame_sr, text = "Cerca", bg = "#3D642D", fg = "#ffffff", 
                          width = 10, command = search_contact)
search_button.grid(row = 0, column = 1, padx = 10, pady = 5)
remove_button = tk.Button(frame_sr, text = "Rimuovi", bg = "#B81414", fg = "#ffffff", width = 10)
remove_button.grid(row = 0, column = 2, padx = 10, pady = 5)
treeview_sr = ttk.Treeview(frame_sr, columns = ["Nome", "Telefono", "Email", "Indirizzo"])
treeview_sr.grid(row = 1, column = 0, columnspan = 3, padx = 10, pady = 5)
set_treeview(treeview_sr)
hide_initial_empty_column_tree(treeview_sr)

# 4. EXISTING CONTACTS MANAGEMENT
frame_save = tk.LabelFrame(window, text = "Contatti salvati")
frame_save.grid(row = 1, column = 1, padx = (0, 10), sticky = "NESW")
treeview_save = ttk.Treeview(frame_save, columns = ["Nome", "Telefono", "Email", "Indirizzo"])
treeview_save.grid(row = 0, column = 0, padx = 10, pady = 5)
set_treeview(treeview_save)
hide_initial_empty_column_tree(treeview_save)

scrollbar_save = tk.Scrollbar(frame_save)
scrollbar_save.grid(row = 0, column = 1, pady = 5, sticky = "NS") 
treeview_save.config(yscrollcommand = scrollbar_save.set)
scrollbar_save.config(command = treeview_save.yview)

conn, cursor = db_connect()
load_contact()

for row in range(0, 5):
    frame_add.grid_rowconfigure(row, weight = 1)

for row in range(0, 2):
    frame_contacts.grid_rowconfigure(row, weight = 1)
    frame_sr.grid_rowconfigure(row, weight = 1)

frame_save.grid_rowconfigure(0, weight = 1)

frame_add.grid_columnconfigure(0, weight = 1)
frame_add.grid_columnconfigure(1, weight = 1)
frame_contacts.grid_columnconfigure(0, weight = 1)
frame_save.grid_columnconfigure(0, weight = 1)
frame_sr.grid_columnconfigure(0, weight = 1)
frame_sr.grid_columnconfigure(1, weight = 1)
frame_sr.grid_columnconfigure(2, weight = 1)

window.mainloop()