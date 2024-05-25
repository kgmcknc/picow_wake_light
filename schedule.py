import time
import ntptime

last_second_check = 0

class wake_times_class():
   wake_time = False

   wake_times = {"monday":[],"tuesday":[],"wednesday":[],"thursday":[],"friday":[],"saturday":[],"sunday":[]}
   off_times = {"monday":[],"tuesday":[],"wednesday":[],"thursday":[],"friday":[],"saturday":[],"sunday":[]}

   def __init__(self):
      self.wake_time = False
   
   def check_wake_time(self, day, current_time):
      day_list = self.get_day_list(self.wake_times, day)
      if(day_list == None):
         return
      for day_item in day_list:
         start_time = day_item["start_time"]
         end_time = day_item["end_time"]
         start_time_decimal = int(start_time[0]) + (int(start_time[1])/100)
         end_time_decimal = int(end_time[0]) + (int(end_time[1])/100)
         current_time_decimal = int(current_time[0]) + (int(current_time[1])/100)
         if(current_time_decimal >= start_time_decimal):
            if(current_time_decimal <= end_time_decimal):
               self.wake_time = True
               return True
      self.wake_time = False
      return False
   
   def check_off_time(self, day, current_time):
      day_list = self.get_day_list(self.off_times, day)
      if(day_list == None):
         return
      for day_item in day_list:
         start_time = day_item["start_time"]
         end_time = day_item["end_time"]
         start_time_decimal = int(start_time[0]) + (int(start_time[1])/100)
         end_time_decimal = int(end_time[0]) + (int(end_time[1])/100)
         current_time_decimal = int(current_time[0]) + (int(current_time[1])/100)
         if(current_time_decimal >= start_time_decimal):
            if(current_time_decimal <= end_time_decimal):
               self.wake_time = True
               return True
      self.wake_time = False
      return False
   
   def get_day_list(self, day_list, day):
      if(isinstance(day, str)):
         if(day.lower() == "monday"):
            return day_list["monday"]
         if(day.lower() == "tuesday"):
            return day_list["tuesday"]
         if(day.lower() == "wednesday"):
            return day_list["wednesday"]
         if(day.lower() == "thursday"):
            return day_list["thursday"]
         if(day.lower() == "friday"):
            return day_list["friday"]
         if(day.lower() == "saturday"):
            return day_list["saturday"]
         if(day.lower() == "sunday"):
            return day_list["sunday"]
      else:
         if(day == 0):
            return day_list["monday"]
         if(day == 1):
            return day_list["tuesday"]
         if(day == 2):
            return day_list["wednesday"]
         if(day == 3):
            return day_list["thursday"]
         if(day == 4):
            return day_list["friday"]
         if(day == 5):
            return day_list["saturday"]
         if(day == 6):
            return day_list["sunday"]
      return None

   def set_wake_time(self, day, wake_time):
      self.clear_wake_times(day)
      self.add_wake_time(day, wake_time)

   def clear_wake_times(self, day):
      day_list = self.get_day_list(self.wake_times, day)
      if(day_list == None):
         return
      day_list.clear()

   def add_wake_time(self, day, wake_time):
      day_list = self.get_day_list(self.wake_times, day)
      if(day_list == None):
         return
      for time_item in wake_time:
         day_list.append(time_item)
      self.reorder_wake_time(day_list)

   def remove_wake_time(self, day, wake_time):
      day_list = self.get_day_list(self.wake_times, day)
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

   def set_off_time(self, day, off_time):
      self.clear_off_times(day)
      self.add_off_time(day, off_time)

   def clear_off_times(self, day):
      day_list = self.get_day_list(self.off_times, day)
      if(day_list == None):
         return
      day_list.clear()

   def add_off_time(self, day, off_time):
      day_list = self.get_day_list(self.off_times, day)
      if(day_list == None):
         return
      for time_item in off_time:
         day_list.append(time_item)
      self.reorder_off_time(day_list)

   def remove_off_time(self, day, off_time):
      day_list = self.get_day_list(self.off_times, day)
      if(day_list == None):
         return
      day_list_copy = day_list.copy()
      self.clear_wake_times(day)
      rem_start_time = off_time["start_time"]
      rem_end_time = off_time["end_time"]
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
               off_time["start_time"] = rem_end_time
               off_time["end_time"] = end_time
         else:
            if(end_time_decimal <= rem_end_time_decimal):
               off_time["start_time"] = start_time
               off_time["end_time"] = rem_start_time
            else:
               off_time["start_time"] = start_time
               off_time["end_time"] = rem_start_time
               day_list_copy.append(wake_item)
               off_time["start_time"] = rem_end_time
               off_time["end_time"] = end_time
      self.add_off_time(day, day_list_copy)
   
   def reorder_wake_time(self, day):
      # get day
      # iterate through day list and split with ":" getting start and end numbers
      # add all start numbers to a "Start" list and add all end numbers to an "end" list
      # iterate through the start and end list and create new ranges encompasing all the values
      pass

   def reorder_off_time(self, day):
      # get day
      # iterate through day list and split with ":" getting start and end numbers
      # add all start numbers to a "Start" list and add all end numbers to an "end" list
      # iterate through the start and end list and create new ranges encompasing all the values
      pass

