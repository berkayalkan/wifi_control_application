from tkinter import *
from tkinter import ttk, messagebox
from scapy_functions import ScapyOperations
import multiprocessing
import json
from subprocess import Popen, PIPE

ips_to_process = {}
founded_ips = {}
source = []
increased = []
decreased = []
DEAD = -1
DECREASED_WITH_BUTTON = 3
DECREASED_WITH_INCREASE = 120
DEFAULT = 100
INCREASED = 1000


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
    founded_ips.clear()
    source.clear()
    ips_to_process.clear()
    increased.clear()
    decreased.clear()
    scapy_operations.dead.clear()
    scapy_operations.speed_of_ips.clear()
    ip_list = scapy_operations.arp_scan("192.168.1.1/24")
    t = Table(root, ip_list)


def decrease_speed():
    for ip_to_process in ips_to_process:
        if scapy_operations.speed_of_ips[ip_to_process] == DEFAULT or scapy_operations.speed_of_ips[ip_to_process] == DECREASED_WITH_INCREASE:
            decreased.append(ip_to_process)
            scapy_operations.speed_of_ips[ip_to_process] = DECREASED_WITH_BUTTON
            decrease_proc = multiprocessing.Process(target=scapy_operations.speed_decrease, args=(source,
                                                                                                  ips_to_process[ip_to_process],
                                                                                                  ip_to_process,
                                                                                                  scapy_operations.speed_of_ips[ip_to_process]))
            decrease_proc.start()
        elif scapy_operations.speed_of_ips[ip_to_process] == INCREASED:
            scapy_operations.speed_of_ips[ip_to_process] = DEFAULT
            increased.remove(ip_to_process)
            if not increased:
                if ip_to_process not in scapy_operations.dead and ip_to_process not in decreased:
                    scapy_operations.speed_of_ips[ip_to_process] = DEFAULT
        children = trv.get_children()
        for child in children:
            if trv.item(child)["values"][0] == ip_to_process:
                if scapy_operations.speed_of_ips[ip_to_process] == DEFAULT:
                    tags = "unchecked-alive"
                elif scapy_operations.speed_of_ips[ip_to_process] == DEAD:
                    tags = "unchecked-dead"
                else:
                    tags="unchecked-decreased"
                values = list(trv.item(child)["values"])
                values.remove("Yes")
                values.append("No")
                trv.item(child, tags=tags, values=values)
    ips_to_process.clear()


def kill_single():
    for ip_to_process in ips_to_process:
        temp_bool = True
        if ip_to_process in increased:
            increased.remove(ip_to_process)
        if ip_to_process in decreased:
            decreased.remove(ip_to_process)
        if ip_to_process in scapy_operations.dead:
            temp_bool = False
        if temp_bool:
            scapy_operations.dead[ip_to_process] = ips_to_process[ip_to_process]
            scapy_operations.speed_of_ips[ip_to_process] = DEAD
            kill_wifi = multiprocessing.Process(target=scapy_operations.kill, args=(source,
                                                                                    ips_to_process[ip_to_process],
                                                                                    ip_to_process,
                                                                                    1))
            kill_wifi.start()
        children = trv.get_children()
        for child in children:
            if trv.item(child)["values"][0] == ip_to_process:
                tags = "unchecked-dead"
                values = list(trv.item(child)["values"])
                values.remove("Yes")
                values.append("No")
                trv.item(child, tags=tags, values=values)
    ips_to_process.clear()


def kill_all():
    for ip_to_process in founded_ips:
        if ip_to_process in increased:
            increased.remove(ip_to_process)
        if ip_to_process in decreased:
            decreased.remove(ip_to_process)
        if ip_to_process in scapy_operations.dead:
            continue
        scapy_operations.dead[ip_to_process] = founded_ips[ip_to_process]
        scapy_operations.speed_of_ips[ip_to_process] = DEAD
        kill_wifi = multiprocessing.Process(target=scapy_operations.kill, args=(source,
                                                                                founded_ips[ip_to_process],
                                                                                ip_to_process,
                                                                                1))
        kill_wifi.start()
        children = trv.get_children()
        for child in children:
            if trv.item(child)["values"][0] == ip_to_process:
                tags = "unchecked-dead"
                values = list(trv.item(child)["values"])
                if "Yes" in values:
                    values.remove("Yes")
                    values.append("No")
                trv.item(child, tags=tags, values=values)
    ips_to_process.clear()


