from tkinter import *
from tkinter import ttk

from scapy_deneme import arp_scan


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
        for i in range(len(ip_list)):
            for j in range(3):
                self.e = Entry(root, width=20, fg='blue',
                               font=('Arial', 16, 'bold'))

                self.e.grid(row=2+i, column=j)
                self.e.insert(END, ip_list[i][j])


if __name__ == '__main__':
    root = Tk()

    # lst = [(1, 'Raj', 'Mumbai', 19),
    #        (2, 'Aaryan', 'Pune', 18),
    #        (3, 'Vaishnavi', 'Mumbai', 20),
    #        (4, 'Rachna', 'Mumbai', 21),
    #        (5, 'Shubham', 'Delhi', 21)]
    # total_rows = len(lst)
    # total_columns = len(lst[0])

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

    #t = Table(root)

    root.geometry("1000x450")
    root.mainloop()
