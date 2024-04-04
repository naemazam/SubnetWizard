import ipaddress
import argparse
from os import system
from typing import Tuple

# Create the parser
parser = argparse.ArgumentParser(description='SubnetWizard')

# Add the arguments
ip_help = "The IPv4 address to calculate\nExample: 192.168.0.100/24 or 10.0.0.1/255.255.255.0\nSupports both CIDR and Subnet Mask after the slash"
parser.add_argument('-i', dest='ip', type=str, help=ip_help)
subnet_help = "The netmask to subnet (optional)\nExample: 255.255.255.0 or /24"
parser.add_argument('-s', dest='subnet', type=str, help=subnet_help)

def display_logo() -> None:
    print("\033[H\033[2J\033[1m\033[36m                                                        ")
    print("      (                                                                             ")           
    print(" )\ )             )                     )                                    (      ") 
    print("(()/(     (    ( /(             (    ( /(   (  (     (            )   (      )\ )   ")
    print(" /(_))   ))\   )\())   (       ))\   )\())  )\))(    )\   (    ( /(   )(    (()/(   ")
    print("(_))    /((_) ((_)\    )\ )   /((_) (_))/  ((_)()\  ((_)  )\   )(_)) (()\    ((_))  ")
    print(" / __|  (_))(  | |(_)  _(_/(  (_))   | |_   _(()((_)  (_) ((_) ((_)_   ((_)   _| |  ")
    print(" \__ \  | || | | '_ \ | ' \)) / -_)  |  _|  \ V  V /  | | |_ / / _` | | '_| / _` |  ")
    print(" |___/   \_,_| |_.__/ |_||_|  \___|   \__|   \_/\_/   |_| /__| \__,_| |_|   \__,_|  ")
    print("\033[0m", end="")
                                                          
                        

def get_network(ip: str = None) -> Tuple[ipaddress.IPv4Network, str]:
    
    # Get an IPv4 address from the user.
    if ip:
        try:
            if ip.count("/") == 0: ip += "/24"
            net = ipaddress.IPv4Network(ip, strict=False)
            ip = ip.split("/")[0]
            return (net, ip)
        except ValueError:
            print("\n\033[36m[\033[31m!\033[36m]\033[0m Invalid IP Address!\n")
            exit(1)
    print()
    while True:
        try:
            in_ = input("\033[36m[\033[31m?\033[36m]\033[0m Enter an IP Address (192.168.0.100/24): \033[36m")
            if in_ == "": in_ = "192.168.0.100/24"
            if in_.count("/") == 0: in_ += "/24"
            net = ipaddress.IPv4Network(in_, strict=False)
            ip = in_.split("/")[0]
            return (net, ip)
        except ValueError:
            print("\n\033[36m[\033[31m!\033[36m]\033[0m Invalid IP Address!\n")
            continue

def get_subnet(subnet: str = None) -> str:
    
    # Get a netmask from the user to subnet given network.
    
    if subnet:
        if subnet == "0": 
            print("\n\033[36m[\033[31m!\033[36m]\033[0m Invalid Netmask!\n")
            exit(1)
        try:
            net = ipaddress.IPv4Network(f"10.0.0.0/{subnet}", strict=False)
            return net.prefixlen
        except ValueError:
            print("\n\033[36m[\033[31m!\033[36m]\033[0m Invalid Netmask!\n")
            exit(1)
    print()
    while True:
        try:
            in_ = input("\033[36m[\033[31m?\033[36m]\033[0m Enter a Netmask to subnet (optional): \033[36m")
            if in_ == "0": 
                print("\n\033[36m[\033[31m!\033[36m]\033[0m Invalid Netmask!\n")
                continue
            if in_ == "": return None
            net = ipaddress.IPv4Network(f"10.0.0.0/{in_.strip('/')}", strict=False)
            return net.prefixlen
        except ValueError:
            print("\n\033[36m[\033[31m!\033[36m]\033[0m Invalid Netmask!\n")
            continue