def increase_speed():
    to_be_decreased = []
    for ip_to_process in founded_ips:
        if ip_to_process not in ips_to_process and scapy_operations.speed_of_ips[ip_to_process] == DEFAULT:
            to_be_decreased.append(ip_to_process)

    temp_bool = False
    for ip_to_process in ips_to_process:
        if ip_to_process in scapy_operations.dead:
            pass
            # messagebox
        elif scapy_operations.speed_of_ips[ip_to_process] == INCREASED:
            pass
        elif scapy_operations.speed_of_ips[ip_to_process] == DECREASED_WITH_BUTTON:
            decreased.remove(ip_to_process)
            scapy_operations.speed_of_ips[ip_to_process] = DEFAULT
        elif scapy_operations.speed_of_ips[ip_to_process] == DECREASED_WITH_INCREASE:
            scapy_operations.speed_of_ips[ip_to_process] = DEFAULT
        else:
            scapy_operations.speed_of_ips[ip_to_process] = INCREASED
            increased.append(ip_to_process)
            temp_bool = True
        children = trv.get_children()
        for child in children:
            if trv.item(child)["values"][0] == ip_to_process:
                if scapy_operations.speed_of_ips[ip_to_process] == DEAD:
                    tags = "unchecked-dead"
                elif scapy_operations.speed_of_ips[ip_to_process] == INCREASED:
                    tags = "unchecked-increased"
                else:
                    tags = "unchecked-alive"
                values = list(trv.item(child)["values"])
                values.remove("Yes")
                values.append("No")
                trv.item(child, tags=tags, values=values)
    ips_to_process.clear()

    if temp_bool:
        for ip_to_process in to_be_decreased:
            scapy_operations.speed_of_ips[ip_to_process] = DECREASED_WITH_INCREASE
            decrease_proc = multiprocessing.Process(target=scapy_operations.speed_decrease, args=(source,
                                                                                                  founded_ips[ip_to_process],
                                                                                                  ip_to_process,
                                                                                                  scapy_operations.speed_of_ips[ip_to_process]))
            decrease_proc.start()


def recover():
    for ip_to_process in ips_to_process:
        if ip_to_process in increased:
            increased.remove(ip_to_process)
        if ip_to_process in decreased:
            decreased.remove(ip_to_process)
        scapy_operations.speed_of_ips[ip_to_process] = DEFAULT
        unkill_wifi = multiprocessing.Process(target=scapy_operations.unkill, args=(source,
                                                                                    ips_to_process[ip_to_process],
                                                                                    ip_to_process,))
        unkill_wifi.start()
        children = trv.get_children()
        for child in children:
            if trv.item(child)["values"][0] == ip_to_process:
                tags = "unchecked-alive"
                values = list(trv.item(child)["values"])
                values.remove("Yes")
                values.append("No")
                trv.item(child, tags=tags, values=values)
    ips_to_process.clear()


def recover_all():
    for ip_to_process in founded_ips:
        if ip_to_process in increased:
            increased.remove(ip_to_process)
        if ip_to_process in decreased:
            decreased.remove(ip_to_process)
        scapy_operations.speed_of_ips[ip_to_process] = DEFAULT
        unkill_wifi = multiprocessing.Process(target=scapy_operations.unkill, args=(source,
                                                                                    founded_ips[ip_to_process],
                                                                                    ip_to_process,))
        unkill_wifi.start()
        scapy_operations.speed_of_ips[ip_to_process] = DEFAULT
        children = trv.get_children()
        for child in children:
            if trv.item(child)["values"][0] == ip_to_process:
                tags = "unchecked-alive"
                values = list(trv.item(child)["values"])
                if "Yes" in values:
                    values.remove("Yes")
                    values.append("No")
                trv.item(child, tags=tags, values=values)
    ips_to_process.clear()


