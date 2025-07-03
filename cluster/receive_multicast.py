import socket
import struct
import pickle
import sys
from cluster import hosts, ports

#multicast IP & UDP Socket
multicast_address = (hosts.multicast, ports.multicast_port)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', ports.multicast_port))

# Explizite Netzwerkschnittstellen-Konfiguration
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(hosts.myIP))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, 
                socket.inet_aton(hosts.multicast) + socket.inet_aton(hosts.myIP))

#start point for multicast
def receive_multicast_message():
    global sock
    print(f'\n[MULTICAST RECEIVER {hosts.myIP}] UDP-Socket Start is ready , listening on Port {ports.multicast_port}',
          file=sys.stderr)
 
    while True:
        try:
            received_data, address = sock.recvfrom(hosts.buffer_size)
        
            print(f'\n[MULTICAST RECEIVER {hosts.myIP}] Data from {address} received\n',
              file=sys.stderr)
 
            if hosts.current_leader == hosts.myIP and pickle.loads(received_data)[0] == 'JOIN':
                complete_message = pickle.dumps([hosts.current_leader, ''])
                sock.sendto(complete_message, address)
                print(f'[MULTICAST RECEIVER {hosts.myIP}] Client {address} wants to join ASAChat Room\n',
                  file=sys.stderr)
 
            if len(pickle.loads(received_data)[0]) == 0:
                hosts.server_list.append(address[0]) if address[0] not in hosts.server_list else hosts.server_list
                sock.sendto('ack'.encode(hosts.unicode), address)
                hosts.has_network_changed = True
 
            elif pickle.loads(received_data)[1] and hosts.current_leader != hosts.myIP or pickle.loads(received_data)[3]:
                hosts.server_list = pickle.loads(received_data)[0]
                hosts.current_leader = pickle.loads(received_data)[1]
                hosts.client_list = pickle.loads(received_data)[4]
                print(f'[MULTICAST RECEIVER {hosts.myIP}] All Data have beed updated',
                  file=sys.stderr)
                sock.sendto('ack'.encode(hosts.unicode), address)
                hosts.has_network_changed = True

        except KeyboardInterrupt:
            print(f'[MULTICAST RECEIVER {hosts.myIP}] UDP-Socket is closed',
              file=sys.stderr)
