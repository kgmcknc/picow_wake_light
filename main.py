import time
import network
import secret
import server
import json
import webpage
import schedule
import machine
import led
from machine import Pin, PWM

max_connections = 1

server_socket = server.server_socket_class()

def main():
   red_duty = 30000
   green_duty = 30000
   blue_duty = 30000

   print('starting wifi')
   ssid = secret.SSID
   password = secret.PASSWORD
   wlan = network.WLAN(network.STA_IF)
   wlan.active(True)
   wlan.connect(ssid, password)

   # Wait for connect or fail
   max_wait = 10
   while max_wait > 0:
      data = wlan.status()
      print('got', data)
      if(data < 0):
         time.sleep(1)
         continue
      if(data >= 3):
         break;
      max_wait = max_wait - 1
      print('waiting for connection...')
      print(data)
      time.sleep(2)

   # Handle connection error
   if wlan.status() != 3:
      raise RuntimeError('network connection failed')
   else:
      print('connected')
      status = wlan.ifconfig()
      print(status)
      device_ip = status[0]
      device_port = 80
      print( 'ip = ' + status[0] )
   
   try:
      server_socket.create_socket(device_ip, device_port, max_connections)
      print("socket configured")
   except:
      server_socket.destroy_socket()

   led.init_led_test()
   led_on = 1
   schedule.get_network_time()

   while(wlan.status() == 3):
      try:
         read_ready = server_socket.check_socket()
      except:
         print("main_select_error")
         read_ready = False
      if(read_ready == True):
         read_data = server_socket.read_data(1024)
         process_data = webpage.process_read_data(read_data)
         if(process_data != None):
            if(process_data[0] == 'GET'):
               server_socket.write_data(process_data[1])
            if(process_data[0] == 'POST'):
               post_data = json.loads(process_data[1])
               if "led_state" in post_data:
                  if(post_data['led_state'] == "on"):
                     print("led on!")
                     led_on = 1
                  if(post_data['led_state'] == "off"):
                     print("led off!")
                     led_on = 0
               if "led_red" in post_data:
                  red_duty = int(post_data["led_red"])
               if "led_green" in post_data:
                  green_duty = int(post_data["led_green"])
               if "led_blue" in post_data:
                  blue_duty = int(post_data["led_blue"])
               empty_response = webpage.create_empty_response()
               server_socket.write_data(empty_response)
               server_socket.close_connection()
         else:
            empty_response = webpage.create_empty_response()
            server_socket.write_data(empty_response)
            server_socket.close_connection()
      
      if(led_on):
         led.set_led(blue_duty, green_duty, red_duty)
      else:
         led.set_led(0,0,0)
      
      #led.led_test(led_on)

   server_socket.destroy_socket()

if __name__ == "__main__":
   time.sleep(2)
   print("Starting Main in 5 seconds")
   led.on()
   time.sleep(5)
   led.off()
   machine.reset()
   try:
      while(1):
         main()
   except:
      server_socket.destroy_socket()
      print("main error, restarting in 5")
      time.sleep(5)
      machine.reset()