def calculate(network: Tuple[ipaddress.IPv4Network, str], subnet: str) -> None:
    
    # Calculate the network and other information.
    

    ip = network[1]
    network = network[0]

    # Get the network and broadcast addresses
    network_address = network.network_address
    broadcast_address = network.broadcast_address
    usable_hosts = list(network.hosts())

    # Calculate the number of usable hosts
    num_usable_hosts = len(usable_hosts)

    # Format the usable hosts
    usable_hosts = f"{usable_hosts[0]} - {usable_hosts[-1]}" if usable_hosts[0] != usable_hosts[-1] else "NA"

    # Convert the IP address to binary
    octets = str(ip).split('.')
    binary_octets = [bin(int(octet))[2:].zfill(8) for octet in octets]
    bin_ip = '.'.join(binary_octets)

    bin_addr = str(bin(int(network_address))[2:].zfill(32))
    bin_addr = '.'.join([bin_addr[i:i+8] for i in range(0, len(bin_addr), 8)])

    bin_mask = str(bin(int(network.netmask))[2:].zfill(32))
    bin_mask = '.'.join([bin_mask[i:i+8] for i in range(0, len(bin_mask), 8)])

    # Print the results
    print(f"\033[0mIP Address:             \033[36m{ip}")
    print(f"\033[0mIP Address (bin):       \033[36m{bin_ip}")
    print(f"\033[0mNetwork Address:        \033[36m{network_address}")
    print(f"\033[0mNetwork Address (bin):  \033[36m{bin_addr}")
    print(f"\033[0mNetmask:                \033[36m{network.netmask}")
    print(f"\033[0mNetmask (bin):          \033[36m{bin_mask}")
    print(f"\033[0mCIDR Notation:          \033[36m/{network.prefixlen}")
    print(f"\033[0mBroadcast Address:      \033[36m{broadcast_address}")
    print(f"\033[0mUsable IP Range:        \033[36m{usable_hosts}")
    print(f"\033[0mNumber of Hosts:        \033[36m{network.num_addresses:,d}")
    print(f"\033[0mNumber of Usable Hosts: \033[36m{num_usable_hosts:,d}")
    print(f"\033[0mWildcard Mask:          \033[36m{network.hostmask}")
    print(f"\033[0mPrivate IP:             \033[36m{network.is_private}")
    print()

    # Display subnets if present
    if subnet is None or int(subnet) == int(network.prefixlen):
        return
    
    # if CIDR is greater than current network, subnet it, else supernet it.
    if int(subnet) > int(network.prefixlen): 
        print("\033[0mSubneted Network Details:\n")
        subnets = list(network.subnets(new_prefix=int(subnet)))
        print(f"\033[0mNetmask:                \033[36m{subnets[0].netmask}")
        print(f"\033[0mWildcard Mask:          \033[36m{subnets[0].hostmask}")
        print(f"\033[0mCIDR Notation:          \033[36m/{int(subnet)}")
        print(f"\033[0mHosts per network:      \033[36m{2 ** (32 - int(subnet)) - 2:,d}")

        # if CIDR is 32, do not print subnets
        if int(subnet) == 32: 
            return

        print("\n\033[0m{:<15} | {:^31} | {:<15}".format(
            "Network Address", "Host Range", "Broadcast Address"))
        print("-" * 72)
        for subnet in subnets:
            host_range = list(subnet.hosts())
            host_range = host_range if len(host_range) > 1 else [host_range[0], host_range[0]]
            # print(host_range)
            print("{:<24} | {:<22} - {:>24} | {:<24}".format(
                f"\033[36m{subnet.network_address}\033[0m", f"\033[36m{host_range[0]}\033[0m", 
                f"\033[36m{host_range[-1]}\033[0m", f"\033[36m{subnet.broadcast_address}\033[0m"
                ))
    else: 
        print("\033[0mSuperneted Network Details:\n")
        subnets = network.supernet(new_prefix=int(subnet))
        print(f"\033[0mNetmask:                \033[36m{subnets.netmask}")
        print(f"\033[0mWildcard Mask:          \033[36m{subnets.hostmask}")
        print(f"\033[0mCIDR Notation:          \033[36m/{int(subnet)}")
        print(f"\033[0mHosts/Network:          \033[36m{2 ** (32 - int(subnet)) - 2:,d}")
        
        print("\n\033[0m{:<15} | {:^31} | {:<15}".format(
            "Network Address", "Host Range", "Broadcast Address"))
        print("-" * 72)
        print("{:<24} | {:<22} - {:>24} | {:<24}".format(
            f"\033[36m{subnets[0]}\033[0m", f"\033[36m{subnets[1]}\033[0m", 
            f"\033[36m{subnets[-2]}\033[0m", f"\033[36m{subnets.broadcast_address}\033[0m"
            ))
    print()

def main():
    system("") # Fix for ANSI escape codes on Windows

    display_logo()
    print("                         \033[36mMade by: Azam\033[0m")

    args = parser.parse_args()
    
    ip = None
    if args.ip:
        ip = args.ip
    subnet = None
    if args.subnet:
        subnet = args.subnet

    network = get_network(ip)
    subnet = get_subnet(subnet)

    print()
    calculate(network, subnet)

if __name__ == "__main__":
    main()
