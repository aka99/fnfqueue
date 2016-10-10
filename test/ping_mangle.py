import pynfq
from scapy.all import *

queue = 1

conn = pynfq.Connection()

conn.bind(queue)
conn.set_mode(queue, 1000, pynfq.COPY_PACKET)

for packet in conn:
    x = IP(packet.payload)
    x[ICMP].load = x[ICMP].load[:-2] + b'\x00'*5
    del x[ICMP].chksum
    del x[IP].len
    packet.payload = bytes(x)
    packet.mangle()

conn.close()
