from tkinter import *
from tkinter import ttk
import tkinter as tk
import time
from scapy_functions import arp_scan
from PIL import ImageTk, Image

ips_to_process = {}
founded_ips = []
source = []
def speed_test():
    print("speed test")


def scan():
    founded_ips = []
    source = []
    ips_to_process = {}
    ip_list = arp_scan("192.168.1.1/24")
    t = Table(root, ip_list)


def kill_all():
    print("kill all")


def kill_single():
    print("kill single")


def recover():
    print("recover")
    

def toggleCheck(event):
    try:
        rowid = trv.identify_row(event.y)
        tag = trv.item(rowid, "tags")[0]
        ip_to_process = trv.item(rowid, "values")[0]
        mac_to_process = trv.item(rowid, "values")[1]
        tags = list(trv.item(rowid, "tags"))
        tags.remove(tag)
        trv.item(rowid, tags=tag)
        if tag == "checked":
            trv.item(rowid, tags="unchecked")
            del ips_to_process[ip_to_process]
        else:
            trv.item(rowid, tags="checked")
            ips_to_process[ip_to_process] = mac_to_process
    except IndexError:
        pass

class Table:
    def __init__(self, root, ip_list):
        # code for creating table
        for child in trv.get_children():
            trv.delete(child)
        i = 0
        for ip_info in ip_list:
            founded_ip = ip_info[0]
            founded_mac = ip_info[1]
            if i == 0:
                source.append(founded_ip)
                source.append(founded_mac)
                i += 1
            else:
                trv.insert("", "end", values=ip_info, tags="unchecked")
                founded_ips.append(founded_ip)

if __name__ == '__main__':
    root = Tk()
    """
    label = Label(root, text="Wifi Control Application", fg="blue", font=(('Arial'), 30))
    btn_speed_test = Button(root, text="Speed Test", command=speed_test)
    btn_scan = Button(root, text="Scan", command=scan)
    btn_kill_all = Button(root, text="Kill All", command=kill_all)
    btn_kill_single = Button(root, text="Kill", command=kill_single)
    btn_recover = Button(root, text="Recover", command=recover)

    label.grid(row=0, column=1)
    btn_speed_test.grid(row=1, column=0)
    btn_scan.grid(row=1, column=1)
    btn_kill_all.grid(row=1, column=2)
    btn_kill_single.grid(row=1, column=3)
    btn_recover.grid(row=1, column=4)
    """
    wrapper1 = LabelFrame(root, text="Local Connected Users", fg="black", font=(('Arial'), 20))

    wrapper1.pack(fill = "both", expand="yes", padx=20, pady=10)

    btn_scan = Button(wrapper1, text="Scan", command=scan)
    btn_kill_all = Button(wrapper1, text="Kill All", command=kill_all)
    btn_kill_single = Button(wrapper1, text="Kill", command=kill_single)
    btn_recover = Button(wrapper1, text="Recover", command=recover)

    btn_scan.pack()
    btn_kill_all.pack()
    btn_kill_single.pack()
    btn_recover.pack()


    im_check = ImageTk.PhotoImage(Image.open("images/check.png"))
    im_uncheck = ImageTk.PhotoImage(Image.open("images/uncheck.png"))

    trv = ttk.Treeview(wrapper1, columns=(1,2,3))
    style = ttk.Style(trv)
    style.configure("Treeview", foreground="blue", rowheight=32)
    trv.tag_configure("checked", image=im_check)
    trv.tag_configure("unchecked", image=im_uncheck)

    trv.pack()
    trv.heading("#0", text="")
    trv.column("#0", width=80)
    trv.heading("#1", text="IP Address")
    trv.heading("#2", text="MAC Address")
    trv.heading("#3", text="Manufacturer")

    trv.bind("<Button 1>", toggleCheck)

    root.title("Wifi Control Application")
    root.geometry("800x400")
    root.mainloop()