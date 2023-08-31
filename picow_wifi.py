
import network
from time import sleep

class picow_ap_class():
   ap = network.WLAN(network.AP_IF)
   ap_active = False
   ap_ssid = "PICOW"
   ap_password = "picow"
   ap_gateway = '192.168.4.1' # currently can't change due to bug in picow fw
   ap_subnet_mask = '255.255.0.0'
   ap_ip_address = '192.168.4.1' # currently can't change due to bug in picow fw
   ap_dns_server = '0.0.0.0'
   
   def __init__(self, ssid=None, password=None, ip_address=None, subnet_mask=None, gateway=None, dns_server=None):
      self.configure_access_point(ssid, password, ip_address, subnet_mask, gateway, dns_server)

   def configure_access_point(self, ssid=None, password=None, ip_address=None, subnet_mask=None, gateway=None, dns_server=None):
      if(ssid != None):
         self.ap_ssid = ssid
      if(password != None):
         self.ap_password = password
      if(ip_address != None):
         self.ap_ip_address = ip_address
      if(subnet_mask != None):
         self.ap_subnet_mask = subnet_mask
      if(gateway != None):
         self.ap_gateway = gateway
      if(dns_server != None):
         self.ap_dns_server = dns_server
   
   def enable_access_point(self):
      if(self.ap_active == False):
         print("Enabling Network Access Point")
         self.ap_active = True
         self.ap.config(ssid=self.ap_ssid, password=self.ap_password)
         self.ap.ifconfig((self.ap_ip_address, self.ap_subnet_mask, self.ap_gateway, self.ap_dns_server))
         self.ap.active(True)

      while(self.ap.active() == False):
         sleep(0.5)

      self.ap.ifconfig((self.ap_ip_address, self.ap_subnet_mask, self.ap_gateway, self.ap_dns_server))
      
      print(f"Made Access Point: SSID={self.ap_ssid}, PW={self.ap_password}")
      print(self.ap)
   
   def disable_access_point(self):
      if(self.ap_active == True):
         print("Disabling Network Access Point")
         self.ap_active = False
         self.ap.active(False)
   
   def get_ap_ip_address(self):
      return self.ap_ip_address

