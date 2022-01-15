apps=['patients']
import os
def getMigrations():
   migrations=[]
   for app in apps:
        for i in os.listdir(os.path.join(app,'migrations')):
            if os.path.isfile(os.path.join(app,'migrations',i)) and i.endswith('.py') and not i =='__init__.py':
                migrations.append('.'.join([app,'migrations',i[:-3]]))
   print(migrations)
