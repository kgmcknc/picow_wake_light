import time
import ntptime

last_second_check = 0

class wake_times_class():
   wake_sunday = []
   wake_monday = []
   wake_tuesday = []
   wake_wednesday = []
   wake_thursday = []
   wake_friday = []
   wake_saturday = []

   def __init__(self):
      self.wake_sunday = []
      self.wake_monday = []
      self.wake_tuesday = []
      self.wake_wednesday = []
      self.wake_thursday = []
      self.wake_friday = []
      self.wake_saturday = []
   
   def check_wake_time(self, day, current_time):
      pass
   
   def get_day_from_string(self, day_string):
      pass

   def set_wake_time(self, day, wake_time):
      pass

   def clear_wake_times(self, day):
      pass

   def add_wake_time(self, day, wake_time):
      pass

   def remove_wake_time(self, day, wake_time):
      pass

   def reorder_wake_time(self, day):
      pass

class time_class():
   time_locked = False
   hour_offset = 0
   
   def __init__(self, hour_offset=None):
      if(hour_offset != None):
         self.hour_offset = hour_offset
         if(ntptime.host == None):
            print("Fixing ntp time host")
            ntptime.host = 'pool.ntp.org'
         if(ntptime.timeout != 1):
            print("Fixing ntp timeout")
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

   def get_weekday(self):
      current_time = time.localtime()
      day_num = current_time[6]
      if(day_num == 0):
         return "Monday"
      if(day_num == 1):
         return "Tuesday"
      if(day_num == 2):
         return "Wednesday"
      if(day_num == 3):
         return "Thursday"
      if(day_num == 4):
         return "Friday"
      if(day_num == 5):
         return "Saturday"
      if(day_num == 6):
         return "Sunday"
   
   def get_local_time(self):
      time.localtime()
      # convert hour/day as needed