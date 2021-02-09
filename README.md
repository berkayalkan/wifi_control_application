# Wifi Control Application
### Purpose of the program
This is a desktop application which allows users to discover other users that are connected to the same LAN with their IP, MAC addresses and manufacturer name. The user can cut the wifi connection and slow down the connection bandwidth of an user who is available on the LAN. The user also will be able to speed up the connection bandwidth of slowed down users. Moreover, the user can check her connection speed from the application.
### How to run
You can simply run the code with 
```
sudo python3 main.py
```
command on your terminal in the project directory. After typing your password, the application will open.
### User Manual
* Press "Scan" to discover connected users.
* Press "Speed Test" to check your internet connection. <br/><br/>
After scanning;
* Press "Kill All" to cut all users' wifi connection.
* Press "Recover All" to stop cutting the wifi connection of the users. <br/><br/>
After scanning and selecting a user;
* Press "Kill" to cut the wifi connection of the user.
* Press "Recover" to stop cutting the wifi connection of the user.
* Press "Increase Speed" to increase the speed of the user.
* Press "Decrease Speed" to decrease the speed of the user.
##### Notes
* User can understand which rows are selected by looking at the "Selected" column which is on the most right part.
* Killed users' speed can not be changed with buttons, it can only be recovered.
* When a user is cut or recovered speed changes of this user is initialized.
* After scanning, all speed changes and cut-recovered status are initialized.
### How to exit
You can simply exit the program by clicking the close button of the application.
### Requirements
* Python 3.8 is used.
* tkinter library
* scapy library
* manuf library
* speedtest-cli library
### Contributors
* M. Olcayto Türker
* Berkay Alkan
### References
* https://github.com/sivel/speedtest-cli
* https://scapy.readthedocs.io/en/latest/
* https://www.geeksforgeeks.org/python-how-to-create-an-arp-spoofer-using-scapy/
* https://dev.to/zeyu2001/network-scanning-with-scapy-in-python-3off
* https://docs.python.org/3/library/tk.html
