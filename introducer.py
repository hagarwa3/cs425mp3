import errno
import multiprocessing
import socket
import struct
import time

from config import *
from disseminator import *

introducer_server = None

class introducer():

  # Initializes an introducer object
  def __init__(self, member_list=[]):
    self.member_list = member_list
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.server_socket.bind((socket.gethostname(), introducer_port))

  def wait_for_join(self):
    print("Introducer waiting for order on")
    print("host:{} port:{}".format(socket.gethostname(), introducer_port))
    message, joiner_address = self.server_socket.recvfrom(4096)

    print("{} requested to be introduced".format(joiner_address))
    return joiner_address

  def send_state(self, joiner_address):
    for member in self.member_list:
      send_update(member, 'a', [joiner_address])

  def introduce(self):
    joiner_address = self.wait_for_join()
    self.member_list.append(joiner_address[0])
    send_update(joiner_address[0], 'a', self.member_list)
    print("Intros sent to {}".format(self.member_list))
    self.send_state(joiner_address[0])

  def shutdown(self):
    self.server_socket.close()

def main():
  global introducer_server
  introducer_server = introducer()
  while (True):
    joiner_address = introducer_server.wait_for_join()
    # TODO Send this joiner to all the members
