import time
import ntptime

class time_class():
   time_locked = False
   hour_offset = 0

   def __init__(self, hour_offset=None):
      if(hour_offset != None):
         self.hour_offset = hour_offset
      self.get_network_time()

   def get_network_time(self):
      try:
         ntptime.settime()
      except:
         self.time_locked = False
      self.time_locked = True
      print(time.localtime())
   
   def get_local_time(self):
      time.localtime()
      # convert hour/day as needed