def toggle_check(event):
    try:
        rowid = trv.identify_row(event.y)
        tag = trv.item(rowid, "tags")[0]
        ip_to_process = trv.item(rowid, "values")[0]
        mac_to_process = trv.item(rowid, "values")[1]
        values = list(trv.item(rowid, "values"))
        tags = list(trv.item(rowid, "tags"))[0]
        if "unchecked" not in tags:  # checked
            values.remove("Yes")
            values.append("No")
            if "dead" in tags:
                tags = "unchecked-dead"
            elif "decreased" in tags:
                tags = "unchecked-decreased"
            elif "increased" in tags:
                tags = "unchecked-increased"
            else:
                tags = "unchecked-alive"
            trv.item(rowid, tags=tags, values=values)
            if ip_to_process in ips_to_process:
                del ips_to_process[ip_to_process]
        else:
            values.remove("No")
            values.append("Yes")
            if "dead" in tags:
                tags = "checked-dead"
            elif "decreased" in tags:
                tags = "checked-decreased"
            elif "increased" in tags:
                tags = "checked-increased"
            else:
                tags = "checked-alive"
            trv.item(rowid, tags=tags, values=values)
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
                ip_info = ip_info + ("No",)
                trv.insert("", "end", values=ip_info, tags="unchecked")
                founded_ips[founded_ip] = founded_mac
                scapy_operations.speed_of_ips[founded_ip] = DEFAULT


if __name__ == '__main__':
    global scapy_operations
    scapy_operations = ScapyOperations()
    root = Tk()
    wrapper1 = LabelFrame(root, text="Local Connected Users", fg="black", font=('Arial', 20))
    wrapper1.pack(fill="both", expand="yes", padx=20, pady=50)

    btn_scan = Button(wrapper1, text="Scan", command=scan)
    btn_kill_single = Button(wrapper1, text="Kill", command=kill_single)
    btn_recover = Button(wrapper1, text="Recover", command=recover)
    btn_kill_all = Button(wrapper1, text="Kill All", command=kill_all)
    btn_recover_all = Button(wrapper1, text="Recover All", command=recover_all)
    btn_speed_test = Button(wrapper1, text="Speed Test", command=speed_test)
    btn_increase = Button(wrapper1, text="Increase speed", command=increase_speed)
    btn_decrease = Button(wrapper1, text="Decrease speed", command=decrease_speed)

    btn_scan.place(relx=0.180, rely=0.025)
    btn_kill_single.place(relx=0.235, rely=0.025)
    btn_recover.place(relx=0.280, rely=0.025)
    btn_kill_all.place(relx=0.352, rely=0.025)
    btn_recover_all.place(relx=0.415, rely=0.025)
    btn_increase.place(relx=0.505, rely=0.025)
    btn_decrease.place(relx=0.615, rely=0.025)
    btn_speed_test.place(relx=0.727, rely=0.025)

    trv = ttk.Treeview(wrapper1, columns=(1, 2, 3, 4), show="headings")
    style = ttk.Style(trv)
    style.configure("Treeview", foreground="steel blue", rowheight=32)
    trv.tag_configure("checked", background="LightSkyBlue2", foreground="white")
    trv.tag_configure("unchecked")

    trv.tag_configure("unchecked-dead", background="tomato2", foreground="white")
    trv.tag_configure("unchecked-decreased", background="indian red", foreground="white")
    trv.tag_configure("unchecked-increased", background="green2", foreground="white")
    trv.tag_configure("unchecked-alive")

    trv.tag_configure("checked-dead", background="tomato2", foreground="white")
    trv.tag_configure("checked-alive", background="LightSkyBlue2", foreground="white")
    trv.tag_configure("checked-decreased", background="indian red", foreground="white")
    trv.tag_configure("checked-increased", background="green2", foreground="white")

    trv.place(relx=0.20, rely=0.1, relheight=0.8)

    trv.heading("#1", text="IP Address")
    trv.heading("#2", text="MAC Address")
    trv.heading("#3", text="Manufacturer")
    trv.heading("#4", text="Selected")
    trv.column("#4", width=80)

    trv.bind("<Button-1>", toggle_check)
    btn_kill_single.bind("<Button-1>", kill_single)
    btn_kill_all.bind("<Button-1>", kill_all)

    root.title("Wifi Control Application")
    root.geometry("1200x800")
    root.mainloop()
