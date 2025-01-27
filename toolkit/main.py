from tkinter import *
import server
import vlsm

class Main(Tk):
    def __init__(self):
        super().__init__()
        self.bg_global="#606060"
        self.fg_global="#f5f5f5"
        self.font_global="Arial,12"

        #Fő ablak konfiguráció
        self.title("ToolKit pre-1.2.4")
        self.resizable(False,False)
        self.config(bg=self.bg_global)
        
        #Cím
        self.title = Label(bg=self.bg_global,fg=self.fg_global,font=("Times new roman", 20),text="Toolkit")
        self.title.pack(padx=70,pady=5)

        #Eszköztár
        self.section_select_tool = Frame(self,bg=self.bg_global)
        self.section_select_tool.pack(padx=5,pady=5,fill="x")

        self.button_select_server = Button(self.section_select_tool,
                                           text="Szerver",
                                           disabledforeground="#00d0f0",
                                           bg=self.bg_global,
                                           fg=self.fg_global,
                                           font=self.font_global,
                                           command=self.select_server)
        self.button_select_server.pack(padx=5,pady=5,side="left")

        self.button_select_vlsm = Button(self.section_select_tool,
                                         text="VLSM majd lesz",
                                         disabledforeground="#00d0f0",
                                         bg=self.bg_global,
                                         fg=self.fg_global,
                                         font=self.font_global,
                                         command=self.select_vlsm)
        self.button_select_vlsm.pack(padx=5,pady=5,side="left")
        
        self.server = server.Server()
        self.server.config(bg=self.bg_global)
        self.vlsm = vlsm.VLSM()
        self.vlsm.config(bg=self.bg_global)
        
    def select_server(self):
        self.vlsm.pack_forget()
        self.server.pack()
        self.button_select_server.config(state="disabled")
        self.button_select_vlsm.config(state="normal")

    def select_vlsm(self):
        self.server.pack_forget()
        self.vlsm.pack()
        self.button_select_vlsm.config(state="disabled")
        self.button_select_server.config(state="normal")
    
if __name__ == "__main__":
    ToolKit = Main()
    ToolKit.mainloop()
