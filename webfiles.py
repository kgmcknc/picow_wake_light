
def get_index_html():
   html_file = '''
      <html>
         <head>
            <title>PicoW LED Wake Light</title>
         </head>
         <body>
            Wake Time Settings:
            <br>
            <br>
            Select a day:
            <select name="weekday" id="weekday" onchange="update_wake_status()">
            <option value="sunday">Sunday</option>
            <option value="monday">Monday</option>
            <option value="tuesday">Tuesday</option>
            <option value="wednesday">Wednesday</option>
            <option value="thursday">Thursday</option>
            <option value="friday">Friday</option>
            <option value="saturday">Saturday</option>
            </select>
            <br>
            <br>
            <label for="timer_hour">Timer Length:</label>
            Hours: <input type="number" id="timer_hour" name="timer_hour" step="1" min="0" step="1" value="1">
            Minutes: <input type="number" id="timer_min" name="timer_min" min="0" max="59" step="1" value="0">
            Seconds: <input type="number" id="timer_sec" name="timer_sec" min="0" max="59" step="1" value="0">
            <br>
            <button onclick="set_timer()">Set Timer</button>
            <button onclick="clear_timer()">Clear Timer</button>
            <br>
            <br>
            <label for="start_time">Start Time:</label>
            <input type="time" id="start_time" name="start_time">
            <label for="end_time">End Time:</label>
            <input type="time" id="end_time" name="end_time">
            <br>
            <button onclick="add_wake_time()">Add Wake Time</button>
            <button onclick="clear_wake_times()">Clear Wake Times</button>
            <br>
            <button onclick="add_off_time()">Add Off Time</button>
            <button onclick="clear_off_times()">Clear Off Times</button>
            <div id="schedule_div">
               <div>No Wake Times Scheduled</div>
            </div>
            <div id="off_schedule_div">
               <div>No Off Times Scheduled</div>
            </div>
            <br><br>
            <div id="status_div"></div>
            <br><br>
            <label for="wakecolor">Select Wake Color:</label>
            <input type="color" id="wakecolor" name="wakecolor" value="#00ff00">
            <input type="button" value="Set Wake Color" onclick="set_wake_color()">
            <input type="button" value="Get Wake Color" onclick="get_wake_color()">
            <br>
            <label for="sleepcolor">Select Sleep Color:</label>
            <input type="color" id="sleepcolor" name="sleepcolor" value="#0000ff">
            <input type="button" value="Set Sleep Color" onclick="set_sleep_color()">
            <input type="button" value="Get Sleep Color" onclick="get_sleep_color()">
            <br>
            <label for="customcolor">Select Custom color:</label>
            <input type="color" id="customcolor" name="customcolor" value="#ff00ff">
            <input type="button" value="Set Custom Color" onclick="set_custom_color()">
            <input type="button" value="Get Custom Color" onclick="get_custom_color()">
            <br>
            <label for="timercolor">Select Timer color:</label>
            <input type="color" id="timercolor" name="timercolor" value="#ff00ff">
            <input type="button" value="Set Timer Color" onclick="set_timer_color()">
            <input type="button" value="Get Timer Color" onclick="get_timer_color()">
            <br>
            <input type="button" value="Resume Schedule" onclick="set_led_mode(0)">
            <input type="button" value="Force Wake" onclick="set_led_mode(1)">
            <input type="button" value="Force Sleep" onclick="set_led_mode(2)">
            <input type="button" value="Force Custom" onclick="set_led_mode(3)">
            <input type="button" value="Turn LED Off" onclick="set_led_mode(4)">
            <br><br>
            <label for="ssid">SSID:</label><br>
            <input type="text" id="ssid" name="ssid"><br>
            <label for="pwd">Password:</label><br>
            <input type="password" id="pwd" name="pwd"><br><br>
            <label for="ip_addr">IP_Address:</label><br>
            <input type="text" id="ip_addr" name="ip_addr"><br>
            <label for="gateway">Subnet_Mask:</label><br>
            <input type="text" id="mask" name="mask"><br>
            <label for="gateway">Gateway:</label><br>
            <input type="text" id="gateway" name="gateway"><br>
            <label for="dns">DNS:</label><br>
            <input type="text" id="dns" name="dns"><br>
            <button onclick="add_network()">Add Network</button>
            <button onclick="remove_network()">Remove Network</button>
            <button onclick="set_ap_ssid()">Set AP SSID</button>
            <button onclick="clear_ap_ssid()">Clear AP SSID</button>
            <button onclick="restart_network()">Restart Network</button>
            <br><br>
            <script src="index.js"></script>
         </body>
      </html>
      '''
   return html_file


