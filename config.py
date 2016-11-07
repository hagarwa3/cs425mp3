
target_machines = [
  'fa16-cs425-g22-01.cs.illinois.edu',
  'fa16-cs425-g22-02.cs.illinois.edu',
  'fa16-cs425-g22-03.cs.illinois.edu',
  'fa16-cs425-g22-04.cs.illinois.edu',
  'fa16-cs425-g22-05.cs.illinois.edu',
  'fa16-cs425-g22-06.cs.illinois.edu',
  'fa16-cs425-g22-07.cs.illinois.edu',
  'fa16-cs425-g22-08.cs.illinois.edu',
  'fa16-cs425-g22-09.cs.illinois.edu',
  'fa16-cs425-g22-10.cs.illinois.edu'
]
'''

target_machines = [
  'wirelessprv-10-193-165-145.near.illinois.edu'
]
'''

introducer_port = 57500
disseminator_port = 57501
detector_port = 57502
listener_port = 57503

ping_message = 'p'

# String that will be sent as the ack
execution_ack_string = "ack\r\n"

# This is the number of characters that represent the length of the command.
arg_length_size = 4 

# This is the machine that will be our introducer
introducer_hostname = 'fa16-cs425-g22-01.cs.illinois.edu'
#ntroducer_hostname = 'wirelessprv-10-193-165-145.near.illinois.edu'

# Creates a string of predefined size containing the length of socket message.
def length_padder(length):
  length = str(length)
  length_string = '0'*(arg_length_size-len(length)) + length
  return length_string
