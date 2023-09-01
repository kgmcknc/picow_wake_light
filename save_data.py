save_file_name = "./save_file.txt"
class_data_updated = 0
save_fp = 0

class save_data_class():
   ap_ssid = ''
   ap_pw = ''
   ssid_list = []
   pw_list = []
   ip_list = []
   led_red = 0
   led_green = 0
   led_blue = 0
   wake_red = 0
   wake_green = 0
   wake_blue = 0
   sleep_red = 0
   sleep_green = 0
   sleep_blue = 0
   hour_offset = 0
   wakesunday = []
   wakemonday = []
   waketuesday = []
   wakewednesday = []
   wakethursday = []
   wakefriday = []
   wakesaturday = []
   
   def __init__(self):
      self.init_class_from_save_file()

   def init_class_from_save_file(self):
      open_error = 0
      try:
         self.read_save_file()
      except:
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

      save_fp = open(save_file_name, "rt")
      file_data = save_fp.read()
      save_fp.close()
      file_lines = file_data.splitlines()
      class_vars = self.get_class_var_list()
      for line in file_lines:
         item = line.split(":", 1)
         if(item[0] in class_vars):
            if(len(item) > 1):
               if(item[1][0] == '['):
                  if(item[1] == '[]'):
                     list_data = []
                  else:
                     list_data = item[1].strip('][').split(',')
                  setattr(self, item[0], list_data)
               else:
                  setattr(self, item[0], int(item[1]))
      new_list = self.save_class_to_text_list()
      if(file_lines != new_list):
         print("save file doesn't match class...rewriting save file")
         self.rewrite_save_file()

   def save_class_to_text_list(self):
      text_list = []
      class_vars = self.get_class_var_list()
      for class_var in class_vars:
         data = getattr(self, class_var)
         # if(data == ''):
         #    data = '\'\''
         new_line = f"""{class_var}:{data}"""
         text_list.append(new_line)
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