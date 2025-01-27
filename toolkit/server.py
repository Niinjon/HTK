from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import pycdlib
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

class Server(Frame):
    def __init__(self):
        super().__init__()
        #Változók
        self.bg_global="#606060"
        self.fg_global="#f5f5f5"
        self.font_global="Arial,12"
        
        self.var_system_id = IntVar(value=0)

        self.var_name_nic_linux = StringVar(value="eth0")
        self.var_name_nic_windows = StringVar(value="Ethernet")
        self.var_type_nic = StringVar(value="Outside")
        self.var_address_ip = StringVar()
        self.var_address_netmask = StringVar()
        self.var_address_gateway = StringVar()

        self.var_nic2_active = BooleanVar()
        self.var_name_nic2_linux = StringVar(value="eth1")
        self.var_name_nic2_windows = StringVar(value="Ethernet 2")
        self.var_type_nic2 = StringVar(value="Inside")
        self.var_address_ip2 = StringVar()
        self.var_address_netmask2 = StringVar()
        self.var_address_gateway2 = StringVar()

        self.var_dns2_active = BooleanVar()
        self.var_address_dns = StringVar(value="8.8.8.8")
        self.var_address_dns2 = StringVar()
        
        self.var_service_dns_active = BooleanVar()
        self.var_service_dhcp_active = BooleanVar()
        self.var_service_web_active = BooleanVar()
        self.var_service_iptables_active = BooleanVar()
        self.var_service_ftp_active = BooleanVar()
        self.var_service_smb_active = BooleanVar()
        self.var_service_ssh_active = BooleanVar()
        self.var_service_activedirectory_active = BooleanVar()
        self.var_service_iis_active = BooleanVar()

            #szolgátatások
        self.var_domain_name = StringVar()
        self.var_zone_name = StringVar()
        self.var_dhcp_start = StringVar()
        self.var_dhcp_end = StringVar()
        #self.var_nic_dns =
        #self.var_nic_dhcp =

            #üzenetek
        temp = open("data/messages/install.txt","rt",encoding="utf-8")
        self.var_message_howtoinstall = temp.read()
        temp.close()
        
        #Rendszer választás
        self.section_select_sys = Frame(self,bg=self.bg_global)
        self.section_select_sys.pack(padx=5,pady=5,fill="x")
        self.button_select_windows = Radiobutton(self.section_select_sys,
                                              bg=self.bg_global,
                                              fg=self.fg_global,
                                              font=self.font_global,
                                              activebackground=self.fg_global,
                                              activeforeground=self.bg_global,
                                              disabledforeground="#00d0f0",
                                              text="Windows",
                                              command=self.select_windows,
                                              variable=self.var_system_id,
                                              value=0,
                                              state="disabled")
        self.button_select_windows.pack(padx=5,pady=5,side="left")
        
        self.button_select_linux = Radiobutton(self.section_select_sys,
                                            bg=self.bg_global,
                                            fg=self.fg_global,
                                            font=self.font_global,
                                            activebackground=self.fg_global,
                                            activeforeground=self.bg_global,
                                            disabledforeground="#00d0f0",
                                            text="Linux",
                                            command=self.select_linux,
                                            variable=self.var_system_id,
                                            value=1)
        self.button_select_linux.pack(padx=5,pady=5,side="left")

        #Adatok
        self.section_middle = Frame(self,bg=self.bg_global)
        self.section_middle.pack(padx=5,pady=5)
        
            #Hálózati kártya
        self.section_nic = Frame(self.section_middle,bg=self.bg_global,bd=2,relief="raised")
        self.section_nic.pack(padx=5,pady=5,side="left",anchor="n")

        self.section_name_nic = Frame(self.section_nic,bg=self.bg_global)
        self.section_name_nic.pack(anchor="w")
        self.entry_name_nic_windows = Entry(self.section_name_nic,width=16,textvariable=self.var_name_nic_windows)
        self.entry_name_nic_linux = Entry(self.section_name_nic,width=16,textvariable=self.var_name_nic_linux)
        self.entry_name_nic_windows.pack(padx=5,pady=5,side="left")

        self.choose_nic_type = ttk.Combobox(self.section_name_nic,textvariable=self.var_type_nic,width=8,state="readonly")
        self.choose_nic_type.bind("<FocusIn>",lambda x: self.var_type_nic.get() == "Outside" and self.choose_nic2_type.current(0))
        self.choose_nic_type["values"] = ["Inside","Outside"]
        self.choose_nic_type.current(1)
        self.choose_nic_type.pack(padx=5,pady=5,side="left")
              
                #Ip cím
        self.section_ipaddr = Frame(self.section_nic,bg=self.bg_global)
        self.section_ipaddr.pack(padx=5,pady=5)
        self.text_ipaddr = Label(self.section_ipaddr,
                                 width=16,
                                 anchor="w",
                                 bg=self.bg_global,
                                 fg=self.fg_global,
                                 font=self.font_global,
                                 text="IP cím:")
        self.text_ipaddr.pack(side="left")
        self.entry_ipaddr = Entry(self.section_ipaddr,width=16,textvariable=self.var_address_ip)
        self.entry_ipaddr.pack(side="right")
        self.entry_ipaddr.bind("<Return>",lambda x: self.check_address_ip(self.var_address_ip))
        self.entry_ipaddr.bind("<Escape>",lambda x: self.check_address_ip(self.var_address_ip))
        self.entry_ipaddr.bind("<FocusOut>",lambda x: self.check_address_ip(self.var_address_ip))

                #Maszk
        self.section_netmask = Frame(self.section_nic,bg=self.bg_global)
        self.section_netmask.pack(padx=5,pady=5)
        self.text_netmask = Label(self.section_netmask,
                                  width=16,
                                  anchor="w",
                                  bg=self.bg_global,
                                  fg=self.fg_global,
                                  font=self.font_global,
                                  text="Alhálózati maszk:")
        self.text_netmask.pack(side="left")
        self.entry_netmask = Entry(self.section_netmask,width=16,textvariable=self.var_address_netmask)
        self.entry_netmask.pack(side="right")
        self.entry_netmask.bind("<Return>",lambda x: self.check_address_netmask(self.var_address_netmask))
        self.entry_netmask.bind("<Escape>",lambda x: self.check_address_netmask(self.var_address_netmask))
        self.entry_netmask.bind("<FocusOut>",lambda x: self.check_address_netmask(self.var_address_netmask))

                #Átjáró
        self.section_gateway = Frame(self.section_nic,bg=self.bg_global)
        self.section_gateway.pack(padx=5,pady=5)
        self.text_gateway = Label(self.section_gateway,
                                  width=16,
                                  anchor="w",
                                  bg=self.bg_global,
                                  fg=self.fg_global,
                                  font=self.font_global,
                                  text="Átjáró:")
        self.text_gateway.pack(side="left")
        self.entry_gateway = Entry(self.section_gateway,width=16,textvariable=self.var_address_gateway)
        self.entry_gateway.pack(side="right")
        self.entry_gateway.bind("<Return>",lambda x: self.check_address_gateway(self.var_address_gateway))
        self.entry_gateway.bind("<Escape>",lambda x: self.check_address_gateway(self.var_address_gateway))
        self.entry_gateway.bind("<FocusOut>",lambda x: self.check_address_gateway(self.var_address_gateway))

            #Második hálózati kártya
        self.switch_nic2 = Checkbutton(self.section_nic,
                                       bg=self.bg_global,
                                       fg=self.fg_global,
                                       font=self.font_global,
                                       anchor="w",
                                       selectcolor=self.bg_global,
                                       text="Másodlagos hálózati kártya (belső)",
                                       var=self.var_nic2_active,
                                       command=self.update_nic2)
        self.switch_nic2.pack(fill="x")
        
        self.section_nic2 = Frame(self.section_nic,bg=self.bg_global)

        self.section_name_nic2 = Frame(self.section_nic2,bg=self.bg_global)
        self.section_name_nic2.pack(anchor="w")
        self.entry_name_nic2_windows = Entry(self.section_name_nic2,width=16,textvariable=self.var_name_nic2_windows)
        self.entry_name_nic2_linux = Entry(self.section_name_nic2,width=16,textvariable=self.var_name_nic2_linux)
        self.entry_name_nic2_windows.pack(padx=5,pady=5,side="left")

        self.choose_nic2_type = ttk.Combobox(self.section_name_nic2,textvariable=self.var_type_nic2,width=8,state="readonly")
        self.choose_nic2_type.bind("<FocusIn>",lambda x: self.var_type_nic2.get() == "Outside" and self.choose_nic_type.current(0))
        self.choose_nic2_type["values"] = ["Inside","Outside"]
        self.choose_nic2_type.current(0)
        self.choose_nic2_type.pack(padx=5,pady=5,side="left")

                #Ip cím
        self.section_ipaddr2 = Frame(self.section_nic2,bg=self.bg_global)
        self.section_ipaddr2.pack(padx=5,pady=5)
        self.text_ipaddr2 = Label(self.section_ipaddr2,
                                 width=16,
                                 anchor="w",
                                 bg=self.bg_global,
                                 fg=self.fg_global,
                                 font=self.font_global,
                                 text="IP cím:")
        self.text_ipaddr2.pack(side="left")
        self.entry_ipaddr2 = Entry(self.section_ipaddr2,width=16,textvariable=self.var_address_ip2)
        self.entry_ipaddr2.pack(side="right")
        self.entry_ipaddr2.bind("<Return>",lambda x: self.check_address_ip(self.var_address_ip2))
        self.entry_ipaddr2.bind("<Escape>",lambda x: self.check_address_ip(self.var_address_ip2))
        self.entry_ipaddr2.bind("<FocusOut>",lambda x: self.check_address_ip(self.var_address_ip2))

                #Maszk
        self.section_netmask2 = Frame(self.section_nic2,bg=self.bg_global)
        self.section_netmask2.pack(padx=5,pady=5)
        self.text_netmask2 = Label(self.section_netmask2,
                                  width=16,
                                  anchor="w",
                                  bg=self.bg_global,
                                  fg=self.fg_global,
                                  font=self.font_global,
                                  text="Alhálózati maszk:")
        self.text_netmask2.pack(side="left")
        self.entry_netmask2 = Entry(self.section_netmask2,width=16,textvariable=self.var_address_netmask2)
        self.entry_netmask2.pack(side="right")
        self.entry_netmask2.bind("<Return>",lambda x: self.check_address_netmask(self.var_address_netmask2))
        self.entry_netmask2.bind("<Escape>",lambda x: self.check_address_netmask(self.var_address_netmask2))
        self.entry_netmask2.bind("<FocusOut>",lambda x: self.check_address_netmask(self.var_address_netmask2))

                #Átjáró
        self.section_gateway2 = Frame(self.section_nic2,bg=self.bg_global)
        self.section_gateway2.pack(padx=5,pady=5)
        self.text_gateway2 = Label(self.section_gateway2,
                                  width=16,
                                  anchor="w",
                                  bg=self.bg_global,
                                  fg=self.fg_global,
                                  font=self.font_global,
                                  text="Átjáró:")
        self.text_gateway2.pack(side="left")
        self.entry_gateway2 = Entry(self.section_gateway2,width=16,textvariable=self.var_address_gateway2)
        self.entry_gateway2.pack(side="right")
        self.entry_gateway2.bind("<Return>",lambda x: self.check_address_gateway(self.var_address_gateway2))
        self.entry_gateway2.bind("<Escape>",lambda x: self.check_address_gateway(self.var_address_gateway2))
        self.entry_gateway2.bind("<FocusOut>",lambda x: self.check_address_gateway(self.var_address_gateway2))

            #Névfeloldás
        self.section_resolv = Frame(self.section_middle,bg=self.bg_global,bd=2,relief="raised")
        self.section_resolv.pack(padx=5,pady=5,side="left",anchor="n")
                #DNS cím
        self.section_dns1 = Frame(self.section_resolv,bg=self.bg_global)
        self.section_dns1.pack(padx=5,pady=5,fill="x")
        self.text_dns = Label(self.section_dns1,
                              bg=self.bg_global,
                              fg=self.fg_global,
                              font=self.font_global,
                              text="DNS cím:")
        self.text_dns.pack(side="left")
        self.entry_dns = Entry(self.section_dns1,width=16,textvariable=self.var_address_dns)
        self.entry_dns.pack(side="right")
        self.entry_dns.bind("<Return>",lambda x: self.check_address_ip(self.var_address_dns))
        self.entry_dns.bind("<Escape>",lambda x: self.check_address_ip(self.var_address_dns))
        self.entry_dns.bind("<FocusOut>",lambda x: self.check_address_ip(self.var_address_dns))
                #Másodlagos DNS cím
        self.section_dns2 = Frame(self.section_resolv,bg=self.bg_global)
        self.section_dns2.pack(padx=5,pady=5)
        self.switch_dns2 = Checkbutton(self.section_dns2,
                                       bg=self.bg_global,
                                       fg=self.fg_global,
                                       font=self.font_global,
                                       selectcolor=self.bg_global,
                                       text="2. DNS cím:",
                                       var=self.var_dns2_active,
                                       command=self.update_dns2)
        self.switch_dns2.pack(side="left")
        self.entry_dns2 = Entry(self.section_dns2,width=16,textvariable=self.var_address_dns2,state="disabled")
        self.entry_dns2.pack(side="right")
        self.entry_dns2.bind("<Return>",lambda x: self.check_address_ip(self.var_address_dns2))
        self.entry_dns2.bind("<Escape>",lambda x: self.check_address_ip(self.var_address_dns2))
        self.entry_dns2.bind("<FocusOut>",lambda x: self.check_address_ip(self.var_address_dns2))

            #Szolgáltatások
        self.section_services = Frame(self.section_middle,bg=self.bg_global,bd=2,relief="raised")
        self.section_services.pack(padx=5,pady=5,side="left",anchor="n")
        
        self.switch_service_dns = Checkbutton(self.section_services,
                                              width=24,
                                              bg=self.bg_global,
                                              fg=self.fg_global,
                                              font=self.font_global,
                                              anchor="w",
                                              selectcolor=self.bg_global,
                                              text="DNS Szolgáltatás",
                                              var=self.var_service_dns_active,
                                              command=self.update_service_dns)
        self.switch_service_dns.pack(fill="x")
        self.section_service_dns_datas = Frame(self.section_services)
        
        self.switch_service_dhcp = Checkbutton(self.section_services,
                                               width=24,
                                               bg=self.bg_global,
                                               fg=self.fg_global,
                                               font=self.font_global,
                                               anchor="w",
                                               selectcolor=self.bg_global,
                                               text="DHCP Szolgáltatás",
                                               var=self.var_service_dhcp_active,
                                               command=self.update_service_dhcp)
        self.switch_service_dhcp.pack(fill="x")
        self.section_service_dhcp_datas = Frame(self.section_services)
        
                #linux
        self.section_services_linux = Frame(self.section_services,bg=self.bg_global)
        
        self.switch_service_web = Checkbutton(self.section_services_linux,
                                              width=24,
                                              bg=self.bg_global,
                                              fg=self.fg_global,
                                              font=self.font_global,
                                              anchor="w",
                                              selectcolor=self.bg_global,
                                              text="WEB Szolgáltatás",
                                              var=self.var_service_web_active,
                                              command=self.update_service_web)
        self.switch_service_web.pack(fill="x")
        self.section_service_web_datas = Frame(self.section_services)

        self.switch_service_iptables = Checkbutton(self.section_services_linux,
                                                   width=24,
                                                   bg=self.bg_global,
                                                   fg=self.fg_global,
                                                   font=self.font_global,
                                                   anchor="w",
                                                   selectcolor=self.bg_global,
                                                   text="IP-Tables Szolgáltatás",
                                                   var=self.var_service_iptables_active,
                                                   command=self.update_service_iptables)
        self.switch_service_iptables.pack(fill="x")
        self.section_service_iptables_datas = Frame(self.section_services)

        self.switch_service_ftp = Checkbutton(self.section_services_linux,
                                              width=24,
                                              bg=self.bg_global,
                                              fg=self.fg_global,
                                              font=self.font_global,
                                              anchor="w",
                                              selectcolor=self.bg_global,
                                              text="FTP Szolgáltatás",
                                              var=self.var_service_ftp_active,
                                              command=self.update_service_ftp)
        self.switch_service_ftp.pack(fill="x")
        self.section_service_ftp_datas = Frame(self.section_services)

        self.switch_service_smb = Checkbutton(self.section_services_linux,
                                              width=24,
                                              bg=self.bg_global,
                                              fg=self.fg_global,
                                              font=self.font_global,
                                              anchor="w",
                                              selectcolor=self.bg_global,
                                              text="Samba Szolgáltatás",
                                              var=self.var_service_smb_active,
                                              command=self.update_service_smb)
        self.switch_service_smb.pack(fill="x")
        self.section_service_smb_datas = Frame(self.section_services)

        self.switch_service_ssh = Checkbutton(self.section_services_linux,
                                              width=24,
                                              bg=self.bg_global,
                                              fg=self.fg_global,
                                              font=self.font_global,
                                              anchor="w",
                                              selectcolor=self.bg_global,
                                              text="SSH Szolgáltatás",
                                              var=self.var_service_ssh_active,
                                              command=self.update_service_ssh)
        self.switch_service_ssh.pack(fill="x")
        self.section_service_ssh_datas = Frame(self.section_services)
        
                #windows
        self.section_services_windows = Frame(self.section_services,bg=self.bg_global)
        self.section_services_windows.pack(fill="x")
        self.switch_service_activedirectory = Checkbutton(self.section_services_windows,
                                                          width=24,
                                                          bg=self.bg_global,
                                                          fg=self.fg_global,
                                                          font=self.font_global,
                                                          anchor="w",
                                                          selectcolor=self.bg_global,
                                                          text="Active Directory Szolgáltatás",
                                                          var=self.var_service_activedirectory_active,
                                                          command=self.update_service_activedirectory)
        self.switch_service_activedirectory.pack(fill="x")
        self.section_service_activedirectory_datas = Frame(self.section_services)

        self.switch_service_iis = Checkbutton(self.section_services_windows,
                                              width=24,
                                              bg=self.bg_global,
                                              fg=self.fg_global,
                                              font=self.font_global,
                                              anchor="w",
                                              selectcolor=self.bg_global,
                                              text="IIS Szolgáltatás",
                                              var=self.var_service_iis_active,
                                              command=self.update_service_iis)
        self.switch_service_iis.pack(fill="x")
        self.section_service_iis_datas = Frame(self.section_services)

        #Konfigurációs fájl írása
        self.section_control_buttons = Frame(self,bg=self.bg_global)
        self.section_control_buttons.pack(padx=5,pady=5,fill="x")
        
        self.button_generate_config = Button(self.section_control_buttons,
                                      text="Konfigurációk\ngenerálása",
                                      bg=self.bg_global,
                                      fg=self.fg_global,
                                      disabledforeground="#d05050",
                                      font=self.font_global,
                                      command=self.generate_config)
        self.button_generate_config.pack(side="left",padx=20,pady=20)
        
        self.button_generate_tester = Button(self.section_control_buttons,
                                      text="Tesztelő\ngenerálása",
                                      bg=self.bg_global,
                                      fg=self.fg_global,
                                      disabledforeground="#d05050",
                                      font=self.font_global,
                                      command=self.generate_tester)
        self.button_generate_tester.pack(side="left",padx=20,pady=20)

        self.button_help = Button(self.section_control_buttons,
                                      text="Telepítés\nmenete",
                                      bg="#2050a0",
                                      fg=self.fg_global,
                                      disabledforeground="#d05050",
                                      font=self.font_global,
                                      command=self.show_message_howtoinstall)
        self.button_help.pack(side="left",padx=20,pady=20)

        #Kijelző az ablak alján, lehet fölösleges
        self.section_messages = Frame(self)
        self.section_messages.pack(padx=5,pady=5,fill="x")
        
        self.scroll = Scrollbar(self.section_messages)
        self.scroll.pack(side="right",fill="y")
        
        self.messages_display = Text(self.section_messages,
                                     state="disabled",
                                     width=20,
                                     height=5,
                                     bg="#000000",
                                     fg="#00ff00",
                                     yscrollcommand=self.scroll.set)
        self.messages_display.pack(side="left",fill="x",expand=True)

        self.scroll.config(command=self.messages_display.yview)
        
    #Methódusok
    def select_windows(self):
        self.button_select_windows.config(state="disabled")
        self.button_select_linux.config(state="normal")
        #self.list_nic = [self.var_name_nic_windows.get(),self.var_name_nic2_windows.get()]
        self.section_services_linux.pack_forget()
        self.section_services_windows.pack(fill="x")
        self.entry_name_nic_linux.pack_forget()
        self.entry_name_nic2_linux.pack_forget()
        self.entry_name_nic_windows.pack(padx=5,pady=5,side="left",before=self.choose_nic_type)
        self.entry_name_nic2_windows.pack(padx=5,pady=5,side="left",before=self.choose_nic2_type)
        
    def select_linux(self):
        self.button_select_linux.config(state="disabled")
        self.button_select_windows.config(state="normal")
        #self.list_nic = [self.var_name_nic_linux.get(),self.var_name_nic2_linux.get()]
        self.section_services_windows.pack_forget()
        self.section_services_linux.pack(fill="x")
        self.entry_name_nic_windows.pack_forget()
        self.entry_name_nic2_windows.pack_forget()
        self.entry_name_nic_linux.pack(padx=5,pady=5,side="left",before=self.choose_nic_type)
        self.entry_name_nic2_linux.pack(padx=5,pady=5,side="left",before=self.choose_nic2_type)
    """
    def update_name_nic(self,x):
        print(x)
        self.choose_nic_dns["values"] = [self.var_name_nic_windows.get(),self.var_name_nic2_windows.get()]
        #self.choose_nic_dns.current(1)
    """
    def update_nic2(self):
        if self.var_nic2_active.get():
            self.section_nic2.pack(fill="x")
        else:
            self.section_nic2.pack_forget()
            self.var_address_ip2.set("")
            self.var_address_netmask2.set("")
            self.var_address_gateway2.set("")
            self.var_service_dns_active.set(False)
            self.update_service_dns()
            self.var_service_dhcp_active.set(False)
            self.update_service_dhcp()
            if self.var_system_id.get() == 1:
                self.var_service_iptables_active.set(False)
                self.update_service_iptables()

    def update_dns2(self):
        if self.var_dns2_active.get():
            self.entry_dns2.config(state="normal")
        else:
            self.entry_dns2.config(state="disabled")
            self.var_address_dns2.set("")

    def update_service_dns(self):
        if self.var_service_dns_active.get():
            self.section_service_dns_datas.pack(after=self.switch_service_dns)
            self.var_nic2_active.set(True)
            self.update_nic2()
        else:
            self.section_service_dns_datas.pack_forget()
            if self.var_system_id.get() == 0:
                self.var_service_activedirectory_active.set(False)
                self.section_service_activedirectory_datas.pack_forget()
                    
    def update_service_dhcp(self):
        if self.var_service_dhcp_active.get():
            self.section_service_dhcp_datas.pack(after=self.switch_service_dhcp)
            self.var_nic2_active.set(True)
            self.update_nic2()
        else:
            self.section_service_dhcp_datas.pack_forget()
            
    def update_service_web(self):
        if self.var_service_web_active.get():
            self.section_service_web_datas.pack(after=self.switch_service_web)
        else:
            self.section_service_web_datas.pack_forget()
            
    def update_service_iptables(self):
        if self.var_service_iptables_active.get():
            self.section_service_iptables_datas.pack(after=self.switch_service_iptables)
            self.var_nic2_active.set(True)
            self.update_nic2()
        else:
            self.section_service_iptables_datas.pack_forget()
            
    def update_service_ftp(self):
        if self.var_service_ftp_active.get():
            self.section_service_ftp_datas.pack(after=self.switch_service_ftp)
        else:
            self.section_service_ftp_datas.pack_forget()
            
    def update_service_smb(self):
        if self.var_service_smb_active.get():
            self.section_service_smb_datas.pack(after=self.switch_service_smb)
        else:
            self.section_service_smb_datas.pack_forget()
            
    def update_service_ssh(self):
        if self.var_service_ssh_active.get():
            self.section_service_ssh_datas.pack(after=self.switch_service_ssh)
        else:
            self.section_service_ssh_datas.pack_forget()
            
    def update_service_activedirectory(self):
        if self.var_service_activedirectory_active.get():
            self.section_service_activedirectory_datas.pack(after=self.switch_service_activedirectory)
            self.var_service_dns_active.set(True)
            self.update_service_dns()
        else:
            self.section_service_activedirectory_datas.pack_forget()
            
    def update_service_iis(self):
        if self.var_service_iis_active.get():
            self.section_service_iis_datas.pack(after=self.switch_service_iis)
        else:
            self.section_service_iis_datas.pack_forget()
    
    def is_valid_address(self,address):
        #1.0.0.1 - 223.255.255.254
        #nem lehet szórás cím
        #nem lehet hálózat cím - ehhez egyeztetni kellesz a maszkkal
        #nem lehet csoportos cím
        #nem lehet loopback
        if not address == "": #ugyebár a nagy büdös semmi nem valid cím, de nem akartam, hogy hibát dobjon arra is
            try:
                octets = address.split(".")
                for i in range(len(octets)):
                    octets[i] = int(octets[i])
            except:
                return False
            if len(octets) != 4:
                return False
            if octets[0] in range(1,224):
                if octets[0] == 127:
                    return False
            else:
                return False
            if not octets[1] in range(0,256):
                return False
            if not octets[2] in range(0,256):
                return False
            if not octets[3] in range(0,255):
                return False
        return True

    def is_valid_netmask(self,address):
        if not address == "":
            try:
                octets = address.split(".")
                for i in range(len(octets)):
                    octets[i] = int(octets[i])
            except:
                return False
            if len(octets) != 4:
                return False
            if not octets[0] == 255:
                return False
            #255.255.x.x
            if octets[1] == 255: 
                #255.255.255.x
                if octets[2] == 255: 
                    if not octets[3] in (0,128,192,224,240,248,252):
                        return False
                #255.255.y.x
                elif octets[2] in (0,128,192,224,240,248,252,254):
                    if not octets[3] == 0:
                        return False
                else:
                    return False
            #255.y.x.x
            elif octets[1] in (0,128,192,224,240,248,252,254):
                if not octets[2] == 0:
                    return False
                if not octets[3] == 0:
                    return False
            else:
                return False  
        return True
    
    def check_address_ip(self,var_address):
        if var_address.get() != "" and not self.is_valid_address(var_address.get()):
            var_address.set("")
            messagebox.showwarning("Hiba","Érvénytelen IP cím")
            
    def check_address_netmask(self,var_address):
        if var_address.get() != "" and not self.is_valid_netmask(var_address.get()):
            var_address.set("")
            messagebox.showwarning("Hiba","Érvénytelen alhálózati maszk")
    
    def check_address_gateway(self,var_address):
        if var_address.get() != "" and not self.is_valid_address(var_address.get()):
            var_address.set("")
            messagebox.showwarning("Hiba","Érvénytelen átjáró cím")
        #az átjárót egyeztetni kellesz az ip címmel és a maszkkal

    def check_address_dns(self,var_address):
        if var_address.get() != "" and not self.is_valid_address(var_address.get()):
            var_address.set("")
            messagebox.showwarning("Hiba","Érvénytelen DNS cím")

    def generate_tester(self):
        self.button_generate_tester.config(state="disabled")
        self.messages_display.config(state="normal")
        self.messages_display.insert("end","Tesztelő fájl generálása\n")
        self.messages_display.config(state="disabled")
        
        #Windows
        if self.var_system_id.get() == 0:
            try:
                with open("data/scripts/windows/TEST.ps1","r",encoding="utf-8") as file:
                    file_content = file.read()
                iso_file = pycdlib.PyCdlib()
                iso_file.new()
                iso_file.add_fp(BytesIO(file_content), len(file_content), iso_path="/TESTER.PS1")
                iso_file.write('tester.iso')
                iso_file.close()
            except Exception as exception:
                self.messages_display.config(state="normal")
                self.messages_display.insert("end",f"Hiba: {exception}\n")
                self.messages_display.config(state="disabled")
                
        #Linux
        elif self.var_system_id.get() == 1:
            try:
                with open("data/scripts/linux/TEST.sh","r",encoding="utf-8") as file:
                    file_content = file.read()
                iso_file = pycdlib.PyCdlib()
                iso_file.new()
                iso_file.add_fp(BytesIO(file_content), len(file_content), iso_path="/TESTER.SH")
                iso_file.write('tester.iso')
                iso_file.close()
            except Exception as exception:
                self.messages_display.config(state="normal")
                self.messages_display.insert("end",f"Hiba: {exception}\n")
                self.messages_display.config(state="disabled")
        self.button_generate_tester.config(state="normal")
    
    def generate_config(self):
        self.button_generate_config.config(state="disabled")
        self.messages_display.config(state="normal")
        self.messages_display.insert("end","Konfigurációs fájl generálása\n")
        self.messages_display.config(state="disabled")
        
        #Windows
        if self.var_system_id.get() == 0:
            try:
                iso_file = pycdlib.PyCdlib()
                iso_file.new()
                file_content = b'windows config here\n'
                iso_file.add_fp(BytesIO(file_content), len(file_content), iso_path="/INSTALL.PS1")
                iso_file.write('config.iso')
                iso_file.close()
            except Exception as exception:
                self.messages_display.config(state="normal")
                self.messages_display.insert("end",f"Hiba: {exception}\n")
                self.messages_display.config(state="disabled")
                
        #Linux
        elif self.var_system_id.get() == 1:
            try:
                with open("data/scripts/linux/BASIC.sh","r",encoding="utf-8") as file:
                    file_content = file.read()
                file_content = file_content.replace("$IP_ADDRESS",self.var_address_ip.get())
                file_content = file_content.replace("$NETMASK",self.var_address_netmask.get())
                file_content = file_content.replace("$GATEWAY",self.var_address_gateway.get())
                file_content = file_content.replace("$DNS_SERVER",self.var_address_dns.get())
                file_content = file_content.encode("utf-8")
                iso_file = pycdlib.PyCdlib()
                iso_file.new()
                iso_file.add_fp(BytesIO(file_content), len(file_content), iso_path="/INSTALL.SH")
                iso_file.write('config.iso')
                iso_file.close()
            except Exception as exception:
                self.messages_display.config(state="normal")
                self.messages_display.insert("end",f"Hiba: {exception}\n")
                self.messages_display.config(state="disabled")
        self.button_generate_config.config(state="normal")

    def show_message_howtoinstall(self):
        messagebox.showinfo("Telepítés menete",self.var_message_howtoinstall)
        
if __name__ == "__main__":
    window = Tk()
    window.title("Server config - standalone")
    server = Server()
    server.pack()
    window.mainloop()
