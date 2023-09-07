import machine
import time

led_mode = 0
saved_ip = ""
blink_index = 0
blink_list = []

wake_led = {"red": 0, "green": 0, "blue": 0}
sleep_led = {"red": 0, "green": 0, "blue": 0}
const_led = {"red": 0, "green": 0, "blue": 0}

led_state = 0
led = machine.Pin("LED", machine.Pin.OUT)
led_blue = machine.PWM(machine.Pin(0))
led_blue.freq(10000)
led_green = machine.PWM(machine.Pin(1))
led_green.freq(10000)
led_red = machine.PWM(machine.Pin(2))
led_red.freq(10000)
led_red.duty_u16(0)
led_green.duty_u16(0)
led_blue.duty_u16(0)
duty_red = 0
duty_green = 0
duty_blue = 0

led_timer = machine.Timer()
led_is_on = False
timer_active = False
blink_count = 0

def init_blink_ip_addr():
   global saved_ip
   saved_ip = ""

def blink_ip_addr(led, ip_addr):
   global saved_ip
   global blink_index
   global blink_list
   global timer_active
   global led_is_on
   global blink_count
   global led_timer

   if(ip_addr != saved_ip):
      saved_ip = ip_addr
      blink_index = 0
      blink_count = 0
      blink_list = []
      led_is_on = False
      led.off()
      led_timer.deinit()
      timer_active = False
      for item in saved_ip:
         if(item == '.'):
            blink_tuple = (2, 1, 1)
         else:
            blink_tuple = (0.5, 0.5, int(item))
         blink_list.append(blink_tuple)
   
   if(timer_active == False):
      timer_active = True
      if(led_is_on == True):
         led.off()
         led_is_on = False
         blink_count = blink_count + 1
         wait_time = blink_list[blink_index][1]
         if(blink_count >= blink_list[blink_index][2]):
            wait_time = wait_time + 1
            blink_count = 0
            blink_index = blink_index + 1
            if(blink_index >= len(blink_list)):
               wait_time = wait_time + 2
               blink_index = 0
         set_led_timer(wait_time)
      else:
         led.on()
         led_is_on = True
         set_led_timer(blink_list[blink_index][0])
   
def set_led_timer(wait_time):
   global led_timer
   timer_period = int(wait_time*1000)
   led_timer.init(mode=machine.Timer.ONE_SHOT, period=timer_period, callback=led_timer_done)

def led_timer_done(timer):
   global timer_active
   timer_active = False

def blink(led, active_time, inactive_time, count, blink_polarity=1):
   blink_count = 0
   while(blink_count < count):
      if(blink_polarity == 1):
         # blinks on
         led.on()
         time.sleep(active_time)
         led.off()
         time.sleep(inactive_time)
      else:
         # blinks off
         led.off()
         time.sleep(active_time)
         led.on()
         time.sleep(inactive_time)
      blink_count = blink_count + 1

# def led_on():
#    global led_state
#    led_state = 1
#    set_led()

def set_led(red_duty, green_duty, blue_duty):
   led_red.duty_u16(red_duty)
   led_green.duty_u16(green_duty)
   led_blue.duty_u16(blue_duty)

def led_wake():
   set_led(wake_led["red"], wake_led["green"], wake_led["blue"])

def led_sleep():
   set_led(sleep_led["red"], sleep_led["green"], sleep_led["blue"])

def led_const():
   set_led(const_led["red"], const_led["green"], const_led["blue"])

def led_off():
   global led_state
   led_state = 0
   set_led(0, 0, 0)

def get_led_state():
   global led_state
   return led_state

def configure_led_duty(red_duty=None, green_duty=None, blue_duty=None):
   global duty_red
   global duty_green
   global duty_blue
   if(red_duty != None):
      duty_blue = red_duty
   if(green_duty != None):
      duty_green = green_duty
   if(blue_duty != None):
      duty_red = blue_duty

