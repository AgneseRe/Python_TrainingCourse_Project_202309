import tkinter as tk
from tkinter import ttk, messagebox

window = tk.Tk()
window.title("Rubrica")

# ***** FUNCTIONS *****
def add_contact():
    name = name_entry.get()
    telephone = telephone_entry.get()
    email_address = email_entry.get()
    if name and telephone and email_address:
        contacts.append({"Nome" : name, "Telefono" : telephone, "Email" : email_address})
        print_contacts()
    else:
        tk.messagebox.showwarning(title = "Errore", message = "Alcuni campi non sono compilati")

def print_contacts():
    contacts_listbox.delete(0, tk.END)
    for contact in contacts:
        contacts_listbox.insert(tk.END, contact["Nome"] + "         " + contact["Telefono"])

# ***** PROGRAM *****
contacts = []
header_label = tk.Label(window, text = "Telefono")
header_label.grid(row = 0, column = 0)

# 1. Creation of a LabelFrame for adding contacts in phone book.
#       Very useful for improving the organization and clarity of GUI
add_frame = tk.LabelFrame(window, text = "Aggiungi contatto")
add_frame.grid(row = 1, column = 0, sticky = "WE")

name_label = tk.Label(add_frame, text = "Nome")
name_label.grid(row = 0, column = 0, sticky = "W")
name_entry = tk.Entry(add_frame, borderwidth = 2, relief = "groove")     # flat, groove, raised, ridge, solid, or sunken
name_entry.grid(row = 0, column = 1)

telephone_label = tk.Label(add_frame, text = "Telefono")
telephone_label.grid(row = 1, column = 0, sticky = "W")
telephone_entry = tk.Entry(add_frame, borderwidth = 2, relief = "groove")
telephone_entry.grid(row = 1, column = 1)

email_label = tk.Label(add_frame, text = "Email")
email_label.grid(row = 2, column = 0, sticky = "W")
email_entry = tk.Entry(add_frame, borderwidth = 2, relief = "groove")
email_entry.grid(row = 2, column = 1)

add_button = tk.Button(add_frame, text = "AGGIUNGI", command = add_contact)
add_button.grid(row = 3, column = 0)

contacts_frame = tk.LabelFrame(window, text = "Contatti in rubrica")
contacts_frame.grid(row = 2, column = 0, sticky = "WE")
contacts_listbox = tk.Listbox(contacts_frame)
contacts_listbox.grid(row = 0, column = 0, sticky = "nsew")

for widget in add_frame.winfo_children():
    widget.grid_configure(padx = 5, pady = 5)



window.mainloop()