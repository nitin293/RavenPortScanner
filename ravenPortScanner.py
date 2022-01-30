import socket
import re
import threading
import argparse
import time


def banner():
    ban = '''
 ____  ____  _     ______     ____  ____  ____  _____  ____  ____  ____  _     _     _________ 
/  __\/  _ \/ \ |\/  __/ \  //  __\/  _ \/  __\/__ __\/ ___\/   _\/  _ \/ \  // \  //  __/  __\\
|  \/|| / \|| | //|  \ | |\ ||  \/|| / \||  \/|  / \  |    \|  /  | / \|| |\ || |\ ||  \ |  \/|
|    /| |-||| \// |  /_| | \||  __/| \_/||    /  | |  \___ ||  \_ | |-||| | \|| | \||  /_|    /
\_/\_\\\\_/ \|\__/  \____\_/  \\\\_/   \____/\_/\_\  \_/  \____/\____/\_/ \|\_/  \\\\_/  \\\\____\_/\_\\
                                                                                               
                                                                                                                               
Author: Nitin Choudhury
Version: 0.0.3                                                                                                                                                                                                                                                                          
    '''
    print(ban)


class PortScan:

    def __init__(self, domain):
        self.domain = domain
        self.IP = None
        self.portList = [port for port in range(1, 65536)]
        self.openPorts = []
        self.thread = 65535
        self.verbose = False


    def setIP(self):
        url = re.sub('(http|https)://', '', self.domain)
        IP = socket.gethostbyname(url)
        self.IP = IP

    def setPortList(self, portlist):
        if portlist:
            self.portList = portlist

    def setVervose(self, verbose):
        if verbose==True:
            self.verbose = True

    def setThread(self, thread):
        if thread:
            self.thread = thread

    def response(self, port):
        s = socket.socket()
        s.settimeout(5)
        response = s.connect_ex((self.IP, port))

        if response==0:
            time.sleep(1)
            self.openPorts.append(port)
            if self.verbose==True:
                print(f"OPEN PORT {port}")

        s.close()

    def main(self):
        self.setIP()

        for port in self.portList:
            print(f"Scanning Port: {port}", end="\r")
            t = threading.Thread(target=self.response, args=(port, ))
            t.start()

            if port%self.thread==0 or port==self.portList[-1]:
                t.join()

        print("\n\nPORTS\tSTATE")
        for openPort in self.openPorts:
            print(openPort, "\tOPEN")



if __name__ == '__main__':

    banner()
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d", "--domain",
        type=str,
        required=True,
        help="ADD DOMAIN NAME OR IP"
    )

    parser.add_argument(
        "-t", "--thread",
        type=int,
        help="SET NO. OF THREADS"
    )

    parser.add_argument(
        "-v", "--verbose",
        type=bool,
        help="SET VERBOSE TRUE/FALSE",
        choices=[True, False]
    )

    parser.add_argument(
        "-p", "--port",
        type=str,
        help="SET PORTS MANUALLY"
    )

    args = parser.parse_args()

    domain = args.domain
    thread = args.thread
    verbose = args.verbose

    portScanner = PortScan(domain)
    if thread:
        portScanner.setThread(thread)

    if verbose:
        portScanner.setVervose(verbose)

    if args.port:
        portlist = list(map(int, args.port.split(',')))
        portScanner.setPortList(portlist)


    portScanner.main()
