import socket
import select

class server_socket_class:
   created = 0
   connected = 0

   def __init__(self):
      self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
   def create_socket(self, device_ip = None, device_port = 80, max_connections = 1):
      if(device_ip != None):
         if(self.created == 0):
            try:
               #self.server_socket.setblocking(False)
               self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
               self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
               self.server_socket.bind((device_ip, device_port))
               self.server_socket.listen(max_connections)
               self.created = 1
            except:
               self.destroy_socket()

   def socket_select_check(self, timeout=0):
      rx_list = [self.server_socket]
      tx_list = []
      x_list = []
      if(self.connected):
         rx_list.append(self.connection)
      try:
         rx_ready, tx_ready, x_ready = select.select(rx_list, tx_list, x_list, timeout)
      except:
         print("select error")
         rx_ready = []
         tx_ready = []
         x_ready = []
         return None
      for ready in rx_ready:
         if(ready == self.server_socket):
            if(self.connected):
               self.reject_connection()
            else:
               self.accept_connection()
            return None
         else:
            return True
   
   def reject_connection(self):
      try:
         new_connection = self.server_socket.accept()
         new_connection[0].close()
      except:
         print("error rejecting")

   def accept_connection(self):
      try:
         new_connection = self.server_socket.accept()
         self.connection = new_connection[0]
         self.connected = 1
      except:
         self.connected = 0

   def check_read_ready(self):
      try:
         read_ready = self.socket_select_check()
      except Exception as e:
         print(e)
         print("socket_select_error")
         read_ready = False
      return read_ready

   def read_data(self, buffer_size):
      if(self.connected == 1):
         try:
            read_data = self.connection.recv(buffer_size)
            if(read_data == b''):
               self.close_connection()
            return read_data
         except Exception as e:
            print(e)
            return None
      else:
         return None
   
   def write_data(self, data):
      if(self.connected == 1):
         try:
            self.connection.sendall(data)
         except:
            print("error writing")
      else:
         print("Connection closed - not writing")

   def close_connection(self):
      if(self.connected == 1):
         self.connection.close()
         self.connected = 0

   def destroy_socket(self):
      self.close_connection()
      if(self.created == 1):
         self.created = 0
         self.server_socket.close()
