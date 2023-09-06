import time
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
         start_time = wake_item["start_time"]
         end_time = wake_item["end_time"]
         start_time_decimal = int(start_time[0]) + (int(start_time[1])/100)
         end_time_decimal = int(end_time[0]) + (int(end_time[1])/100)
         current_time_decimal = int(current_time[0]) + (int(current_time[1])/100)
         if(current_time_decimal >= start_time_decimal):
            if(current_time_decimal <= end_time_decimal):
               self.wake_time = True
               return True
      self.wake_time = False
      return False
   
   def get_day_list(self, day):
      if(isinstance(day, str)):
         if(day.lower() == "monday"):
            return self.wake_monday
         if(day.lower() == "tuesday"):
            return self.wake_tuesday
         if(day.lower() == "wednesday"):
            return self.wake_wednesday
         if(day.lower() == "thursday"):
            return self.wake_thursday
         if(day.lower() == "friday"):
            return self.wake_friday
         if(day.lower() == "saturday"):
            return self.wake_saturday
         if(day.lower() == "sunday"):
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
      rem_start_time = wake_time["start_time"]
      rem_end_time = wake_time["end_time"]
      rem_start_time_decimal = rem_start_time[0] + (rem_start_time[1]/100)
      rem_end_time_decimal = rem_end_time[0] + (rem_end_time[1]/100)
      for wake_item in day_list:
         start_time = wake_item["start_time"]
         end_time = wake_item["end_time"]
         start_time_decimal = start_time[0] + (start_time[1]/100)
         end_time_decimal = end_time[0] + (end_time[1]/100)

         if(start_time_decimal >= rem_start_time_decimal):
            if(end_time_decimal <= rem_end_time_decimal):
               continue
            else:
               wake_time["start_time"] = rem_end_time
               wake_time["end_time"] = end_time
         else:
            if(end_time_decimal <= rem_end_time_decimal):
               wake_time["start_time"] = start_time
               wake_time["end_time"] = rem_start_time
            else:
               wake_time["start_time"] = start_time
               wake_time["end_time"] = rem_start_time
               day_list_copy.append(wake_item)
               wake_time["start_time"] = rem_end_time
               wake_time["end_time"] = end_time
      self.add_wake_time(day, day_list_copy)
   
   def reorder_wake_time(self, day):
      # get day
      # iterate through day list and split with ":" getting start and end numbers
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
      current_time = time.localtime()
      return (current_time[3], current_time[4])
      # convert hour/day as needed