import socket


# get own IP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("8.8.8.8", 80))
myIP = sock.getsockname()[0]



#Connection variables
buffer_size = 1024 
unicode = 'utf-8'
 
# Global IP-Adress Variables
multicast = '239.0.0.1'
current_leader = ''
current_neighbour = ''
server_list = []
client_list = []
 
# States Variables
is_client_running = False
has_network_changed = False
is_leader_crashed = ''
is_replica_crashed = ''