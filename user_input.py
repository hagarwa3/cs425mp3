import errno
import multiprocessing
import random
import socket
import struct
import time
import sys

from config import *
from disseminator import *

class user_input():

  def __init__(self, 
                member_list=[], 
                sdfs_local_map={}, 
                local_sdfs_map={},
                sdfs_owners={}):
    self.member_list = member_list
    self.name = socket.gethostbyname(socket.gethostname())
    self.sdfs_local_map = sdfs_local_map
    self.local_sdfs_map = local_sdfs_map
    self.sdfs_owners = sdfs_owners

  def get(self, sdfs_fn, local_fn):
    local_file = open(sdfs_fn, 'r')
    data = local_file.read()
    for owner in self.sdfs_owners[sdfs_fn]:
      if owner in self.member_list:
        send_update(self.name, 'g', [owner])
    local_file_w = open(local_fn, 'w')
    local_file_w.write(data)
    local_file.close()
    local_file_w.close()

  def put(self, local_fn, sdfs_fn):
    local_file = open(local_fn)
    data = local_file.read()
    o1, o2, o3 = [self.name]*3
    if (len(self.member_list) >= 3):
      o1, o2, o3 = random.sample(self.member_list, 3)
    send_update('{} {} {} {} {}'.format(sdfs_fn, o1, o2, o3, data), 'z', self.member_list)

  def delete(self, sdfs_fn):
    send_update(sdfs_fn, 'd', self.member_list)

  def ls(self, sdfs_fn):
    print(self.sdfs_owners[sdfs_fn])

  def store(self):
    for file_name in self.sdfs_owners.keys():
      if self.name in self.sdfs_owners[file_name]:
        print(file_name)

  def get_inputs(self):
    order = raw_input()
    print('got input = {}'.format(order))
    order_type = order.split()[0]
    if (order_type == "put"):
      local_fn, sdfs_fn = order.split()[1:]
      self.put(local_fn, sdfs_fn)

    elif (order_type == "get"):
      sdfs_fn, local_fn = order.split()[1:]
      self.get(sdfs_fn, local_file_w)

    elif (order_type == "delete"):
      sdfs_fn = order.split()[1]
      self.delete(sdfs_fn)

    elif (order_type == "ls"):
      sdfs_fn = order.split()[1]
      self.ls(sdfs_fn)

    elif (order_type == "store"):
      self.store()

