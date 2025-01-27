from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
#ttk.treeview

class VLSM(Frame):
    def __init__(self):
        super().__init__()
        self.bg_global="#606060"
        self.fg_global="#f5f5f5"
        self.font_global="Arial,12"

        #Bemeneti adatok
        self.section_regular_data = Frame(self)
        self.section_regular_data.pack(padx=5,pady=5,fill="x",side="top")

        self.section_network_address = Frame(self.section_regular_data)
        self.section_network_address.pack(fill="x")
        self.network_address_text = Label(self.section_network_address, width=14, text="Hálózati cím:")
        self.network_address_text.pack(side="left", fill="x")
        self.network_address_entry = Entry(self.section_network_address, width=20)
        self.network_address_entry.pack(side="left")
        
        self.prefix_text = Label(self.section_network_address, text="/")
        self.prefix_text.pack(side="left")
        self.prefix_entry = Entry(self.section_network_address, width=2)
        self.prefix_entry.pack(side="left")

        self.section_netmask = Frame(self.section_regular_data)
        self.section_netmask.pack(fill="x")
        self.netmask_text = Label(self.section_netmask, width=14, text="Alhálózati maszk:")
        self.netmask_text.pack(side="left", fill="x")
        self.netmask_entry = Entry(self.section_netmask, width=20)
        self.netmask_entry.pack(side="left")

        #Számolt adatok
        self.section_calculations = Frame(self,bg="red")
        self.section_calculations.pack(padx=5,pady=5,fill="x",side="top")
        """
        self.section_addresses = Frame(self.section_calculations)
        self.section_addresses.pack(padx=5,pady=5,fill="x",side="left")
        self.section_options = Frame(self.section_calculations)
        self.section_options.pack(padx=5,pady=5,fill="x",side="left")
        """

if __name__ == "__main__":
    window = Tk()
    window.title("VLSM calc - standalone")
    window.config(bg="#506090")
    server = VLSM()
    server.pack()
    window.mainloop()
