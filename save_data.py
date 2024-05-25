import json

save_file_name = "./save_file.txt"
class_data_updated = False
save_fp = 0

class save_data_class():
   ap_ssid = ''
   ap_pw = ''
   ssid_list = []
   pw_list = []
   config_list = []
   hour_offset = 0
   led_mode = 0
   wake_led = {"blue":0,"green":0,"red":0}
   sleep_led = {"blue":0,"green":0,"red":0}
   custom_led = {"blue":0,"green":0,"red":0}
   timer_led = {"blue":0,"green":0,"red":0}
   wake_times = {"monday":[],"tuesday":[],"wednesday":[],"thursday":[],"friday":[],"saturday":[],"sunday":[]}
   off_times = {"monday":[],"tuesday":[],"wednesday":[],"thursday":[],"friday":[],"saturday":[],"sunday":[]}
   timer_end_time = 0.0
   
   def __init__(self):
      self.init_class_from_save_file()

   def init_class_from_save_file(self):
      open_error = 0
      try:
         print("Trying to read save file")
         self.read_save_file()
      except Exception as e:
         print(e)
         open_error = 1
      if(open_error == 1):
         try:
            print("Trying to create default save file")
            self.initialize_save_file()
         except Exception as e:
            print(e)
            open_error = 2
      if(open_error == 2):
         print("Couldn't initialize default save data")

   def read_save_file(self):
      global save_file_name
      global save_fp

      save_fp = open(save_file_name, "r")
      file_data = save_fp.read()
      save_fp.close()
      file_lines = file_data.splitlines()
      class_vars = self.get_class_var_list()
      for line in file_lines:
         line_data = json.loads(line)
         key_list = list(line_data.keys())
         key = key_list[0]
         if key in class_vars:
            value = line_data.get(key)
            setattr(self, key, value)
         else:
            print("Unknown File Key:", key)
      new_list = self.save_class_to_text_list()
      rewrite_file = 0
      for class_var in class_vars:
         key_found = 0
         for line in file_lines:
            line_data = json.loads(line)
            key_list = list(line_data.keys())
            key = key_list[0]
            if(key in class_var):
               key_found = 1
               break
         if(key_found == 0):
            rewrite_file = 1
      if(rewrite_file):
         print("save file doesn't match class...rewriting save file")
         self.rewrite_save_file()

   def save_class_to_text_list(self):
      text_list = []
      class_vars = self.get_class_var_list()
      for class_var in class_vars:
         new_dict = {class_var: getattr(self, class_var)}
         json_var = json.dumps(new_dict)
         text_list.append(json_var)
      return text_list

   def initialize_save_file(self):
      global save_file_name
      global save_fp

      save_fp = open(save_file_name, "x")
      text_list = self.save_class_to_text_list()
      init_text = "\n".join(text_list)
      save_fp.write(init_text)
      save_fp.close()
      print("Initialized save file")

   def rewrite_save_file(self):
      global save_fp
      save_fp = open(save_file_name, "w")
      text_list = self.save_class_to_text_list()
      new_text = "\n".join(text_list)
      save_fp.write(new_text)
      save_fp.close()

   def get_class_var_list(self):
      var_list = dir(self)
      ret_list = []
      for var in var_list:
         if(not callable(getattr(self, var)) and not var.startswith("__")):
            ret_list.append(var)
      return ret_list
   
   def sync_file(self):
      global class_data_updated
      if(class_data_updated == True):
         class_data_updated = False
         self.rewrite_save_file()
