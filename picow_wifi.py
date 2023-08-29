
import network
from time import sleep

ap_ssid = "WAKELIGHT"
ap_password = "wakelight"
ap_gateway = '192.168.4.1' # currently can't change due to bug in picow fw
ap_sub_mask = '255.255.0.0'
ap_ip_addr = '192.168.4.1' # currently can't change due to bug in picow fw
ap_dns_serv = '0.0.0.0'

network_type = 0 # 0 is ap, 1 is wifi connection
wlan = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)

def create_access_point():
   global ap

   print("Making Network Access Point")
   ap.config(ssid=ap_ssid, password=ap_password)
   ap.ifconfig((ap_ip_addr, ap_sub_mask, ap_gateway, ap_dns_serv))
   ap.active(True)

   while(ap.active == False):
      sleep(0.5)

   ap.ifconfig((ap_ip_addr, ap_sub_mask, ap_gateway, ap_dns_serv))
   
   print(f"Made Access Point: SSID={ap_ssid}, PW={ap_password}")
   print(ap)
   
   return ap_ip_addr

def disable_access_point():
   print("Disabling Network Access Point")
   ap.active(False)

def connect_to_wifi(ssid, password):
   global wlan
   
   print("connecting To Wifi")
   wlan.active(True)
   wlan.connect(ssid, password)

   # Wait for connect or fail
   max_wait = 10
   while max_wait > 0:
      data = wlan.status()
      if(data < 0):
         sleep(1)
         continue
      if(data >= 3):
         break;
      max_wait = max_wait - 1
      sleep(1)

   # Handle connection error
   if wlan.status() != 3:
      return None
   else:
      print('connected')
      status = wlan.ifconfig()
      print(status)
      device_ip = status[0]
      print( 'ip = ' + status[0] )
      return device_ip
   
def disable_wifi():
   print("Disabling Wifi Interface")
   wlan.disconnect()
   wlan.active(False)
   
def wifi_connected():
   global ap
   global wlan
   is_connected = 0

   if(network_type == 0):
      if(ap.active):
         is_connected = 1
   else:
      if(wlan.status == network.STAT_GOT_IP):
         is_connected = 1

   if(is_connected):
      return True
   else:
      return False
   
def network_shutdown():
   print("Shutting Down Network Interfaces")
   if(network_type == 0):
      disable_access_point()
   else:
      disable_wifi()