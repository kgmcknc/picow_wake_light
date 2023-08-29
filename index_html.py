
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
            <button onclick="set_led()">Set LED</button>
         </body>
         <script>
            function send_on(){
               var send_data = {"led_state":"on"}
               send_xmlhttp(send_data)
            }
            function send_off(){
               var send_data = {"led_state":"off"}
               send_xmlhttp(send_data)
            }
            function set_led(){
               var redval = document.getElementById("redrange").value
               var greenval = document.getElementById("greenrange").value
               var blueval = document.getElementById("bluerange").value
               var send_data = {"led_red":redval,"led_green":greenval,"led_blue":blueval}
               send_xmlhttp(send_data)
            }
            function send_xmlhttp(data){
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
               // xmlhttp.onreadystatechange = function() {
               //    if (this.readyState == 4 && this.status == 200) {
               //       alert(this.responseText)
               //    }
               // }
            }
         </script>
      </html>
      '''
   return html_webpage