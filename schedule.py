import time
import datetime
import ntptime

last_second_check = 0

class wake_times_class():
   wake_time = False
   wake_monday = []
   wake_tuesday = []
   wake_wednesday = []
   wake_thursday = []
   wake_friday = []
   wake_saturday = []
   wake_sunday = []

   def __init__(self):
      self.wake_time = False
      self.wake_monday = []
      self.wake_tuesday = []
      self.wake_wednesday = []
      self.wake_thursday = []
      self.wake_friday = []
      self.wake_saturday = []
      self.wake_sunday = []
   
   def check_wake_time(self, day, current_time):
      day_list = self.get_day_list(day)
      if(day_list == None):
         return
      for wake_item in day_list:
         times = wake_item.split(":")
         start_time = tuple(times[0])
         end_time = tuple(times[1])
         if(current_time[0] >= start_time[0] and current_time[1] >= start_time[1]):
            if(current_time[0] <= end_time[0] and current_time[1] <= end_time[1]):
               self.wake_time = True
               return True
      self.wake_time = False
      return False
   
   def get_day_list(self, day):
      if(isinstance(day, str)):
         if(day == "Monday"):
            return self.wake_monday
         if(day == "Tuesday"):
            return self.wake_tuesday
         if(day == "Wednesday"):
            return self.wake_wednesday
         if(day == "Thursday"):
            return self.wake_thursday
         if(day == "Friday"):
            return self.wake_friday
         if(day == "Saturday"):
            return self.wake_saturday
         if(day == "Sunday"):
            return self.wake_sunday
      else:
         if(day == 0):
            return self.wake_monday
         if(day == 1):
            return self.wake_tuesday
         if(day == 2):
            return self.wake_wednesday
         if(day == 3):
            return self.wake_thursday
         if(day == 4):
            return self.wake_friday
         if(day == 5):
            return self.wake_saturday
         if(day == 6):
            return self.wake_sunday
      return None

   def set_wake_time(self, day, wake_time):
      self.clear_wake_times(day)
      self.add_wake_time(day, wake_time)

   def clear_wake_times(self, day):
      day_list = self.get_day_list(day)
      if(day_list == None):
         return
      day_list.clear()

   def add_wake_time(self, day, wake_time):
      day_list = self.get_day_list(day)
      if(day_list == None):
         return
      for time_item in wake_time:
         day_list.append(time_item)
      self.reorder_wake_time(day_list)

   def remove_wake_time(self, day, wake_time):
      day_list = self.get_day_list(day)
      if(day_list == None):
         return
      day_list_copy = day_list.copy()
      self.clear_wake_times(day)
      rem_times = wake_time.split(":")
      rem_start_time = tuple(rem_times[0])
      rem_end_time = tuple(rem_times[1])
      for wake_item in day_list:
         if(wake_item == wake_time):
            # don't add item to be removed to the new list
            continue

         # NEED TO FINISH THIS!!
         times = wake_item.split(":")
         start_time = tuple(times[0])
         end_time = tuple(times[1])
         if(rem_start_time == start_time):
            pass
         if(rem_start_time[0] >= start_time[0] and rem_start_time[1] >= start_time[1]):
            if(rem_end_time[0] <= end_time[0] and rem_end_time[1] <= end_time[1]):
               # this will be two new list items
               pass
            else:
               day_list_copy.append(wake_item)
         else:
            day_list_copy.append(wake_item)
   
   def add_time_tuple(self, time_tuple):
      hours = time_tuple(0)
      mins = time_tuple(1)
      mins = mins + 1
      if(mins >= 60):
         mins = 0
         hours = hours + 1
      if(hours == 24):
         hours = 23
         mins = 59
      return (hours, mins)

   def reorder_wake_time(self, day):
      #get day
      #iterate through day list and split with ":" getting start and end numbers
      # add all start numbers to a "Start" list and add all end numbers to an "end" list
      # iterate through the start and end list and create new ranges encompasing all the values
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