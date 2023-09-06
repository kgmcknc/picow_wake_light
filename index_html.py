
def get_index_html():
   html_webpage = '''
      <html>
         <head>
            <title>Kids LED Wake Light</title>
         </head>
         <body>
            This is a test page!
            <br>
            <button onclick="send_on()">led on</button>
            <button onclick="send_off()">led off</button>
            <br>
            Red: <input type="range" oninput="set_led()" onchange="set_led()" min="0" max="65535" value="30000" class="slider" id="redrange">
            <br>
            Green: <input type="range" oninput="set_led()" onchange="set_led()" min="0" max="65535" value="30000" class="slider" id="greenrange">
            <br>
            Blue: <input type="range" oninput="set_led()" onchange="set_led()" min="0" max="65535" value="30000" class="slider" id="bluerange">
            <br>
            <button onclick="set_led()">Set LED</button>
            <button onclick="get_led()">Get LED</button>
            <button onclick="get_duty()">Get DUTY</button>
            <br>
            ssid: <input type="text" id="ssid_text">
            <br>
            password: <input type="text" id="pw_text">
            <br>
            <button onclick="add_network()">Add Network</button>
            <button onclick="remove_network()">Remove Network</button>
            <button onclick="set_ap_ssid()">Set AP SSID</button>
            <button onclick="clear_ap_ssid()">Clear AP SSID</button>
            <br>
            <button onclick="restart_network()">Restart Network</button>
            <br>
            <select name="weekday" id="weekday">
            <option value="sunday">Sunday</option>
            <option value="monday">Monday</option>
            <option value="tuesday">Tuesday</option>
            <option value="wednesday">Wednesday</option>
            <option value="thursday">Thursday</option>
            <option value="friday">Friday</option>
            <option value="saturday">Saturday</option>
            </select>
            <br>
            Start Hour: <input type="number" id="start_hour" name="starthour" min="0" max="23" value="0">
            Start Min: <input type="number" id="start_min" name="startmin" min="0" max="59" value="0">
            End Hour: <input type="number" id="end_hour" name="endhour" min="0" max="23" value="0">
            End Min: <input type="number" id="end_min" name="endmin" min="0" max="59" value="0">
            <br>
            <button onclick="add_wake_time()">Add Wake Time</button>
            <button onclick="clear_wake_times()">Clear Wake Times</button>
         </body>
         <script>
            function add_network(){
               new_ssid = document.getElementById("ssid_text").value
               new_pw = document.getElementById("pw_text").value
               var send_data = {"add_wifi_ssid":{"ssid":new_ssid,"password":new_pw}}
               send_xmlhttp_post(send_data)
            }
            function remove_network(){
               new_ssid = document.getElementById("ssid_text").value
               var send_data = {"remove_wifi_ssid":new_ssid}
               send_xmlhttp_post(send_data)
            }
            function set_ap_ssid(){
               new_ssid = document.getElementById("ssid_text").value
               new_pw = document.getElementById("pw_text").value
               var send_data = {"set_ap_ssid":{"ssid":new_ssid,"password":new_pw}}
               send_xmlhttp_post(send_data)
            }
            function clear_ap_ssid(){
               new_ssid = document.getElementById("ssid_text").value
               var send_data = {"clear_ap_ssid":new_ssid}
               send_xmlhttp_post(send_data)
            }
            function restart_network(){
               var send_data = {"restart_network":"True"}
               send_xmlhttp_post(send_data)
            }
            function send_on(){
               var send_data = {"led_state":"on"}
               send_xmlhttp_post(send_data)
            }
            function send_off(){
               var send_data = {"led_state":"off"}
               send_xmlhttp_post(send_data)
            }
            function set_led(){
               var redval = document.getElementById("redrange").value
               var greenval = document.getElementById("greenrange").value
               var blueval = document.getElementById("bluerange").value
               var send_data = {"led_red":redval,"led_green":greenval,"led_blue":blueval}
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
               var start_hour = document.getElementById("start_hour").value
               var start_min = document.getElementById("start_min").value
               var end_hour = document.getElementById("end_hour").value
               var end_min = document.getElementById("end_min").value
               var start_time = [start_hour, start_min]
               var end_time = [end_hour, end_min]
               var time_string = "[("+start_hour+","+start_min+"):("+end_hour+","+end_min+")]"
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