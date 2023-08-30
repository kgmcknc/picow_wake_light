
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
         </body>
         <script>
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