def get_led_duty():
   global duty_red
   global duty_green
   global duty_blue
   return (duty_red, duty_green, duty_blue)

def init_led_test():
   global led_state
   global test
   global duty
   global duty_red
   global duty_green
   global duty_blue
   global increase
   global state
   global increase1
   global increase2
   global increase3
   global decrease1
   global decrease2
   global decrease3
   
   led_state = 1
   test = 2
   duty = 60000
   duty_red = 30000
   duty_green = 30000
   duty_blue = 30000
   increase = 0
   state = 0
   increase1 = 0
   increase2 = 0
   increase3 = 0
   decrease1 = 0
   decrease2 = 0
   decrease3 = 0
   

def led_test():
   global led_state
   global test
   global duty
   global duty_red
   global duty_green
   global duty_blue
   global increase
   global state
   global increase1
   global increase2
   global increase3
   global decrease1
   global decrease2
   global decrease3

   if(led_state == 0):
      led_red.duty_u16(0)
      led_green.duty_u16(0)
      led_blue.duty_u16(0)
      return None

   if(test == 0):
      print(duty)
      led_red.duty_u16(duty)
      led_green.duty_u16(0)
      led_blue.duty_u16(0)
      time.sleep(1)
      led_red.duty_u16(0)
      led_green.duty_u16(duty)
      led_blue.duty_u16(0)
      time.sleep(1)
      led_red.duty_u16(0)
      led_green.duty_u16(0)
      led_blue.duty_u16(duty)
      time.sleep(1)
      if(duty == 60000):
         increase = 0
      else:
         if(duty == 0):
            increase = 1
      if(increase):
         duty = duty + 5000
      else:
         duty = duty - 5000
   if(test == 1):
      duty_red = duty_red + 1
      duty_green = duty_green + 2
      duty_blue = duty_blue + 3
      if(duty_red >= 65535):
         duty_red = 0
      if(duty_green >= 65535):
         duty_green = 0
      if(duty_blue >= 65535):
         duty_blue = 0
      led_red.duty_u16(duty_red)
      led_green.duty_u16(duty_green)
      led_blue.duty_u16(duty_blue)
      time.sleep(0.001)
   if(test == 2):
      increase1 = (state == 0) or (state == 5)
      decrease1 = (state == 2) or (state == 7)
      increase2 = (state == 1) or (state == 6)
      decrease2 = (state == 4) or (state == 7)
      increase3 = (state == 3)
      decrease3 = (state == 7)
      if(increase1):
         duty_red = duty_red + 1
      if(decrease1):
         duty_red = duty_red - 1
      if(increase2):
         duty_green = duty_green + 1
      if(decrease2):
         duty_green = duty_green - 1
      if(increase3):
         duty_blue = duty_blue + 1
      if(decrease3):
         duty_blue = duty_blue - 1
      prev_state = state
      if(state == 0):
            if(duty_red >= 65535):
               duty_red = 65535
               state = 1
      elif(state == 1):
            if(duty_green >= 65535):
               duty_green = 65535
               state = 2
      elif(state == 2):
            if(duty_red <= 0):
               duty_red = 0
               state = 3
      elif(state == 3):
            if(duty_blue >= 65535):
               duty_blue = 65535
               state = 4
      elif(state == 4):
            if(duty_green <= 0):
               duty_green = 0
               state = 5
      elif(state == 5):
            if(duty_red >= 65535):
               duty_red = 65535
               state = 6
      elif(state == 6):
            if(duty_green >= 65535):
               duty_red = 65535
               duty_green = 65535
               duty_blue = 65535
               state = 7
      elif(state == 7):
            if(duty_red <= 0):
               duty_red = 0
               duty_green = 0
               duty_blue = 0
               state = 0
      else:
         state = 0
      if(prev_state != state):
         print("new_state: ", state)
      led_red.duty_u16(duty_red)
      led_green.duty_u16(duty_green)
      led_blue.duty_u16(duty_blue)
