from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
import time
from scapy_functions import ScapyOperations
import multiprocessing
from PIL import ImageTk, Image
import json
from subprocess import Popen, PIPE

ips_to_process = {}
founded_ips = {}
source = []
scapy_operations = ScapyOperations()

def speed_test():
    stdout = Popen('speedtest-cli --json', shell=True, stdout=PIPE).stdout
    output = json.loads(stdout.read().decode("utf-8"))
    result = "Tested from {0}\n".format(output["client"]["isp"])
    result += "Hosted by {0}\n".format(output["server"]["sponsor"])
    result += "Location: {0}-{1}\n".format(output["server"]["name"], output["server"]["country"])
    result += "Ping: {0} ms\n".format(output["ping"])
    result += "Download: {:.2f} Mbit/s\n".format(output["download"] / 1000.0 / 1000.0)
    result += "Upload: {:.2f} Mbit/s\n".format(output["upload"] / 1000.0 / 1000.0)
    messagebox.showinfo("Connection Speed", result)


def scan():
    founded_ips = {}
    source = []
    ips_to_process = {}
    ip_list = scapy_operations.arp_scan("192.168.1.1/24")
    t = Table(root, ip_list)


def kill_single():
    processed_ips = []
    for ip_to_process in ips_to_process:
        kill_wifi = multiprocessing.Process(target = scapy_operations.kill, args=(source, ips_to_process[ip_to_process], ip_to_process,))
        kill_wifi.start()
        print("kill single")
        processed_ips.append(ip_to_process)
        children = trv.get_children()
        for child in children:
            if trv.item(child)["values"][0] == ip_to_process:
                tags = "unchecked-dead"
                trv.item(child, tags=tags)
    for ip in processed_ips:
        ips_to_process.pop(ip)
    print(ips_to_process)


def kill_all():
    for ip in founded_ips:
        #kill_wifi = multiprocessing.Process(target = scapy_operations.kill, args=(source, ips_to_process[ip_to_process], ip_to_process,))
        #kill_wifi.start()
        children = trv.get_children()
        for child in children:
            if trv.item(child)["values"][0] == ip:
                tags = "unchecked-dead"
                trv.item(child, tags=tags)
    ips_to_process = {}
    print("kill all")
    print(ips_to_process)


def recover():
    processed_ips = []
    for ip_to_process in ips_to_process:
        #unkill_wifi = multiprocessing.Process(target = scapy_operations.unkill, args=(source, ips_to_process[ip_to_process], ip_to_process,))
        #unkill_wifi.start()
        processed_ips.append(ip_to_process)
        children = trv.get_children()
        for child in children:
            if trv.item(child)["values"][0] == ip_to_process:
                tags = "unchecked-alive"
                trv.item(child, tags=tags)
    for ip in processed_ips:
        ips_to_process.pop(ip)
    print(ips_to_process)
    print("recover")

def recover_all():
    for ip_to_process in founded_ips:
        #unkill_wifi = multiprocessing.Process(target = scapy_operations.unkill, args=(source, ips_to_process[ip_to_process], ip_to_process,))
        #unkill_wifi.start()
        children = trv.get_children()
        for child in children:
            if trv.item(child)["values"][0] == ip_to_process:
                tags = "unchecked-alive"
                trv.item(child, tags=tags)
    ips_to_process = {}
    print(ips_to_process)
    print("recover all")


def toggleCheck(event):
    try:
        rowid = trv.identify_row(event.y)
        tag = trv.item(rowid, "tags")[0]
        ip_to_process = trv.item(rowid, "values")[0]
        mac_to_process = trv.item(rowid, "values")[1]
        tags = list(trv.item(rowid, "tags"))[0]
        if "unchecked" not in tags: # checked
            if "dead" in tags:
                tags = "unchecked-dead"
            else:
                tags = "unchecked-alive"
            trv.item(rowid, tags=tags)
            del ips_to_process[ip_to_process]
        else:
            if "dead" in tags:
                tags = "checked-dead"
            else:
                tags = "checked-alive"
            trv.item(rowid, tags=tags)
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
                #trv.insert("", "end", values=ip_info, tags=("unchecked", "alive"))
                founded_ips[founded_ip] = founded_mac


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
    btn_kill_single = Button(wrapper1, text="Kill", command= kill_single)
    btn_recover = Button(wrapper1, text="Recover", command=recover)
    btn_recover_all = Button(wrapper1, text="Recover All", command=recover_all)

    btn_scan.pack()
    btn_kill_all.pack()
    btn_kill_single.pack()
    btn_recover.pack()
    btn_recover_all.pack()


    im_check = ImageTk.PhotoImage(Image.open("images/check.png"))
    im_uncheck = ImageTk.PhotoImage(Image.open("images/uncheck.png"))

    trv = ttk.Treeview(wrapper1, columns=(1,2,3))
    style = ttk.Style(trv)
    style.configure("Treeview", foreground="blue", rowheight=32)
    trv.tag_configure("checked", image=im_check)
    trv.tag_configure("unchecked", image=im_uncheck)

    trv.tag_configure("unchecked-dead", background="red", foreground="white", image=im_uncheck)
    trv.tag_configure("unchecked-alive", image=im_uncheck)

    trv.tag_configure("checked-dead", background="red", foreground="white", image=im_check)
    trv.tag_configure("checked-alive", image=im_check)
    #trv.tag_configure("killed", background=red, image=im_uncheck)
    trv.pack()
    trv.heading("#0", text="")
    trv.column("#0", width=80)
    trv.heading("#1", text="IP Address")
    trv.heading("#2", text="MAC Address")
    trv.heading("#3", text="Manufacturer")

    trv.bind("<Button-1>", toggleCheck)
    btn_kill_single.bind("<Button-1>", kill_single)
    btn_kill_all.bind("<Button-1>", kill_all)

    root.title("Wifi Control Application")
    root.geometry("800x400")
    root.mainloop()