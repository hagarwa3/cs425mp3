import errno
import multiprocessing
import select
import socket
import struct
import time

from disseminator import *
from config import *

class detector():

  def __init__(self, member_list=[]):
    self.member_list = member_list
    self.name = socket.gethostbyname(socket.gethostname())

  def re_join_group(self):
    print("Attempting to rejoin: false positive failure")
    join_request = length_padder(len(ping_message)) + ping_message
    introducer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    introducer.connect((introducer_hostname, introducer_port))
    introducer.close()

  def get_neighbours(self):
    index = None
    try:
      index = self.member_list.index(self.name)
    except:
      self.re_join_group()
      return set(self.member_list)
    if (len(self.member_list) < 4):
      neighbours = set(self.member_list)
      #neighbours.remove(self.name)
      return neighbours
    neighbours = set()
    nn = len(member_list)
    neighbours.add(self.member_list[(index-2)%nn])
    neighbours.add(self.member_list[(index-1)%nn])
    neighbours.add(self.member_list[(index+1)%nn])
    neighbours.add(self.member_list[(index+2)%nn])
    return neighbours

  def ping_neighbours(self):
    print(self.member_list)
    ping_order = length_padder(len(ping_message)) + ping_message
    neighbours = self.get_neighbours()
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setblocking(False)
    for neighbour in neighbours:
      # Ping the neighbour's listener
      neighbour_address = (neighbour, listener_port)
      sent_bytes = udp_socket.sendto(ping_message, neighbour_address)

      # Wait no more than 1 second to hear the ack
      ready = select.select([udp_socket], [], [], 1)

      # read the ack
      if (len(ready[0]) > 0):
        if (ready[0][0] is udp_socket):
          message, address = udp_socket.recvfrom(1024)
          if not (message == execution_ack_string):
            send_update(neighbour, 'r', self.member_list)

      # else this has died
      else:
        send_update(neighbour, 'r', self.member_list)

