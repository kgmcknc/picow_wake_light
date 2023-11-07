import time
import picow_wifi
import server
import save_data
import json
import webpage
import schedule
import machine
import gc
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
   gc.collect()
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
         
         led.set_led(10000, 0, 0)
         if(database.ap_ssid != ""):
            wifi.ap_ssid = database.ap_ssid
            wifi.ap_password = database.ap_pw

         sched_time.hour_offset = database.hour_offset
         print("hour offset, ", sched_time.hour_offset, database.hour_offset)
         
         if(len(database.ssid_list) > 0):
            wifi.configure_wifi(ssid=database.ssid_list.copy(), password=database.pw_list.copy(), config=database.config_list.copy(), auto_connect=False, wait_for_connect=True)
         print("Database SSID List", database.ssid_list)
         print("Wifi SSID List", wifi.wifi_ssid_list)

         copy_wake_schedule(database, wake_times)
         # load schedule from database to schedule file
         led.wake_led = database.wake_led.copy()
         led.sleep_led = database.sleep_led.copy()
         led.custom_led = database.custom_led.copy()
         led.timer_led = database.timer_led.copy()
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
               # print(read_data)
               # print("")
               try:
                  response_data = process_socket_read(read_data, wifi, wake_times, sched_time)
               except:
                  response_data = None
               send_response(server_socket, response_data)
            sync_save_file(database, wifi, wake_times, sched_time)

         # end of network connected while loop
         sync_save_file(database, wifi, wake_times, sched_time)
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
   sched.wake_times["sunday"] = database.wake_times["sunday"].copy()
   sched.wake_times["monday"] = database.wake_times["monday"].copy()
   sched.wake_times["tuesday"] = database.wake_times["tuesday"].copy()
   sched.wake_times["wednesday"] = database.wake_times["wednesday"].copy()
   sched.wake_times["thursday"] = database.wake_times["thursday"].copy()
   sched.wake_times["friday"] = database.wake_times["friday"].copy()
   sched.wake_times["saturday"] = database.wake_times["saturday"].copy()

   sched.off_times["sunday"] = database.off_times["sunday"].copy()
   sched.off_times["monday"] = database.off_times["monday"].copy()
   sched.off_times["tuesday"] = database.off_times["tuesday"].copy()
   sched.off_times["wednesday"] = database.off_times["wednesday"].copy()
   sched.off_times["thursday"] = database.off_times["thursday"].copy()
   sched.off_times["friday"] = database.off_times["friday"].copy()
   sched.off_times["saturday"] = database.off_times["saturday"].copy()

def sync_save_file(database: save_data.save_data_class, wifi: picow_wifi.picow_network_class, sched: schedule.wake_times_class, sched_time: schedule.time_class):
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
   if(database.config_list != wifi.wifi_config_list):
      database.config_list = wifi.wifi_config_list.copy()
      file_changed = True
   if(database.hour_offset != sched_time.hour_offset):
      database.hour_offset = sched_time.hour_offset
      file_changed = True
   if(database.wake_times != sched.wake_times):
      database.wake_times = sched.wake_times.copy()
      file_changed = True
   if(database.off_times != sched.off_times):
      database.off_times = sched.off_times.copy()
      file_changed = True
   if(database.led_mode != led.led_mode):
      database.led_mode = led.led_mode
      file_changed = True
   if(database.wake_led != led.wake_led):
      database.wake_led = led.wake_led.copy()
      file_changed = True
   if(database.sleep_led != led.sleep_led):
      database.sleep_led = led.sleep_led.copy()
      file_changed = True
   if(database.custom_led != led.custom_led):
      database.custom_led = led.custom_led.copy()
   if(database.timer_led != led.timer_led):
      database.timer_led = led.timer_led.copy()
      file_changed = True

   if(file_changed == True):
      print("save file changed")
      save_data.class_data_updated = True
      database.sync_file()

