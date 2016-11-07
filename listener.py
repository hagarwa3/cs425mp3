import errno
import multiprocessing
import socket
import struct
import time

from config import *

class listener():

  def __init__(self, 
                member_list=[], 
                sdfs_local_map={}, 
                local_sdfs_map={},
                sdfs_owners={}):
    self.member_list = member_list
    self.name = socket.gethostbyname(socket.gethostname())
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.server_socket.bind((socket.gethostname(), listener_port))
    self.sdfs_local_map = sdfs_local_map
    self.local_sdfs_map = local_sdfs_map
    self.sdfs_owners = sdfs_owners

  def wait_for_order(self):
    # print("Listening for updates on:")
    # print("host:{} port:{}".format(socket.gethostname(), listener_port))
    update, updater_address = self.server_socket.recvfrom(4096)
    #print("Update from {}: {}".format(updater_address, update))
    self.server_socket.sendto(execution_ack_string, updater_address)
    return update

  def parse_order(self, order):

    # simple ping
    if (order == ping_message):
      return

    # Add a machine to the member list
    elif (order[0] == 'a'):
      joiner_address = order[1:]
      if joiner_address in self.member_list:
        return
      else:
        print ("Join - {}".format(joiner_address))
        self.member_list.append(joiner_address)
        self.member_list.sort()

    # Remove a machine from the member list
    elif (order[0] == 'r'):
      leaver_address = order[1:]
      if leaver_address in self.member_list:
        print ("Fail - {}".format(leaver_address))
        self.member_list.remove(leaver_address)
        self.member_list.sort()
      else:
        return

    # Remove a machine from the member list
    elif (order[0] == 'l'):
      leaver_address = order[1:]
      if leaver_address in self.member_list:
        print ("Leave - {}".format(leaver_address))
        self.member_list.remove(leaver_address)
        self.member_list.sort()
      else:
        return

    # Respond to a PUT
    elif(order[0] == 'z'):
      order_details = order[1:]
      sdfs_fn, o1, o2, o3, data = order_details.split()
      owners = [o1, o2, o3]
      self.sdfs_owners[sdfs_fn] = owners
      local_file = open(sdfs_fn, 'w')
      local_file.write(data)
      local_file.close()

    # Respond to a delete request
    elif(order[0] == 'd'):
      sdfs_fn = order[1:]
      local_fn = sdfs_local_map[sdfs_fn]
      sdfs_local_map.pop(sdfs_fn, None)
      sdfs_owners.pop(sdfs_fn, None)
      local_sdfs_map.pop(local_fn, None)