class time_class():
   time_locked = False
   hour_offset = 0
   timer_active = False
   timer_end_time = 0.0
   
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

   def set_hour_offset(self, hour_offset):
      self.hour_offset = hour_offset

   def get_weekday(self):
      current_time = time.localtime()
      day_num = current_time[6]
      hour_num = current_time[3] - self.hour_offset
      # adjust hour if needed
      if(hour_num > 23):
         hour_num = hour_num - 24
         day_num = day_num + 1
      if(hour_num < 0):
         hour_num = hour_num + 24
         day_num = day_num - 1
      # adjust day if needed
      if(day_num > 6):
         day_num = day_num - 7
      if(day_num < 0):
         day_num = day_num + 7
      # return day number
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
      current_min = current_time[4]
      current_hour = current_time[3] - self.hour_offset
      # adjust hour if needed
      if(current_hour > 23):
         current_hour = current_hour - 24
      if(current_hour < 0):
         current_hour = current_hour + 24
      return (current_hour, current_min)
   
   def check_timer(self):
      current_time = time.localtime()
      current_time_int = time.mktime(current_time)
      if(self.timer_end_time == 0.0):
         self.timer_active = False
      else:
         if(current_time_int < self.timer_end_time):
            self.timer_active = True
         else:
            self.timer_end_time = 0.0
            self.timer_active = False
   
   def set_timer(self, timer_time):
      current_time = time.localtime()
      timer_hour = int(timer_time[0])
      timer_minute = int(timer_time[1])
      timer_second = int(timer_time[2])
      end_time = (current_time[0], current_time[1], current_time[2], current_time[3]+timer_hour, current_time[4]+timer_minute, current_time[5]+timer_second, current_time[6], current_time[7])
      self.timer_end_time = time.mktime(end_time)
      self.timer_active = True

   def clear_timer(self):
      self.timer_end_time = 0.0
      self.timer_active = False

   def get_timer_status(self):
      if(self.timer_active == True):
         current_time = time.localtime()
         current_time_int = time.mktime(current_time)
         timer_remaining = self.timer_end_time - current_time_int
         remaining_hours = int(timer_remaining / 3600)
         timer_remaining = timer_remaining - (remaining_hours*3600)
         remaining_minutes = int(timer_remaining / 60)
         timer_remaining = timer_remaining - (remaining_minutes*60)
         remaining_seconds = int(timer_remaining)
         return (remaining_hours, remaining_minutes, remaining_seconds)
      else:
         return (0,0,0)

