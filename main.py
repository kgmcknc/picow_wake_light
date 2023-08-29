import time
import picow_wifi
import secret
import server
import json
import webpage
import schedule
import machine
import led

picow_led = machine.Pin("LED", machine.Pin.OUT)

max_connections = 1

server_socket = server.server_socket_class()

def main():
   red_duty = 30000
   green_duty = 30000
   blue_duty = 30000

   device_ip = picow_wifi.create_access_point()

   #device_ip = picow_wifi.connect_to_wifi(secret.SSID, secret.PASSWORD)
   device_port = 80

   try:
      server_socket.create_socket(device_ip, device_port, max_connections)
      print("socket configured")
   except:
      server_socket.destroy_socket()

   led.init_led_test()
   led_on = 1
   #schedule.get_network_time()

   while(picow_wifi.wifi_connected()):
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

   main_cleanup()

def main_cleanup():
   server_socket.destroy_socket()
   picow_wifi.network_shutdown()

if __name__ == "__main__":
   time.sleep(1)
   print("Starting Main in 1 seconds")
   picow_led.on()
   time.sleep(1)
   picow_led.off()
   try:
      while(1):
         main()
   except KeyboardInterrupt:
      print("got keyboard interrupt. stopping now")
      main_cleanup()
   except Exception as e:
      print("main error, resetting in 1 sec")
      print(e)
      main_cleanup()
      time.sleep(1)
      machine.reset()