def get_index_js():
   javascript_file = '''
      led_mode = 0
      wake_schedule = 0
      off_schedule = 0
      timer_remaining = (0, 0, 0)
      setInterval(get_status, 5000);
      get_led_values()
      async function get_led_values(){
         await sleep(1000)
         set_hour_offset()
         await sleep(500)
         get_wake_color()
         await sleep(500)
         get_sleep_color()
         await sleep(500)
         get_custom_color()
         await sleep(500)
         get_timer_color()
      }
      async function get_status(){
         if(!document.hidden){
            await sleep(600)
            get_led_mode()
            await sleep(600)
            get_wake_status()
            await sleep(600)
            get_timer_status()
            await sleep(600)
            get_wake_times()
            await sleep(600)
            get_off_times()
         }
      }
      function sleep(ms) {
         return new Promise(resolve => setTimeout(resolve, ms));
      }
      function set_hour_offset(){
         var current_date = new Date();
         current_day = current_date.getDay();
         day_list = document.getElementById("weekday");
         day_list.selectedIndex = current_day;
         var hour_offset = current_date.getTimezoneOffset();
         hour_offset = hour_offset/60
         var send_data = {"set_hour_offset":hour_offset}
         send_xmlhttp_post(send_data)
      }
      function add_network(){
         new_ssid = document.getElementById("ssid").value
         new_pw = document.getElementById("pwd").value
         new_ip = document.getElementById("ip_addr").value
         new_mask = document.getElementById("mask").value
         new_gw = document.getElementById("gateway").value
         new_dns = document.getElementById("dns").value
         var send_data = {"add_wifi_ssid":{"ssid":new_ssid,"password":new_pw,"ip_addr":new_ip,"mask":new_mask,"gateway":new_gw,"dns":new_dns}}
         send_xmlhttp_post(send_data)
      }
      function remove_network(){
         new_ssid = document.getElementById("ssid").value
         var send_data = {"remove_wifi_ssid":new_ssid}
         send_xmlhttp_post(send_data)
      }
      function set_ap_ssid(){
         new_ssid = document.getElementById("ssid").value
         new_pw = document.getElementById("pwd").value
         var send_data = {"set_ap_ssid":{"ssid":new_ssid,"password":new_pw}}
         send_xmlhttp_post(send_data)
      }
      function clear_ap_ssid(){
         new_ssid = document.getElementById("ssid").value
         var send_data = {"clear_ap_ssid":new_ssid}
         send_xmlhttp_post(send_data)
      }
      function restart_network(){
         var send_data = {"restart_network":"True"}
         send_xmlhttp_post(send_data)
      }
      function set_led_mode(mode){
         if(mode >= 0 && mode <= 4){
            var send_data = send_data = {"set_led_mode":mode}
            send_xmlhttp_post(send_data)
         }
      }
      function set_wake_color(){
         var color_value = document.getElementById("wakecolor").value
         var send_data = {"set_wake_color":color_value.slice(1)}
         send_xmlhttp_post(send_data)
      }
      function set_sleep_color(){
         var color_value = document.getElementById("sleepcolor").value
         var send_data = {"set_sleep_color":color_value.slice(1)}
         send_xmlhttp_post(send_data)
      }
      function set_custom_color(){
         var color_value = document.getElementById("customcolor").value
         var send_data = {"set_custom_color":color_value.slice(1)}
         send_xmlhttp_post(send_data)
      }
      function set_timer_color(){
         var color_value = document.getElementById("timercolor").value
         var send_data = {"set_timer_color":color_value.slice(1)}
         send_xmlhttp_post(send_data)
      }
      function get_wake_color(){
         var send_data = {"get_wake_color":""}
         send_xmlhttp_get(send_data, set_wake_value)
      }
      function get_sleep_color(){
         var send_data = {"get_sleep_color":""}
         send_xmlhttp_get(send_data, set_sleep_value)
      }
      function get_custom_color(){
         var send_data = {"get_custom_color":""}
         send_xmlhttp_get(send_data, set_custom_value)
      }
      function get_timer_color(){
         var send_data = {"get_timer_color":""}
         send_xmlhttp_get(send_data, set_timer_value)
      }
      function set_wake_value(response_data){
         document.getElementById("wakecolor").value = "#"+response_data["get_wake_color"]
      }
      function set_sleep_value(response_data){
         document.getElementById("sleepcolor").value = "#"+response_data["get_sleep_color"]
      }
      function set_custom_value(response_data){
         document.getElementById("customcolor").value = "#"+response_data["get_custom_color"]
      }
      function set_timer_value(response_data){
         document.getElementById("timercolor").value = "#"+response_data["get_timer_color"]
      }
      function set_timer(){
         var timer_hour = document.getElementById("timer_hour").value
         var timer_min = document.getElementById("timer_min").value
         var timer_sec = document.getElementById("timer_sec").value
         var timer_length = [timer_hour, timer_min, timer_sec]
         var send_data = {"start_timer": {"timer_length":timer_length}}
         send_xmlhttp_post(send_data, get_wake_times)
      }
      function clear_timer(){
         var send_data = {"clear_timer": ""}
         send_xmlhttp_post(send_data)
      }
      function add_wake_time(){
         var day = document.getElementById("weekday").value
         var start = document.getElementById("start_time").value
         var end = document.getElementById("end_time").value
         var start_split = start.split(":")
         var end_split = end.split(":")
         var start_time = [start_split[0], start_split[1]]
         var end_time = [end_split[0], end_split[1]]
         var send_data = {"add_wake_time": {"day":day, "time":{"start_time":start_time,"end_time":end_time}}}
         send_xmlhttp_post(send_data)
      }
      function clear_wake_times(){
         var day = document.getElementById("weekday").value
         var send_data = {"clear_wake_times": day}
         send_xmlhttp_post(send_data)
      }
      function get_wake_times(){
         var send_data = {"get_wake_times": ""}
         send_xmlhttp_get(send_data, set_wake_schedule)
      }
      function set_wake_schedule(response_data){
         schedule_div = document.getElementById("schedule_div")
         wake_schedule = response_data["get_wake_times"]
         update_status_divs()
      }
      function update_wake_status(){
         var day = document.getElementById("weekday").value
         wake_list = wake_schedule[day]
         while(schedule_div.childElementCount > 0){
            schedule_div.removeChild(schedule_div.children[0])
         }
         list_len = wake_list.length
         if(list_len == 0){
            new_child = document.createElement("div");
            new_child.innerHTML = "No Times Scheduled"
            schedule_div.appendChild(new_child)
         }
         for (let i = 0; i < list_len; i++) {
            start_time = wake_list[i]["start_time"]
            end_time = wake_list[i]["end_time"]
            if(start_time[0] > 11){
               if(start_time[0] == 12){
                  start_hour = start_time[0]
               } else {
                  start_hour = start_time[0]-12
               }
               start_string = "Wake_Start: "+start_hour+":"+start_time[1]+"PM"
            } else {
               start_hour = start_time[0]
               start_string = "Wake_Start: "+start_hour+":"+start_time[1]+"AM"
            }
            if(end_time[0] > 11){
               if(end_time[0] == 12){
                  end_hour = end_time[0]
               } else {
                  end_hour = end_time[0]-12
               }
               end_string = "Wake_End: "+end_hour+":"+end_time[1]+"PM"
            } else {
               end_hour = start_time[0]
               end_string = "Wake_End: "+end_hour+":"+end_time[1]+"AM"
            }
            new_child = document.createElement("div");
            new_child.innerHTML = start_string+"<br>"+end_string
            schedule_div.appendChild(new_child)
         }
      }
      function add_off_time(){
         var day = document.getElementById("weekday").value
         var start = document.getElementById("start_time").value
         var end = document.getElementById("end_time").value
         var start_split = start.split(":")
         var end_split = end.split(":")
         var start_time = [start_split[0], start_split[1]]
         var end_time = [end_split[0], end_split[1]]
         var send_data = {"add_off_time": {"day":day, "time":{"start_time":start_time,"end_time":end_time}}}
         send_xmlhttp_post(send_data)
      }
      function clear_off_times(){
         var day = document.getElementById("weekday").value
         var send_data = {"clear_off_times": day}
         send_xmlhttp_post(send_data)
      }
      function get_off_times(){
         var send_data = {"get_off_times": ""}
         send_xmlhttp_get(send_data, set_off_schedule)
      }
      function set_off_schedule(response_data){
         off_schedule_div = document.getElementById("off_schedule_div")
         off_schedule = response_data["get_off_times"]
         update_status_divs()
      }
      function update_off_status(){
         var day = document.getElementById("weekday").value
         off_list = off_schedule[day]
         while(off_schedule_div.childElementCount > 0){
            off_schedule_div.removeChild(off_schedule_div.children[0])
         }
         list_len = off_list.length
         if(list_len == 0){
            new_child = document.createElement("div");
            new_child.innerHTML = "No Times Scheduled"
            off_schedule_div.appendChild(new_child)
         }
         for (let i = 0; i < list_len; i++) {
            start_time = off_list[i]["start_time"]
            end_time = off_list[i]["end_time"]
            if(start_time[0] > 11){
               if(start_time[0] == 12){
                  start_hour = start_time[0]
               } else {
                  start_hour = start_time[0]-12
               }
               start_string = "Off_Start: "+start_hour+":"+start_time[1]+"PM"
            } else {
               start_hour = start_time[0]
               start_string = "Off_Start: "+start_hour+":"+start_time[1]+"AM"
            }
            if(end_time[0] > 11){
               if(end_time[0] == 12){
                  end_hour = end_time[0]
               } else {
                  end_hour = end_time[0]-12
               }
               end_string = "Off_End: "+end_hour+":"+end_time[1]+"PM"
            } else {
               end_hour = start_time[0]
               end_string = "Off_End: "+end_hour+":"+end_time[1]+"AM"
            }
            new_child = document.createElement("div");
            new_child.innerHTML = start_string+"<br>"+end_string
            off_schedule_div.appendChild(new_child)
         }
      }
      function update_status_divs(){
         update_wake_status()
         update_off_status()
      }
      function get_led_mode(){
         var send_data = {"get_led_mode": ""}
         send_xmlhttp_get(send_data, save_led_mode)
      }
      function get_wake_status(){
         var send_data = {"get_led_status": ""}
         send_xmlhttp_get(send_data, set_wake_status)
      }
      function get_timer_status(){
         var send_data = {"get_timer_status": ""}
         send_xmlhttp_get(send_data, set_timer_status)
      }
      function save_led_mode(response_data){
         led_mode = response_data["get_led_mode"]
      }
      function set_wake_status(response_data){
         wake_color = document.getElementById("wakecolor").value
         sleep_color = document.getElementById("sleepcolor").value
         custom_color = document.getElementById("customcolor").value
         timer_color = document.getElementById("timercolor").value

         status_div = document.getElementById("status_div")
         if(led_mode == 0){
            if(response_data["get_led_status"] == 0){
               status_div.innerHTML = "Sleep Time!"
               status_div.style.color = sleep_color
            }
            if(response_data["get_led_status"] == 1){
               status_div.innerHTML = "Wake Time!"
               status_div.style.color = wake_color
            }
            if(response_data["get_led_status"] == 2){
               status_div.innerHTML = "Forcing Sleep!"
               status_div.style.color = wake_color
            }
            if(response_data["get_led_status"] == 3){
               status_div.innerHTML = "Forcing Custom!"
               status_div.style.color = custom_color
            }
            if(response_data["get_led_status"] == 4){
               status_div.innerHTML = "Led Off!"
               status_div.style.color = "black"
            }
            if(response_data["get_led_status"] == 5){
               status_div.innerHTML = "Timer Active! Time Remaining: " + timer_remaining[0] + " hr, " + timer_remaining[1] + " min, " + timer_remaining[2]  + " sec"
               status_div.style.color = timer_color
            }
            return
         }
         if(led_mode == 1){
            status_div.innerHTML = "Forcing Awake!"
            status_div.style.color = wake_color
            return
         }
         if(led_mode == 2){
            status_div.innerHTML = "Forcing Sleep!"
            status_div.style.color = sleep_color
            return
         }
         if(led_mode == 3){
            status_div.innerHTML = "Forcing Custom!"
            status_div.style.color = custom_color
            return
         }
         status_div.innerHTML = "Led Off!"
         status_div.style.color = ""
      }
      function set_timer_status(response_data){
         timer_remaining = response_data["get_timer_status"]
      }
      function send_get(get_data, callback_function){
         send_xmlhttp_get(get_data, callback_function)
      }
      function send_post(post_data, callback_function){
         send_xmlhttp_post(post_data, callback_function)
      }
      function alert_response(response){
         if(typeof(response) == "string"){
            alert(response)
         } else {
            alert(JSON.stringify(response))
         }
      }
      function send_xmlhttp_get(data, callback=null){
         var xmlhttp;
         var new_request = JSON.stringify(data);
         if (window.XMLHttpRequest) {
            xmlhttp = new XMLHttpRequest();
         } else {
            // code for IE6, IE5
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
         }
         xmlhttp.open("GET", new_request, true);
         xmlhttp.send();
         xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
               if(callback != null){
                  try {
                     response_json = JSON.parse(this.responseText);
                  } catch (e) {
                     console.log(e)
                     alert("Getting data failed - try again!")
                     return
                  }
                  if(response_json != "DB_ERR"){
                     callback(response_json)
                  }
               }
            }
            if(this.readyState == 4 && this.status != 200){
               alert("Getting data failed - try again!")
               console.log("ERROR")
               console.log(this.statusText)
            }
         }
      }
      function send_xmlhttp_post(data, callback=null){
         var xmlhttp;
         var new_request = JSON.stringify(data);
         if (window.XMLHttpRequest) {
            xmlhttp = new XMLHttpRequest();
         } else {
            // code for IE6, IE5
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
         }
         xmlhttp.open("POST", new_request, true);
         xmlhttp.send();
         xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
               if(callback != null){
                  try {
                     response_json = JSON.parse(this.responseText);
                  } catch (e) {
                     alert("Setting data failed - try again!")
                     return
                  }
                  if(response_json != "DB_ERR"){
                     callback(response_json);
                  }
               }
            }
            if (this.readyState == 4 && this.status != 200){
               alert("Setting data failed - try again!")
            }
         }
      }
      '''
   return javascript_file