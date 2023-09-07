
def get_index_html():
   html_webpage = '''
      <html>
         <head>
            <title>PicoW LED Wake Light</title>
         </head>
         <body>
            get status of all leds from board and update the values of the colors
            <br><br>
            <label for="wakecolor">Select your favorite color:</label>
            <input type="color" id="wakecolor" name="wakecolor" value="#00ff00">
            <input type="button" value="Set Wake Color" onclick="set_wake_color()">
            <br>
            <label for="sleepcolor">Select your favorite color:</label>
            <input type="color" id="sleepcolor" name="sleepcolor" value="#0000ff">
            <input type="button" value="Set Sleep Color" onclick="set_sleep_color()">
            <br>
            <label for="constcolor">Select your favorite color:</label>
            <input type="color" id="constcolor" name="constcolor" value="#ff00ff">
            <input type="button" value="Set Constant Color" onclick="set_const_color()">
            <br>
            <input type="button" value="Resume Schedule" onclick="set_led_mode(0)">
            <input type="button" value="Force Wake" onclick="set_led_mode(1)">
            <input type="button" value="Force Sleep" onclick="set_led_mode(2)">
            <input type="button" value="Force Constant" onclick="set_led_mode(3)">
            <input type="button" value="Turn LED Off" onclick="set_led_mode(4)">
            <br><br>
            Get current wake status
            Get current wake schedule
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
            Wake Time Settings:
            <br>
            Select a day:
            <select name="weekday" id="weekday">
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
         </body>
         <script>
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
            function get_led(){
               var send_data = {"led_state":""}
               send_xmlhttp_get(send_data, alert_response)
            }
            function get_duty(){
               var send_data = {"led_duty":""}
               send_xmlhttp_get(send_data, alert_response)
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
               send_xmlhttp_post(send_data)
            }
            function clear_wake_times(){
               var day = document.getElementById("weekday").value
               var send_data = {"clear_wake_times": day}
               send_xmlhttp_post(send_data)
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