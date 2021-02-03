from tkinter import *
from tkinter import ttk
import tkinter as tk
import time
from scapy_functions import arp_scan


ip_to_kill = []

def speed_test():
    print("speed test")


def scan():
    ip_list = arp_scan("192.168.1.1/24")
    t = Table(root, ip_list)


def kill_all():
    print("kill all")


def kill_single():
    print("kill single")


def recover():
    print("recover")


class Table:
    def __init__(self, root, ip_list):
        # code for creating table
        for ip_info in ip_list:
                trv.insert("", "end", values=ip_info)
        """
        for i in range(len(ip_list)):
            choose = Checkbutton(root)
            for j in range(3):
                self.e = Entry(root, width=20, fg='blue', bg="yellow",
                               font=('Arial', 16, 'bold'))
                self.e.choose.grid(row=2+i, column=0)
                self.e.grid(row=2+i, column=j+1)
                self.e.insert(END, ip_list[i][j])
        #t.e.configure(state="readonly")
        """
        


if __name__ == '__main__':
    root = Tk()

    # lst = [(1, 'Raj', 'Mumbai', 19),
    #        (2, 'Aaryan', 'Pune', 18),
    #        (3, 'Vaishnavi', 'Mumbai', 20),
    #        (4, 'Rachna', 'Mumbai', 21),
    #        (5, 'Shubham', 'Delhi', 21)]
    # total_rows = len(lst)
    # total_columns = len(lst[0])
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
    #t = Table(root)
    wrapper1 = LabelFrame(root, text="Local Connected Users", fg="black", font=(('Arial'), 20))
    wrapper1.pack(fill = "both", expand="yes", padx=20, pady=20)
    buttons = Label(wrapper1)
    buttons.pack(side=tk.TOP)
    btn_scan = Button(wrapper1, text="Scan", command=scan)
    btn_kill_all = Button(wrapper1, text="Kill All", command=kill_all)
    btn_kill_single = Button(wrapper1, text="Kill", command=kill_single)
    btn_recover = Button(wrapper1, text="Recover", command=recover)

    btn_scan.place(x=80, y=10)
    btn_kill_all.place(x=150, y=10)
    btn_kill_single.place(x=240, y=10)
    btn_recover.place(x=310, y=10)

    trv = ttk.Treeview(wrapper1, columns=(1,2,3), show="headings")
    style = ttk.Style(root)
    style.configure("Treeview", foreground="blue", background="yellow")
    trv.place(x=80, y=60)
    trv.heading(1, text="IP Address")
    trv.heading(2, text="MAC Address")
    trv.heading(3, text="Manufacturer")



    root.title("Wifi Control Application")
    root.geometry("800x400")
    root.mainloop()
