import platform
DATABASE_NAME = '/tmp/data.db'

if platform.system() == 'Windows':
  DATABASE_NAME = 'C:\\Users\\bmahmoud\\Dropbox\\thesis\\IoP\\data.db'
elif platform.system() == 'Darwin':
  DATABASE_NAME = '/Users/admin/Dropbox/thesis/IoP/data.db'
else:
  DATABASE_NAME = '/local/db/data.db'
