import time
import picow_wifi
import server
import save_data
import json
import webpage
import schedule
import machine
import led

picow_led = machine.Pin("LED", machine.Pin.OUT)

def main():

   # main, one time, initialization code
   server_socket = server.server_socket_class()
   wifi = picow_wifi.picow_network_class(ap_ssid="WAKELIGHT", ap_password="wakelight")
   database = save_data.save_data_class()
   device_port = 80
   max_socket_connections = 1
   # done init code
   
   print("Kids Wake To Sleep Light")
   
   # main loop here
   try:
      while True:
         device_ip = ""
         
         led.configure_led_duty(10000, 0, 0)
         led.led_on()

         if(len(database.ssid_list) > 0):
            wifi.configure_wifi(ssid=database.ssid_list, password=database.pw_list, auto_connect=False, wait_for_connect=True)
         
         # load schedule from database to schedule file
         # load led stuff from database to led file
         
         print("Starting Web Check")
         max_wifi_attempts = 3
         while(wifi.check_network_connected() == False):
            print("Finding Network Connection...")
            if(len(database.ssid_list) > 0 and max_wifi_attempts > 0):
               wifi.set_network_mode(0)
               wifi.enable_network()
               wifi.connect_wifi()
               max_wifi_attempts = max_wifi_attempts - 1
            else:
               wifi.set_network_mode(1)
               wifi.enable_network()
         
         if(wifi.network_mode == 0):
            print("Network is Wifi")
         else:
            print("Network is AP")

         device_ip = wifi.get_ip_address()
         print("device_ip")
         sched = schedule.time_class()
         sched.get_network_time()

         if(sched.time_locked == True):
            # load wake schedule light
            pass
         else:
            # load last saved static led settings from database here
            led.configure_led_duty(0, 0, 10000)
            led.set_led()
      
         while (wifi.check_network_connected() == True):
            led.blink_ip_addr(picow_led, device_ip)
            
            if(server_socket.created == 0):
               try:
                  server_socket.create_socket(device_ip, device_port, max_socket_connections)
               except:
                  server_socket.destroy_socket()
            if(server_socket.connected):
               server_socket.close_connection()
            try:
               read_ready = server_socket.socket_select_check()
            except Exception as e:
               print(e)
               print("socket_select_error")
               read_ready = False
            if(read_ready == True):
               read_data = server_socket.read_data(1024)
               try:
                  process_data = webpage.process_read_data(read_data)
                  if(process_data != None):
                     if(process_data[0] == 'GET'):
                        if(process_data[1] == ''):
                           server_socket.write_data(webpage.get_webpage())
                        else:
                           response = process_get_request(process_data[1])
                           if(len(response) == 0):
                              raise 
                           server_socket.write_data(response)
                           server_socket.close_connection()
                     if(process_data[0] == 'POST'):
                        response = process_post_request(process_data[1])
                        if(len(response) == 0):
                           raise
                        server_socket.write_data(response)
                        server_socket.close_connection()
                  else:
                     raise
               except:
                  empty_response = webpage.create_empty_response()
                  server_socket.write_data(empty_response)
                  server_socket.close_connection()
            
            #led.update_led()

         # end of network connected while loop
         print("restarting network")
         main_cleanup(server_socket, wifi)
      # end of while True
   except KeyboardInterrupt:
      print("got keyboard interrupt. stopping now")
      main_cleanup(server_socket, wifi)
   except Exception as e:
      print("main error, resetting in 1 sec")
      main_cleanup(server_socket, wifi)
      print(e)
      time.sleep(1)
      print("Kids Wake Light Done")
      machine.reset()

def process_get_request(request):
   response = dict()
   try:
      get_data = json.loads(request)
   except:
      get_data = dict()
      print("json error", request)
   if "led_state" in get_data:
      if(led.get_led_state() == 0):
         response['led_state'] = 'led_off'
      else:
         response['led_state'] = 'led_on'
   if "led_duty" in get_data:
      led_duty = led.get_led_duty()
      response['led_red'] = led_duty[0]
      response['led_green'] = led_duty[1]
      response['led_blue'] = led_duty[2]
   return json.dumps(response)

def process_post_request(request):
   response = dict()
   try:
      post_data = json.loads(request)
   except:
      post_data = dict()
      print("json error", request)
   if "led_state" in post_data:
      if(post_data['led_state'] == 'on'):
         print('led on!')
         led.led_on()
         response['led_state'] = 'led_on'
      if(post_data['led_state'] == 'off'):
         print('led off!')
         led.led_off()
         response['led_state'] = 'led_off'
   if "led_red" in post_data:
      duty = int(post_data['led_red'])
      if(duty >= 0 and duty <= 65535):
         led.configure_led_duty(red_duty=duty)
         response['led_red'] = duty
   if "led_green" in post_data:
      duty = int(post_data['led_green'])
      if(duty >= 0 and duty <= 65535):
         led.configure_led_duty(green_duty=duty)
         response['led_green'] = duty
   if "led_blue" in post_data:
      duty = int(post_data['led_blue'])
      if(duty >= 0 and duty <= 65535):
         led.configure_led_duty(blue_duty=duty)
         response['led_blue'] = duty
   return json.dumps(response)

def main_cleanup(server_socket, wifi):
   server_socket.destroy_socket()
   wifi.disable_network()

if __name__ == "__main__":
   time.sleep(1)
   print("Starting Main in 1 seconds")
   picow_led.on()
   time.sleep(1)
   picow_led.off()
   try:
      main()
      print("Kids Wake Light Done")
   except:
      print("Kids Wake Light Done")