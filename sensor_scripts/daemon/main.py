import pause
import datetime

def round_up(x, base=5):
  return x + base if x % base == 0 else x + base - x % base

def round_base(x, base=5):
  return int(base * round(float(x)/base))

def time_overflow_correction(minute, hour):
  return (minute, hour) if minute < 59 else (minute - 59, hour + 1)
  # if minute > 59:
  #   minute -= 59
  #   hour += 1

  # return minute, hour


current_time = datetime.datetime.now()

minute, hour = time_overflow_correction(current_time.minute, current_time.hour)
minute = round_up(minute)

next_execution = datetime.datetime(current_time.year, current_time.month, current_time.day, hour, minute, 0)
# # next_execution = 'test'

print(next_execution)
counter = 5
while True:
  counter += 1 if counter < 7 else 0
  pause.until(next_execution)
  print('test')
  minute, hour = time_overflow_correction(next_execution.minute + 5, next_execution.hour)
  minute = round_base(minute)
  next_execution = datetime.datetime(next_execution.year, next_execution.month, next_execution.day, hour, minute, 0)
  print(next_execution)


# get current time
#   first time round up by 5
# pause until
# execute 'dummy' scripts
# get time + 5
# delete seconds + miliseconds, timerounder

# 2 Databases
#   detailed
#   -> 100 records per sensor per plant
#   normal
# 5 min executer
# if change < 1
#   -> execute 30min
#     -> reset counter of happend
#   -> if no such change after counter == 6
#     -> reset counter

# def roundup(x):
#   return x if x % 5 == 0 else x + 5 - x % 5

