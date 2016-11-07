import errno
import multiprocessing
import socket
import struct
import sys
import time
import threading

from config import *
from listener import *
from detector import *
from introducer import *
from user_input import *

member_list = []
keep_running = True
sdfs_local_map={}
local_sdfs_map={}
sdfs_owners={}

def listener_runner():
  global member_list, keep_running
  listening_server = listener(member_list)
  while (keep_running):
    order = listening_server.wait_for_order()
    listening_server.parse_order(order)

def detector_runner():
  global member_list, keep_running
  detective = detector(member_list)
  while (keep_running):
    time.sleep(2)
    detective.ping_neighbours()

def join_group():
  print("Requesting for introductions")
  udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  udp_socket.setblocking(False)
  introducer_address = (introducer_hostname, introducer_port)
  sent_bytes = udp_socket.sendto('j', introducer_address)

def introducer_runner():
  global member_list, keep_running
  introducer_server = introducer(member_list)
  while (keep_running):
    introducer_server.introduce()

def user_input_runner():
  global member_list, sdfs_owners_map, keep_running
  user_inputs = user_input()
  print("ready for input")
  while(keep_running):
    user_inputs.get_inputs()


def main(is_introducer=False):
  # create empty members list
  global member_list, keep_running
  keep_running = True
  member_list = []

  # start introducer thread if is_introducer
  if is_introducer:
    introducer_thread = threading.Thread(target=introducer_runner)
    introducer_thread.start()
    time.sleep(3)

  # start listener thread
  listener_thread = threading.Thread(target=listener_runner)
  listener_thread.start()

  join_group()
  
  # start detector thread
  detector_thread = threading.Thread(target=detector_runner)
  detector_thread.start()

  user_input_thread = threading.Thread(target=user_input_runner)
  user_input_thread.start()

  listener_thread.join()
  detector_thread.join()

  # join the group

if __name__ == "__main__":
  if (len(sys.argv) == 1):
    main()
  else:
    main(True)
