import time
import ntptime

class time_class():
   
   def __init__(self):
      get_network_time()


def get_network_time():
   print(time.localtime())
   print(ntptime.settime())
   print(time.localtime())
