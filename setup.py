import socket

from models.plant import Plant
from models.plant import Person
from models.sensor import Sensor
from models.sensor import SensorHardware, SensorHardwareConnector

print('Welcome to the configuration of IoP')
if Plant.select().count() == 0:
  print('CREATE FIRST PLANT: \n\n')
  plant = Plant()
  plant.name = input('How do you want to call your first plant? ').lower()
  plant.location = input('The location? ').lower()
  plant.species = input('The species? ').lower()

  def interval():
    int_interval = input('emailing interval? (int) ')

    if int_interval.isdigit() is True:
      return int(int_interval)
    else:
      return interval()

  plant.interval = interval()

  person = Person()
  print('\nto:')
  person.name = input('     Name: ')
  person.email = input('    Email: ')
  person.wizard = True
  person.save()
  print('\n')

  plant.person = person

  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("gmail.com", 80))

  plant.ip = s.getsockname()[0]
  plant.localhost = True

  s.close()

  plant.sat_streak = 0
  plant.save()
  input('Plant setup finished! Continue? (if not ^C)\n')


def model(sensor):
  model_str = input('model: ')

  if sensor == 'temperature' or sensor == 'humidity':
    if model_str != 'DHT22' and model_str != 'DHT11':
      print('temperature valid values - DHT11 and DHT22, pls try again\n')
      model(sensor)

  return model_str

for sensor in ['temperature', 'light', 'humidity', 'moisture']:
  if Sensor.select().where(Sensor.name == sensor).count() == 0:
    print('\n\nCREATE {}: \n\n'.format(sensor.upper()))
    db_sensor = Sensor()
    db_sensor.name = sensor
    db_sensor.model = model(sensor)
    db_sensor.unit = input('unit (only for display) ')
    db_sensor.min_value = input('minimum value? ')
    db_sensor.max_value = input('maximum value? ')
    db_sensor.persistant_offset = input('to persistant offset? ')

    db_sensor.save()

if SensorHardware.select().count() == 0:
  print('doing some other stuff')
  all_sensors = ['temperature', 'light', 'humidity', 'moisture']
  hardware_collection = {'led_traffic_light': all_sensors,
                         'led_bar': ['moisture'],
                         'display': ['temperature', 'humidity'],
                         'mailer': all_sensors,
                         'water_pump': ['moisture']}

  for hardware, values in hardware_collection.items():
    current = SensorHardware(label=hardware).save()

    for sensor in values:
      sensor = Sensor.get(name=sensor)
      c = SensorHardwareConnector(hardware=current, sensor=sensor)
      c.save()