def check_wake_led(sched: schedule.time_class, wake_times: schedule.wake_times_class):
   # led priority when running schedule (0):
   # if timer is set, do timer mode
   # if off, turn led off
   # if wake time, set wake color
   # do sleep color
   if(led.led_mode == 0):
      if(sched.time_locked == True):
         if(sched.timer_active == True):
            sched.check_timer()
            led.led_timer()
            led.led_status = 5
         else:
            current_time = sched.get_local_time()
            current_day = sched.get_weekday()
            if(wake_times.check_off_time(current_day, current_time)):
               led.led_status = 4
               led.led_off()
            else:
               if(wake_times.check_wake_time(current_day, current_time)):
                  led.led_status = 1
                  led.led_wake()
               else:
                  led.led_status = 0
                  led.led_sleep()
      else:
         # load last saved static led settings from database here
         led.led_status = -1
         led.led_custom()
   if(led.led_mode == 1):
      led.led_status = 1
      led.led_wake()
   if(led.led_mode == 2):
      led.led_status = 2
      led.led_sleep()
   if(led.led_mode == 3):
      led.led_status = 3
      led.led_custom()
   if(led.led_mode == 4):
      led.led_status = 4
      led.led_off()

def process_socket_read(read_data, wifi, wake_times, sched_time):
   response_data = None
   process_data = webpage.process_read_data(read_data)
   if(process_data == None):
      return None
   if(process_data[0] == 'GET'):
      if(process_data[1] == ''):
         response_data = webpage.get_webfile("index.html")
         return response_data
      if(process_data[1] == 'index.js'):
         response_data = webpage.get_webfile("index.js")
         return response_data
      else:
         response_data = process_get_request(process_data[1], wifi, wake_times, sched_time)
         request_response = webpage.create_request_response(response_data)
         response_data = request_response
   if(process_data[0] == 'POST'):
      response_data = process_post_request(process_data[1], wifi, wake_times, sched_time)
      request_response = webpage.create_request_response(response_data)
      response_data = request_response
   return response_data
   
def send_response(server_socket: server.server_socket_class, response):
   if(response == None):
      response_data = webpage.create_empty_response()
   else:
      if(len(response) == 0):
         response_data = webpage.create_empty_response()
      else:
         response_data = response
   # print(response_data)
   server_socket.write_data(response_data)
   server_socket.close_connection()

def process_get_request(request, wifi: picow_wifi.picow_network_class, wake_times: schedule.wake_times_class, schedule: schedule.time_class):
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
   if "get_wifi_ssid" in get_data:
      response['get_wifi_ssid'] = wifi.wifi_ssid_list
   if "get_ap_ssid" in get_data:
      response['get_ap_ssid'] = wifi.ap_ssid
   if "get_wake_color" in get_data:
      color_string = ""
      value = "%02X" % int(led.wake_led["red"]/257)
      color_string = color_string + value
      value = "%02X" % int(led.wake_led["green"]/257)
      color_string = color_string + value
      value = "%02X" % int(led.wake_led["blue"]/257)
      color_string = color_string + value
      response['get_wake_color'] = color_string
   if "get_sleep_color" in get_data:
      color_string = ""
      value = "%02X" % int(led.sleep_led["red"]/257)
      color_string = color_string + value
      value = "%02X" % int(led.sleep_led["green"]/257)
      color_string = color_string + value
      value = "%02X" % int(led.sleep_led["blue"]/257)
      color_string = color_string + value
      response['get_sleep_color'] = color_string
   if "get_custom_color" in get_data:
      color_string = ""
      value = "%02X" % int(led.custom_led["red"]/257)
      color_string = color_string + value
      value = "%02X" % int(led.custom_led["green"]/257)
      color_string = color_string + value
      value = "%02X" % int(led.custom_led["blue"]/257)
      color_string = color_string + value
      response['get_custom_color'] = color_string
   if "get_timer_color" in get_data:
      color_string = ""
      value = "%02X" % int(led.timer_led["red"]/257)
      color_string = color_string + value
      value = "%02X" % int(led.timer_led["green"]/257)
      color_string = color_string + value
      value = "%02X" % int(led.timer_led["blue"]/257)
      color_string = color_string + value
      response['get_timer_color'] = color_string
   if "get_wake_times" in get_data:
      day = get_data["get_wake_times"]["day"]
      day_list = wake_times.get_day_list(wake_times.wake_times, day)
      if(day_list != None):
         response['get_wake_times'] = day_list.copy()
      else:
         response['get_wake_times'] = ""
   if "get_off_times" in get_data:
      day = get_data["get_off_times"]["day"]
      day_list = wake_times.get_day_list(wake_times.off_times, day)
      if(day_list != None):
         response['get_off_times'] = day_list.copy()
      else:
         response['get_wake_times'] = ""
   if "get_led_status" in get_data:
      response['get_led_status'] = led.led_status
   if "get_timer_status" in get_data:
      response['get_timer_status'] = schedule.get_timer_status()
   if "get_led_mode" in get_data:
      response['get_led_mode'] = led.led_mode

   return json.dumps(response)

