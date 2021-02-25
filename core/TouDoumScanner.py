import iptools
from core.lib import scan, console, data

ip_private = iptools.IpRangeList(
    '0.0.0.0/8', '10.0.0.0/8', '100.64.0.0/10', '127.0.0.0/8',
    '169.254.0.0/16', '172.16.0.0/12', '192.0.0.0/24', '192.0.2.0/24',
    '192.88.99.0/24', '192.168.0.0/16', '198.18.0.0/15', '198.51.100.0/24',
    '203.0.113.0/24', '224.0.0.0/4', '240.0.0.0/4', '255.255.255.255/32'
)


class TouDoumScanner:
    # input mode
    ip: iptools.IpRangeList = None  # ip range list
    shodan: str = None  # shodan api key
    ipfile: str = None  # file with one ip by line

    timeout: int = None
    skip_private: bool = None  # todo change name of args to skip
    scan_memcached: bool = None
    scan_ntp: bool = None
    scan_dns: bool = None
    scan_used = []
    output_file_name: str = None
    file: data.Data = None
    verbose: bool = None
    threads: int = None

    def __init__(self, ip, ipfile, shodan, skip_private, memcached, ntp, dns, timeout, verbose, threads):
        self.ip = ip
        self.ipfile = ipfile
        self.shodan = shodan
        self.skip_private = skip_private
        self.scan_memcached = memcached
        self.scan_ntp = ntp
        self.scan_dns = dns
        self.timeout = timeout
        self.verbose = verbose
        self.threads = threads

    def set_file_name(self, name):
        if name is not None:
            self.output_file_name = name

    def init(self):
        # generate list of service to scan
        if self.scan_memcached:
            self.scan_used.append("memcached")
        if self.scan_dns:
            self.scan_used.append("dns")
        if self.scan_ntp:
            self.scan_used.append("ntp")

        if len(self.scan_used) == 0:
            console.error("no type scan specified")
            exit(-1)

        if self.output_file_name is not None:
            self.file = data.load(self.output_file_name)
        # all is ok run next of the scanners

    def send(self):
        # send to scanner all ip on cidr
        if self.ip is not None:  # todo add print configuration of scan
            ips = self.ip.__iter__()

            while True:
                try:
                    ip = iptools.next(ips)

                    if ip in ip_private:
                        if not self.skip_private:
                            self.scanner(ip)
                        else:
                            if self.verbose:
                                console.ip_skipped(ip)
                    else:
                        self.scanner(ip)

                except StopIteration:
                    print("All send to scanner !")
                    break

        # send to scanner all ip get by shodan
        elif self.shodan is not None:
            for ip in scan.get_from_shodan(self.shodan):
                self.scanner(ip)

        # open given file given with ip list and send it to scanner
        elif self.ipfile is not None:
            try:
                with open(self.ipfile) as f:
                    for line in f.readlines():
                        self.scanner(line.replace("\n", ""))
            except FileNotFoundError:
                console.error("File " + self.ipfile + " not found :/")

        # next of scanner when all is end

    def scanner(self, ip):
        if "memcached" in self.scan_used:
            if scan.memcache_udp(ip, self.timeout):
                console.ip_found(ip, "Memcached")
                if self.output_file_name is not None:
                    self.file.add_memcached(ip)
            else:
                if self.verbose:
                    console.ip_not_found(ip, "Memcached")

        if "dns" in self.scan_used:
            if scan.dns_udp(ip, self.timeout):
                console.ip_found(ip, "DNS")
                if self.output_file_name is not None:
                    self.file.add_dns(ip)
            else:
                if self.verbose:
                    console.ip_not_found(ip, "DNS")

        if "ntp" in self.scan_used:
            if scan.ntp_udp(ip, self.timeout):
                console.ip_found(ip, "NTP")
                if self.output_file_name is not None:
                    self.file.add_ntp(ip)
            else:
                if self.verbose:
                    console.ip_not_found(ip, "NTP")

        if self.file is not None:
            self.file.save()
