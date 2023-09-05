import time
import picow_wifi
import server
import save_data
import json
import webpage
import schedule
import machine
import led

infinite_main_loop = False

#todo
# finish remove_wake_time function
# do reorder wake time function
# do hour offset adjustment in time stuff
# do led schedule stuff and wake window ranges
# restart network if on ap mode for 5 mins
# re-lock time every hour?

picow_led = machine.Pin("LED", machine.Pin.OUT)

def main():
   # main, one time, initialization code
   database = save_data.save_data_class()
   wifi = picow_wifi.picow_network_class(ap_ssid="WAKELIGHT", ap_password="wakelight")
   server_socket = server.server_socket_class()
   sched_time = schedule.time_class()
   wake_times = schedule.wake_times_class()
   device_port = 80
   max_socket_connections = 1

   led.init_blink_ip_addr()
   # done init code
   
   print("Kids Wake To Sleep Light")
   
   # main loop here
   try:
      while True:
         device_ip = ""
         
         led.configure_led_duty(10000, 0, 0)
         led.led_on()
         wifi.ap_ssid = database.ap_ssid
         wifi.ap_password = database.ap_pw
         
         if(len(database.ssid_list) > 0):
            wifi.configure_wifi(ssid=database.ssid_list.copy(), password=database.pw_list.copy(), auto_connect=False, wait_for_connect=True)
         print("Database SSID List", database.ssid_list)
         print("Wifi SSID List", wifi.wifi_ssid_list)

         copy_wake_schedule(database, wake_times)
         # load schedule from database to schedule file
         # load led stuff from database to led file
         led.led_mode = database.led_mode
         
         print("Starting Web Check")
         max_wifi_attempts = 3
         while(wifi.check_network_connected() == False):
            print("Finding Network Connection...")
            if(len(database.ssid_list) > 0 and max_wifi_attempts > 0 and wifi.force_ap_mode is False):
               wifi.set_network_mode(0, False)
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
         print(device_ip)

         if(wifi.network_mode == 0 and wifi.check_network_connected == True):
            sched_time.get_network_time()
         
         print("Starting Main Network Connected While Loop")
         while (wifi.check_network_connected() == True):
            if(sched_time.time_locked == False):
               if(wifi.network_mode == 0):
                  sched_time.get_network_time()
            
            led.blink_ip_addr(picow_led, device_ip)

            check_wake_led(sched_time, wake_times)
            
            server_socket.create_socket(device_ip, device_port, max_socket_connections)
            read_ready = server_socket.check_read_ready()
            if(read_ready == True):
               read_data = server_socket.read_data(1024)
               try:
                  response_data = process_socket_read(read_data, wifi)
               except:
                  response_data = None
               send_response(server_socket, response_data)
            sync_save_file(database, wifi, wake_times)

         # end of network connected while loop
         sync_save_file(database, wifi, wake_times)
         print("Restarting Network")
         time.sleep(3)
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

def copy_wake_schedule(database: save_data.save_data_class, sched: schedule.wake_times_class):
   sched.wake_sunday = database.wake_sunday.copy()
   sched.wake_monday = database.wake_monday.copy()
   sched.wake_tuesday = database.wake_tuesday.copy()
   sched.wake_wednesday = database.wake_wednesday.copy()
   sched.wake_thursday = database.wake_thursday.copy()
   sched.wake_friday = database.wake_friday.copy()
   sched.wake_saturday = database.wake_saturday.copy()

def sync_save_file(database: save_data.save_data_class, wifi: picow_wifi.picow_network_class, sched: schedule.wake_times_class):
   file_changed = False
   if(database.ap_ssid != wifi.ap_ssid):
      database.ap_ssid = wifi.ap_ssid
      file_changed = True
   if(database.ap_pw != wifi.ap_password):
      database.ap_pw = wifi.ap_password
      file_changed = True
   if(database.ssid_list != wifi.wifi_ssid_list):
      database.ssid_list = wifi.wifi_ssid_list.copy()
      file_changed = True
   if(database.pw_list != wifi.wifi_pw_list):
      database.pw_list = wifi.wifi_pw_list.copy()
      file_changed = True
   if(database.wake_sunday != sched.wake_sunday):
      database.wake_sunday = sched.wake_sunday.copy()
      file_changed = True
   if(database.wake_monday != sched.wake_monday):
      database.wake_monday = sched.wake_monday.copy()
      file_changed = True
   if(database.wake_tuesday != sched.wake_tuesday):
      database.wake_tuesday = sched.wake_tuesday.copy()
      file_changed = True
   if(database.wake_wednesday != sched.wake_wednesday):
      database.wake_wednesday = sched.wake_wednesday.copy()
      file_changed = True
   if(database.wake_thursday != sched.wake_thursday):
      database.wake_thursday = sched.wake_thursday.copy()
      file_changed = True
   if(database.wake_friday != sched.wake_friday):
      database.wake_friday = sched.wake_friday.copy()
      file_changed = True
   if(database.wake_saturday != sched.wake_saturday):
      database.wake_saturday = sched.wake_saturday.copy()
      file_changed = True
   if(database.led_mode != led.led_mode):
      database.led_mode = led.led_mode
      file_changed = True

   if(file_changed == True):
      print("save file changed")
      save_data.class_data_updated = True
      database.sync_file()

