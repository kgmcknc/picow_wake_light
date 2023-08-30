import machine
import time

led_state = 0
led = machine.Pin("LED", machine.Pin.OUT)
led1 = machine.PWM(machine.Pin(0))
led1.freq(1000)
led2 = machine.PWM(machine.Pin(1))
led2.freq(1000)
led3 = machine.PWM(machine.Pin(2))
led3.freq(1000)
led1.duty_u16(0)
led2.duty_u16(0)
led3.duty_u16(0)
duty1 = 0
duty2 = 0
duty3 = 0

def led_on():
   global led_state
   led_state = 1

def led_off():
   global led_state
   led_state = 0

def get_led_state():
   global led_state
   return led_state

def configure_led_duty(red_duty=None, green_duty=None, blue_duty=None):
   global duty1
   global duty2
   global duty3
   if(red_duty != None):
      duty3 = red_duty
   if(green_duty != None):
      duty2 = green_duty
   if(blue_duty != None):
      duty1 = blue_duty

def get_led_duty():
   global duty1
   global duty2
   global duty3
   return (duty1, duty2, duty3)

def set_led():
   global led_state
   global duty1
   global duty2
   global duty3

   if(led_state == 0):
      led1.duty_u16(0)
      led2.duty_u16(0)
      led3.duty_u16(0)
   else:
      led1.duty_u16(duty1)
      led2.duty_u16(duty2)
      led3.duty_u16(duty3)

def update_led():
   set_led()

def init_led_test():
   global led_state
   global test
   global duty
   global duty1
   global duty2
   global duty3
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
   duty1 = 30000
   duty2 = 30000
   duty3 = 30000
   increase = 0
   state = 0
   increase1 = 0
   increase2 = 0
   increase3 = 0
   decrease1 = 0
   decrease2 = 0
   decrease3 = 0
   
   print("starting led test")
   configure_led_duty(duty1, duty2, duty3)
   set_led()
   time.sleep(2)

def led_test():
   global led_state
   global test
   global duty
   global duty1
   global duty2
   global duty3
   global increase
   global state
   global increase1
   global increase2
   global increase3
   global decrease1
   global decrease2
   global decrease3

   if(led_state == 0):
      led1.duty_u16(0)
      led2.duty_u16(0)
      led3.duty_u16(0)
      return None

   if(test == 0):
      print(duty)
      led1.duty_u16(duty)
      led2.duty_u16(0)
      led3.duty_u16(0)
      time.sleep(1)
      led1.duty_u16(0)
      led2.duty_u16(duty)
      led3.duty_u16(0)
      time.sleep(1)
      led1.duty_u16(0)
      led2.duty_u16(0)
      led3.duty_u16(duty)
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
      duty1 = duty1 + 1
      duty2 = duty2 + 2
      duty3 = duty3 + 3
      if(duty1 >= 65535):
         duty1 = 0
      if(duty2 >= 65535):
         duty2 = 0
      if(duty3 >= 65535):
         duty3 = 0
      led1.duty_u16(duty1)
      led2.duty_u16(duty2)
      led3.duty_u16(duty3)
      time.sleep(0.001)
   if(test == 2):
      increase1 = (state == 0) or (state == 5)
      decrease1 = (state == 2) or (state == 7)
      increase2 = (state == 1) or (state == 6)
      decrease2 = (state == 4) or (state == 7)
      increase3 = (state == 3)
      decrease3 = (state == 7)
      if(increase1):
         duty1 = duty1 + 1
      if(decrease1):
         duty1 = duty1 - 1
      if(increase2):
         duty2 = duty2 + 1
      if(decrease2):
         duty2 = duty2 - 1
      if(increase3):
         duty3 = duty3 + 1
      if(decrease3):
         duty3 = duty3 - 1
      prev_state = state
      if(state == 0):
            if(duty1 >= 65535):
               duty1 = 65535
               state = 1
      elif(state == 1):
            if(duty2 >= 65535):
               duty2 = 65535
               state = 2
      elif(state == 2):
            if(duty1 <= 0):
               duty1 = 0
               state = 3
      elif(state == 3):
            if(duty3 >= 65535):
               duty3 = 65535
               state = 4
      elif(state == 4):
            if(duty2 <= 0):
               duty2 = 0
               state = 5
      elif(state == 5):
            if(duty1 >= 65535):
               duty1 = 65535
               state = 6
      elif(state == 6):
            if(duty2 >= 65535):
               duty1 = 65535
               duty2 = 65535
               duty3 = 65535
               state = 7
      elif(state == 7):
            if(duty1 <= 0):
               duty1 = 0
               duty2 = 0
               duty3 = 0
               state = 0
      else:
         state = 0
      if(prev_state != state):
         print("new_state: ", state)
      led1.duty_u16(duty1)
      led2.duty_u16(duty2)
      led3.duty_u16(duty3)