def process_post_request(request, wifi: picow_wifi.picow_network_class, wake_times: schedule.wake_times_class, sched: schedule.time_class):
   response = dict()
   try:
      post_data = json.loads(request)
      #print(post_data)
   except:
      post_data = dict()
      print("json error", request)
   if "set_hour_offset" in post_data:
      hour_offset = post_data['set_hour_offset']
      if(hour_offset > 23 or hour_offset < -23):
         return
      if(sched.time_locked == True):
         response['set_hour_offset'] = "success"
         sched.set_hour_offset(hour_offset)
      else:
         response['set_hour_offset'] = "failed"

   if "set_led_mode" in post_data:
      response['set_led_mode'] = post_data['set_led_mode']
      if(post_data['set_led_mode'] >= 0 and post_data['set_led_mode'] <= 4):
         led.led_mode = post_data['set_led_mode']
   if "set_wake_color" in post_data:
      response['set_wake_color'] = "success"
      led_color = post_data['set_wake_color']
      if(isinstance(led_color, str)):
         if(len(led_color) == 6):
            led.wake_led["red"] = int(led_color[0:2], 16)*257
            led.wake_led["green"] = int(led_color[2:4], 16)*257
            led.wake_led["blue"] = int(led_color[4:6], 16)*257
   if "set_sleep_color" in post_data:
      response['set_sleep_color'] = "success"
      led_color = post_data['set_sleep_color']
      if(isinstance(led_color, str)):
         if(len(led_color) == 6):
            led.sleep_led["red"] = int(led_color[0:2], 16)*257
            led.sleep_led["green"] = int(led_color[2:4], 16)*257
            led.sleep_led["blue"] = int(led_color[4:6], 16)*257
   if "set_custom_color" in post_data:
      response['set_custom_color'] = "success"
      led_color = post_data['set_custom_color']
      if(isinstance(led_color, str)):
         if(len(led_color) == 6):
            led.custom_led["red"] = int(led_color[0:2], 16)*257
            led.custom_led["green"] = int(led_color[2:4], 16)*257
            led.custom_led["blue"] = int(led_color[4:6], 16)*257
   if "set_timer_color" in post_data:
      response['set_timer_color'] = "success"
      led_color = post_data['set_timer_color']
      if(isinstance(led_color, str)):
         if(len(led_color) == 6):
            led.timer_led["red"] = int(led_color[0:2], 16)*257
            led.timer_led["green"] = int(led_color[2:4], 16)*257
            led.timer_led["blue"] = int(led_color[4:6], 16)*257
   if "add_wifi_ssid" in post_data:
      new_ssid = post_data["add_wifi_ssid"]["ssid"]
      new_password = post_data["add_wifi_ssid"]["password"]
      new_ip = post_data["add_wifi_ssid"]["ip_addr"]
      new_mask = post_data["add_wifi_ssid"]["mask"]
      new_gw = post_data["add_wifi_ssid"]["gateway"]
      new_dns = post_data["add_wifi_ssid"]["dns"]
      config = (new_ip, new_mask, new_gw, new_dns)
      wifi.add_ssid(new_ssid, new_password, config)
      response['add_wifi_ssid'] = "success"
   if "remove_wifi_ssid" in post_data:
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
   if "add_wake_time" in post_data:
      day = post_data["add_wake_time"]["day"]
      time = post_data["add_wake_time"]["time"]
      wake_time_list = [time]
      wake_times.add_wake_time(day, wake_time_list)
      response['add_wake_time'] = "success"
   if "clear_wake_times" in post_data:
      day = post_data["clear_wake_times"]
      wake_times.clear_wake_times(day)
      response['clear_wake_times'] = "success"
   if "add_off_time" in post_data:
      day = post_data["add_off_time"]["day"]
      time = post_data["add_off_time"]["time"]
      off_time_list = [time]
      wake_times.add_off_time(day, off_time_list)
      response['add_off_time'] = "success"
   if "clear_off_times" in post_data:
      day = post_data["clear_off_times"]
      wake_times.clear_off_times(day)
      response['clear_off_times'] = "success"
   if "start_timer" in post_data:
      time = post_data["start_timer"]["timer_length"]
      sched.set_timer(time)
      response['start_timer'] = "success"
   if "clear_timer" in post_data:
      day = post_data["clear_timer"]
      sched.clear_timer()
      response['clear_timer'] = "success"

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