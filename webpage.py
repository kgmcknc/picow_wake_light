
import index_html

_hexdig = '0123456789ABCDEFabcdef'
_hextobyte = None

resp_header_okay = 'HTTP/1.1 200 OK\r\nAccept-Ranges: bytes\r\n'
resp_header_cont_len = 'Content-Length: '
resp_header_cont_type = 'Content-Type: text/html\r\n'
resp_header_con_close = 'Connection: close\r\n'
header_end = "Connection: close\r\nContent-Type: text/html\r\nX-Pad: avoid browser bug\r\n"

website_request = 'GET / HTTP/1.1'

def create_html_packet(html_data):
   new_packet = ''
   new_packet = new_packet + resp_header_okay + resp_header_cont_type + create_content_length_header(html_data) + header_end + '\r\n'
   new_packet = new_packet + html_data
   return new_packet

def create_empty_response():
   new_packet = ''
   new_packet = new_packet + resp_header_okay + resp_header_cont_type + header_end + '\r\n'
   new_packet = new_packet
   return new_packet

def create_content_length_header(data):
   len_header = ''
   data_len = len(data)
   len_header = len_header + resp_header_cont_len + str(data_len) + '\r\n'
   return len_header

def get_webpage():
   html = index_html.get_index_html()
   return create_html_packet(html)

def process_read_data(read_data):
   response = None
   if(read_data == b''):
      return response
   decoded_read = read_data.decode()
   split_decode = decoded_read.split()
   if(split_decode[0] == 'GET'):
      get_data = unquote(split_decode[1][1:])
      response = ['GET', get_data]
   else:
      if(split_decode[0] == 'POST'):
         #end_string = decoded_read.find("HTTP/1.1")
         #post_data = unquote(decoded_read[6:end_string])
         post_data = unquote(split_decode[1][1:])
         response = ['POST', post_data]
      else:
         print("unknown data")
         print(decoded_read)
   return response

def unquote(string):
   new_string = ''
   startval = 0
   loc = string.find("%", startval)
   if(loc < 0):
      return string
   while(loc >= 0):
      new_string = new_string + string[startval:loc]
      startval = loc + 3
      changedat = string[loc:loc+3]
      if(changedat == '%7B'):
         new_string = new_string + '{'
      if(changedat == '%7D'):
         new_string = new_string + '}'
      if(changedat == '%22'):
         new_string = new_string + '\"'
      loc = string.find("%", startval)
   return new_string


def unquote_full(string):
   """unquote('abc%20def') -> b'abc def'."""
   global _hextobyte
   # Note: strings are encoded as UTF-8. This is only an issue if it contains
   # unescaped non-ASCII characters, which URIs should not.
   if not string:
      return b''

   if isinstance(string, str):
      string = string.encode('utf-8')

   bits = string.split(b'%')
   if len(bits) == 1:
      return string

   res = [bits[0]]
   append = res.append

   # Delay the initialization of the table to not waste memory
   # if the function is never called
   if _hextobyte is None:
      _hextobyte = {(a + b).encode(): bytes([int(a + b, 16)])
                     for a in _hexdig for b in _hexdig}

   for item in bits[1:]:
      try:
         append(_hextobyte[item[:2]])
         append(item[2:])
      except KeyError:
         append(b'%')
         append(item)
   return b''.join(res)