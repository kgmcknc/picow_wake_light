
led = Pin("LED", Pin.OUT)
led1 = PWM(Pin(0))
led1.freq(1000)
led2 = PWM(Pin(1))
led2.freq(1000)
led3 = PWM(Pin(2))
led3.freq(1000)
led1.duty_u16(0)
led2.duty_u16(0)
led3.duty_u16(0)


def set_led(red_duty, green_duty, blue_duty):
   global duty1
   global duty2
   global duty3
   led1.duty_u16(red_duty)
   led2.duty_u16(green_duty)
   led3.duty_u16(blue_duty)

def init_led_test():
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

   test = 2
   duty = 60000
   duty1 = 0
   duty2 = 0
   duty3 = 0
   increase = 0
   state = 0
   increase1 = 0
   increase2 = 0
   increase3 = 0
   decrease1 = 0
   decrease2 = 0
   decrease3 = 0
   
   print("starting led test")
   time.sleep(2)

def led_test(led_on):
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

   if(led_on == 0):
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
