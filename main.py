import time
import picow_wifi
import secret
import server
import save_data
import json
import webpage
import schedule
import machine
import led

picow_led = machine.Pin("LED", machine.Pin.OUT)
wifi_ready = 0
device_port = 80

max_connections = 1

server_socket = server.server_socket_class()
wifi = picow_wifi.picow_network_class(ap_ssid="WAKELIGHT", ap_password="wakelight")
database = save_data.save_data_class()

def main():
   wifi.configure_wifi(ssid="WilmotFiber", password="daisy09!", wait_for_connect=True, auto_connect=True)
   
   # ap = picow_wifi.picow_ap_class(ssid="WAKELIGHT", password="wakelight")
   # wifi = picow_wifi.picow_wifi_class()

   # get wifi ssid list
   # if list is 0, connect as ap
   # if list > 0, try to connect to wifi

   # loop main once connected to something
   # in main loop if connection is ap, check if wifi list is ever greater than 1 and wifi timeout is 0
   # if you check all wifi and none work, set wifi timeout to a value and then it'll decrement if ever > 0 in main loop

   # ap.enable_access_point()
   # if(len(database.ssid_list) > 0){
   # } else {
      
   # }
   # device_ip = ap.get_ap_ip_address()

   #device_ip = picow_wifi.connect_to_wifi(secret.SSID, secret.PASSWORD)

   try:
      server_socket.create_socket(device_ip, device_port, max_connections)
      print("socket configured")
   except:
      server_socket.destroy_socket()

   led.init_led_test()
   #schedule.get_network_time()

   while(picow_wifi.wifi_connected()):
      try:
         read_ready = server_socket.check_socket()
      except:
         print("main_select_error")
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
      
      led.update_led()

   main_cleanup()

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

def main_cleanup():
   server_socket.destroy_socket()
   wifi.disable_network()

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