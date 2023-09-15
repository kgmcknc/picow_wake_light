
def get_index_html():
   html_webpage = '''
      <html>
         <head>
            <title>PicoW LED Wake Light</title>
         </head>
         <body>
            Wake Time Settings:
            <br>
            Select a day:
            <select name="weekday" id="weekday" onchange="get_wake_times()">
            <option value="sunday">Sunday</option>
            <option value="monday">Monday</option>
            <option value="tuesday">Tuesday</option>
            <option value="wednesday">Wednesday</option>
            <option value="thursday">Thursday</option>
            <option value="friday">Friday</option>
            <option value="saturday">Saturday</option>
            </select>
            <label for="wake_start">Start Time:</label>
            <input type="time" id="wake_start" name="wake_start">
            <label for="wake_end">End Time:</label>
            <input type="time" id="wake_end" name="wake_end">
            <br>
            <button onclick="add_wake_time()">Add Wake Time</button>
            <button onclick="clear_wake_times()">Clear Wake Times</button>
            <div id="schedule_div">
               <div>No Times Scheduled</div>
            </div>
            <br><br>
            <div id="status_div"></div>
            <br><br>
            <label for="wakecolor">Select your favorite color:</label>
            <input type="color" id="wakecolor" name="wakecolor" value="#00ff00">
            <input type="button" value="Set Wake Color" onclick="set_wake_color()">
            <input type="button" value="Get Wake Color" onclick="get_wake_color()">
            <br>
            <label for="sleepcolor">Select your favorite color:</label>
            <input type="color" id="sleepcolor" name="sleepcolor" value="#0000ff">
            <input type="button" value="Set Sleep Color" onclick="set_sleep_color()">
            <input type="button" value="Get Sleep Color" onclick="get_sleep_color()">
            <br>
            <label for="constcolor">Select your favorite color:</label>
            <input type="color" id="constcolor" name="constcolor" value="#ff00ff">
            <input type="button" value="Set Constant Color" onclick="set_const_color()">
            <input type="button" value="Get Constant Color" onclick="get_const_color()">
            <br>
            <input type="button" value="Resume Schedule" onclick="set_led_mode(0)">
            <input type="button" value="Force Wake" onclick="set_led_mode(1)">
            <input type="button" value="Force Sleep" onclick="set_led_mode(2)">
            <input type="button" value="Force Constant" onclick="set_led_mode(3)">
            <input type="button" value="Turn LED Off" onclick="set_led_mode(4)">
            <br><br>
            <label for="ssid">SSID:</label><br>
            <input type="text" id="ssid" name="ssid"><br>
            <label for="pwd">Password:</label><br>
            <input type="password" id="pwd" name="pwd"><br><br>
            <button onclick="add_network()">Add Network</button>
            <button onclick="remove_network()">Remove Network</button>
            <button onclick="set_ap_ssid()">Set AP SSID</button>
            <button onclick="clear_ap_ssid()">Clear AP SSID</button>
            <button onclick="restart_network()">Restart Network</button>
            <br><br>
         </body>
         <script>
            led_mode = 0
            setInterval(get_status, 5000);
            get_led_values()
            async function get_led_values(){
               await sleep(1000)
               get_wake_color()
               await sleep(500)
               get_sleep_color()
               await sleep(500)
               get_const_color()
               await sleep(500)
               get_wake_times()
            }
            async function get_status(){
               await sleep(1000)
               get_led_mode()
               await sleep(1000)
               get_wake_status()
            }
            function sleep(ms) {
               return new Promise(resolve => setTimeout(resolve, ms));
            }
            function add_network(){
               new_ssid = document.getElementById("ssid").value
               new_pw = document.getElementById("pwd").value
               var send_data = {"add_wifi_ssid":{"ssid":new_ssid,"password":new_pw}}
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
            function set_const_color(){
               var color_value = document.getElementById("constcolor").value
               var send_data = {"set_const_color":color_value.slice(1)}
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
            function get_const_color(){
               var send_data = {"get_const_color":""}
               send_xmlhttp_get(send_data, set_const_value)
            }
            function set_wake_value(response_data){
               document.getElementById("wakecolor").value = "#"+response_data["get_wake_color"]
            }
            function set_sleep_value(response_data){
               document.getElementById("sleepcolor").value = "#"+response_data["get_sleep_color"]
            }
            function set_const_value(response_data){
               document.getElementById("constcolor").value = "#"+response_data["get_const_color"]
            }
            function add_wake_time(){
               var day = document.getElementById("weekday").value
               var wake_start = document.getElementById("wake_start").value
               var wake_end = document.getElementById("wake_end").value
               var start_split = wake_start.split(":")
               var end_split = wake_end.split(":")
               var start_time = [start_split[0], start_split[1]]
               var end_time = [end_split[0], end_split[1]]
               var send_data = {"add_wake_time": {"day":day, "time":{"start_time":start_time,"end_time":end_time}}}
               send_xmlhttp_post(send_data, get_wake_times)
            }
            function clear_wake_times(){
               var day = document.getElementById("weekday").value
               var send_data = {"clear_wake_times": day}
               send_xmlhttp_post(send_data, get_wake_times)
            }
            function get_wake_times(){
               var day = document.getElementById("weekday").value
               var send_data = {"get_wake_times": {"day":day}}
               send_xmlhttp_get(send_data, set_wake_schedule)
            }
            function set_wake_schedule(response_data){
               schedule_div = document.getElementById("schedule_div")
               wake_list = response_data["get_wake_times"]
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
            function get_led_mode(){
               var send_data = {"get_led_mode": ""}
               send_xmlhttp_get(send_data, save_led_mode)
            }
            function get_wake_status(){
               var send_data = {"get_wake_status": ""}
               send_xmlhttp_get(send_data, set_wake_status)
            }
            function save_led_mode(response_data){
               led_mode = response_data["get_led_mode"]
            }
            function set_wake_status(response_data){
               wake_color = document.getElementById("wakecolor").value
               sleep_color = document.getElementById("sleepcolor").value
               const_color = document.getElementById("constcolor").value

               status_div = document.getElementById("status_div")
               if(led_mode == 0){
                  if(response_data["get_wake_status"] == true){
                     status_div.innerHTML = "Wake Time!"
                     status_div.style.color = wake_color
                  } else {
                     status_div.innerHTML = "Sleep Time!"
                     status_div.style.color = sleep_color
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
                  status_div.innerHTML = "Forcing Constant!"
                  status_div.style.color = const_color
                  return
               }
               status_div.innerHTML = "Led Off!"
               status_div.style.color = ""
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
                           return
                        }
                        if(response_json != "DB_ERR"){
                           callback(response_json);
                        }
                     }
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
                           return
                        }
                        if(response_json != "DB_ERR"){
                           callback(response_json);
                        }
                     }
                  }
               }
            }
         </script>
      </html>
      '''
   return html_webpage