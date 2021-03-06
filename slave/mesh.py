import os
import json
import socket
import ubinascii
EXTERNAL_PORT = 4012
MULTICAST_ADDRESS = '224.0.0.1'


class MeshString(str):
  import sys

  def reverse(self):
    self = ''.join(list(reversed(self)))
    return self

  def rreplace(self, old, new, maxcount=sys.maxsize):
    """ reverse replace
        reverses string and runs replace at reversed old and new
        returns reversed reversed string
    """
    old = MeshString(old)
    new = MeshString(new)
    self = self.reverse().replace(old.reverse(), new.reverse(), maxcount)
    self = MeshString(self).reverse()
    return self


class MeshTools:
  def __init__(self):
    pass

  def random_string(self, length, digits=False, custom=''):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabet += '0123456789' if digits is True else ''
    alphabet += custom

    output = ''
    for _ in range(0, length):
      pointer = len(alphabet)
      while pointer >= len(alphabet):
        pointer = int(ubinascii.hexlify(os.urandom(1)), 16)
      output += alphabet[pointer]

    return output


class MeshNetwork(object):
  """ response daemon for mesh network """

  def __init__(self):
    import network
    sta_if = network.WLAN(network.STA_IF)
    self.IP = sta_if.ifconfig()[0]

  def verification(self, message, received):
    passthrough = False
    raw = received[0]

    if (raw[0] != '<' or
        raw[-1] != '>' or
        len(message) != 6 or
        len(message[1]) != 2 or
        len(message[2]) != 2 or
        len(message[3]) != 1 or
        len(message[4]) != 4 or
        len(str(message[3][0])) != 5 or
        not str(message[3][0]).isdigit() or
        message[0] not in [0, 1] or
        message[0] != message[5] or
        not str(message[2][0]).isdigit() or
        message[2][0] > 255):

      print('potential spoofing attack - no valid package')
      return False

    if 'config.json' in os.listdir():
      with open('config.json', 'r') as out:
        config = json.loads(out.read())

      if config['master']['uuid'] == message[1][0] and config['master']['ip'] == received[1][0]:
        passthrough = True
      elif str(message[3][0])[0] in ['4', '6']:
        passthrough = True

    return passthrough

  def daemon_process(self, received):
    message = received[0].decode('utf-8')
    print('received following package: \n' + message)
    message = message.replace('<', '[').replace('>', ']')
    message = eval(message)

    passthrough = self.verification(message, received)
    if self.IP != received[1][0] and passthrough:
      code = str(message[3][0])
      if code[0] == '1':
        if int(code[1:3]) == 1:
          target = [message[1][0], received[1][0]]
          self.alive(target, 2, additional_information=message[4][0])
      elif code[0] == '2':
        target = [message[1][0], received[1][0]]
        self.slave(mode=int(code[1:3]) + 1, target=target, messages=message[4])
      elif code[0] == '4':
        if int(code[1:3]) == 1:
          self.discover(target=[message[1][0], received[1][0]], mode=2)
      elif code[0] == '6':
        target = [message[1][0], received[1][0]]
        local = message[2][1]
        self.register_lite(mode=int(code[1:3]) + 1, target=target, messages=message[4], local=local)
      elif code[0] == '7':
        target = [message[1][0], received[1][0]]
        self.slave_update(mode=int(code[1:3]), sub=int(code[3:]) + 1, target=target, messages=message[4])
      elif code[0] == '8':
        target = [message[1][0], received[1][0]]
        self.remove(int(code[1:3]), int(code[3:]) + 1, target, messages=message[4])
    else:
      print('not processing request - same ip')

  def ip32bit(self, target):
    import ustruct
    return ustruct.pack('4B', *(int(x) for x in target.split('.')))

  def daemon(self):
    print('started')
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = EXTERNAL_PORT

    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    client.bind(('', port))
    while True:
      try:
        received = client.recvfrom(2048)
        self.daemon_process(received)
      except KeyboardInterrupt:
        break
      except Exception as e:
        print(e)

  def send_local(self, mode, code, port=2311):
    """ method for communication between daemon and other scripts """
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sender.sendto(str([mode, code]).encode(), ('127.0.0.1', port))
    sender.close()

  def send(self, code, plant=True, messages=[], master=False, priority=255,
           recipient=None, multicast=False, no_database=False, local_uuid=None):
    """ main method for sending information in the mesh_network
        code - 5 digit number for mode
        plant - optional (origin, plant object)
        messages - 4len array with additional information to be sended
                  -> auto cut to 4 existing
        master - mode of sended information - currently only Master supportet
        priority - 0-255 higher mor priority (not implemented fully yet)
        recipient - [str with UUID, ip] or peewee plant object or None if multicast
        multicast - sending with multicast
        no_database - function does not use database
    """
    configured = plant
    if configured and 'config.json' in os.listdir():
      with open('config.json') as out:
        plant = json.loads(out.read())
    else:
      configured = False

    if type(recipient) == list:
      recipient_uuid = recipient[0]
      external_address = recipient[1]
    elif recipient is None:
      recipient_uuid = ''
      external_address = ''
    else:
      recipient_uuid = str(recipient.uuid)
      external_address = recipient.ip

    len_message = len(messages)
    [messages.append('') for _ in range(0, 4 - len_message) if len_message < 4]
    [messages.pop() for _ in range(0, len_message - 4) if len_message > 4]

    messages = [x if x != '' else '-' * 256 for x in messages]

    master = int(master)
    package = [master, [], [], [], [], master]

    if configured:
      package[1].append(plant['uuid'])
    elif local_uuid is not None:
      package[1].append(local_uuid)
    else:
      package[1].append('')

    package[1].append('')

    package[2].append(priority)
    package[2].append(recipient_uuid)
    package[3].append(code)
    package[4] = messages

    package = '<' + repr(package)[1:-1] + '>'
    # package = repr(package).replace('[', '<', 1)
    # package = MeshString(package).rreplace(']', '>', 1).encode('utf-8')
    print('sending following package: \n' + package)
    package = package.encode()

    if multicast is False:
      print('package destination: ' + external_address)
      address = external_address
      sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
      print('package destination: multicast ({})'.format(MULTICAST_ADDRESS))
      address = MULTICAST_ADDRESS
      sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
      sender.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    sender.sendto(package, (address, EXTERNAL_PORT))

    sender.close()

  def alive(self, target, mode=1, additional_information=''):
    if mode > 2:
      raise ValueError('invalid mode')

    if mode == 1:
      code = 10100
    elif mode == 2:
      code = 10200

    self.send(code, recipient=target, messages=[additional_information])

  def discover(self, target=None, mode=1):
    """ if mode is 1 - target == peewee plant object
        if mode is 2 - target == list [UUID, IP]
    """
    if mode == 1:
      print('not supported in slave module')
    elif mode == 2:
      if 'config.json' not in os.listdir():
        print('discovered - slave not registered')
        code = 40400
        self.send(code, plant=False, recipient=target, messages=['NOT_LOGGED', 'NOT_CONFIGURED', 'SLAVE'])
      else:
        print('discovered - slave registered')
        code = 40500
        self.send(code, recipient=target, messages=['NOT_LOGGED', 'CONFIGURED', 'SLAVE'])

  def slave(self, target=None, mode=2, messages=[]):
    print(target)
    print(messages)
    print(mode)

    if mode != 2:
      print('mode not supported')
    else:
      if 'config.json' in os.listdir():
        with open('config.json', 'r') as out:
          config = json.loads(out.read())
        print(config)

        if target[0] == config['master']['uuid']:
          code = 20200

          if messages[0] == 'moisture':
            from sensor import measure
            current = measure()

            self.send(code, recipient=target, messages=[current, messages[0]])

  def register_lite(self, target=None, mode=1, messages=[], local=None):
    if mode == 2:
      if 'config.json' not in os.listdir():
        code = 60200
        self.send(code, recipient=target, plant=False, local_uuid=local)
    elif mode == 4:
      code = 60400
      with open('config.json', 'w') as out:
        out.write(json.dumps({'uuid': messages[2],
                              'master': {
                                  'ip': messages[1],
                                  'uuid': messages[0]}
                              }))
      self.send(code, recipient=target)

  def slave_update(self, mode=1, sub=1, target=None, messages=[]):
    if mode > 3:
      print('mode currently not supported')
    elif mode in [1, 3]:
      if sub != 2:
        print('not supported sub mode')
      elif sub == 2:
        entry = 'sleep' if mode == 1 else 'range'
        raw = 70002
        code = raw + (mode * 100)

        with open('config.json', 'r') as out:
          config = json.loads(out.read())
          config[entry] = {}
          config[entry]['min'] = messages[0]
          config[entry]['max'] = messages[1]

        with open('config.json', 'w') as out:
          out.write(json.dumps(config))

        self.send(code, recipient=target)
    elif mode in [2]:
      if sub != 2:
        print('not supported sub mode')
      else:
        code = 70202

        with open('config.json', 'r') as out:
          config = json.loads(out.read())

        if config['master']['uuid'] == target[0] and config['master']['ip'] == target[1]:
          config['master']['uuid'] = messages[0]
          config['master']['ip'] = messages[1]

          with open('config.json', 'w') as out:
            out.write(json.dumps(config))

          self.send(code, recipient=target)

          import machine
          machine.reset()
    elif mode in [4]:
      if sub != 2:
        print('not supported sub mode')
      else:
        code = 70402

        with open('config.json', 'r') as out:
          config = json.loads(out.read())

        if config['master']['uuid'] == target[0]:
          changed = True if config['master']['ip'] != target[1] else False
          config['master']['ip'] = target[1]

          with open('config.json', 'w') as out:
            out.write(json.dumps(config))

          self.send(code, recipient=target, messages=[changed])

  def remove(self, mode, sub, target, messages=[]):
    if mode == 2:
      if sub == 2:
        with open('config.json', 'r') as out:
          config = json.loads(out.read())

        print(target)
        if config['master']['ip'] == target[1] and config['master']['uuid'] == target[0]:
          token = MeshTools().random_string(100)
          information = {'token': token}

          with open('transaction.json', 'w') as out:
            out.write(json.dumps(information))

          self.send(80202, recipient=target, messages=[token])

      elif sub == 4:
        with open('config.json', 'r') as out:
          config = json.loads(out.read())

        with open('transaction.json', 'r') as out:
          information = json.loads(out.read())

        if config['master']['ip'] == target[1] and config['master']['uuid'] == target[0] and information['token'] == messages[0]:
          information['mode'] = 'remove'

          with open('transaction.json', 'w') as out:
            out.write(json.dumps(information))

          self.send(80204, recipient=target)

      elif sub == 6:
        with open('config.json', 'r') as out:
          config = json.loads(out.read())

        with open('transaction.json', 'r') as out:
          information = json.loads(out.read())

        if config['master']['ip'] == target[1] and config['master']['uuid'] == target[0] and information['token'] == messages[0]:
          information['token'] = MeshTools().random_string(100)

          with open('transaction.json', 'w') as out:
            out.write(json.dumps(information))

          self.send(80206, recipient=target, messages=[information['token']])

      elif sub == 8:
        with open('config.json', 'r') as out:
          config = json.loads(out.read())

        with open('transaction.json', 'r') as out:
          information = json.loads(out.read())

        if config['master']['ip'] == target[1] and config['master']['uuid'] == target[0] and information['token'] == messages[0]:
          import machine
          import os

          os.remove('config.json')
          os.remove('credentials.json')
          os.remove('transaction.json')
          machine.reset()

          self.send(80208, recipient=target)


if __name__ == '__main__':
  MeshNetwork().daemon()