def check_wake_led(sched: schedule.time_class, wake_times):
   if(sched.time_locked == True):
      # load wake schedule light
      pass
   else:
      # load last saved static led settings from database here
      led.configure_led_duty(0, 0, 10000)
      led.set_led()

def process_socket_read(read_data, wifi):
   response_data = None
   process_data = webpage.process_read_data(read_data)
   if(process_data == None):
      return None
   if(process_data[0] == 'GET'):
      if(process_data[1] == ''):
         response_data = webpage.get_webpage()
      else:
         response_data = process_get_request(process_data[1], wifi)
   if(process_data[0] == 'POST'):
      response_data = process_post_request(process_data[1], wifi)
   return response_data
   
def send_response(server_socket, response):
   if(response == None):
      response_data = webpage.create_empty_response()
   else:
      if(len(response) == 0):
         response_data = webpage.create_empty_response()
      else:
         response_data = response
   server_socket.write_data(response_data)
   server_socket.close_connection()

def process_get_request(request, wifi: picow_wifi.picow_network_class):
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
   if "get_wifi_ssid" in get_data:
      response['get_wifi_ssid'] = wifi.wifi_ssid_list
   if "get_ap_ssid" in get_data:
      response['get_ap_ssid'] = wifi.ap_ssid
   return json.dumps(response)

def process_post_request(request, wifi: picow_wifi.picow_network_class):
   response = dict()
   try:
      post_data = json.loads(request)
      print(post_data)
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
   if "add_wifi_ssid" in post_data:
      new_ssid = post_data["add_wifi_ssid"]["ssid"]
      new_password = post_data["add_wifi_ssid"]["password"]
      wifi.add_ssid(new_ssid, new_password)
      response['add_wifi_ssid'] = "success"
   if "remove_wifi_ssid" in post_data:
      print("removing wifi ssid")
      rem_ssid = post_data["remove_wifi_ssid"]
      wifi.remove_ssid(rem_ssid)
      if(wifi.network_mode == 0):
         if(wifi.check_network_connected() == True):
            if(rem_ssid == wifi.wifi_current_ssid):
               wifi.disconnect_on_next_check = True
      response['remove_wifi_ssid'] = "success"
   if "set_ap_ssid" in post_data:
      new_ssid = post_data["set_ap_ssid"]["ssid"]
      new_password = post_data["set_ap_ssid"]["password"]
      if(wifi.set_ap_ssid(new_ssid, new_password)):
         if(wifi.network_mode == 1):
            if(wifi.check_network_connected() == True):
               wifi.disconnect_on_next_check = True
         response['set_ap_ssid'] = "success"
      else:
         response['set_ap_ssid'] = "false"
   if "clear_ap_ssid" in post_data:
      rem_ssid = post_data["clear_ap_ssid"]
      wifi.clear_ap_ssid()
      response['clear_ap_ssid'] = "success"
   if "restart_network" in post_data:
      wifi.disconnect_on_next_check = True
      response['restart_network'] = "success"

   return json.dumps(response)

def main_cleanup(server_socket: server.server_socket_class, wifi: picow_wifi.picow_network_class):
   server_socket.destroy_socket()
   wifi.disable_network()
   led.led_off()

if __name__ == "__main__":
   time.sleep(1)
   print("Starting Main in 1 seconds")
   picow_led.on()
   time.sleep(1)
   picow_led.off()
   try:
      if(infinite_main_loop == True):
         while True:
            main()
            print("Kids Wake Light Done")
      else:
         main()
         print("Kids Wake Light Done")
   except:
      print("Kids Wake Light Done")