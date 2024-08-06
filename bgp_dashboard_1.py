import netmiko
from datetime import datetime

def fetch_bgp_peer_status(host, username, password):
    try:
        connection = netmiko.ConnectHandler(
            device_type='juniper_junos',
            host=host,
            username=username,
            password=password
        )

        bgp_summary_output = connection.send_command('show bgp summary')
        bgp_prefix_output = connection.send_command('show bgp neighbor detail')
        connection.disconnect()

        peer_status_data = parse_bgp_summary_output(bgp_summary_output)
        prefix_routing_data = parse_bgp_prefix_output(bgp_prefix_output)

        return peer_status_data, prefix_routing_data

    except netmiko.NetMikoAuthenticationException:
        print(f"Authentication error for host: {host}")
    except netmiko.NetMikoTimeoutException:
        print(f"Timeout error for host: {host}")
    except Exception as e:
        print(f"Error fetching BGP data for host {host}: {e}")

    return [], []

def parse_bgp_summary_output(output):
    peer_status_data = []

    lines = output.split('\n')
    for i in range(5, len(lines)):
        line = lines[i].strip()
        if line:
            peer_ip, as_number, peer_state, admin_state, uptime = line.split()
            peer_status_data.append({
                'peer_ip': peer_ip,
                'as_number': as_number,
                'peer_state': peer_state,
                'admin_state': admin_state,
                'uptime': uptime
            })

    return peer_status_data

def parse_bgp_prefix_output(output):
    prefix_routing_data = []

    lines = output.split('\n')
    current_peer = None
    for line in lines:
        if line.startswith('BGP neighbor is'):
            current_peer = line.split()[3]
        elif line.startswith('  Prefixes received'):
            prefixes_received = int(line.split(':')[1].strip())
        elif line.startswith('  Prefixes current'):
            prefixes_current = int(line.split(':')[1].strip())
            prefix_routing_data.append({
                'peer_ip': current_peer,
                'prefixes_received': prefixes_received,
                'prefixes_current': prefixes_current,
                'prefix_changes': prefixes_received - prefixes_current
            })

    return prefix_routing_data

def display_peer_status_table(peer_status_data):
    print("BGP Peer Status")
    print("----------------")
    print("{:<16} {:<10} {:<12} {:<12} {:<20}".format(
        "Peer IP", "AS Number", "Peer State", "Admin State", "Uptime"
    ))
    print("-" * 80)

    for peer in peer_status_data:
        print("{:<16} {:<10} {:<12} {:<12} {:<20}".format(
            peer['peer_ip'], peer['as_number'], peer['peer_state'],
            peer['admin_state'], peer['uptime']
        ))

def display_prefix_routing_table(prefix_routing_data):
    print("\nPrefix Routing Information")
    print("-------------------------")
    print("{:<16} {:<10} {:<12} {:<12}".format(
        "Peer IP", "AS Number", "Prefixes Received", "Prefix Changes"
    ))
    print("-" * 80)

    for peer in prefix_routing_data:
        print("{:<16} {:<10} {:<12} {:<12}".format(
            peer['peer_ip'], peer['as_number'],
            peer['prefixes_received'], peer['prefix_changes']
        ))

def main():
    host = input("Enter the host IP/hostname: ")
    username = input("Enter the username: ")
    password = input("Enter the password: ")

    peer_status_data, prefix_routing_data = fetch_bgp_peer_status(host, username, password)

    display_peer_status_table(peer_status_data)
    display_prefix_routing_table(prefix_routing_data)

if __name__ == "__main__":
    main()