class picow_wifi_class():
   wifi = network.WLAN(network.STA_IF)
   wifi_ready = False
   wifi_active = False
   wifi_connected = False
   wifi_ssid_select = -1 # -1 is auto, index is what index is selected
   wifi_ssid_list = []
   wifi_pw_list = []
   wifi_scan_list = []
   wifi_ip_address = ""
   wifi_auto_connect = False
   wifi_wait_for_connect = False
   wifi_connect_sleep = 1
   max_connect_count = 10
   connect_counter = 0
   # should add ip, subnet, gateway, dns lists here. empty can be '' or None and it won't  configure that setting in wifi
   
   def __init__(self, ssid=None, password=None, auto_connect=None, wait_for_connect=False, connect_sleep=None):
      self.configure_wifi(ssid=ssid, password=password, auto_connect=auto_connect, wait_for_connect=wait_for_connect, connect_sleep=connect_sleep)

   def configure_wifi(self, ssid=None, password=None, auto_connect=None, wait_for_connect=False, connect_sleep=None):
      self.add_ssid(ssid, password)
      if(auto_connect != None):
         self.wifi_auto_connect = auto_connect
      if(wait_for_connect != None):
         self.wifi_wait_for_connect = wait_for_connect
      if(connect_sleep != None):
         self.wifi_connect_sleep = connect_sleep

   def add_ssid(self, ssid=None, password=None):
      if((ssid == None) or (password == None)):
         return
      if(type(ssid) != type(password)):
         return
      if(isinstance(ssid, list) and isinstance(password, list)):
         if(len(ssid) != len(password)):
            for i in range(len(ssid)):
               self.insert_ssid(ssid[i], password[i])
      else:
         self.insert_ssid(ssid, password)

   def remove_ssid(self, ssid=None):
      if(ssid == None):
         return
      if(isinstance(ssid, list)):
         for i in range(len(ssid)):
            self.delete_ssid(ssid[i])
      else:
         self.delete_ssid(ssid)

   def insert_ssid(self, ssid, password):
      if(isinstance(ssid, str) and isinstance(password, str)):
         if(ssid in self.wifi_ssid_list):
            index = self.wifi_ssid_list.index(ssid)
            self.wifi_ssid_list[index] = password
         else:
            self.wifi_ssid_list.append(ssid)
            self.wifi_pw_list.append(password)

   def delete_ssid(self, ssid):
      if(ssid in self.wifi_ssid_list):
         self.wifi_ssid_list.remove(ssid)

   def select_ssid(self, selection):
      if(isinstance(selection,str)):
         if(selection in self.wifi_ssid_list):
            self.wifi_ssid_select = self.wifi_ssid_list.index(selection)
         else:
            if(selection == "auto"):
               self.wifi_ssid_select = -1
      if(isinstance(selection, int)):
         if(len(self.wifi_ssid_list) < selection):
            self.wifi_ssid_select = selection

   def enable_wifi(self):
      if(self.wifi_active == False):
         self.wifi.active(True)
         self.wifi_active = True
         self.wifi_connected = False
      self.wifi_connect_counter = 0
      # while(self.wifi.active() == False):
      while(self.wifi.status() < 0):
         sleep(0.1)
      print("Wifi Enabled")
      sleep(1)
      self.scan_wifi()
      self.check_wifi_ready()
      if(self.wifi_auto_connect == True and self.wifi_connected == False):
         self.connect_wifi()
   
   def disable_wifi(self):
      if(self.wifi_active == True):
         print("Disabling Wifi Interface")
         self.disconnect_wifi()
         self.wifi_active = False
         self.wifi.active(False)
   
   def scan_wifi(self):
      if(self.wifi_active == True):
         scan_list = self.wifi.scan()
         ssids = []
         for item in scan_list:
            ssids.append(str(item[0]))
         self.wifi_scan_list = ssids.copy()

   def auto_select_ssid(self):
      # NEED TO MAKE WIFI_CONNECT_ATTEMPT_LIST so we can loop through all available wifi instead of always selecting first one we find
      new_ssid_index = None
      for x in range(len(self.wifi_ssid_list)):
         if self.wifi_ssid_list[x] in self.wifi_scan_list:
            new_ssid_index = x
            break
      if(new_ssid_index != None):
         self.wifi_ssid_select = new_ssid_index

   def check_wifi_ready(self):
      if(self.wifi_active == False):
         self.wifi_ready = False
         return False
      if(len(self.wifi_ssid_list) == 0 or len(self.wifi_scan_list) == 0):
         self.wifi_ready = False
         return False
      if(self.wifi_ssid_list[self.wifi_ssid_select] in self.wifi_scan_list):
         self.wifi_ready = True
         return True
      return False
   
   def connect_wifi(self):
      if(self.wifi_active == False):
         return
      if(self.wifi_ssid_select >= 0):
         self.select_ssid(self.wifi_ssid_select)
      else:
         self.scan_wifi()
         self.auto_select_ssid()
      self.wifi.connect(self.wifi_ssid_list[self.wifi_ssid_select], self.wifi_pw_list[self.wifi_ssid_select])
      if(self.wifi_wait_for_connect == True):
         self.wait_for_connected()

   def disconnect_wifi(self):
      if(self.wifi_connected == True):
         self.wifi_connected = False
         self.wifi_connect_counter = 0
         self.wifi.disconnect()
   
   def wait_for_connected(self):
      while(self.wifi_active == True and self.wifi_connected == False and self.connect_counter < self.max_connect_count):
         self.check_wifi_connection()
         if(self.wifi_connected == False):
            self.connect_counter = self.connect_counter + 1
            if(self.wifi_connect_sleep > 0):
               sleep(self.wifi_connect_sleep)
      
   def check_wifi_connection(self):
      if(self.wifi_active == False):
         self.wifi_connected = False
         self.connect_counter = 0
         return
      
      if(self.wifi_connected == True):
         self.connect_counter = 0
         if(self.wifi.status() != network.STAT_GOT_IP):
            self.wifi_connected = False
            print("Lost Wifi Connection")
         return
      
      if(self.wifi.status() == network.STAT_GOT_IP):
         self.connect_counter = 0
         self.wifi_connected = True
         self.wifi_ip_address = self.wifi.ifconfig()[0]
         print(f"""Connected to {self.wifi_ssid_list[self.wifi_ssid_select]} at {self.wifi_ip_address}""")
   
class picow_network_class(picow_ap_class, picow_wifi_class):
   network_mode = 0 # mode -1 is not_configured, mode 0 is wifi, mode 1 is AP
   
   def __init__(self, ap_ssid=None, ap_password=None, wifi_ssid=None, wifi_password=None):
      self.configure_access_point(ssid=ap_ssid, password=ap_password)
      self.configure_wifi(ssid=wifi_ssid, password=wifi_password)

   def set_network_mode(self, mode):
      if(self.network_mode != mode):
         print("Changing network mode")
         if(self.network_mode == 0):
            if(self.wifi_active == True):
               self.disable_wifi()
         if(self.network_mode == 1):
            if(self.ap_active == True):
               self.disable_access_point()
         if(mode == 0):
            self.enable_wifi()
         if(mode == 1):
            self.enable_access_point()
         self.network_mode = mode
      else:
         if(self.network_mode == 0 and self.wifi_active == False):
            self.enable_wifi()
         if(self.network_mode == 1 and self.ap_active == False):
            self.enable_access_point()

   def check_network_connected(self):
      if(self.network_mode == -1):
         return False
      if(self.network_mode == 0):
         if(self.wifi_active == True and self.wifi_connected == True):
            return True
         else:
            return False
      if(self.network_mode == 1):
         if(self.ap_active == True):
            return True
         else:
            return False

   def enable_network(self):
      if(self.network_mode == 0):
         self.enable_wifi()
         if(self.wifi_auto_connect == False and self.wifi_ready == True):
            self.connect_wifi()
      if(self.network_mode == 1):
         self.enable_access_point()

   def disable_network(self):
      if(self.network_mode == 0):
         self.disable_wifi()
      if(self.network_mode == 1):
         self.disable_access_point()

   def get_ip_address(self):
         if(self.check_network_connected() == False):
            return ""
         if(self.network_mode == 0):
            return self.wifi_ip_address
         else:
            return self.ap_ip_address
   

