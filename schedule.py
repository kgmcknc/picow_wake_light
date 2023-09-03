import time
import ntptime

last_second_check = 0

class time_class():
   time_locked = False
   hour_offset = 0
   
   def __init__(self, hour_offset=None):
      if(hour_offset != None):
         self.hour_offset = hour_offset
         if(ntptime.host == None):
            ntptime.host = 'pool.ntp.org'
         if(ntptime.timeout != 1):
            ntptime.timeout = 1

   def get_network_time(self):
      global last_second_check
      current_time = time.localtime()
      if(current_time[5] == last_second_check):
         return
      try:
         time.localtime()
         ntptime.settime()
         self.time_locked = True
      except Exception as e:
         print(e)
         self.time_locked = False
      if(self.time_locked == True):
         print("Locked Time:", time.localtime())
      else:
         print("Unlocked Time:", time.localtime())
      current_time = time.localtime()
      last_second_check = current_time[5]
   
   def get_local_time(self):
      time.localtime()
      # convert hour/day as needed