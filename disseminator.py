import errno
import multiprocessing
import socket
import struct
import time

from config import *

def send_update(machine, status, members):
  update_order = build_update_order(machine, status)
  print("Sending Order: {}".format(update_order))
  udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  for member in members:
    member_address = (member, listener_port)
    print ("  -  {}".format(member_address))
    sent_bytes = udp_socket.sendto(build_update_order(machine, status), member_address)
    # I don't know that we need to care about the ack here

def build_update_order(machine, status):
  order = status + machine
  return order